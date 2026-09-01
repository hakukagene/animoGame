define guide = Character("Систем", color="#8999FF")


label start:
    $ quick_menu = False
    $ cb_connection_message = ""
    jump crowd_monster_battle


label crowd_monster_battle:
    $ response = cb_start_battle()
    $ renpy.block_rollback()

    while not response.get("success", False):
        call screen crowd_connection_error(response.get("error", "Сервертэй холбогдсонгүй."))
        $ response = cb_start_battle()
        $ renpy.block_rollback()

    call screen crowd_battle_intro

    $ question_index = 0

    while cb_battle_status == "active":
        $ question = CROWD_BATTLE_QUESTIONS[question_index % len(CROWD_BATTLE_QUESTIONS)]
        $ response = cb_start_round(question)
        $ renpy.block_rollback()

        while not response.get("success", False):
            call screen crowd_connection_error(response.get("error", "Асуулт эхлүүлж чадсангүй."))
            $ response = cb_start_round(question)
            $ renpy.block_rollback()

        call screen crowd_battle_round
        $ result = _return or cb_round_result

        if not result:
            $ response = cb_force_finish_round()
            $ result = cb_round_result
            $ renpy.block_rollback()

        call screen crowd_round_result(result)
        $ question_index += 1

    $ victory = cb_battle_status == "victory"
    call screen crowd_battle_ending(victory)

    if _return == "restart":
        jump crowd_monster_battle

    $ cb_reset_battle()
    $ renpy.block_rollback()
    return
