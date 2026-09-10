image nova = "images/cinematic/nova.png"
transform nova_intro_reveal:
    anchor (0.5, 0.5)
    xalign 0.5
    yalign 0.52
    zoom 0.64
    yoffset 36
    alpha 0.0
    matrixcolor TintMatrix("#141827") * BrightnessMatrix(-0.70)
    pause 0.35
    parallel:
        easein 2.8 alpha 1.0
    parallel:
        easeout 3.2 yoffset 0 zoom 0.70
    parallel:
        easein 3.0 matrixcolor TintMatrix("#FFFFFF") * BrightnessMatrix(0.0)
    
label intro:
    scene expression Solid("#000000")
    with fade
    show nova at nova_intro_reveal
    $ cb_current_speaker = "nova"
    $ renpy.pause(3.6, hard=True)
    
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
