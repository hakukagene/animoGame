image nova = "images/cinematic/nova.png"
transform nova_anim:
    xalign 0.5
    yalign 0.5
    zoom 0.7
    
label intro:
    scene expression Solid("#000000")
    with fade
    show nova at nova_anim
    
    python:
        for i in range(len(TextArray)):
            cb_voice_line(
                N,
                TextArray[i],
                "audio/hutlugch{}.ogg".format(i + 1)
            )

    # Creator survey дуусмагц завсрын cinematic руу нэг удаа шилжинэ.
    call crowd_creators_questions
    jump crowd_world_cinematic
