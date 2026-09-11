# Concept 2 artwork is shared; only live content is drawn by Ren'Py.
init -10 python:
    CB_CONSOLE_ROOT = "images/creators_console/"
    CB_CONSOLE_FONT = "fonts/PressStart2P-Regular.ttf"
    CB_CONSOLE_SHEETS = {
        1: ("roles.png", 1672, 941, 4, 2),
        3: ("locations.png", 1536, 1024, 3, 2),
        4: ("citizens.png", 1672, 941, 4, 2),
        5: ("traits.png", 2172, 724, 4, 1),
        6: ("enemies.png", 2172, 724, 3, 1),
    }
    CB_CONSOLE_WORLDS = [
        (110, 400, 324, 258), (485, 400, 324, 258),
        (861, 400, 324, 258), (1238, 400, 324, 258),
    ]

    def cb_console_art(question_number, index, target_size=None):
        if question_number == 2:
            filename = "reference.png"
            x0, y0, width, height = CB_CONSOLE_WORLDS[index]
        else:
            filename, width, height, cols, rows = CB_CONSOLE_SHEETS[question_number]
            col, row = index % cols, index // cols
            x0, x1 = width * col // cols, width * (col + 1) // cols
            y0, y1 = height * row // rows, height * (row + 1) // rows
            width, height = x1-x0, y1-y0
        # Explicit source crop prevents cover-fit artwork spilling over card labels.
        if target_size:
            ratio = float(target_size[0]) / target_size[1]
            if width / float(height) > ratio:
                crop_width = max(1, int(height * ratio))
                x0 += (width-crop_width) // 2
                width = crop_width
            else:
                crop_height = max(1, int(width / ratio))
                y0 += (height-crop_height) // 2
                height = crop_height
        return Crop((x0, y0, width, height), CB_CONSOLE_ROOT + filename)

    def cb_console_card_frame():
        # Actual pixel border from the chosen concept, not an approximation.
        return Frame(Crop((470, 383, 357, 338),
                        CB_CONSOLE_ROOT + "reference.png"), 18, 18)

    def cb_console_layout(question_number):
        # x, y, width, height; all inside the central panel at 1672x941.
        if question_number in (1, 4):
            return [(166 + i*340, 365, 200, 254) for i in range(4)] + [
                (336 + i*340, 565, 200, 254) for i in range(3)]
        if question_number == 3:
            return [(156 + i*276, 410, 256, 310) for i in range(5)]
        if question_number == 6:
            return [(166 + i*454, 355, 256, 310) for i in range(3)]
        return [(96 + i*376, 383, 256, 310) for i in range(4)]


screen cb_console_card(question_number, index, choice, card_width, card_height):
    frame:
        background Solid("#162B50")
        xsize card_width
        ysize card_height
        padding (8, 8)
        fixed:
            xfill True
            yfill True
            add cb_console_card_frame():
                xsize card_width - 16
                ysize card_height - 16
                nearest True
            add Solid("#0C1730"):
                xpos 8
                ypos 8
                xsize card_width - 16
                ysize card_height - 16
        if question_number == 6:
            $ enemy = CB_ENEMY_CARD_DATA.get(choice, {})
            add cb_console_art(question_number, index, (card_width-32, 152)):
                xpos 16
                ypos 16
                xsize card_width-32
                ysize 152
                fit "contain"
                nearest True
            vbox:
                pos (24, 182)
                xsize card_width-48
                spacing 8
                text enemy.get("name", choice):
                    font CB_CONSOLE_FONT
                    size 16
                    color "#EDF7FF"
                    xalign 0.5
                text enemy.get("subtitle", ""):
                    size 19
                    bold True
                    color enemy.get("accent", "#8EACFF")
                    xalign 0.5
                text enemy.get("intro", ""):
                    size 17
                    color "#D7E4FA"
                    text_align 0.5
                    xalign 0.5
                text enemy.get("skill_name", ""):
                    font CB_CONSOLE_FONT
                    size 14
                    color "#8ECFFF"
                    xalign 0.5
                text enemy.get("skill_description", ""):
                    size 17
                    color "#D7E4FA"
                    text_align 0.5
                    xalign 0.5
        else:
            add cb_console_art(question_number, index, (card_width-32, card_height-74)):
                xpos 16
                ypos 16
                xsize card_width-32
                ysize card_height-74
                fit "contain"
                nearest True
            text choice:
                font CB_CONSOLE_FONT
                size (12 if question_number == 3 else 14 if question_number in (1, 4) else 16)
                color "#EDF7FF"
                xcenter card_width//2
                ycenter card_height-34
                xsize card_width-30
                text_align 0.5
                layout "subtitle"


screen crowd_creators_round(question_number, question_total, expected_round_id=None, question_duration=15):
    modal True
    $ current_round = cb_battle.get("current_round") or {}
    $ guarded_round_id = expected_round_id or cb_round_guard_id
    # Preserve polling and finish guards. Voting still happens on participants' devices.
    timer 0.25 repeat True action Function(cb_poll_round_action)
    if cb_round_can_finish(guarded_round_id):
        timer 0.10 action Return(True)
    use cb_creators_console_content(question_number, question_total, current_round, cb_remaining_seconds, question_duration)


screen cb_creators_console_content(question_number, question_total, current_round, remaining, duration):
    fixed:
        xysize (1672, 941)
        at Transform(zoom=config.screen_width / 1672.0)
        add CB_CONSOLE_ROOT + "background.png":
            xysize (1672, 941)
            nearest True
        text "CREATORS' QUESTION · [question_number]/[question_total]":
            font CB_CONSOLE_FONT
            size 20
            color "#8CB7F9"
            xcenter 836
            ypos 167
        text "[remaining] секунд":
            size 32
            bold True
            color "#FF899D"
            xcenter 836
            ypos 207
        # The decorative timer assembly from the reference, covered by live segments.
        add Crop((565, 247, 544, 44), CB_CONSOLE_ROOT + "reference.png"):
            pos (565, 247)
        add Solid("#101C37"):
            pos (578, 258)
            xysize (513, 18)
        hbox:
            pos (578, 259)
            spacing 5
            for segment in range(10):
                add Solid("#FF899D" if segment < int(10 * max(0, min(remaining, duration)) / max(1, duration)) else "#263F65"):
                    xysize (46, 17)
        text current_round.get("question", ""):
            size (30 if question_number == 5 else 36)
            bold True
            color "#F6FAFF"
            xcenter 836
            ypos 306
            xsize 1420
            text_align 0.5
            layout "subtitle"
        $ card_layout = cb_console_layout(question_number)
        for index, choice in enumerate(current_round.get("choices", [])):
            if index < len(card_layout):
                $ cx, cy, cw, ch = card_layout[index]
                fixed:
                    pos (cx, cy)
                    xysize (cw, ch)
                    use cb_console_card(question_number, index, choice, cw, ch)
