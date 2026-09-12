# Creators survey console. All geometry is authored at the artwork's native
# 1672x941 resolution, then the complete screen is scaled to the game window.
init -10 python:
    CB_CONSOLE_ROOT = "images/creators_console/"
    CB_CONSOLE_FONT = "fonts/PressStart2P-Regular.ttf"

    # filename, source width, source height, columns, rows
    CB_CONSOLE_SHEETS = {
        1: ("roles.png", 1672, 941, 4, 2),
        3: ("locations.png", 1536, 1024, 3, 2),
        4: ("citizens.png", 1672, 941, 4, 2),
        5: ("traits.png", 2172, 724, 4, 1),
        6: ("enemies.png", 2172, 724, 3, 1),
    }

    CB_CONSOLE_WORLD_ART = (
        "images/world_types/futuristic.webp",
        "images/world_types/fantasy.webp",
        "images/world_types/modern.webp",
        "images/world_types/post_apocalyptic.webp",
    )

    CB_CONSOLE_CARD_ACCENTS = (
        "#25D8FF", "#25D8FF", "#FF55C8", "#9C66FF",
        "#FFB34F", "#FF55C8", "#25D8FF",
    )


    def cb_console_art(question_number, index, target_size=None):
        """Return one undistorted, center-cropped answer illustration."""
        if question_number == 2:
            safe_index = max(0, min(int(index), len(CB_CONSOLE_WORLD_ART) - 1))
            source = CB_CONSOLE_WORLD_ART[safe_index]
            x0, y0, width, height = 0, 0, 1280, 720
        else:
            filename, sheet_width, sheet_height, columns, rows = CB_CONSOLE_SHEETS[question_number]
            safe_index = max(0, min(int(index), columns * rows - 1))
            column = safe_index % columns
            row = safe_index // columns
            x0 = sheet_width * column // columns
            x1 = sheet_width * (column + 1) // columns
            y0 = sheet_height * row // rows
            y1 = sheet_height * (row + 1) // rows
            width, height = x1 - x0, y1 - y0
            source = CB_CONSOLE_ROOT + filename

        if target_size is None:
            target_size = (width, height)

        target_width, target_height = target_size
        target_ratio = float(target_width) / max(1, target_height)
        source_ratio = float(width) / max(1, height)

        if source_ratio > target_ratio:
            crop_width = max(1, int(height * target_ratio))
            x0 += (width - crop_width) // 2
            width = crop_width
        elif source_ratio < target_ratio:
            crop_height = max(1, int(width / target_ratio))
            y0 += (height - crop_height) // 2
            height = crop_height

        return Crop((x0, y0, width, height), source)


    def cb_console_card_frame(index):
        # Reuse the supplied cyan/purple pixel frames. Frame() preserves their
        # corners while adapting them to portrait cards without scaling text.
        frame_y = 160 if index % 4 in (0, 1) else 350
        return Frame(
            Crop(
                (44, frame_y, 1584, 160),
                CB_CONSOLE_ROOT + "answer bar detail.png",
            ),
            72,
            52,
        )


    def cb_console_layout(question_number):
        """Card positions matching the selected 4+3 reference composition."""
        if question_number in (1, 4):
            top = [(235 + index * 302, 380, 240, 200) for index in range(4)]
            bottom = [(386 + index * 303, 570, 240, 200) for index in range(3)]
            return top + bottom

        if question_number == 3:
            top = [(240 + index * 480, 400, 240, 210) for index in range(3)]
            bottom = [(480 + index * 480, 535, 240, 210) for index in range(2)]
            return top + bottom

        if question_number == 6:
            return [(386 + index * 306, 400, 288, 350) for index in range(3)]

        # Questions 2 and 5 each have four choices.
        return [(235 + index * 302, 380, 288, 350) for index in range(4)]


    def cb_console_question_size(question_number):
        return {
            1: 40,
            2: 25,
            3: 31,
            4: 27,
            5: 24,
            6: 31,
        }.get(question_number, 30)


    def cb_console_choice_size(question_number):
        return {
            1: 16,
            2: 14,
            3: 13,
            4: 12,
            5: 13,
            6: 11,
        }.get(question_number, 13)


    def cb_console_text_line_width(text, font_size, maximum, minimum=72):
        """Approximate Press Start 2P text width for a fitted underline."""
        estimated = len(str(text or "")) * (int(font_size) + 1)
        return max(int(minimum), min(int(maximum), estimated))


screen cb_console_card(question_number, index, choice, card_width, card_height):
    $ accent = CB_CONSOLE_CARD_ACCENTS[index % len(CB_CONSOLE_CARD_ACCENTS)]
    $ label_height = 58
    $ image_width = card_width - 30
    $ image_height = card_height - label_height - 24
    $ choice_font_size = cb_console_choice_size(question_number)
    $ choice_line_width = cb_console_text_line_width(
        choice,
        choice_font_size,
        card_width - 50,
        80,
    )

    fixed:
        xysize (card_width, card_height)

        add cb_console_card_frame(index):
            xysize (card_width, card_height)
            nearest True

        add cb_console_art(question_number, index, (image_width, image_height)):
            xpos 15
            ypos 13
            xysize (image_width, image_height)
            nearest True

        # An opaque label panel guarantees readable answers on bright artwork.
        add Solid("#06142BF2"):
            xpos 15
            ypos card_height - label_height - 11
            xysize (card_width - 30, label_height)

        add Solid(accent):
            xpos (card_width - choice_line_width) // 2
            ypos card_height - 18
            xysize (choice_line_width, 3)

        text choice:
            font CB_CONSOLE_FONT
            size choice_font_size
            color "#FFFFFF"
            # Ren'Py treats float positions as proportions. Integer division
            # keeps these centers in card-local pixels instead of placing the
            # answer text far outside the small label box.
            xcenter card_width // 2
            ycenter card_height - (label_height // 2) - 8
            xsize card_width - 48
            text_align 0.5
            layout "subtitle"
            line_spacing 2
            slow_cps 0
            outlines [(2, "#000814", 0, 1)]


screen crowd_creators_round(question_number, question_total, expected_round_id=None, question_duration=15):
    modal True

    $ current_round = cb_battle.get("current_round") or {}
    $ guarded_round_id = expected_round_id or cb_round_guard_id

    timer 0.25 repeat True action Function(cb_poll_round_action)

    if cb_round_can_finish(guarded_round_id):
        timer 0.10 action Return(
            current_round.get("result")
            or cb_round_result
            or {}
            )

    use cb_creators_console_content(
        question_number,
        question_total,
        current_round,
        cb_remaining_seconds,
        question_duration,
    )


screen cb_creators_console_content(question_number, question_total, current_round, remaining, duration):
    fixed:
        xysize (1672, 941)
        at Transform(zoom=config.screen_width / 1672.0)

        add CB_CONSOLE_ROOT + "background.png":
            xysize (1672, 941)
            nearest True

        text "CREATORS' QUESTION · [question_number]/[question_total]":
            font CB_CONSOLE_FONT
            size 22
            color "#8ECFFF"
            xcenter 836
            ypos 200
            text_align 0.5

        text "[remaining] секунд":
            font CB_CONSOLE_FONT
            size 26
            color "#FF7FA4"
            xcenter 836
            ypos 240
            text_align 0.5

        # Supplied timer frame and ten live segments are separate layers.
        add Crop(
            (180, 535, 1490, 170),
            CB_CONSOLE_ROOT + "answer bar detail.png",
        ):
            xpos 610
            ypos 153
            xysize (452, 40)
            nearest True

        add Solid("#101C37"):
            xpos 625
            ypos 168
            xysize (422, 11)

        hbox:
            xpos 625
            ypos 280
            spacing 3

            for segment in range(10):
                add Solid(
                    "#FF668F"
                    if segment < int(
                        10 * max(0, min(remaining, duration)) / max(1, duration)
                    )
                    else "#263F65"
                ):
                    xysize (39, 11)

        text current_round.get("question", ""):
            font CB_CONSOLE_FONT
            size cb_console_question_size(question_number)
            color "#F7FAFF"
            xcenter 836
            ypos 320
            xsize 1420
            ysize 60

            text_align 0.5
            layout "subtitle"
            outlines [(2, "#071126", 0, 2)]

        $ card_layout = cb_console_layout(question_number)

        for index, choice in enumerate(current_round.get("choices", [])):
            if index < len(card_layout):
                $ card_x, card_y, card_width, card_height = card_layout[index]

                fixed:
                    pos (card_x, card_y)
                    xysize (card_width, card_height)
                    use cb_console_card(
                        question_number,
                        index,
                        choice,
                        card_width,
                        card_height,
                    )


init -10 python:
    def cb_console_result_row_accent(index):
        return "#25D8FF" if index % 2 == 0 else "#A657FF"


    def cb_console_result_row_frame(index):
        """Alternating cyan and purple answer rows from the supplied sheet."""
        frame_y = 160 if index % 2 == 0 else 350
        return Frame(
            Crop(
                (44, frame_y, 1584, 160),
                CB_CONSOLE_ROOT + "answer bar detail.png",
            ),
            72,
            22,
        )


    def cb_console_result_progress_frame():
        return Frame(
            Crop(
                (180, 535, 1490, 170),
                CB_CONSOLE_ROOT + "answer bar detail.png",
            ),
            70,
            16,
        )


    def cb_console_result_decoration(side):
        if side == "left":
            return Crop(
                (88, 710, 478, 165),
                CB_CONSOLE_ROOT + "answer bar detail.png",
            )
        return Crop(
            (558, 710, 505, 165),
            CB_CONSOLE_ROOT + "answer bar detail.png",
        )


    def cb_console_result_layout(choice_count):
        """Center 3-7 text-only result rows inside the console safe area."""
        if choice_count >= 6:
            return (292, 42, 7, 13, 668, 706)
        if choice_count == 5:
            return (300, 50, 10, 15, 664, 704)
        if choice_count == 4:
            return (315, 58, 12, 17, 654, 698)
        return (330, 66, 14, 18, 642, 692)


    def cb_console_result_question_size(question_text):
        text_length = len(question_text or "")
        if text_length > 55:
            return 20
        if text_length > 38:
            return 23
        return 27


screen crowd_creators_result(question, result):
    modal True
    default auto_seconds = 15

    $ latest_round = cb_battle.get("current_round") or {}
    $ latest_result = result or latest_round.get("result") or {}
    $ choices = list(question.get("choices", []))
    $ counts = list(latest_result.get("choice_counts", latest_round.get("choice_counts", [])))
    $ total_answers = max(0, int(latest_result.get("total_answers", latest_round.get("total_answers", 0))))
    $ row_y, row_height, row_gap, row_font_size, total_y, countdown_y = cb_console_result_layout(len(choices))

    timer 1.0 repeat True action If(
        auto_seconds > 1,
        SetScreenVariable("auto_seconds", auto_seconds - 1),
        Return(True),
    )

    fixed:
        xysize (1672, 941)
        at Transform(zoom=config.screen_width / 1672.0)

        add CB_CONSOLE_ROOT + "background.png":
            xysize (1672, 941)
            nearest True

        text "САНАЛ АСУУЛГЫН ҮР ДҮН":
            font CB_CONSOLE_FONT
            size 36
            color "#F7FAFF"
            xcenter 836
            ypos 178
            text_align 0.5
            outlines [(2, "#071126", 0, 2)]

        text question.get("question", ""):
            font CB_CONSOLE_FONT
            size cb_console_result_question_size(question.get("question", ""))
            color "#F7FAFF"
            xcenter 836
            ypos 238
            xmaximum 1300
            text_align 0.5
            layout "subtitle"
            outlines [(2, "#071126", 0, 2)]

        for index, choice in enumerate(choices):
            $ count = max(0, int(counts[index])) if index < len(counts) else 0
            $ percentage = int(round(100.0 * count / total_answers)) if total_answers else 0
            $ current_row_y = row_y + index * (row_height + row_gap)
            $ row_accent = cb_console_result_row_accent(index)
            $ stats_text = "{} · {}%".format(count, percentage)

            hbox:
                xcenter 836
                ypos current_row_y
                ysize row_height
                spacing 34

                text choice:
                    font CB_CONSOLE_FONT
                    size row_font_size
                    color "#F7FAFF"
                    yalign 0.5
                    xmaximum 920
                    text_align 0.5
                    layout "subtitle"
                    line_spacing 2
                    slow_cps 0
                    outlines [(2, "#061020", 0, 1)]

                text stats_text:
                    font CB_CONSOLE_FONT
                    size row_font_size
                    color row_accent
                    yalign 0.5
                    text_align 0.5
                    slow_cps 0
                    outlines [(2, "#061020", 0, 1)]

        text "Нийт оролцогч: [total_answers] · Нийт санал: [total_answers]":
            font CB_CONSOLE_FONT
            size 14
            color "#AAB8D5"
            xcenter 836
            ypos total_y
            text_align 0.5

        text "[auto_seconds] секундын дараа автоматаар үргэлжилнэ.":
            font CB_CONSOLE_FONT
            size 14
            color "#91A8FF"
            xcenter 836
            ypos countdown_y
            text_align 0.5
