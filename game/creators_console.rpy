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
        (110, 400, 324, 258),
        (485, 400, 324, 258),
        (861, 400, 324, 258),
        (1238, 400, 324, 258),
    ]

    def cb_console_art(question_number, index):
        if question_number == 2:
            x, y, w, h = CB_CONSOLE_WORLDS[index]
            return Crop(
                (x, y, w, h),
                CB_CONSOLE_ROOT + "reference.png"
            )

        filename, width, height, cols, rows = CB_CONSOLE_SHEETS[question_number]

        col = index % cols
        row = index // cols

        x0 = width * col // cols
        y0 = height * row // rows
        x1 = width * (col + 1) // cols
        y1 = height * (row + 1) // rows

        return Crop(
            (x0, y0, x1 - x0, y1 - y0),
            CB_CONSOLE_ROOT + filename
        )

    def cb_console_layout(question_number):
        if question_number in (1, 4):
            return [
                (166 + i * 340, 365, 320, 182)
                for i in range(4)
            ] + [
                (336 + i * 340, 565, 320, 182)
                for i in range(3)
            ]

        if question_number == 3:
            return [
                (156 + i * 276, 410, 256, 310)
                for i in range(5)
            ]

        if question_number == 6:
            return [
                (166 + i * 454, 355, 432, 397)
                for i in range(3)
            ]

        return [
            (96 + i * 376, 383, 352, 337)
            for i in range(4)
        ]