# Creator survey -> monster battle cinematic.

default cb_creator_results = []
default cb_creator_summary_rows = []
default cb_creator_count = 0

default cb_world_name = "FUTURISTIC"
default cb_world_image = "cb_cinematic_world_futuristic"
default cb_team_city_image = "cb_team_city_futuristic"

default cb_enemy_key = "void"
default cb_enemy_name = "The Void"
default cb_enemy_title = "THE VOID — ХООСРОЛ"
default cb_enemy_idle_image = "images/cinematic/boss_void.webp"
default cb_enemy_attack_image = "images/cinematic/boss_void_attack.webp"
default cb_enemy_reveal_movie = "video/cinematic/reveal/reveal_void.webm"
default cb_enemy_name_voice = "audio/mangas6.ogg"
default cb_battle_end_reason = ""


# Cinematic background-ууд WebM болсон тул raw file path-ийг `scene`
# рүү өгөхийн оронд Ren'Py Movie displayable болгон тодорхойлно.
image cb_cinematic_world_futuristic = Movie(
    play="video/cinematic/BG/BG_Futuristic.webm",
    channel="cb_world_futuristic",
    loop=True,
    size=(config.screen_width, config.screen_height),
    image="images/cinematic/world_futuristic.webp",
)
image cb_cinematic_world_fantasy = Movie(
    play="video/cinematic/BG/BG_Fantasy.webm",
    channel="cb_world_fantasy",
    loop=True,
    size=(config.screen_width, config.screen_height),
    image="images/cinematic/world_fantasy.webp",
)
image cb_cinematic_world_modern = Movie(
    play="video/cinematic/BG/BG_Modern.webm",
    channel="cb_world_modern",
    loop=True,
    size=(config.screen_width, config.screen_height),
    image="images/cinematic/world_modern.webp",
)
image cb_cinematic_world_post = Movie(
    play="video/cinematic/BG/BG_Post.webm",
    channel="cb_world_post",
    loop=True,
    size=(config.screen_width, config.screen_height),
    image="images/cinematic/world_post.webp",
)


init -20 python:
    def cb_record_creator_result(question_index, question, result):
        """Keep a rollback-safe, primitive snapshot for the cinematic."""

        result = result or {}
        snapshot = {
            "question": str(question.get("question", "")),
            "choices": list(question.get("choices", [])),
            "choice_counts": list(result.get("choice_counts", [])),
            "top_choice_indices": list(result.get("top_choice_indices", [])),
            "total_answers": max(0, int(result.get("total_answers", 0))),
        }

        saved = list(store.cb_creator_results)
        while len(saved) <= question_index:
            saved.append(None)
        saved[question_index] = snapshot
        store.cb_creator_results = saved


    def cb_creator_winner_index(snapshot):
        if not snapshot:
            return 0

        choices = snapshot.get("choices", [])
        counts = snapshot.get("choice_counts", [])
        top_indices = snapshot.get("top_choice_indices", [])

        for raw_index in top_indices:
            try:
                index = int(raw_index)
            except Exception:
                continue
            if 0 <= index < len(choices):
                return index

        if counts:
            usable = [max(0, int(value)) for value in counts[:len(choices)]]
            if usable:
                return usable.index(max(usable))

        return 0


    def cb_prepare_cinematic():
        """Resolve the voted world and enemy, then build the short summary."""

        snapshots = list(store.cb_creator_results)
        rows = []
        participant_count = 0

        for snapshot in snapshots:
            if not snapshot:
                continue

            choices = snapshot.get("choices", [])
            counts = snapshot.get("choice_counts", [])
            total = max(0, int(snapshot.get("total_answers", 0)))
            winner_index = cb_creator_winner_index(snapshot)
            winner = choices[winner_index] if 0 <= winner_index < len(choices) else "—"
            votes = counts[winner_index] if 0 <= winner_index < len(counts) else 0
            votes = max(0, int(votes))
            percentage = int(round(100.0 * votes / total)) if total else 0

            rows.append({
                "question": snapshot.get("question", ""),
                "winner": winner,
                "votes": votes,
                "percentage": percentage,
            })
            participant_count = max(participant_count, total)

        worlds = {
            0: ("FUTURISTIC", "cb_cinematic_world_futuristic", "cb_team_city_futuristic"),
            1: ("FANTASY", "cb_cinematic_world_fantasy", "cb_team_city_fantasy"),
            2: ("MODERN", "cb_cinematic_world_modern", "cb_team_city_modern"),
            3: ("POST-APOCALYPTIC", "cb_cinematic_world_post", "cb_team_city_post"),
        }

        enemies = {
            0: {
                "key": "void",
                "name": "The Void",
                "title": "THE VOID — ХООСРОЛ",
                "idle": "video/cinematic/Attack/Void_Idle.webm",
                "attack": "video/cinematic/Attack/Void_Attack.webm",
                "movie": "video/cinematic/reveal/reveal_void.webm",
                "voice": "audio/mangas6.ogg",
            },
            1: {
                "key": "devourer",
                "name": "THE DEVOURER",
                "title": "THE DEVOURER — ЕРТӨНЦ ЗАЛГИГЧ",
                "idle": "video/cinematic/Attack/Devourer_Idle.webm",
                "attack": "video/cinematic/Attack/Devourer_Attack.webm",
                "movie": "video/cinematic/reveal/reveal_devourer.webm",
                "voice": "audio/mangas7.ogg",
            },
            2: {
                "key": "colossus",
                "name": "THE COLOSSUS",
                "title": "THE COLOSSUS — АВАРГА МАШИН",
                "idle": "video/cinematic/Attack/Colossus_Idle.webm",
                "attack": "video/cinematic/Attack/Colossus_Attack.webm",
                "movie": "video/cinematic/reveal/reveal_colossus.webm",
                # mangas8.ogg is not present in the repository. The line below
                # therefore uses a timed text fallback instead of wrong audio.
                "voice": None,
            },
        }

        world_snapshot = snapshots[1] if len(snapshots) > 1 else None
        enemy_snapshot = snapshots[5] if len(snapshots) > 5 else None
        world_name, world_image, team_city_image = worlds.get(
            cb_creator_winner_index(world_snapshot),
            worlds[0],
        )
        enemy = enemies.get(cb_creator_winner_index(enemy_snapshot), enemies[0])

        store.cb_creator_summary_rows = rows
        store.cb_creator_count = participant_count
        store.cb_world_name = world_name
        store.cb_world_image = world_image
        store.cb_team_city_image = team_city_image
        store.cb_enemy_key = enemy["key"]
        store.cb_enemy_name = enemy["name"]
        store.cb_enemy_title = enemy["title"]
        store.cb_enemy_idle_image = enemy["idle"]
        store.cb_enemy_attack_image = enemy["attack"]
        store.cb_enemy_reveal_movie = enemy["movie"]
        store.cb_enemy_name_voice = enemy["voice"]


transform cb_cinematic_world:
    xysize (config.screen_width, config.screen_height)
    xalign 0.5
    yalign 0.5


transform cb_cinematic_boss:
    anchor (0.5, 0.5)
    xalign 0.5
    yalign 0.48
    alpha 0.0
    zoom 0.82
    linear 0.75 alpha 1.0 zoom 1.0
    block:
        linear 1.1 zoom 1.025
        linear 1.1 zoom 1.0
        repeat


transform cb_cinematic_attack:
    anchor (0.5, 0.5)
    xalign 0.5
    yalign 0.48
    zoom 0.95
    linear 0.18 zoom 1.18
    linear 0.16 zoom 1.05


transform cb_boss_death:
    anchor (0.5, 0.5)
    xalign 0.5
    yalign 0.48
    alpha 1.0
    zoom 1.0
    parallel:
        easeout 2.8 alpha 0.0
    parallel:
        easeout 2.8 zoom 1.35 yoffset -45


transform cb_destroyed_world:
    xysize (config.screen_width, config.screen_height)
    xalign 0.5
    yalign 0.5
    matrixcolor TintMatrix("#B85C68") * BrightnessMatrix(-0.20)


screen crowd_creator_summary(rows, participant_count):
    modal True
    add Solid("#070B14")
    add Solid("#6F7CFF18")

    timer 5.0 action Return(True)
    key "dismiss" action NullAction()

    frame:
        at cb_result_pop
        background Solid("#121B30F7")
        xalign 0.5
        yalign 0.5
        xsize 1480
        padding (64, 40)

        vbox:
            spacing 14
            xfill True

            text "БҮТЭЭГЧДИЙН СОНГОЛТ":
                style "cb_title_text"
                xalign 0.5

            for row in rows:
                $ row_percentage = row.get("percentage", 0)
                $ row_votes = row.get("votes", 0)
                hbox:
                    spacing 30
                    xfill True

                    vbox:
                        spacing 2
                        xsize 1040
                        text row.get("question", ""):
                            color "#9DA7C2"
                            size 18
                        text row.get("winner", "—"):
                            color "#FFFFFF"
                            size 25
                            bold True

                    text "[row_percentage]%  ·  [row_votes] санал":
                        color "#8999FF"
                        size 23
                        bold True
                        xalign 1.0
                        text_align 1.0
                        xsize 280

            text "Нийт оролцогч: [participant_count]":
                style "cb_small_text"
                xalign 0.5

            textbutton "ҮРГЭЛЖЛҮҮЛЭХ":
                style "cb_button"
                xalign 0.5
                action Return(True)


screen crowd_cinematic_title(title, duration=2.8, warning=False):
    modal True
    $ accent = "#FF6E86" if warning else "#8999FF"
    add Solid("#05070D")

    timer duration action Return(True)
    key "dismiss" action NullAction()

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22

        text title:
            color accent
            size 62
            bold True
            text_align 0.5
            xalign 0.5
            outlines [(2, "#000000A0", 0, 0)]



screen crowd_system_panel(title, lines, duration=3.2, warning=False):
    modal True
    $ accent = "#FF6E86" if warning else "#59E6A8"
    add Solid("#05070DCC")

    timer duration action Return(True)
    key "dismiss" action NullAction()

    frame:
        background Solid("#10192DF2")
        xalign 0.5
        yalign 0.5
        xsize 1180
        padding (70, 52)

        vbox:
            spacing 18
            xfill True

            text title:
                color accent
                size 35
                bold True
                xalign 0.5

            for line in lines:
                text line:
                    color "#F6F7FF"
                    size 29
                    bold True
                    xalign 0.5
                    text_align 0.5


screen crowd_cinematic_movie(movie_path, duration=9.12):
    modal True
    add Solid("#000000")
    add Movie(
        play=movie_path,
        loop=False,
        size=(config.screen_width, config.screen_height)
    )

    timer duration action Return(True)
    key "dismiss" action NullAction()

    text "UNKNOWN ENTITY":
        color "#FF6E86"
        size 29
        bold True
        xpos 60
        ypos 48

    textbutton "АЛГАСАХ":
        style "cb_button"
        xalign 0.97
        yalign 0.95
        action Return("skip")


screen crowd_stability_tick(stability):
    modal True
    $ tick_duration = 0.8 if stability == 0 else 0.32
    $ stability_color = "#FF405F" if stability <= 3 else "#FF899D"

    add Solid("#05070DB8")
    timer tick_duration action Return(True)
    key "dismiss" action NullAction()

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 12

        text "WORLD STABILITY":
            color "#D7DCEF"
            size 38
            bold True
            xalign 0.5

        text "[stability]%":
            color stability_color
            size 128
            bold True
            xalign 0.5
            outlines [(3, "#000000B0", 0, 0)]


label crowd_world_cinematic:
    $ quick_menu = False
    $ cb_prepare_cinematic()
    window hide

    scene expression Solid("#000000")
    with fade
    show nova at nova_anim
    $ cb_voice_line(N, "Баярлалаа.", "audio/hutlugch18.ogg")
    $ cb_voice_line(N, "Энэ бол...", "audio/hutlugch19.ogg")
    $ cb_voice_line(N, "...та нарын бүтээсэн ертөнц.", "audio/hutlugch20.ogg")
    $ cb_voice_line(N, "Би энд юу байхыг шийдээгүй.", "audio/hutlugch21.ogg")
    $ cb_voice_line(N, "Энэ хот ямар байхыг...", "audio/hutlugch22.ogg")
    $ cb_voice_line(N, "Энд хэн амьдрахыг...", "audio/hutlugch23.ogg")
    $ cb_voice_line(N, "Тэд юунд итгэхийг...", "audio/hutlugch24.ogg")
    $ cb_voice_line(N, "Юунаас айхыг та нар шийдсэн.", "audio/hutlugch25.ogg")

    call screen crowd_creator_summary(cb_creator_summary_rows, cb_creator_count)

    
    call screen crowd_cinematic_title(
        "CREATED BY {} CREATORS".format(cb_creator_count),
        3.2
    )

    scene expression cb_world_image at cb_cinematic_world
    with fade

    $ cb_voice_line(N, "Эцэст нь шинэ ертөнц мэндэллээ.", "audio/hutlugch26.ogg")
    $ cb_voice_line(N, "Эхний өдөр.", "audio/hutlugch27.ogg")
    $ cb_voice_line(N, "Бүх зүйл тайван байлаа.", "audio/hutlugch28.ogg")
    $ cb_voice_line(N, "Хэнтэй ч дайтах шаардлагагүй.", "audio/hutlugch29.ogg")
    $ cb_voice_line(N, "Юунд ч санаа зовох шаардлагагүй.", "audio/hutlugch30.ogg")
    $ cb_voice_line(N, "Хүмүүс зүгээр л...", "audio/hutlugch31.ogg")
    $ cb_voice_line(N, "...амьдарч байлаа.", "audio/hutlugch32.ogg")

    window hide
    $ renpy.pause(2.5, hard=True)

    call screen crowd_system_panel(
        "SYSTEM",
        [
            "WEATHER — NORMAL.",
            "ENERGY — NORMAL.",
            "POPULATION — NORMAL.",
            "WORLD STABILITY — 100%.",
        ],
        3.8
    )

    $ cb_voice_line(N, "Магадгүй...", "audio/hutlugch33.ogg")
    $ cb_voice_line(N, "...бид үнэхээр төгс ертөнц бүтээчихсэн бололтой.", "audio/hutlugch34.ogg")

    window hide
    play sound "audio/cinematic_rumble.ogg" fadein 1.0
    $ renpy.pause(0.8, hard=True)
    with hpunch
    $ renpy.pause(0.7, hard=True)
    with vpunch

    call screen crowd_system_panel(
        "SYSTEM",
        ["UNKNOWN PHENOMENON DETECTED."],
        2.4,
        True
    )

    $ cb_voice_line(N, "Тэр юу вэ?", "audio/hutlugch35.ogg")

    call screen crowd_system_panel(
        "SYSTEM",
        ["UNKNOWN.", "UNKNOWN.", "UNKNOWN.", "SIZE: UNMEASURABLE."],
        3.3,
        True
    )

    call screen crowd_cinematic_movie(cb_enemy_reveal_movie, 9.12)
    with vpunch
    stop sound fadeout 1.0

    scene expression cb_world_image at cb_cinematic_world
    show expression cb_enemy_idle_image as crowd_enemy at cb_cinematic_boss
    with dissolve

    call screen crowd_system_panel(
        "WARNING",
        [
            "ATMOSPHERIC DISTORTION.",
            "GRAVITY FLUCTUATION.",
            "WORLD STABILITY — 94%.",
            "UNKNOWN ENTITY",
        ],
        3.8,
        True
    )

    $ cb_voice_line(Monster, "Энэ ертөнц...", "audio/mangas1.ogg")
    $ renpy.pause(0.8, hard=True)
    $ cb_voice_line(Monster, "...та нарынх биш.", "audio/mangas2.ogg")

    N "Чи хэн бэ?{w=1.5}{nw}"

    $ cb_voice_line(Monster, "Намайг мэдэх хүн та нарын дунд байхгүй.", "audio/mangas3.ogg")
    $ cb_voice_line(Monster, "Учир нь...", "audio/mangas4.ogg")
    $ cb_voice_line(Monster, "...би та нараас ч өмнө байсан.", "audio/mangas5.ogg")

    if cb_enemy_name_voice:
        $ enemy_name_line = "Намайг “{}” гэдэг.".format(cb_enemy_name)
        $ cb_voice_line(Monster, enemy_name_line, cb_enemy_name_voice)
    else:
        Monster "Намайг “THE COLOSSUS” гэдэг.{w=2.8}{nw}"

    $ cb_voice_line(N, "Яагаад бидэн рүү дайрч байна вэ?", "audio/hutlugch36.ogg")
    $ cb_voice_line(Monster, "Дайрах гэж үү?", "audio/mangas9.ogg")
    $ cb_voice_line(Monster, "ХА-ХА-ХА!", "audio/mangas10.ogg")
    $ cb_voice_line(Monster, "Би буцаан авч байна.", "audio/mangas11.ogg")
    $ cb_voice_line(N, "Юуг?", "audio/hutlugch37.ogg")
    $ cb_voice_line(Monster, "Ертөнцийг.", "audio/mangas12.ogg")

    window hide
    hide crowd_enemy
    show expression cb_enemy_attack_image as crowd_enemy at cb_cinematic_attack
    play sound "audio/cinematic_impact.ogg"
    with hpunch
    with fade
    $ renpy.pause(0.7, hard=True)
    hide crowd_enemy
    show expression cb_enemy_idle_image as crowd_enemy at cb_cinematic_boss

    $ cb_voice_line(N, "Бүтээгчдээ!", "audio/hutlugch38.ogg")
    $ cb_voice_line(N, "Та нар энэ ертөнцийг бүтээсэн!", "audio/hutlugch39.ogg")
    $ cb_voice_line(N, "Одоо...", "audio/hutlugch40.ogg")
    $ cb_voice_line(N, "...ХАМГААЛ!", "audio/hutlugch41.ogg")
    $ cb_voice_line(N, "Тулалд!", "audio/hutlugch42.ogg")
    $ cb_voice_line(N, "Гэхдээ бид бяр чадлаар тулалдахгүй.", "audio/hutlugch43.ogg")
    $ cb_voice_line(N, "Мэдлэгээрээ тулалдах болно.", "audio/hutlugch44.ogg")

    window hide
    call screen crowd_cinematic_title(
        "ANIME & ANIMATION QUIZ",
        "ДУНД / ХҮНД",
        3.2
    )

    jump crowd_monster_battle


label crowd_defeat_ending:
    $ quick_menu = False
    window hide

    scene expression cb_world_image at cb_cinematic_world
    show expression cb_enemy_attack_image as crowd_enemy at cb_cinematic_attack
    play sound "audio/cinematic_impact.ogg"
    with hpunch
    with vpunch
    with fade

    scene expression "images/cinematic/world_post.webp" at cb_destroyed_world
    show expression cb_enemy_idle_image as crowd_enemy at cb_cinematic_boss
    with Fade(0.35, 0.15, 0.65, color="#5A0714")

    $ cb_voice_line(N, "...үгүй ээ.", "audio/defeat1.ogg")
    $ cb_voice_line(Monster, "Та нар хангалттай хичээлээ.", "audio/mangas13.ogg")
    $ cb_voice_line(Monster, "Гэхдээ энэ ертөнц...", "audio/mangas14.ogg")
    $ renpy.pause(0.9, hard=True)
    $ cb_voice_line(Monster, "...одоо минийх.", "audio/mangas15.ogg")

    window hide
    play sound "audio/cinematic_rumble.ogg" fadein 0.8
    $ world_stability = 10
    while world_stability >= 0:
        call screen crowd_stability_tick(world_stability)
        $ world_stability -= 1

    stop sound fadeout 0.4
    scene expression Solid("#000000")
    with Fade(0.8, 0.4, 1.0)
    $ renpy.pause(2.0, hard=True)
    return


label crowd_victory_ending:
    $ quick_menu = False
    window hide

    scene expression cb_world_image at cb_cinematic_world
    show expression cb_enemy_idle_image as crowd_enemy at cb_cinematic_boss
    with dissolve

    play sound "audio/cinematic_impact.ogg"
    with hpunch
    with fade
    show expression cb_enemy_idle_image as crowd_enemy at cb_boss_death
    $ renpy.pause(2.9, hard=True)
    hide crowd_enemy

    call screen crowd_system_panel(
        "SYSTEM",
        [
            "WORLD STABILITY — 100%.",
            "POPULATION — SAFE.",
            "CITY — STABLE.",
            "CORE — STABLE.",
        ],
        4.0
    )

    $ cb_voice_line(N, "ANIMO World...", "audio/win2.ogg")
    $ cb_voice_line(N, "...амьд үлдлээ.", "audio/win3.ogg")
    $ cb_voice_line(N, "Та нар өөрсдийн бүтээсэн ертөнцийг хамгаалж чадлаа.", "audio/win4.ogg")

    window hide
    call screen crowd_cinematic_title("YOUR WORLD.", "", 1.5)
    call screen crowd_cinematic_title("YOUR CHOICES.", "", 1.5)
    call screen crowd_cinematic_title("YOUR ANIMO.", "", 2.5)
    return
