import math
import os
import threading
import time
import uuid

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


class BattleStore:
    """Thread-safe in-memory state for one live audience battle."""

    def __init__(self):
        self.lock = threading.RLock()
        self.reset()

    def reset(self):
        with getattr(self, "lock", threading.RLock()):
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

    def _finalize_if_due(self, force=False):
        current = self.battle.get("current_round")
        if not current or current["status"] != "open":
            return current

        if not force and time.time() < current["ends_at"]:
            return current

        answers = current["answers"].values()
        correct_count = sum(
            1 for answer in answers
            if answer["choice_index"] == current["correct_index"]
        )
        total_answers = len(current["answers"])
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

        current["status"] = "finished"
        current["finished_at"] = time.time()
        current["result"] = {
            "round_id": current["round_id"],
            "round_number": current["round_number"],
            "correct_index": current["correct_index"],
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "total_answers": total_answers,
            "monster_damage": monster_damage,
            "player_damage": player_damage,
            "monster_hp": self.battle["monster_hp"],
            "player_hp": self.battle["player_hp"],
            "battle_status": self.battle["status"],
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
            if not isinstance(choices, list) or not 2 <= len(choices) <= 6:
                raise ValueError("choices нь 2-6 сонголттой жагсаалт байна.")

            choices = [clean_text(choice, "", 160) for choice in choices]
            if any(not choice for choice in choices):
                raise ValueError("Сонголтын текст хоосон байж болохгүй.")

            correct_index = clamp_int(payload.get("correct_index"), 0, len(choices) - 1)
            duration = clamp_int(payload.get("duration", 15), 5, 120)
            attack_power = clamp_int(payload.get("attack_power", 5), 0, 10_000)
            enemy_attack_power = clamp_int(payload.get("enemy_attack_power", 3), 0, 10_000)
            now = time.time()

            self.battle["round_number"] += 1
            self.battle["current_round"] = {
                "round_id": uuid.uuid4().hex,
                "round_number": self.battle["round_number"],
                "question": question,
                "choices": choices,
                "correct_index": correct_index,
                "duration": duration,
                "attack_power": attack_power,
                "enemy_attack_power": enemy_attack_power,
                "started_at": now,
                "ends_at": now + duration,
                "finished_at": None,
                "status": "open",
                "answers": {},
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
            return {
                "accepted": True,
                "round_id": current["round_id"],
                "total_answers": len(current["answers"]),
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
        data = {
            "round_id": current["round_id"],
            "round_number": current["round_number"],
            "question": current["question"],
            "choices": current["choices"],
            "duration": current["duration"],
            "attack_power": current["attack_power"],
            "enemy_attack_power": current["enemy_attack_power"],
            "started_at": current["started_at"],
            "ends_at": current["ends_at"],
            "status": current["status"],
            "total_answers": len(current["answers"]),
            "remaining_seconds": max(0, math.ceil(current["ends_at"] - time.time())),
            "result": current["result"],
        }
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
