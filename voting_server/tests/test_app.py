import time

try:
    from voting_server.app import app, store
except ModuleNotFoundError:
    from app import app, store


def host_headers():
    return {"Content-Type": "application/json"}


def test_health():
    with app.test_client() as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.get_json()["success"] is True


def test_full_battle_round(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        started = client.post(
            "/api/battle/start",
            headers=host_headers(),
            json={"player_hp": 100, "monster_hp": 100},
        )
        assert started.status_code == 200

        round_started = client.post(
            "/api/round/start",
            headers=host_headers(),
            json={
                "question": "2 + 2 = ?",
                "choices": ["3", "4", "5"],
                "correct_index": 1,
                "duration": 15,
                "attack_power": 10,
                "enemy_attack_power": 7,
            },
        )
        assert round_started.status_code == 200

        for player_id, choice_index in (("player-0001", 1), ("player-0002", 1), ("player-0003", 0)):
            answer = client.post(
                "/api/round/answer",
                json={"player_id": player_id, "player_name": player_id, "choice_index": choice_index},
            )
            assert answer.status_code == 200

        duplicate = client.post(
            "/api/round/answer",
            json={"player_id": "player-0001", "choice_index": 2},
        )
        assert duplicate.status_code == 409

        finished = client.post("/api/round/finish", json={"force": True})
        body = finished.get_json()
        result = body["round"]["result"]
        assert result["correct_count"] == 2
        assert result["wrong_count"] == 1
        assert result["monster_damage"] == 20
        assert result["player_damage"] == 7
        assert result["monster_hp"] == 80
        assert result["player_hp"] == 93


def test_host_token(monkeypatch):
    monkeypatch.setenv("BATTLE_HOST_TOKEN", "secret")
    store.reset()

    with app.test_client() as client:
        denied = client.post("/api/battle/start", json={})
        assert denied.status_code == 401

        allowed = client.post(
            "/api/battle/start",
            headers={"X-Host-Token": "secret"},
            json={},
        )
        assert allowed.status_code == 200


def test_survey_round(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        started = client.post(
            "/api/battle/start",
            headers=host_headers(),
            json={"player_hp": 100, "monster_hp": 100},
        )
        assert started.status_code == 200

        choices = ["A", "B", "C", "D", "E", "F", "G", "H"]
        round_started = client.post(
            "/api/round/start",
            headers=host_headers(),
            json={
                "question": "ANIMO world?",
                "choices": choices,
                "mode": "survey",
                "duration": 15,
            },
        )
        assert round_started.status_code == 200
        assert round_started.get_json()["battle"]["current_round"]["mode"] == "survey"

        for player_id, choice_index in (
            ("player-0001", 2),
            ("player-0002", 2),
            ("player-0003", 7),
        ):
            answer = client.post(
                "/api/round/answer",
                json={
                    "player_id": player_id,
                    "player_name": player_id,
                    "choice_index": choice_index,
                },
            )
            assert answer.status_code == 200

        live_round = client.get("/api/round/status").get_json()["round"]
        assert live_round["status"] == "open"
        assert live_round["total_answers"] == 3
        assert live_round["choice_counts"] == [0, 0, 2, 0, 0, 0, 0, 1]

        finished = client.post("/api/round/finish", json={"force": True})
        finished_round = finished.get_json()["round"]
        result = finished_round["result"]

        assert finished_round["remaining_seconds"] == 0
        assert result["mode"] == "survey"
        assert result["correct_index"] is None
        assert result["choice_counts"] == [0, 0, 2, 0, 0, 0, 0, 1]
        assert result["top_choice_indices"] == [2]
        assert result["monster_damage"] == 0
        assert result["player_damage"] == 0
        assert result["monster_hp"] == 100
        assert result["player_hp"] == 100



def test_round_finishes_after_every_active_player_answers(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.get("/api/battle/status?player_id=player-0001")
        client.get("/api/battle/status?player_id=player-0002")
        client.post("/api/battle/start", json={"player_hp": 100, "monster_hp": 100})

        started = client.post(
            "/api/round/start",
            json={
                "question": "2 + 2 = ?",
                "choices": ["3", "4"],
                "correct_index": 1,
                "duration": 15,
            },
        )
        current = started.get_json()["battle"]["current_round"]
        assert current["expected_answers"] == 2
        assert current["status"] == "open"

        client.post(
            "/api/round/answer",
            json={"player_id": "player-0001", "choice_index": 1},
        )
        current = client.get("/api/round/status").get_json()["round"]
        assert current["status"] == "open"
        assert current["all_answers_received"] is False

        client.post(
            "/api/round/answer",
            json={"player_id": "player-0002", "choice_index": 0},
        )
        current = client.get("/api/round/status").get_json()["round"]
        assert current["status"] == "finished"
        assert current["all_answers_received"] is True
        assert current["result"]["completion_reason"] == "all_answered"


def test_round_finishes_when_duration_expires(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={"player_hp": 100, "monster_hp": 100})
        client.post(
            "/api/round/start",
            json={
                "question": "2 + 2 = ?",
                "choices": ["3", "4"],
                "correct_index": 1,
                "duration": 15,
            },
        )

        with store.lock:
            store.battle["current_round"]["ends_at"] = time.time() - 1

        current = client.get("/api/round/status").get_json()["round"]
        assert current["status"] == "finished"
        assert current["result"]["completion_reason"] == "duration"


def test_answer_from_unregistered_player_does_not_finish_early(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={"player_hp": 100, "monster_hp": 100})
        client.post(
            "/api/round/start",
            json={
                "question": "2 + 2 = ?",
                "choices": ["3", "4"],
                "correct_index": 1,
                "duration": 15,
            },
        )
        client.post(
            "/api/round/answer",
            json={"player_id": "player-late1", "choice_index": 1},
        )

        current = client.get("/api/round/status").get_json()["round"]
        assert current["expected_answers"] == 0
        assert current["status"] == "open"
