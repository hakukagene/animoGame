init -100 python:
    CROWD_BATTLE_SERVER_URL = "https://game-bnkw.onrender.com/"
    CROWD_BATTLE_HOST_TOKEN = ""
    CROWD_BATTLE_MONSTER_DAMAGE = 40
    CROWD_BATTLE_PLAYER_DAMAGE = 25

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
default cb_round_guard_id = ""
default cb_round_local_deadline = 0.0
default cb_expected_answers = 0
default cb_all_answers_received = False


init python:
    import time


    def cb_server_url():
        return CROWD_BATTLE_SERVER_URL.rstrip("/")


    def cb_host_headers():
        token = CROWD_BATTLE_HOST_TOKEN.strip()
        if token:
            return {"X-Host-Token": token}
        return {}


    def cb_api(path, method="GET", payload=None, host=False, timeout=6):
        headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        if host:
            headers.update(cb_host_headers())

        try:
            result = renpy.fetch(
                cb_server_url() + path,
                method=method,
                json=payload,
                result="json",
                timeout=timeout,
                headers=headers,
            )

            if not hasattr(result, "get"):
                return {
                    "success": False,
                    "error": "Серверийн JSON хариу object биш байна: {}".format(type(result).__name__),
                }

            return result
        except Exception as exc:
            return {
                "success": False,
                "error": "Сервертэй холбогдсонгүй: {}".format(exc),
            }


    def cb_apply_battle(response):
        battle = response.get("battle") if hasattr(response, "get") else None
        if not hasattr(battle, "get"):
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
        store.cb_expected_answers = max(0, int(current.get("expected_answers", 0)))
        store.cb_all_answers_received = bool(current.get("all_answers_received", False))
        return True


    def cb_start_battle():
        response = cb_api(
            "/api/battle/start",
            method="POST",
            payload={
                "team_name": "Үзэгчдийн баг",
                "monster_name": getattr(store, "cb_enemy_name", "Сүүдрийн мангас"),
                "monster_key": getattr(store, "cb_enemy_key", "void"),
                "player_hp": 200,
                "monster_hp": 250,
            },
            host=True,
        )
        cb_apply_battle(response)
        return response



    def cb_start_round(question):

        print("DEBUG 1: cb_start_round START")

        store.cb_round_status = "starting"
        store.cb_round_result = {}
        store.cb_total_answers = 0
        store.cb_expected_answers = 0
        store.cb_all_answers_received = False
        store.cb_round_guard_id = ""
        store.cb_round_local_deadline = 0.0

        print("DEBUG 2: state reset OK")

        requested_duration = max(
            5,
            min(120, int(question.get("duration", 15)))
        )

        store.cb_remaining_seconds = requested_duration

        mode = question.get("mode", "battle")

        payload = {
            "question": question["question"],
            "choices": question["choices"],
            "mode": mode,
            "duration": requested_duration,
        }

        if mode == "survey":
            payload["attack_power"] = 0
            payload["enemy_attack_power"] = 0

        else:
            payload["correct_index"] = question["correct_index"]
            # Нэг хүний хариултыг damage болгохгүй. Server нийт зөв/буруу
            # хариултын хувийг эдгээр дээд утгаар үржүүлж бодно.
            payload["attack_power"] = CROWD_BATTLE_MONSTER_DAMAGE
            payload["enemy_attack_power"] = CROWD_BATTLE_PLAYER_DAMAGE

        print("DEBUG 3: PAYLOAD READY")
        print(payload)

        print("DEBUG 4: BEFORE cb_api")

        try:

            response = cb_api(
                "/api/round/start",
                method="POST",
                payload=payload,
                host=True,
            )

        except Exception as e:
            import traceback

            print("====================================")
            print("CB_API ERROR")
            print("TYPE =", type(e))
            print("REPR =", repr(e))
            print("STR =", str(e))
            traceback.print_exc()
            print("====================================")

            return {
                "success": False,
                "error": "Сервертэй холбогдсонгүй: {}".format(repr(e)),
        }

        print("DEBUG 5: AFTER cb_api")
        print("RESPONSE =", response)

        cb_apply_battle(response)

        print("DEBUG 6: AFTER cb_apply_battle")

        if response.get("success"):

            current = store.cb_battle.get("current_round") or {}

            print("CURRENT ROUND =", current)

            round_id = current.get("round_id")

            print("ROUND ID =", round_id)

            if round_id:

                server_duration = max(
                    5,
                    min(
                        120,
                        int(
                            current.get(
                                "duration",
                                requested_duration
                            )
                        )
                    )
                )

                store.cb_round_guard_id = round_id
                store.cb_round_local_deadline = (
                    time.monotonic()
                    + server_duration
                )

        print("DEBUG 7: cb_start_round RETURN")

        return response


    def cb_round_can_finish(expected_round_id):
        current = store.cb_battle.get("current_round") or {}

        if not expected_round_id or current.get("round_id") != expected_round_id:
            return False

        result = current.get("result") or {}
        if current.get("status") != "finished" or not result:
            return False

        # Server өөрөө бүх идэвхтэй тоглогч хариулсан эсвэл duration дууссан
        # үед л round-ыг finished болгодог. Client талд deadline/participant
        # нөхцөлийг дахин шалгавал server/local timer-ийн зөрүүнээс болж
        # result гацаж болно. Энд зөвхөн хамгаалагдсан round_id-г шалгана.
        return result.get("round_id") == expected_round_id


    def cb_uncached_path(path):
        separator = "&" if "?" in path else "?"
        return "{}{}cb={}".format(path, separator, int(time.time() * 1000))


    def cb_poll_round():
        response = cb_api(
            cb_uncached_path("/api/round/status"), 
            timeout=4
            )

        if response.get("success"):
            store.cb_connection_message = ""
            cb_apply_battle(response)
        else:
            store.cb_connection_message = response.get(
                "error",
                "Холболтын алдаа"
            )

        return response


    def cb_poll_round_action():
        cb_poll_round()
        return None


    def cb_fetch_round_result(expected_round_id):
        response = cb_api(cb_uncached_path("/api/round/result"), timeout=6)
        if not response.get("success"):
            return {}

        result = response.get("result") or {}
        if expected_round_id and result.get("round_id") != expected_round_id:
            return {}

        cb_apply_battle(response)
        store.cb_round_result = result
        store.cb_connection_message = ""
        return result


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
        store.cb_round_guard_id = ""
        store.cb_round_local_deadline = 0.0
        store.cb_expected_answers = 0
        store.cb_all_answers_received = False
        response = cb_api(
            "/api/battle/reset",
            method="POST",
            payload={},
            host=True,
        )
        cb_apply_battle(response)
        return response
