import time

try:
    from voting_server.app import app, percentage_amount, store
except ModuleNotFoundError:
    from app import app, percentage_amount, store


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
            json={"player_hp": 1, "monster_hp": 2},
        )
        assert started.status_code == 200
        battle = started.get_json()["battle"]
        assert battle["player_hp"] == 1000
        assert battle["player_max_hp"] == 1000
        assert battle["monster_hp"] == 1000
        assert battle["monster_max_hp"] == 1000

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
        current_round = round_started.get_json()["battle"]["current_round"]
        assert current_round["attack_power"] == 100
        assert current_round["enemy_attack_power"] == 100

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
        assert result["correct_percentage"] == 66.7
        assert result["wrong_percentage"] == 33.3
        assert result["monster_damage"] == 67
        assert result["player_damage"] == 33
        assert result["monster_hp"] == 933
        assert result["player_hp"] == 967


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
            json={},
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
        assert result["monster_hp"] == 1000
        assert result["player_hp"] == 1000



def test_round_finishes_after_every_active_player_answers(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.get("/api/battle/status?player_id=player-0001")
        client.get("/api/battle/status?player_id=player-0002")
        client.post("/api/battle/start", json={})

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


def test_empty_battle_round_applies_max_player_damage_after_duration(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={})
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
        assert current["total_answers"] == 0
        assert current["result"]["total_answers"] == 0
        assert current["result"]["correct_percentage"] == 0.0
        assert current["result"]["wrong_percentage"] == 100.0
        assert current["result"]["monster_damage"] == 0
        assert current["result"]["requested_player_damage"] == 100
        assert current["result"]["player_damage"] == 100
        assert current["result"]["player_hp"] == 900
        assert current["result"]["no_answer_penalty"] is True
        assert current["result"]["completion_reason"] == "duration"


def test_empty_survey_round_does_not_damage_player(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={})
        client.post(
            "/api/round/start",
            json={
                "question": "Choose a world",
                "choices": ["A", "B"],
                "mode": "survey",
                "duration": 15,
            },
        )

        result = client.post(
            "/api/round/finish",
            json={"force": True},
        ).get_json()["round"]["result"]

        assert result["total_answers"] == 0
        assert result["wrong_percentage"] == 0.0
        assert result["player_damage"] == 0
        assert result["player_hp"] == 1000
        assert result["no_answer_penalty"] is False


def test_round_finishes_after_duration_once_an_answer_exists(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={})
        client.post(
            "/api/round/start",
            json={
                "question": "2 + 2 = ?",
                "choices": ["3", "4"],
                "correct_index": 1,
                "duration": 15,
            },
        )

        answer = client.post(
            "/api/round/answer",
            json={"player_id": "player-late1", "choice_index": 1},
        )
        assert answer.status_code == 200

        with store.lock:
            store.battle["current_round"]["ends_at"] = time.time() - 1

        current = client.get("/api/round/status").get_json()["round"]
        assert current["status"] == "finished"
        assert current["total_answers"] == 1
        assert current["result"]["total_answers"] == 1
        assert current["result"]["completion_reason"] == "duration"


def test_answer_from_unregistered_player_does_not_finish_early(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={})
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


def test_percentage_damage_is_player_count_independent():
    assert percentage_amount(100, 7, 10) == 70
    assert percentage_amount(100, 700, 1000) == 70
    assert percentage_amount(100, 3, 10) == 30
    assert percentage_amount(100, 300, 1000) == 30


def test_64_percent_correct_deals_64_and_36_damage(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={})
        client.post(
            "/api/round/start",
            json={
                "question": "64/36 balance",
                "choices": ["Correct", "Wrong"],
                "correct_index": 0,
                "duration": 15,
            },
        )

        for player_number in range(25):
            choice_index = 0 if player_number < 16 else 1
            client.post(
                "/api/round/answer",
                json={
                    "player_id": "player-balance-{:02d}".format(player_number),
                    "choice_index": choice_index,
                },
            )

        result = client.post(
            "/api/round/finish",
            json={"force": True},
        ).get_json()["round"]["result"]

        assert result["correct_percentage"] == 64.0
        assert result["wrong_percentage"] == 36.0
        assert result["monster_damage"] == 64
        assert result["player_damage"] == 36
        assert result["monster_hp"] == 936
        assert result["player_hp"] == 964


def test_answered_round_damage_split_totals_exactly_100(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post("/api/battle/start", json={})
        client.post(
            "/api/round/start",
            json={
                "question": "Rounding balance",
                "choices": ["Correct", "Wrong"],
                "correct_index": 0,
                "duration": 15,
            },
        )

        for player_number in range(8):
            client.post(
                "/api/round/answer",
                json={
                    "player_id": "player-rounding-{:02d}".format(player_number),
                    "choice_index": 0 if player_number == 0 else 1,
                },
            )

        result = client.post(
            "/api/round/finish",
            json={"force": True},
        ).get_json()["round"]["result"]

        assert result["correct_percentage"] == 12.5
        assert result["wrong_percentage"] == 87.5
        assert result["monster_damage"] == 13
        assert result["player_damage"] == 87
        assert result["monster_damage"] + result["player_damage"] == 100


def test_void_glitch_shortens_every_third_battle_round(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post(
            "/api/battle/start",
            json={"player_hp": 1000, "monster_hp": 1000, "monster_key": "void"},
        )

        for _ in range(2):
            started = client.post(
                "/api/round/start",
                json={
                    "question": "Void test",
                    "choices": ["A", "B"],
                    "correct_index": 0,
                    "duration": 15,
                },
            )
            assert started.get_json()["battle"]["current_round"]["duration"] == 15
            client.post("/api/round/finish", json={"force": True})

        third = client.post(
            "/api/round/start",
            json={
                "question": "Void glitch",
                "choices": ["A", "B"],
                "correct_index": 0,
                "duration": 15,
            },
        ).get_json()["battle"]["current_round"]

        assert third["base_duration"] == 15
        assert third["duration"] == 10
        assert third["duration_penalty"] == 5
        assert third["mechanic_event"] == "void_glitch"


def test_devourer_heals_by_wrong_answer_percentage(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post(
            "/api/battle/start",
            json={"player_hp": 1000, "monster_hp": 1000, "monster_key": "devourer"},
        )

        client.post(
            "/api/round/start",
            json={
                "question": "Damage first",
                "choices": ["A", "B"],
                "correct_index": 0,
                "duration": 15,
            },
        )
        client.post(
            "/api/round/answer",
            json={"player_id": "player-dev-01", "choice_index": 0},
        )
        first = client.post("/api/round/finish", json={"force": True}).get_json()["round"]["result"]
        assert first["monster_damage"] == 100
        assert first["monster_hp"] == 900

        client.post(
            "/api/round/start",
            json={
                "question": "Heal now",
                "choices": ["A", "B"],
                "correct_index": 0,
                "duration": 15,
            },
        )
        client.post(
            "/api/round/answer",
            json={"player_id": "player-dev-01", "choice_index": 0},
        )
        client.post(
            "/api/round/answer",
            json={"player_id": "player-dev-02", "choice_index": 1},
        )
        second = client.post("/api/round/finish", json={"force": True}).get_json()["round"]["result"]

        assert second["monster_damage"] == 50
        assert second["monster_heal"] == 10
        assert second["monster_hp"] == 860
        assert second["player_damage"] == 50
        assert second["player_hp"] == 950
        assert second["mechanic_event"] == "devourer_heal"


def test_colossus_armor_breaks_after_two_qualifying_combo_rounds(monkeypatch):
    monkeypatch.delenv("BATTLE_HOST_TOKEN", raising=False)
    store.reset()

    with app.test_client() as client:
        client.post(
            "/api/battle/start",
            json={"player_hp": 1000, "monster_hp": 1000, "monster_key": "colossus"},
        )

        results = []
        for round_number in range(2):
            client.post(
                "/api/round/start",
                json={
                    "question": "Armor combo {}".format(round_number + 1),
                    "choices": ["A", "B"],
                    "correct_index": 0,
                    "duration": 15,
                },
            )
            for player_number, choice_index in enumerate((0, 0, 0, 1, 1)):
                client.post(
                    "/api/round/answer",
                    json={
                        "player_id": "player-col-{:02d}".format(player_number),
                        "choice_index": choice_index,
                    },
                )
            results.append(
                client.post("/api/round/finish", json={"force": True}).get_json()["round"]["result"]
            )

        first, second = results
        assert first["correct_percentage"] == 60.0
        assert first["monster_damage"] == 0
        assert first["monster_damage_blocked"] == 60
        assert first["armor_combo"] == 1
        assert first["armor_active"] is True
        assert first["mechanic_event"] == "colossus_armor_block"

        assert second["monster_damage"] == 60
        assert second["monster_hp"] == 940
        assert second["armor_combo"] == 2
        assert second["armor_active"] is False
        assert second["armor_broken_this_round"] is True
        assert second["mechanic_event"] == "colossus_armor_break"
