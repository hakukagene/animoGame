# ANIMO-ийн үе шат бүрийн background music.
# Бүх BGM music mixer ашиглах тул Voice Volume-оос тусдаа удирдагдана.
init -50 python:
    CB_STORY_BGM_PATH = "audio/ay/nuutslag ay.ogg"
    CB_CREATOR_WAIT_BGM_PATH = "audio/ay/nuutslag, hariult huleeh ay.ogg"
    CB_BATTLE_BGM_PATH = "audio/ay/zodoontoi ay.ogg"

    for _cb_bgm_channel in (
        "cb_story_bgm",
        "cb_creator_wait_bgm",
        "cb_battle_bgm",
    ):
        if not renpy.music.channel_defined(_cb_bgm_channel):
            renpy.music.register_channel(
                _cb_bgm_channel,
                mixer="music",
                loop=True,
                stop_on_mute=True,
            )

    

    def _cb_play_looped_bgm(path, channel, fadein=0.5, volume=0.5):
        if not renpy.loadable(path):
            renpy.notify("BGM файл олдсонгүй: {}".format(path))
            return False

        renpy.music.set_volume(volume, delay=0.0, channel=channel)

        if renpy.music.get_playing(channel=channel) != path:
            renpy.music.play(
                path,
                channel=channel,
                loop=True,
                fadein=fadein,
                fadeout=0.35,
            )
        return True


    def cb_start_story_bgm():
        # Direct test label-ээс орсон байсан ч хуучин үеийн ая давхардахгүй.
        renpy.music.stop(channel="cb_battle_bgm", fadeout=0.25)
        renpy.music.stop(channel="cb_creator_wait_bgm", fadeout=0.20)
        renpy.music.set_pause(False, channel="cb_story_bgm")
        return _cb_play_looped_bgm(
            CB_STORY_BGM_PATH,
            "cb_story_bgm",
            fadein=0.7,
        )


    def cb_start_creator_wait_bgm():
        # Хүлээлгийн файл байхгүй үед үндсэн аяыг дэмий pause хийхгүй.
        if not renpy.loadable(CB_CREATOR_WAIT_BGM_PATH):
            renpy.notify(
                "BGM файл олдсонгүй: {}".format(CB_CREATOR_WAIT_BGM_PATH)
            )
            return False

        renpy.music.set_pause(True, channel="cb_story_bgm")
        return _cb_play_looped_bgm(
            CB_CREATOR_WAIT_BGM_PATH,
            "cb_creator_wait_bgm",
            fadein=0.25,
        )


    def cb_finish_creator_wait_bgm():
        renpy.music.stop(channel="cb_creator_wait_bgm", fadeout=0.25)
        # Mystery BGM-г эхнээс нь restart хийхгүй, pause хийсэн цэгээс үргэлжлүүлнэ.
        renpy.music.set_pause(False, channel="cb_story_bgm")


    def cb_stop_story_bgm():
        renpy.music.stop(channel="cb_creator_wait_bgm", fadeout=0.20)
        renpy.music.set_pause(False, channel="cb_story_bgm")
        renpy.music.stop(channel="cb_story_bgm", fadeout=0.7)


    def cb_start_battle_bgm():
        cb_stop_story_bgm()
        return _cb_play_looped_bgm(
            CB_BATTLE_BGM_PATH,
            "cb_battle_bgm",
            fadein=0.7,
        )


    def cb_stop_battle_bgm():
        renpy.music.stop(channel="cb_battle_bgm", fadeout=0.8)


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
    $ cb_start_story_bgm()
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
