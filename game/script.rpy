define guide = Character("Систем", color="#8999FF")


label start:
    $ quick_menu = False
    $ cb_connection_message = ""
    jump intro 
    jump crowd_monster_battle


label crowd_creators_questions:
    $ response = cb_start_battle()
    $ renpy.block_rollback()

    while not response.get("success", False):
        call screen crowd_connection_error(response.get("error", "Сервертэй холбогдсонгүй."))
        $ response = cb_start_battle()
        $ renpy.block_rollback()

    $ creator_question_index = 0

    while creator_question_index < len(Creators_Question):
        $ question = Creators_Question[creator_question_index]
        $ response = cb_start_round(question)
        $ renpy.block_rollback()

        while not response.get("success", False):
            call screen crowd_connection_error(response.get("error", "Санал асуулгыг эхлүүлж чадсангүй."))
            $ response = cb_start_round(question)
            $ renpy.block_rollback()

        call screen crowd_creators_round(creator_question_index + 1, len(Creators_Question))

        # Read once more after the timer closes so the result screen never
        # receives the empty response saved when the round was first opened.
        $ response = cb_poll_round()
        $ latest_round = cb_battle.get("current_round") or {}
        $ result = latest_round.get("result") or cb_round_result or {}

        if not result:
            $ response = cb_force_finish_round()
            $ latest_round = cb_battle.get("current_round") or {}
            $ result = latest_round.get("result") or cb_round_result or {}
            $ renpy.block_rollback()

        call screen crowd_creators_result(question, result)
        $ creator_question_index += 1

    return


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
