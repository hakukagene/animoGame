define guide = Character("Систем", color="#8999FF")


label start:
    $ quick_menu = False
    $ cb_connection_message = ""
    $ cb_start_story_bgm()
    jump intro


label crowd_creators_questions:
    # Label-ийг developer menu-гээс шууд тестэлсэн ч үндсэн ая ажиллана.
    $ cb_start_story_bgm()
    $ response = cb_start_battle()
    $ renpy.block_rollback()

    while not response.get("success", False):
        call screen crowd_connection_error(response.get("error", "Сервертэй холбогдсонгүй."))
        $ response = cb_start_battle()
        $ renpy.block_rollback()

    $ creator_question_index = 0
    $ cb_creator_results = []

    while creator_question_index < len(Creators_Question):
        $ question = Creators_Question[creator_question_index]

        # Асуултыг OGG дуустал дэлгэцэнд харуулна. Үүний дараа server
        # round эхлэх тул 15 секундийн санал авах хугацаа бүтнээрээ үлдэнэ.
        $ cb_voice_line(N, question.get("question", ""), question.get("voice"))
        $ renpy.block_rollback()

        $ response = cb_start_round(question)
        $ renpy.block_rollback()

        while not response.get("success", False):
            call screen crowd_connection_error(
                response.get("error", "Санал асуулгыг эхлүүлж чадсангүй.")
            )
            $ response = cb_start_round(question)
            $ renpy.block_rollback()

        # Одоо эхэлсэн асуултын ID.
        $ creator_round_id = (cb_battle.get("current_round") or {}).get("round_id")

        # Яг санал авах хугацаанд хүлээлгийн ая тоглоно.
        # Screen дуусахад mystery ая pause хийсэн цэгээсээ үргэлжилнэ.
        $ cb_start_creator_wait_bgm()

        # Энэ screen duration дуусаж, сервер finished болтол return хийхгүй.
        call screen crowd_creators_round(
            creator_question_index + 1,
            len(Creators_Question),
            creator_round_id,
            question.get("duration", 15)
        )

        $ cb_finish_creator_wait_bgm()

        # Duration дууссаны дараа серверээс эцсийн үр дүнг авна.
        $ result = cb_fetch_round_result(creator_round_id)
        $ latest_round = cb_battle.get("current_round") or {}
        $ result = result or latest_round.get("result") or cb_round_result or {}

        # Cinematic-д ертөнц, мангасын төрлийг бодит саналын ялагчаар сонгоно.
        $ cb_record_creator_result(creator_question_index, question, result)

        # Зөвхөн одоо үр дүнгийн дэлгэц гарна.
        call screen crowd_creators_result(question, result)

        $ creator_question_index += 1
    return


label crowd_monster_battle:
    # Battle-ийн бүх асуулт, result болон ending дэлгэцийн турш loop хийнэ.
    $ cb_start_battle_bgm()
    $ cb_battle_end_reason = ""
    $ response = cb_start_battle()
    $ renpy.block_rollback()

    while not response.get("success", False):
        call screen crowd_connection_error(response.get("error", "Сервертэй холбогдсонгүй."))
        $ response = cb_start_battle()
        $ renpy.block_rollback()

    $ question_index = 0

    # Нэг battle-д 20 асуултыг нэг удаа л ашиглана.
    while cb_battle_status == "active" and question_index < len(CROWD_BATTLE_QUESTIONS):
        $ question = CROWD_BATTLE_QUESTIONS[question_index]

        # Anime quiz эхэлснээс хойш say/dialogue screen рүү шилжихгүй.
        # Ижил battle HUD дээр асуулт + хариултыг харуулж OGG-г дуусгана.
        show screen crowd_battle_voice_preview(question)
        $ voice_played = cb_play_ogg_and_wait(question.get("voice"))
        if not voice_played:
            $ renpy.pause(1.5, hard=True, modal=False)
        hide screen crowd_battle_voice_preview
        $ renpy.block_rollback()
        
        
        $ response = cb_start_round(question)
        $ renpy.block_rollback()

        while not response.get("success", False):
            call screen crowd_connection_error(response.get("error", "Асуулт эхлүүлж чадсангүй."))
            $ response = cb_start_round(question)
            $ renpy.block_rollback()

        $ battle_round_id = (cb_battle.get("current_round") or {}).get("round_id")
        
        call screen crowd_battle_round(battle_round_id)
        $ result = _return or cb_round_result

        if not result:
            $ response = cb_force_finish_round()
            $ result = cb_round_result
            $ renpy.block_rollback()

        $ is_final_question = question_index + 1 >= len(CROWD_BATTLE_QUESTIONS)
        call screen crowd_round_result(result, is_final_question)
        $ question_index += 1

    # Хожих нөхцөл: мангасын HP 0. Хоёр тал зэрэг 0 болсон бол серверийн
    # одоогийн дүрмээр final strike хийсэн тоглогчдын баг ялна.
    $ victory = cb_battle_status == "victory" or cb_monster_hp <= 0

    if victory:
        $ cb_battle_end_reason = "Мангасын HP 0 болсон."
        call crowd_victory_ending
    else:
        if cb_player_hp <= 0:
            $ cb_battle_end_reason = "Үзэгчдийн багийн HP 0 болсон."
        else:
            $ cb_battle_end_reason = "20 асуулт дуусахад мангас амьд үлдсэн."
        call crowd_defeat_ending

    call screen crowd_battle_ending(victory)

    if _return == "restart":
        jump crowd_monster_battle

    # Battle label бүрэн дуусаж гарах мөчид зодооны ая зогсоно.
    $ cb_stop_battle_bgm()
    $ cb_reset_battle()
    $ renpy.block_rollback()
    return


label screen:
    pass
