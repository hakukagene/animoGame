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
label intro2:
    scene expression Solid("#000000")   
    with fade

    python:
        for i in range(len(TextArray2)):

            cb_voice_line(
                N,
                TextArray2[i],
                "audio/hutlugch{}.ogg".format(i + 18)
            )
        
    call crowd_creators_questions
