# Voice files

Place every spoken line in this directory as an OGG file.

Recommended naming:

- `001.ogg`
- `002.ogg`
- `nova_001.ogg`
- `monster_001.ogg`

Use the helper from `game/voice_sync.rpy`:

```renpy
define nova = Character("Nova", color="#7EDB78")
define monster = Character("Мангас", color="#FF4B4B")

label story_example:
    $ cb_voice_line(None, "Энд одоогоор юу ч байхгүй.", "001")
    $ cb_voice_line(nova, "Чи хэн бэ?", "nova_001")
    $ cb_voice_line(monster, "Энэ ертөнц та нарынх биш.", "monster_001")
    return
```

The helper automatically waits for the real OGG duration. Do not write the
duration in seconds. While a synced voice is playing, clicking cannot cut it
off. If a referenced file is missing, the game shows a notification and falls
back to normal click-to-continue dialogue.

## Play one OGG and wait for its return

```renpy
label test_ogg_wait:
    $ completed = cb_play_ogg_and_wait("001")

    if completed:
        "001.ogg тоглож дууслаа."
    else:
        "001.ogg файл олдсонгүй."

    return
```

`cb_play_ogg_and_wait()` returns `True` only after the OGG finishes. It
returns `False` when the file is missing. The function uses a dedicated
`voice_wait` channel and blocks dismiss/skip clicks while waiting.
