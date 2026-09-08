# Voice-synchronised dialogue for Ren'Py 8.5+.
#
# Usage:
#     $ cb_voice_line(None, "Narration text.", "001")
#     $ cb_voice_line(nova, "Character dialogue.", "nova_001")
#     $ completed = cb_play_ogg_and_wait("sound_001")
#
# Voice ids are resolved to game/audio/voice/<id>.ogg.
# A full relative path such as "audio/voice/scene_01.ogg" is also accepted.

define config.afm_voice_delay = 0.05
define config.afm_bonus = 0
define config.afm_characters = 10000


transform cb_speaker_nova:
    xalign 0.5
    yalign 0.5
    zoom 0.68
    alpha 0.0
    linear 0.20 alpha 1.0


transform cb_speaker_monster:
    xalign 0.82
    yalign 0.5
    zoom 0.88
    alpha 0.0
    linear 0.20 alpha 1.0


init -90 python:
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


    def cb_show_speaker_portrait(who):
        """Keeps the visible portrait in sync with the speaking character."""

        nova_character = getattr(store, "N", None)
        monster_character = getattr(store, "Monster", None)

        if nova_character is not None and who is nova_character:
            renpy.hide("crowd_enemy")
            renpy.show("nova", at_list=[store.cb_speaker_nova])
        elif monster_character is not None and who is monster_character:
            renpy.hide("nova")
            renpy.show(
                "crowd_enemy dialogue",
                at_list=[store.cb_speaker_monster],
            )
        else:
            # Narration/System/Creators lines do not leave an old speaker up.
            renpy.hide("nova")
            renpy.hide("crowd_enemy")


    def cb_nova_portrait_callback(event, interact=True, **kwargs):
        # Direct `N "..."` lines also receive the same portrait behavior.
        if event == "begin" and not renpy.showing("nova"):
            cb_show_speaker_portrait(getattr(store, "N", None))


    def cb_monster_portrait_callback(event, interact=True, **kwargs):
        # Direct `Monster "..."` lines use the creators' selected monster.
        if event == "begin" and not renpy.showing("crowd_enemy dialogue"):
            cb_show_speaker_portrait(getattr(store, "Monster", None))


    def cb_voice_line(who, what, voice_id):
        """
        Shows one dialogue line and advances immediately after its OGG finishes.

        who:
            Character object, or None for narration.
        what:
            Text shown in the say screen.
        voice_id:
            "001", "nova_001.ogg", or a full game-relative audio path.                                                                                                          

        If the audio file is missing, the line falls back to normal
        click-to-continue dialogue instead of crashing the game.
        """

        global _cb_voice_lock_dismiss

        cb_show_speaker_portrait(who)
        voice_file = cb_voice_path(voice_id)

        if not voice_file or not renpy.loadable(voice_file):
            if voice_file:
                renpy.notify("Voice файл олдсонгүй: {}".format(voice_file))
            renpy.say(who, what)
            return False

        old_afm_enable = preferences.afm_enable
        old_afm_after_click = preferences.afm_after_click
        old_afm_time = preferences.afm_time
        old_wait_voice = preferences.wait_voice
        old_text_cps = preferences.text_cps

        try:
            # The text delay is almost zero. Ren'Py's voice callback keeps AFM
            # blocked until the voice channel finishes.
            preferences.afm_enable = True
            preferences.afm_after_click = True
            preferences.afm_time = 1
            preferences.wait_voice = True
            preferences.text_cps = 0

            _cb_voice_lock_dismiss = True
            voice(voice_file)
            renpy.say(who, what)
            return True
        finally:
            _cb_voice_lock_dismiss = False
            preferences.afm_enable = old_afm_enable
            preferences.afm_after_click = old_afm_after_click
            preferences.afm_time = old_afm_time
            preferences.wait_voice = old_wait_voice
            preferences.text_cps = old_text_cps



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
        # channel no longer has a playing filename.
        renpy.pause(interval, hard=True)

        while renpy.music.get_playing(channel="voice_wait") is not None:
            renpy.pause(interval, hard=True)

        return True


    config.say_allow_dismiss = cb_voice_allow_dismiss


image crowd_enemy dialogue = DynamicDisplayable(cb_dialogue_enemy_displayable)
