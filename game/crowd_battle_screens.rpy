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

        text "СҮҮДРИЙН МАНГАС" style "cb_title_text" xalign 0.5
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


screen crowd_battle_round():
    modal True
    $ current_round = cb_battle.get("current_round") or {}
    add Solid("#070B14")
    add Solid("#101A31") xysize (1920, 270)

    timer 0.7 repeat True action Function(cb_poll_round)

    if cb_round_status == "finished":
        timer 0.25 action Return(cb_round_result)

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
        text "СҮҮДРИЙН МАНГАС" style "cb_small_text" xalign 1.0
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

    text "МАНГАС":
        at cb_monster_idle
        xalign 0.5
        ypos 395
        color "#B983FF"
        size 94
        bold True
        outlines [(6, "#3B174FFF", 0, 0)]

    frame:
        background Solid("#121B30EE")
        xalign 0.5
        ypos 660
        xsize 1540
        padding (50, 34)

        vbox:
            spacing 18
            text "[cb_remaining_seconds] секунд":
                color "#FF899D"
                size 30
                bold True
                xalign 0.5

            if current_round:
                text current_round.get("question", ""):
                    color "#FFFFFF"
                    size 37
                    bold True
                    text_align 0.5
                    xalign 0.5

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


screen crowd_round_result(result):
    modal True
    $ correct_count = result.get("correct_count", 0)
    $ wrong_count = result.get("wrong_count", 0)
    $ monster_damage = result.get("monster_damage", 0)
    $ player_damage = result.get("player_damage", 0)
    $ total_answers = result.get("total_answers", 0)
    add Solid("#070B14")
    add Solid("#7C3AED22")

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

            textbutton "ДАРААГИЙН АСУУЛТ":
                style "cb_button"
                xalign 0.5
                action Return(True)


screen crowd_battle_ending(victory):
    modal True
    add Solid("#070B14")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        if victory:
            text "ЯЛАЛТ!" color "#59E6A8" size 100 bold True xalign 0.5
            text "Үзэгчдийн баг Сүүдрийн мангасыг яллаа." style "cb_body_text" xalign 0.5
        else:
            text "ЯЛАГДАЛ" color "#FF8296" size 100 bold True xalign 0.5
            text "Багийн HP дууслаа. Дахин оролдоорой." style "cb_body_text" xalign 0.5

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
