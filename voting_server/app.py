import math
import os
import threading
import time
import uuid

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

ACTIVE_PLAYER_TTL = 30


class BattleStore:
    """Thread-safe in-memory state for one live audience battle."""

    def __init__(self):
        self.lock = threading.RLock()
        self.reset()

    def reset(self):
        with getattr(self, "lock", threading.RLock()):
            self.active_players = {}
            self.battle = {
                "battle_id": None,
                "status": "idle",
                "team_name": "Үзэгчдийн баг",
                "monster_name": "Сүүдрийн мангас",
                "player_hp": 500,
                "player_max_hp": 500,
                "monster_hp": 1000,
                "monster_max_hp": 1000,
                "round_number": 0,
                "current_round": None,
            }

    def touch_player(self, player_id):
        player_id = clean_text(player_id, "", 100)
        if len(player_id) < 8:
            return

        with self.lock:
            self.active_players[player_id] = time.time()

    def _active_player_ids(self, now=None):
        now = time.time() if now is None else now
        cutoff = now - ACTIVE_PLAYER_TTL
        self.active_players = {
            player_id: last_seen
            for player_id, last_seen in self.active_players.items()
            if last_seen >= cutoff
        }
        return sorted(self.active_players)

    def _finalize_if_due(self, force=False):
        current = self.battle.get("current_round")
        if not current or current["status"] != "open":
            return current

        now = time.time()
        expected_player_ids = set(current.get("expected_player_ids", []))
        answered_player_ids = set(current["answers"])
        all_answers_received = (
            bool(expected_player_ids)
            and expected_player_ids.issubset(answered_player_ids)
        )
        duration_finished = now >= current["ends_at"]

        if not force and not all_answers_received and not duration_finished:
            return current

        answers = list(current["answers"].values())
        choice_counts = [0] * len(current["choices"])
        for answer in answers:
            choice_counts[answer["choice_index"]] += 1

        total_answers = len(answers)
        mode = current.get("mode", "battle")
        correct_index = current.get("correct_index")

        if mode == "survey":
            correct_count = 0
            wrong_count = 0
            monster_damage = 0
            player_damage = 0
        else:
            correct_count = choice_counts[correct_index]
            wrong_count = total_answers - correct_count

            requested_monster_damage = correct_count * current["attack_power"]
            requested_player_damage = wrong_count * current["enemy_attack_power"]
            monster_damage = min(requested_monster_damage, self.battle["monster_hp"])
            player_damage = min(requested_player_damage, self.battle["player_hp"])

            self.battle["monster_hp"] -= monster_damage
            self.battle["player_hp"] -= player_damage

            if self.battle["monster_hp"] <= 0:
                self.battle["status"] = "victory"
            elif self.battle["player_hp"] <= 0:
                self.battle["status"] = "defeat"

        highest_count = max(choice_counts) if choice_counts else 0
        top_choice_indices = (
            [index for index, count in enumerate(choice_counts) if count == highest_count]
            if highest_count > 0 else []
        )

        current["status"] = "finished"
        current["finished_at"] = now
        current["completion_reason"] = (
            "forced" if force
            else "all_answered" if all_answers_received
            else "duration"
        )
        current["result"] = {
            "round_id": current["round_id"],
            "round_number": current["round_number"],
            "mode": mode,
            "correct_index": correct_index,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "total_answers": total_answers,
            "choice_counts": choice_counts,
            "top_choice_indices": top_choice_indices,
            "monster_damage": monster_damage,
            "player_damage": player_damage,
            "monster_hp": self.battle["monster_hp"],
            "player_hp": self.battle["player_hp"],
            "battle_status": self.battle["status"],
            "expected_answers": len(expected_player_ids),
            "completion_reason": current["completion_reason"],
        }
        return current

    def start_battle(self, payload):
        with self.lock:
            player_max_hp = clamp_int(payload.get("player_hp", 500), 1, 1_000_000)
            monster_max_hp = clamp_int(payload.get("monster_hp", 1000), 1, 1_000_000)
            self.battle = {
                "battle_id": uuid.uuid4().hex,
                "status": "active",
                "team_name": clean_text(payload.get("team_name"), "Үзэгчдийн баг", 60),
                "monster_name": clean_text(payload.get("monster_name"), "Сүүдрийн мангас", 60),
                "player_hp": player_max_hp,
                "player_max_hp": player_max_hp,
                "monster_hp": monster_max_hp,
                "monster_max_hp": monster_max_hp,
                "round_number": 0,
                "current_round": None,
            }
            return self.public_battle()

    def start_round(self, payload):
        with self.lock:
            self._finalize_if_due()
            if self.battle["status"] != "active":
                raise ValueError("Тулаан идэвхгүй байна. Эхлээд battle/start дуудна уу.")

            previous = self.battle.get("current_round")
            if previous and previous["status"] == "open":
                raise ValueError("Өмнөх асуултын хугацаа дуусаагүй байна.")

            question = clean_text(payload.get("question"), "", 300)
            choices = payload.get("choices")
            if not question:
                raise ValueError("question хоосон байж болохгүй.")
            if not isinstance(choices, list) or not 2 <= len(choices) <= 10:
                raise ValueError("choices нь 2-10 сонголттой жагсаалт байна.")

            choices = [clean_text(choice, "", 160) for choice in choices]
            if any(not choice for choice in choices):
                raise ValueError("Сонголтын текст хоосон байж болохгүй.")

            mode = clean_text(payload.get("mode"), "battle", 20).lower()
            if mode not in ("battle", "survey"):
                raise ValueError("mode нь battle эсвэл survey байна.")

            duration = clamp_int(payload.get("duration", 15), 5, 120)
            if mode == "survey":
                correct_index = None
                attack_power = 0
                enemy_attack_power = 0
            else:
                correct_index = clamp_int(payload.get("correct_index"), 0, len(choices) - 1)
                attack_power = clamp_int(payload.get("attack_power", 5), 0, 10_000)
                enemy_attack_power = clamp_int(payload.get("enemy_attack_power", 3), 0, 10_000)

            now = time.time()
            expected_player_ids = self._active_player_ids(now)

            self.battle["round_number"] += 1
            self.battle["current_round"] = {
                "round_id": uuid.uuid4().hex,
                "round_number": self.battle["round_number"],
                "question": question,
                "choices": choices,
                "mode": mode,
                "correct_index": correct_index,
                "duration": duration,
                "attack_power": attack_power,
                "enemy_attack_power": enemy_attack_power,
                "started_at": now,
                "ends_at": now + duration,
                "finished_at": None,
                "status": "open",
                "answers": {},
                "expected_player_ids": expected_player_ids,
                "completion_reason": None,
                "result": None,
            }
            return self.public_battle()

    def submit_answer(self, payload):
        with self.lock:
            self._finalize_if_due()
            current = self.battle.get("current_round")
            if not current or current["status"] != "open":
                raise RoundClosedError("Энэ асуултын санал хураалт хаагдсан байна.")

            player_id = clean_text(payload.get("player_id"), "", 100)
            player_name = clean_text(payload.get("player_name"), "Тоглогч", 40)
            if len(player_id) < 8:
                raise ValueError("player_id буруу байна.")
            if player_id in current["answers"]:
                raise DuplicateAnswerError("Та энэ асуултад аль хэдийн хариулсан байна.")

            choice_index = clamp_int(payload.get("choice_index"), 0, len(current["choices"]) - 1)
            current["answers"][player_id] = {
                "player_name": player_name,
                "choice_index": choice_index,
                "answered_at": time.time(),
            }
            total_answers = len(current["answers"])
            self._finalize_if_due()
            return {
                "accepted": True,
                "round_id": current["round_id"],
                "total_answers": total_answers,
            }

    def finish_round(self, force=False):
        with self.lock:
            current = self._finalize_if_due(force=force)
            if not current:
                raise ValueError("Идэвхтэй асуулт алга.")
            return self.public_battle()

    def public_battle(self):
        with self.lock:
            self._finalize_if_due()
            data = {
                key: value
                for key, value in self.battle.items()
                if key != "current_round"
            }
            data["current_round"] = self.public_round(self.battle.get("current_round"))
            return data

    @staticmethod
    def public_round(current):
        if not current:
            return None
        mode = current.get("mode", "battle")
        expected_player_ids = set(current.get("expected_player_ids", []))
        answered_player_ids = set(current["answers"])
        answered_expected = len(expected_player_ids.intersection(answered_player_ids))
        expected_answers = len(expected_player_ids)
        data = {
            "round_id": current["round_id"],
            "round_number": current["round_number"],
            "mode": mode,
            "question": current["question"],
            "choices": current["choices"],
            "duration": current["duration"],
            "attack_power": current["attack_power"],
            "enemy_attack_power": current["enemy_attack_power"],
            "started_at": current["started_at"],
            "ends_at": current["ends_at"],
            "status": current["status"],
            "total_answers": len(current["answers"]),
            "expected_answers": expected_answers,
            "answered_expected": answered_expected,
            "all_answers_received": (
                expected_answers > 0 and answered_expected >= expected_answers
            ),
            "completion_reason": current.get("completion_reason"),
            "remaining_seconds": (
                max(0, math.ceil(current["ends_at"] - time.time()))
                if current["status"] == "open" else 0
            ),
            "result": current["result"],
        }

        if mode == "survey":
            choice_counts = [0] * len(current["choices"])
            for answer in current["answers"].values():
                choice_counts[answer["choice_index"]] += 1
            data["choice_counts"] = choice_counts

        return data


class DuplicateAnswerError(Exception):
    pass


class RoundClosedError(Exception):
    pass


def clamp_int(value, minimum, maximum):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError("Тоон утга буруу байна.")
    return max(minimum, min(maximum, value))


def clean_text(value, default, max_length):
    if value is None:
        return default
    value = str(value).strip()
    return (value or default)[:max_length]


def json_payload():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ValueError("JSON object илгээнэ үү.")
    return payload


def require_host():
    expected = os.environ.get("BATTLE_HOST_TOKEN", "").strip()
    if expected and request.headers.get("X-Host-Token", "") != expected:
        return jsonify({"success": False, "error": "Host token буруу байна."}), 401
    return None


store = BattleStore()


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Host-Token"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def home():
    return render_template("vote.html")


@app.get("/api/health")
def health():
    return jsonify({"success": True, "service": "animo-crowd-battle"})


@app.post("/api/battle/start")
def start_battle():
    denied = require_host()
    if denied:
        return denied
    try:
        battle = store.start_battle(json_payload())
        return jsonify({"success": True, "battle": battle})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.post("/api/battle/reset")
def reset_battle():
    denied = require_host()
    if denied:
        return denied
    store.reset()
    return jsonify({"success": True, "battle": store.public_battle()})


@app.get("/api/battle/status")
def battle_status():
    store.touch_player(request.args.get("player_id"))
    return jsonify({"success": True, "battle": store.public_battle()})


@app.post("/api/round/start")
def start_round():
    denied = require_host()
    if denied:
        return denied
    try:
        battle = store.start_round(json_payload())
        return jsonify({"success": True, "battle": battle})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.get("/api/round/status")
def round_status():
    battle = store.public_battle()
    return jsonify({
        "success": True,
        "battle": battle,
        "round": battle["current_round"],
    })


@app.post("/api/round/answer")
def answer_round():
    try:
        answer = store.submit_answer(json_payload())
        return jsonify({"success": True, **answer})
    except DuplicateAnswerError as exc:
        return jsonify({"success": False, "error": str(exc), "duplicate": True}), 409
    except RoundClosedError as exc:
        return jsonify({"success": False, "error": str(exc), "closed": True}), 410
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.post("/api/round/finish")
def finish_round():
    denied = require_host()
    if denied:
        return denied
    try:
        payload = json_payload()
        battle = store.finish_round(force=bool(payload.get("force", False)))
        return jsonify({
            "success": True,
            "battle": battle,
            "round": battle["current_round"],
        })
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


@app.get("/api/round/result")
def round_result():
    battle = store.public_battle()
    current = battle.get("current_round")
    if not current or current["status"] != "finished":
        return jsonify({"success": False, "waiting": True}), 202
    return jsonify({
        "success": True,
        "battle": battle,
        "result": current["result"],
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
