init -100 python:
    CROWD_DEFAULT_SERVER_URL = "http://127.0.0.1:5000"

default cb_connection_message = ""
default cb_connection_ok = False
default cb_battle = {}
default cb_round_result = {}
default cb_battle_status = "idle"
default cb_round_status = "idle"
default cb_player_hp = 200
default cb_player_max_hp = 200
default cb_monster_hp = 250
default cb_monster_max_hp = 250
default cb_total_answers = 0
default cb_remaining_seconds = 0


init -10 python:
    if not getattr(persistent, "crowd_server_url", None):
        persistent.crowd_server_url = CROWD_DEFAULT_SERVER_URL

    if not hasattr(persistent, "crowd_host_token"):
        persistent.crowd_host_token = ""


init python:
    def cb_server_url():
        url = getattr(persistent, "crowd_server_url", CROWD_DEFAULT_SERVER_URL)
        url = (url or CROWD_DEFAULT_SERVER_URL).strip().rstrip("/")
        return url


    def cb_host_headers():
        token = (getattr(persistent, "crowd_host_token", "") or "").strip()
        if token:
            return {"X-Host-Token": token}
        return {}


    def cb_api(path, method="GET", payload=None, host=False, timeout=6):
        headers = cb_host_headers() if host else {}

        try:
            result = renpy.fetch(
                cb_server_url() + path,
                method=method,
                json=payload,
                result="json",
                timeout=timeout,
                headers=headers,
            )

            if not isinstance(result, dict):
                return {"success": False, "error": "Сервер буруу форматтай хариу өглөө."}

            return result
        except Exception as exc:
            return {
                "success": False,
                "error": "Сервертэй холбогдсонгүй: {}".format(exc),
            }


    def cb_apply_battle(response):
        battle = response.get("battle") if isinstance(response, dict) else None
        if not isinstance(battle, dict):
            return False

        store.cb_battle = battle
        store.cb_battle_status = battle.get("status", "idle")
        store.cb_player_hp = int(battle.get("player_hp", 0))
        store.cb_player_max_hp = max(1, int(battle.get("player_max_hp", 1)))
        store.cb_monster_hp = int(battle.get("monster_hp", 0))
        store.cb_monster_max_hp = max(1, int(battle.get("monster_max_hp", 1)))

        current = battle.get("current_round") or response.get("round") or {}
        store.cb_round_status = current.get("status", "idle")
        store.cb_total_answers = int(current.get("total_answers", 0))
        store.cb_remaining_seconds = int(current.get("remaining_seconds", 0))
        store.cb_round_result = current.get("result") or {}
        return True


    def cb_test_connection():
        store.cb_connection_message = "Холболтыг шалгаж байна..."
        store.cb_connection_ok = False
        response = cb_api("/api/health", timeout=4)

        if response.get("success"):
            store.cb_connection_ok = True
            store.cb_connection_message = "Сервертэй амжилттай холбогдлоо."
        else:
            store.cb_connection_message = response.get("error", "Сервертэй холбогдсонгүй.")


    def cb_normalize_server_settings():
        persistent.crowd_server_url = cb_server_url()
        persistent.crowd_host_token = (
            getattr(persistent, "crowd_host_token", "") or ""
        ).strip()
        renpy.save_persistent()


    def cb_start_battle():
        response = cb_api(
            "/api/battle/start",
            method="POST",
            payload={
                "team_name": "Үзэгчдийн баг",
                "monster_name": "Сүүдрийн мангас",
                "player_hp": 200,
                "monster_hp": 250,
            },
            host=True,
        )
        cb_apply_battle(response)
        return response


    def cb_start_round(question):
        payload = {
            "question": question["question"],
            "choices": question["choices"],
            "correct_index": question["correct_index"],
            "duration": question.get("duration", 15),
            "attack_power": question.get("attack_power", 25),
            "enemy_attack_power": question.get("enemy_attack_power", 20),
        }
        response = cb_api(
            "/api/round/start",
            method="POST",
            payload=payload,
            host=True,
        )
        cb_apply_battle(response)
        return response


    def cb_poll_round():
        response = cb_api("/api/round/status", timeout=4)
        if response.get("success"):
            store.cb_connection_message = ""
            cb_apply_battle(response)
        else:
            store.cb_connection_message = response.get("error", "Холболтын алдаа")
        return response


    def cb_force_finish_round():
        response = cb_api(
            "/api/round/finish",
            method="POST",
            payload={"force": True},
            host=True,
        )
        cb_apply_battle(response)
        return response


    def cb_reset_battle():
        response = cb_api(
            "/api/battle/reset",
            method="POST",
            payload={},
            host=True,
        )
        cb_apply_battle(response)
        return response
