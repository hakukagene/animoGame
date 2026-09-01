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
