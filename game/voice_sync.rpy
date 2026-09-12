# Voice-synchronised dialogue for Ren'Py 8.5+.
#
# Usage:
#     $ cb_voice_line(None, "Narration text.", "001")
#     $ cb_voice_line(nova, "Character dialogue.", "nova_001")
#     $ completed = cb_play_ogg_and_wait("sound_001")
#
# Voice ids are resolved to game/audio/voice/<id>.ogg.
# A full relative path such as "audio/voice/scene_01.ogg" is also accepted.

define config.afm_voice_delay = 1.5
define config.afm_bonus = 0
define config.afm_characters = 10000

default cb_current_speaker = None


transform cb_speaker_nova:
    anchor (0.5, 1.0)
    xpos 960
    ypos 950
    zoom 0.6
    alpha 0.0
    xoffset -45
    easeout 0.30 alpha 1.0 xoffset 0


transform cb_speaker_monster:
    anchor (0.5, 1.0)
    xpos 390
    ypos 850
    zoom 1.18
    alpha 0.0
    xoffset -45
    easeout 0.30 alpha 1.0 xoffset 0


init -90 python:

    _CB_VOICE_POST_DELAY = 1.5
    if not renpy.music.channel_defined("voice_wait"):
        renpy.music.register_channel(
            "voice_wait",
            mixer="voice",
            loop=False,
            stop_on_mute=False,
        )

    _cb_voice_lock_dismiss = False
    _cb_previous_say_allow_dismiss = config.say_allow_dismiss


    def cb_voice_path(voice_id):
        if voice_id is None:
            return None

        value = str(voice_id).strip().replace("\\", "/")
        if not value:
            return None

        if "/" in value:
            if value.lower().endswith(".ogg"):
                return value
            return value + ".ogg"

        if value.lower().endswith(".ogg"):
            return "audio/voice/" + value

        return "audio/voice/" + value + ".ogg"


    def cb_voice_allow_dismiss():
        # A click must not cut off a synced voice line.
        if _cb_voice_lock_dismiss:
            return False

        if _cb_previous_say_allow_dismiss is not None:
            return _cb_previous_say_allow_dismiss()

        return True


    def cb_dialogue_enemy_displayable(st, at):
        """Returns the monster selected by the creators' final vote."""

        image_path = getattr(
            store,
            "cb_enemy_idle_image",
            "images/cinematic/boss_void.webp",
        ) or "images/cinematic/boss_void.webp"
        return renpy.easy_displayable(image_path), 0.25


    def cb_voice_line(who, what, voice_id):
        """
        Voice дууссаны дараа 1.5 секундийн турш dialogue-г дэлгэцэнд хадгална.
        """

        global _cb_voice_lock_dismiss

        voice_file = cb_voice_path(voice_id)

        if not voice_file or not renpy.loadable(voice_file):
            if voice_file:
                renpy.notify(
                    "Voice файл олдсонгүй: {}".format(voice_file)
                )

            renpy.say(who, what)

            # Voice файл байхгүй үед ч текстийг delay дуусах хүртэл харуулна.
            renpy.say(who, what, interact=False)
            renpy.pause(
                _CB_VOICE_POST_DELAY,
                hard=True,
                modal=False
            )
            return False

        old_afm_enable = preferences.afm_enable
        old_afm_after_click = preferences.afm_after_click
        old_afm_time = preferences.afm_time
        old_wait_voice = preferences.wait_voice
        old_text_cps = preferences.text_cps

        try:
            preferences.afm_enable = True
            preferences.afm_after_click = True
            preferences.afm_time = 1
            preferences.wait_voice = True
            preferences.text_cps = 0

            _cb_voice_lock_dismiss = True

            voice(voice_file)
            renpy.say(who, what)

        finally:
            _cb_voice_lock_dismiss = False

            preferences.afm_enable = old_afm_enable
            preferences.afm_after_click = old_afm_after_click
            preferences.afm_time = old_afm_time
            preferences.wait_voice = old_wait_voice
            preferences.text_cps = old_text_cps

        return True



    def cb_play_ogg_and_wait(voice_id, poll_interval=0.05):
        """
        Plays an OGG file and returns True only after playback finishes.

        The dedicated voice_wait channel uses the Voice Volume setting.
        A muted channel still advances according to the real audio duration.

        Returns False when the requested file does not exist.
        """
        
        voice_file = cb_voice_path(voice_id)
        
        if not voice_file or not renpy.loadable(voice_file):
            if voice_file:
                renpy.notify("OGG файл олдсонгүй: {}".format(voice_file))
            return False

        try:
            interval = float(poll_interval)
        except Exception:
            interval = 0.05

        interval = max(0.01, min(interval, 0.25))

        renpy.music.play(
            voice_file,
            channel="voice_wait",
            loop=False,
            fadeout=0.0,
        )

        # Begin an interaction so queued audio starts, then wait until the
        # channel no longer has a playing filename. The battle HUD is modal,
        # so modal=False is required for each timed pause to finish beneath it.
        while renpy.music.get_playing(channel="voice_wait") is not None:
            renpy.pause(interval, hard=True, modal=False)

        # Voice дууссаны дараа battle question дэлгэцийг
        # нэмэлт 1.5 секунд хадгална.
        renpy.pause(
            _CB_VOICE_POST_DELAY,
            hard=True,
            modal=False
        )

        return True


    config.say_allow_dismiss = cb_voice_allow_dismiss


image crowd_enemy dialogue = DynamicDisplayable(cb_dialogue_enemy_displayable)
