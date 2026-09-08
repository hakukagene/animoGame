transform cb_monster_idle:
    anchor (0.5, 0.5)
    zoom 1.0
    linear 0.8 zoom 1.035
    linear 0.8 zoom 1.0
    repeat


transform cb_result_pop:
    alpha 0.0
    zoom 0.75
    linear 0.22 alpha 1.0 zoom 1.05
    linear 0.12 zoom 1.0


define CB_RESULT_DISPLAY_SECONDS = 4


init -35 python:
    # Creators-ийн ертөнцийн асуултад тоглох жижиг video preview-үүд.
    CB_WORLD_PREVIEW_DATA = {
        "Futuristic": "cb_preview_futuristic",
        "Fantasy": "cb_preview_fantasy",
        "Modern": "cb_preview_modern",
        "Post-apocalyptic": "cb_preview_post",
    }

    # Citizen хавтас дахь сонголт бүрийн зураг.
    CB_CITIZEN_PREVIEW_DATA = {
        "Humans": "citizen/Human.png",
        "Robots": "citizen/Robots.png",
        "Magic Creatures": "citizen/Magic Creatures.png",
        "Aliens": "citizen/Alien.png",
        "Anime Characters": "citizen/Anime.png",
        "Elfs": "citizen/elf.png",
        "Monsters": "images/cinematic/boss_void.webp",
        "Orcs": "citizen/Orc.png",
    }

    # Нэг дэлгэц дээр дөрвөн Movie зэрэг ажиллах тул тус бүр өөр channel-тэй.
    for _cb_movie_channel in (
        "cb_preview_futuristic",
        "cb_preview_fantasy",
        "cb_preview_modern",
        "cb_preview_post",
    ):
        if not renpy.music.channel_defined(_cb_movie_channel):
            renpy.music.register_channel(
                _cb_movie_channel,
                mixer="sfx",
                loop=True,
                stop_on_mute=False,
                buffer_queue=False,
                movie=True,
            )


# Movie displayable-уудыг screen ажиллахаас өмнө init үеэр үүсгэнэ.
# `image` нь video байхгүй/дэмжигдэхгүй төхөөрөмж дээрх fallback зураг.
image cb_preview_futuristic = Movie(
    play="video/cinematic/BG/BG_Futuristic.webm",
    channel="cb_preview_futuristic",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_futuristic.webp",
)
image cb_preview_fantasy = Movie(
    play="video/cinematic/BG/BG_Fantasy.webm",
    channel="cb_preview_fantasy",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_fantasy.webp",
)
image cb_preview_modern = Movie(
    play="video/cinematic/BG/BG_Modern.webm",
    channel="cb_preview_modern",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_modern.webp",
)
image cb_preview_post = Movie(
    play="video/cinematic/BG/BG_Post.webm",
    channel="cb_preview_post",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_post.webp",
)


style cb_title_text:
    color "#F6F7FF"
    size 46
    bold True

style cb_body_text:
    color "#D7DCEF"
    size 28

style cb_small_text:
    color "#A8B0C7"
    size 22

style cb_button is button:
    background Solid("#263354")
    hover_background Solid("#5268D8")
    padding (30, 16)
    xminimum 270

style cb_button_text is button_text:
    color "#FFFFFF"
    size 26
    bold True
    text_align 0.5

screen crowd_battle_intro():
    modal True
    add Solid("#070B14")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 28

        text "[cb_enemy_title]" style "cb_title_text" xalign 0.5
        text "Үзэгчдийн зөв хариулт бүр мангасад damage өгнө.\nБуруу хариулт бүр танай багийн HP-г хасна.":
            style "cb_body_text"
            text_align 0.5
            xalign 0.5

        text "Утаснаасаа нээх хаяг:" style "cb_small_text" xalign 0.5
        text "[cb_server_url()]":
            color "#8999FF"
            size 30
            bold True
            xalign 0.5

        null height 14
        textbutton "ТУЛААН ЭХЛҮҮЛЭХ":
            style "cb_button"
            xalign 0.5
            action Return(True)


screen crowd_battle_round(expected_round_id=None, preview_question=None, preview_mode=False):
    modal True

    $ current_round = cb_battle.get("current_round") or {}
    $ guarded_round_id = expected_round_id or cb_round_guard_id
    $ shown_question = (preview_question or {}).get("question", "") if preview_mode else current_round.get("question", "")

    add Solid("#070B14")
    add Solid("#101A31") xysize (1920, 270)

    # Уншиж байх үед server round хараахан эхлээгүй учраас poll/Return
    # ажиллуулахгүй. Voice дууссаны дараах active mode-д л ажиллана.
    if not preview_mode:
        timer 0.25 repeat True action Function(cb_poll_round_action)

        if cb_round_can_finish(guarded_round_id):
            timer 0.10 action Return(current_round.get("result") or cb_round_result)

    vbox:
        xpos 90
        ypos 45
        xsize 760
        spacing 10
        text "ҮЗЭГЧДИЙН БАГ" style "cb_small_text"
        text "[cb_player_hp] / [cb_player_max_hp] HP":
            color "#7FF0BB"
            size 29
            bold True
        bar:
            value StaticValue(cb_player_hp, cb_player_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#38D99A")
            right_bar Solid("#24304A")

    vbox:
        xpos 1070
        ypos 45
        xsize 760
        spacing 10
        text "[cb_enemy_name]" style "cb_small_text" xalign 1.0
        text "[cb_monster_hp] / [cb_monster_max_hp] HP":
            color "#FF8296"
            size 29
            bold True
            xalign 1.0
        bar:
            value StaticValue(cb_monster_hp, cb_monster_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#FF5F78")
            right_bar Solid("#24304A")
            xalign 1.0

    add cb_enemy_idle_image:
        at cb_monster_idle
        xalign 0.5
        ycenter 470

    frame:
        background Solid("#121B30EE")
        xalign 0.5
        ypos 660
        xsize 1540
        padding (50, 34)

        vbox:
            spacing 18

            if preview_mode:
                text "АСУУЛТ УНШИЖ БАЙНА...":
                    color "#8999FF"
                    size 28
                    bold True
                    xalign 0.5
            else:
                text "[cb_remaining_seconds] секунд":
                    color "#FF899D"
                    size 30
                    bold True
                    xalign 0.5

            if shown_question:
                text shown_question:
                    color "#FFFFFF"
                    size 37
                    bold True
                    text_align 0.5
                    xalign 0.5

            if preview_mode:
                text "Дуу дуусмагц санал авах 15 секунд эхэлнэ.":
                    style "cb_small_text"
                    xalign 0.5
            else:
                text "Хариулсан тоглогч: [cb_total_answers]":
                    style "cb_small_text"
                    xalign 0.5

                text "Утаснаасаа: [cb_server_url()]":
                    color "#8999FF"
                    size 24
                    xalign 0.5

                if cb_connection_message:
                    text cb_connection_message:
                        color "#FF899D"
                        size 20
                        xalign 0.5


screen crowd_round_result(result, final_question=False):
    modal True
    default auto_seconds = CB_RESULT_DISPLAY_SECONDS

    $ correct_count = result.get("correct_count", 0)
    $ wrong_count = result.get("wrong_count", 0)
    $ monster_damage = result.get("monster_damage", 0)
    $ player_damage = result.get("player_damage", 0)
    $ total_answers = result.get("total_answers", 0)
    $ battle_finished = result.get("battle_status", "active") in ("victory", "defeat")
    $ next_part_text = "төгсгөлийн хэсэг" if battle_finished or final_question else "дараагийн асуулт"

    add Solid("#070B14")
    add Solid("#7C3AED22")

    # Button шаардахгүй: үр дүнг дөрвөн секунд үзүүлээд өөрөө үргэлжилнэ.
    timer 1.0 repeat True action If(
        auto_seconds > 1,
        SetScreenVariable("auto_seconds", auto_seconds - 1),
        Return(True)
    )

    frame:
        at cb_result_pop
        background Solid("#121B30F7")
        xalign 0.5
        yalign 0.5
        xsize 1180
        padding (70, 54)

        vbox:
            spacing 24
            xfill True

            text "АСУУЛТЫН ҮР ДҮН" style "cb_title_text" xalign 0.5

            hbox:
                xalign 0.5
                spacing 120

                vbox:
                    spacing 8
                    text "ЗӨВ" color "#59E6A8" size 28 bold True xalign 0.5
                    text "[correct_count]" color "#FFFFFF" size 78 bold True xalign 0.5
                    text "Мангас -[monster_damage] HP" color "#59E6A8" size 24 xalign 0.5

                vbox:
                    spacing 8
                    text "БУРУУ" color "#FF8296" size 28 bold True xalign 0.5
                    text "[wrong_count]" color "#FFFFFF" size 78 bold True xalign 0.5
                    text "Баг -[player_damage] HP" color "#FF8296" size 24 xalign 0.5

            text "Нийт хариулт: [total_answers]" style "cb_small_text" xalign 0.5

            text "[auto_seconds] секундын дараа [next_part_text] руу автоматаар шилжинэ.":
                color "#8999FF"
                size 23
                xalign 0.5
                text_align 0.5


screen crowd_creators_round(question_number, question_total, expected_round_id=None, question_duration=15):
    modal True

    $ current_round = cb_battle.get("current_round") or {}
    $ guarded_round_id = expected_round_id or cb_round_guard_id

    add Solid("#070B14")

    # Серверийн хугацаа, хариултын төлөвийг шинэчилнэ.
    timer 0.25 repeat True action Function(cb_poll_round_action)

    # Бүгд хариулсан ЭСВЭЛ duration дууссан үед return хийнэ.
    if cb_round_can_finish(guarded_round_id):
        timer 0.10 action Return(True)
    
    frame:
        background Solid("#121B30F7")
        xalign 0.5
        yalign 0.5
        xsize 1500
        padding (60, 42)

        vbox:
            spacing 18
            xfill True

            text "CREATORS' QUESTION · [question_number]/[question_total]":
                color "#8999FF"
                size 24
                bold True
                xalign 0.5

            text "[cb_remaining_seconds] секунд":
                color "#FF899D"
                size 30
                bold True
                xalign 0.5

            text current_round.get("question", ""):
                color "#FFFFFF"
                size 38
                bold True
                text_align 0.5
                xalign 0.5

            # 2-р асуулт: BG хавтасны cinematic бүрийг жижиг preview болгоно.
            if question_number == 2:
                hbox:
                    spacing 18
                    xalign 0.5

                    for choice in current_round.get("choices", []):
                        $ preview_image = CB_WORLD_PREVIEW_DATA.get(choice)

                        frame:
                            background Solid("#18233BF5")
                            xsize 330
                            ysize 235
                            padding (14, 14)

                            vbox:
                                spacing 10
                                xalign 0.5

                                if preview_image:
                                    add preview_image:
                                        xysize (300, 169)
                                        xalign 0.5

                                text choice:
                                    color "#F6F7FF"
                                    size 23
                                    bold True
                                    xalign 0.5
                                    text_align 0.5

            # 4-р асуулт: Citizen зургуудыг 4 x 2 сонголтын карт болгоно.
            elif question_number == 4:
                vbox:
                    spacing 12
                    xalign 0.5

                    for row_start in range(0, len(current_round.get("choices", [])), 4):
                        hbox:
                            spacing 16
                            xalign 0.5

                            for choice in current_round.get("choices", [])[row_start:row_start + 4]:
                                $ citizen_image = CB_CITIZEN_PREVIEW_DATA.get(choice)

                                frame:
                                    background Solid("#18233BF5")
                                    xsize 330
                                    ysize 205
                                    padding (12, 10)

                                    vbox:
                                        spacing 7
                                        xalign 0.5

                                        if citizen_image:
                                            add citizen_image:
                                                xysize (230, 135)
                                                xalign 0.5

                                        text choice:
                                            color "#F6F7FF"
                                            size 21
                                            bold True
                                            xalign 0.5
                                            text_align 0.5

            # Бусад creators асуултын layout өөрчлөгдөхгүй.
            else:
                vbox:
                    spacing 12
                    xalign 0.5

                    for choice in current_round.get("choices", []):
                        text choice:
                            color "#D7DCEF"
                            size 28
                            xalign 0.5

            text "Утаснаасаа сонголтоо хийнэ үү.":
                style "cb_small_text"
                xalign 0.5


screen crowd_creators_result(question, result):
    modal True
    default auto_seconds = CB_RESULT_DISPLAY_SECONDS

    $ latest_round = cb_battle.get("current_round") or {}
    $ latest_result = result or latest_round.get("result") or {}
    $ choices = question.get("choices", [])
    $ counts = latest_result.get("choice_counts", latest_round.get("choice_counts", []))
    $ total_answers = max(0, int(latest_result.get("total_answers", latest_round.get("total_answers", 0))))
    $ top_indices = latest_result.get("top_choice_indices", [])
    $ winner_labels = [choices[index] for index in top_indices if 0 <= index < len(choices)]
    $ winner_text = ", ".join(winner_labels)
    add Solid("#070B14")
    add Solid("#6F7CFF18")

    # Result-ийг дөрвөн секунд харуулаад дараагийн үйл явдал руу орно.
    timer 1.0 repeat True action If(
        auto_seconds > 1,
        SetScreenVariable("auto_seconds", auto_seconds - 1),
        Return(True)
    )

    frame:
        at cb_result_pop
        background Solid("#121B30F7")
        xalign 0.5
        yalign 0.5
        xsize 1400
        padding (65, 42)

        vbox:
            spacing 18
            xfill True

            text "САНАЛ АСУУЛГЫН ҮР ДҮН":
                style "cb_title_text"
                xalign 0.5

            text question.get("question", ""):
                color "#FFFFFF"
                size 32
                bold True
                text_align 0.5
                xalign 0.5

            vbox:
                spacing 12
                xfill True

                for index, choice in enumerate(choices):
                    $ count = counts[index] if index < len(counts) else 0
                    $ percentage = int(round(100.0 * count / total_answers)) if total_answers else 0

                    hbox:
                        spacing 18
                        xfill True

                        text choice:
                            color "#D7DCEF"
                            size 24
                            xsize 780

                        text "[count] · [percentage]%":
                            color "#8999FF"
                            size 24
                            bold True
                            xalign 1.0
                            xsize 360
                            text_align 1.0

            text "Нийт оролцогч: [total_answers] · Нийт санал: [total_answers]":
                style "cb_small_text"
                xalign 0.5

            if winner_text:
                text "Хамгийн олон санал: [winner_text]":
                    color "#59E6A8"
                    size 25
                    bold True
                    xalign 0.5

            text "[auto_seconds] секундын дараа автоматаар үргэлжилнэ.":
                color "#8999FF"
                size 23
                xalign 0.5
                text_align 0.5


screen crowd_battle_ending(victory):
    modal True
    add Solid("#070B14")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        if victory:
            text "ЯЛАЛТ!" color "#59E6A8" size 100 bold True xalign 0.5
            text "Үзэгчдийн баг [cb_enemy_name]-г яллаа." style "cb_body_text" xalign 0.5
        else:
            text "ЯЛАГДАЛ" color "#FF8296" size 100 bold True xalign 0.5
            text "Ертөнцийг хамгаалж чадсангүй." style "cb_body_text" xalign 0.5

        text "[cb_battle_end_reason]":
            style "cb_small_text"
            xalign 0.5

        hbox:
            spacing 20
            xalign 0.5
            textbutton "ДАХИН ТОГЛОХ":
                style "cb_button"
                action Return("restart")
            textbutton "ГАРАХ":
                style "cb_button"
                action Return("quit")


screen crowd_connection_error(message):
    modal True
    add Solid("#070B14EE")

    frame:
        background Solid("#191426F7")
        xalign 0.5
        yalign 0.5
        xsize 1050
        padding (60, 45)

        vbox:
            spacing 24
            text "ХОЛБОЛТЫН АЛДАА" color "#FF8296" size 45 bold True xalign 0.5
            text message style "cb_body_text" text_align 0.5 xalign 0.5
            hbox:
                spacing 20
                xalign 0.5
                textbutton "ДАХИН ОРОЛДОХ":
                    style "cb_button"
                    action Return("retry")
