label intro:

    scene black
    with fade

    python:
        for i in range(len(TextArray)):

            cb_voice_line(
                presenter,
                TextArray[i],
                "audio/hutlugch{}.ogg".format(i + 1)
            )
        
    call crowd_creators_questions
    jump crowd_monster_battle
