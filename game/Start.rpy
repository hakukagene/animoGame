label intro:
    scene expression Solid("#000000")
    with fade

    python:
        for i in range(len(TextArray)):
            cb_voice_line(
                N,
                TextArray[i],
                "audio/hutlugch{}.ogg".format(i + 1)
            )

    call crowd_creators_questions
    jump crowd_world_cinematic
