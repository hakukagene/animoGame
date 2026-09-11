# Sci-fi landing screen shown before Ren'Py enters label start.
define CB_START_CONSOLE_ROOT = "images/creators_console/"
define CB_START_CONSOLE_FONT = "fonts/PressStart2P-Regular.ttf"


init -10 python:
    def cb_start_console_frame(hover=False):
        frame_y = 350 if hover else 160
        return Frame(
            Crop(
                (44, frame_y, 1584, 160),
                CB_START_CONSOLE_ROOT + "answer bar detail.png",
            ),
            72,
            30,
        )


    def cb_start_console_decoration(side):
        if side == "left":
            return Crop(
                (88, 710, 478, 165),
                CB_START_CONSOLE_ROOT + "answer bar detail.png",
            )
        return Crop(
            (558, 710, 505, 165),
            CB_START_CONSOLE_ROOT + "answer bar detail.png",
        )


screen animo_start_landing():
    key "K_RETURN" action Start()
    key "K_KP_ENTER" action Start()

    fixed:
        xysize (1672, 941)
        at Transform(zoom=config.screen_width / 1672.0)

        add CB_START_CONSOLE_ROOT + "background.png":
            xysize (1672, 941)
            nearest True

        text "ANIMO CROWD BATTLE":
            font CB_START_CONSOLE_FONT
            size 38
            color "#F7FAFF"
            xcenter 836
            ypos 172
            text_align 0.5
            outlines [(2, "#071126", 0, 2)]

        text "ТОГЛООМД НЭГДЭХ":
            font CB_START_CONSOLE_FONT
            size 21
            color "#8ECFFF"
            xcenter 836
            ypos 224
            text_align 0.5

        add cb_start_console_decoration("left"):
            xpos 220
            ypos 205
            xysize (310, 70)
            nearest True

        add cb_start_console_decoration("right"):
            xpos 1142
            ypos 205
            xysize (310, 70)
            nearest True

        # QR panel.
        add cb_start_console_frame(False):
            xpos 326
            ypos 286
            xysize (372, 372)
            nearest True

        add Solid("#FFFFFF"):
            xpos 364
            ypos 324
            xysize (296, 296)

        add CB_START_CONSOLE_ROOT + "join_qr.png":
            xpos 364
            ypos 324
            xysize (296, 296)
            nearest True

        text "SCAN TO JOIN":
            font CB_START_CONSOLE_FONT
            size 14
            color "#25D8FF"
            xcenter 512
            ypos 674
            text_align 0.5

        # Join instructions and live server address.
        text "УТАСААРАА QR КОДЫГ\nУНШУУЛНА УУ":
            font CB_START_CONSOLE_FONT
            size 20
            color "#F7FAFF"
            xcenter 1112
            ypos 326
            line_spacing 10
            text_align 0.5

        text "[cb_server_url()]":
            font CB_START_CONSOLE_FONT
            size 12
            color "#91A8FF"
            xcenter 1112
            ypos 423
            xmaximum 520
            text_align 0.5

        text "БҮГД ХОЛБОГДСОН БОЛ":
            font CB_START_CONSOLE_FONT
            size 14
            color "#AAB8D5"
            xcenter 1112
            ypos 500
            text_align 0.5

        button:
            xpos 882
            ypos 542
            xysize (460, 92)
            background cb_start_console_frame(False)
            hover_background cb_start_console_frame(True)
            action Start()

            text "START":
                font CB_START_CONSOLE_FONT
                size 28
                color "#FFFFFF"
                hover_color "#FFFFFF"
                xalign 0.5
                yalign 0.5
                outlines [(2, "#071126", 0, 2)]

        text "ENTER дарж мөн эхлүүлж болно":
            font CB_START_CONSOLE_FONT
            size 11
            color "#6F91C8"
            xcenter 1112
            ypos 656
            text_align 0.5

        textbutton "ГАРАХ":
            xpos 1042
            ypos 715
            xsize 140
            text_font CB_START_CONSOLE_FONT
            text_size 12
            text_color "#7E91BB"
            text_hover_color "#FF7FA4"
            text_align 0.5
            action Quit(confirm=True)
