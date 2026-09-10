transform cb_monster_idle:
    anchor (0.5, 0.5)
    zoom 1.0
    linear 0.8 zoom 1.035
    linear 0.8 zoom 1.0
    repeat


transform cb_result_pop:
    alpha 0.0
    zoom 0.75
    linear 0.22 alpha 1.0 zoom 1.05
    linear 0.12 zoom 1.0


transform cb_damage_float:
    anchor (0.5, 0.5)
    alpha 0.0
    yoffset 35
    zoom 0.75
    linear 0.14 alpha 1.0 zoom 1.15
    pause 0.18
    easeout 1.35 yoffset -125 alpha 0.0 zoom 1.0


transform cb_city_damage_float:
    anchor (0.5, 0.5)
    alpha 0.0
    yoffset 35
    zoom 0.75
    pause 0.84
    linear 0.14 alpha 1.0 zoom 1.15
    pause 0.18
    easeout 1.35 yoffset -125 alpha 0.0 zoom 1.0


transform cb_monster_hit_flash:
    # Damage авсан мөчид мангасыг богино хугацаанд улаан болгоод
    # үндсэн өнгөнд нь зөөлөн буцаана. Эхний pause нь city projectile
    # мангасад хүрэх хугацаатай таарна.
    matrixcolor TintMatrix("#FFFFFF")
    pause 0.84
    linear 0.08 matrixcolor TintMatrix("#FF3B4F")
    pause 0.18
    linear 0.28 matrixcolor TintMatrix("#FFFFFF")


transform cb_team_hit_flash:
    matrixcolor TintMatrix("#FFFFFF")
    linear 0.08 matrixcolor TintMatrix("#FF334F")
    pause 0.18
    linear 0.32 matrixcolor TintMatrix("#FFFFFF")


transform cb_city_weapon_idle:
    anchor (0.5, 0.5)
    yoffset 0
    linear 1.15 yoffset -3
    linear 1.15 yoffset 0
    repeat


transform cb_city_weapon_fire:
    anchor (0.5, 0.5)
    matrixcolor BrightnessMatrix(0.0)
    pause 0.10
    linear 0.07 xoffset -18 matrixcolor BrightnessMatrix(0.45)
    linear 0.13 xoffset 5 matrixcolor BrightnessMatrix(0.10)
    linear 0.16 xoffset 0 matrixcolor BrightnessMatrix(0.0)


transform cb_city_projectile_flight:
    anchor (0.5, 0.5)
    subpixel True
    xpos 690
    ypos 470
    zoom 0.34
    alpha 0.0
    pause 0.14
    linear 0.04 alpha 1.0
    easein 0.64 xpos 1410 ypos 440 zoom 0.46
    linear 0.08 alpha 0.0 zoom 0.62


transform cb_void_glitch_strip(wait=0.0):
    alpha 0.0
    pause wait
    block:
        pause 0.38
        alpha 0.62
        xoffset -22
        pause 0.04
        xoffset 16
        pause 0.04
        alpha 0.0
        xoffset 0
        pause 0.72
        repeat


define CB_RESULT_DISPLAY_SECONDS = 4
define CB_ATTACK_RESULT_DISPLAY_SECONDS = 7
define CB_BREAK_START_DELAY = 0.30
define CB_BREAK_SCREEN_SECONDS = 5.80


init -35 python:
    # "ТА ХЭН БЭ?" creators question-ийн role portrait-ууд.
    CB_ROLE_PREVIEW_DATA = {
        "Student": "images/creator_roles/student.png",
        "Worker": "images/creator_roles/worker.png",
        "Creators": "images/creator_roles/creator.png",
        "Gamer": "images/creator_roles/gamer.png",
        "Explorer": "images/creator_roles/explorer.png",
        "Fan": "images/creator_roles/fan.png",
        "Just Here": "images/creator_roles/just_here.png",
    }

    # "Ертөнц хаана байдаг вэ?" асуултын location зургууд.
    CB_LOCATION_PREVIEW_DATA = {
        "Earth": "images/world_locations/earth.png",
        "Another Planet": "images/world_locations/another_planet.png",
        "Floating World": "images/world_locations/floating_world.png",
        "Underground": "images/world_locations/underground.png",
        "Another Dimension": "images/world_locations/another_dimension.png",
    }

    # Creators-ийн ертөнцийн төрлийн асуултын шинэ static зургууд.
    CB_WORLD_PREVIEW_DATA = {
        "Futuristic": "images/world_types/futuristic.webp",
        "Fantasy": "images/world_types/fantasy.webp",
        "Modern": "images/world_types/modern.webp",
        "Post-apocalyptic": "images/world_types/post_apocalyptic.webp",
    }

    # answer_citizen хавтас дахь 7 сонголтын зураг.
    CB_CITIZEN_PREVIEW_DATA = {
        "Humans": {
            "image": "images/cinematic/answer_citizen/human.png",
            "crop": (558, 419, 671, 394),
        },
        "Robots": {
            "image": "images/cinematic/answer_citizen/robot.png",
            "crop": (639, 420, 643, 377),
        },
        "Magic Creatures": {
            "image": "images/cinematic/answer_citizen/magic creatures.png",
            "crop": (636, 423, 650, 382),
        },
        "Aliens": {
            "image": "images/cinematic/answer_citizen/alien.png",
            "crop": (541, 384, 742, 435),
        },
        "Anime Characters": {
            "image": "images/cinematic/answer_citizen/anime.png",
            "crop": (625, 411, 671, 394),
        },
        "Elfs": {
            "image": "images/cinematic/answer_citizen/elf.png",
            "crop": (603, 404, 701, 412),
        },
        "Orcs": {
            "image": "images/cinematic/answer_citizen/orc.png",
            "crop": (528, 369, 783, 460),
        },
    }

    # Сонгогдсон мангасын battle үеийн нэг удаагийн attack болон loop idle.
    CB_BATTLE_MONSTER_MOVIES = {
        "void": {
            "attack": "video/cinematic/Attack/Void_Attack.webm",
            "idle": "video/cinematic/Attack/Void_Idle.webm",
        },
        "devourer": {
            "attack": "video/cinematic/Attack/Devourer_attack.webm",
            "idle": "video/cinematic/Attack/Devourer_idle.webm",
        },
        "colossus": {
            "attack": "video/cinematic/Attack/Colosus_attack.webm",
            "idle": "video/cinematic/Attack/Colosus_idle.webm",
        },
    }

    # Creators-ийн сонгосон дөрвөн world/city тус бүр өөр хамгаалалтын
    # зэвсэг болон projectile ашиглана.
    CB_CITY_ATTACK_MEDIA = {
        "FUTURISTIC": {
            "weapon": "images/cinematic/city_weapons/futuristic_cannon.webp",
            "projectile": "images/cinematic/city_weapons/futuristic_plasma.webp",
            "label": "RAIL CANNON",
        },
        "FANTASY": {
            "weapon": "images/cinematic/city_weapons/fantasy_ballista.webp",
            "projectile": "images/cinematic/city_weapons/fantasy_magic_spear.webp",
            "label": "RUNE BALLISTA",
        },
        "MODERN": {
            "weapon": "images/cinematic/city_weapons/modern_launcher.webp",
            "projectile": "images/cinematic/city_weapons/modern_missile.webp",
            "label": "MISSILE LAUNCHER",
        },
        "POST-APOCALYPTIC": {
            "weapon": "images/cinematic/city_weapons/post_scrap_cannon.webp",
            "projectile": "images/cinematic/city_weapons/post_flaming_shell.webp",
            "label": "SCRAP CANNON",
        },
    }

    # Battle дуусахад ялагдсан талд тоглох нэг удаагийн break animation.
    CB_MONSTER_BREAK_MOVIES = {
        "void": "video/cinematic/break/Void_Die.webm",
        "devourer": "video/cinematic/break/Devourer_die.webm",
        "colossus": "video/cinematic/break/Colosus_Die.webm",
    }

    CB_CITY_BREAK_MOVIES = {
        "FUTURISTIC": "video/cinematic/break/Futurist.webm",
        "FANTASY": "video/cinematic/break/Fantasy.webm",
        "MODERN": "video/cinematic/break/modern.webm",
        "POST-APOCALYPTIC": "video/cinematic/break/Post.webm",
    }

    CB_BREAK_FALLBACK_MOVIE = "video/cinematic/break/Explosion pixel.webm"

    CB_BOSS_MECHANIC_LABELS = {
        "void": "VOID · 3 ДАХЬ АСУУЛТ БҮР ХУГАЦАА -5 СЕК",
        "devourer": "DEVOURER · БУРУУ ХУВИАР HP НӨХНӨ",
        "colossus": "COLOSSUS · 60%+ ЗӨВ ХОЁР COMBO ARMOR ЭВДЭЛНЭ",
    }


    def cb_city_attack_media():
        world_name = str(
            getattr(store, "cb_world_name", "FUTURISTIC") or "FUTURISTIC"
        ).upper()
        return CB_CITY_ATTACK_MEDIA.get(
            world_name,
            CB_CITY_ATTACK_MEDIA["FUTURISTIC"],
        )

    # Нэг дэлгэц дээр дөрвөн Movie зэрэг ажиллах тул тус бүр өөр channel-тэй.
    for _cb_movie_channel in (
        "cb_preview_futuristic",
        "cb_preview_fantasy",
        "cb_preview_modern",
        "cb_preview_post",
    ):
        if not renpy.music.channel_defined(_cb_movie_channel):
            renpy.music.register_channel(
                _cb_movie_channel,
                mixer="sfx",
                loop=True,
                stop_on_mute=False,
                buffer_queue=False,
                movie=True,
            )

    # Хотын WebM-үүд audio track-тай тул battle SFX-ийг давхардуулахгүйгээр
    # тусдаа, дуугүй movie channel дээр loop хийнэ.
    for _cb_city_channel in (
        "cb_city_futuristic",
        "cb_city_fantasy",
        "cb_city_modern",
        "cb_city_post",
    ):
        if not renpy.music.channel_defined(_cb_city_channel):
            renpy.music.register_channel(
                _cb_city_channel,
                mixer="sfx",
                loop=True,
                stop_on_mute=False,
                buffer_queue=False,
                movie=True,
                framedrop=True,
            )
        renpy.music.set_volume(0.0, delay=0.0, channel=_cb_city_channel)

    if not renpy.music.channel_defined("cb_monster_movie"):
        renpy.music.register_channel(
            "cb_monster_movie",
            mixer="sfx",
            loop=False,
            stop_on_mute=False,
            buffer_queue=False,
            movie=True,
            framedrop=True,
        )

    if not renpy.music.channel_defined("cb_break_movie"):
        renpy.music.register_channel(
            "cb_break_movie",
            mixer="sfx",
            loop=False,
            stop_on_mute=False,
            buffer_queue=False,
            movie=True,
            framedrop=True,
        )


    def cb_start_battle_feedback(result):
        """Play one attack whenever the team takes damage, then loop idle."""

        result = result or {}
        enemy_key = getattr(store, "cb_enemy_key", "void")
        media = CB_BATTLE_MONSTER_MOVIES.get(
            enemy_key,
            CB_BATTLE_MONSTER_MOVIES["void"],
        )
        attack_movie = media["attack"]
        idle_movie = media["idle"]
        should_attack = max(0, int(result.get("player_damage", 0))) > 0

        renpy.music.stop(channel="cb_monster_movie", fadeout=0.0)

        if should_attack and renpy.loadable(attack_movie):
            renpy.music.play(
                attack_movie,
                channel="cb_monster_movie",
                loop=False,
                fadeout=0.0,
            )
            if renpy.loadable(idle_movie):
                renpy.music.queue(
                    idle_movie,
                    channel="cb_monster_movie",
                    loop=True,
                    clear_queue=False,
                )
        elif renpy.loadable(idle_movie):
            renpy.music.play(
                idle_movie,
                channel="cb_monster_movie",
                loop=True,
                fadeout=0.0,
            )

        # Screen action-д ашиглагдах тул утга буцааж interaction-ийг
        # санамсаргүй дуусгаж болохгүй.
        return None


    def cb_start_battle_idle():
        """Keep the selected boss on its looping idle movie during questions."""

        enemy_key = getattr(store, "cb_enemy_key", "void")
        media = CB_BATTLE_MONSTER_MOVIES.get(
            enemy_key,
            CB_BATTLE_MONSTER_MOVIES["void"],
        )
        idle_movie = media["idle"]
        if renpy.loadable(idle_movie):
            renpy.music.play(
                idle_movie,
                channel="cb_monster_movie",
                loop=True,
                fadeout=0.0,
            )
        return None


    def cb_stop_battle_feedback():
        renpy.music.stop(channel="cb_monster_movie", fadeout=0.0)
        return None


    def cb_battle_break_movie(victory):
        """Return the selected losing side's break movie."""

        if victory:
            enemy_key = str(
                getattr(store, "cb_enemy_key", "void") or "void"
            ).lower()
            return CB_MONSTER_BREAK_MOVIES.get(
                enemy_key,
                CB_MONSTER_BREAK_MOVIES["void"],
            )

        world_name = str(
            getattr(store, "cb_world_name", "FUTURISTIC") or "FUTURISTIC"
        ).upper()
        return CB_CITY_BREAK_MOVIES.get(
            world_name,
            CB_CITY_BREAK_MOVIES["FUTURISTIC"],
        )


    def cb_prepare_battle_break(victory):
        """Clear old feedback before the final break animation."""

        renpy.music.stop(channel="cb_break_movie", fadeout=0.0)
        renpy.music.stop(channel="cb_monster_movie", fadeout=0.0)

        # Хот ялагдсан үед амьд үлдсэн boss idle хэвээр байна.
        if not victory:
            cb_start_battle_idle()
        return None


    def cb_play_battle_break(victory):
        """Play the losing monster/city animation exactly once."""

        break_movie = cb_battle_break_movie(victory)
        if not renpy.loadable(break_movie):
            break_movie = CB_BREAK_FALLBACK_MOVIE

        if renpy.loadable(break_movie):
            renpy.music.play(
                break_movie,
                channel="cb_break_movie",
                loop=False,
                fadeout=0.0,
            )
        return None


    def cb_stop_battle_break():
        renpy.music.stop(channel="cb_break_movie", fadeout=0.0)
        renpy.music.stop(channel="cb_monster_movie", fadeout=0.0)
        return None


# Movie displayable-уудыг screen ажиллахаас өмнө init үеэр үүсгэнэ.
# `image` нь video байхгүй/дэмжигдэхгүй төхөөрөмж дээрх fallback зураг.
image cb_preview_futuristic = Movie(
    play="video/cinematic/BG/BG_Futuristic.webm",
    channel="cb_preview_futuristic",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_futuristic.webp",
)
image cb_preview_fantasy = Movie(
    play="video/cinematic/BG/BG_Fantasy.webm",
    channel="cb_preview_fantasy",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_fantasy.webp",
)
image cb_preview_modern = Movie(
    play="video/cinematic/BG/BG_Modern.webm",
    channel="cb_preview_modern",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_modern.webp",
)
image cb_preview_post = Movie(
    play="video/cinematic/BG/BG_Post.webm",
    channel="cb_preview_post",
    loop=True,
    size=(300, 169),
    image="images/cinematic/world_post.webp",
)
image cb_team_city_futuristic = Movie(
    play="video/cinematic/city/Futurist.webm",
    channel="cb_city_futuristic",
    loop=True,
    size=(720, 402),
    image="images/cinematic/world_futuristic.webp",
)
image cb_team_city_fantasy = Movie(
    play="video/cinematic/city/fantastic.webm",
    channel="cb_city_fantasy",
    loop=True,
    size=(720, 402),
    image="images/cinematic/world_fantasy.webp",
)
image cb_team_city_modern = Movie(
    play="video/cinematic/city/modern.webm",
    channel="cb_city_modern",
    loop=True,
    size=(720, 402),
    image="images/cinematic/world_modern.webp",
)
image cb_team_city_post = Movie(
    play="video/cinematic/city/post.webm",
    channel="cb_city_post",
    loop=True,
    size=(720, 402),
    image="images/cinematic/world_post.webp",
)


style cb_title_text:
    color "#F6F7FF"
    size 46
    bold True

style cb_body_text:
    color "#D7DCEF"
    size 28

style cb_small_text:
    color "#A8B0C7"
    size 22

style cb_button is button:
    background Solid("#263354")
    hover_background Solid("#5268D8")
    padding (30, 16)
    xminimum 270

style cb_button_text is button_text:
    color "#FFFFFF"
    size 26
    bold True
    text_align 0.5

screen crowd_battle_intro():
    modal True
    add Solid("#070B14")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 28

        text "[cb_enemy_title]" style "cb_title_text" xalign 0.5
        text "Зөв хариултын хувь = мангасад өгөх damage.\nБуруу хариултын хувь = хотод өгөх damage. (Нэг round-д тал бүр 0–100)":
            style "cb_body_text"
            text_align 0.5
            xalign 0.5

        text "Утаснаасаа нээх хаяг:" style "cb_small_text" xalign 0.5
        text "[cb_server_url()]":
            color "#8999FF"
            size 30
            bold True
            xalign 0.5

        null height 14
        textbutton "ТУЛААН ЭХЛҮҮЛЭХ":
            style "cb_button"
            xalign 0.5
            action Return(True)


screen crowd_battle_stage(shown_question, shown_choices=None, voting_active=False):
    $ battle_choices = list(shown_choices or [])
    $ choice_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    $ choice_colors = ("#5677FF", "#A765FF", "#FF9E45", "#35C991")
    $ battle_state = cb_battle or {}
    $ current_round = battle_state.get("current_round") or {}
    $ monster_key = battle_state.get("monster_key", getattr(store, "cb_enemy_key", "void"))
    $ team_city_image = getattr(store, "cb_team_city_image", "cb_team_city_futuristic")
    $ city_attack = cb_city_attack_media()
    $ city_weapon_image = city_attack["weapon"]
    $ city_weapon_label = city_attack["label"]
    $ duration_penalty = max(0, int(current_round.get("duration_penalty", 0)))
    $ void_glitch_active = voting_active and current_round.get("mechanic_event") == "void_glitch"
    $ armor_active = bool(battle_state.get("colossus_armor_active", monster_key == "colossus"))
    $ armor_combo = max(0, int(battle_state.get("colossus_combo", 0)))
    $ armor_target = max(1, int(battle_state.get("colossus_combo_target", 2)))
    $ boss_mechanic_text = CB_BOSS_MECHANIC_LABELS.get(monster_key, "")
    $ boss_mechanic_color = "#A8B0C7"

    if void_glitch_active:
        $ boss_mechanic_text = "VOID GLITCH · ХУГАЦАА -{} СЕК".format(duration_penalty)
        $ boss_mechanic_color = "#D69CFF"
    elif monster_key == "colossus":
        $ boss_mechanic_text = "ARMOR · COMBO {}/{}".format(armor_combo, armor_target) if armor_active else "ARMOR ЭВДЭРСЭН"
        $ boss_mechanic_color = "#FFD36D" if armor_active else "#59E6A8"

    add Solid("#070B14")
    add Solid("#101A31") xysize (1920, 270)

    vbox:
        xpos 90
        ypos 45
        xsize 760
        spacing 10
        text "ҮЗЭГЧДИЙН БАГ" style "cb_small_text"
        text "[cb_player_hp] / [cb_player_max_hp] HP":
            color "#7FF0BB"
            size 29
            bold True
        bar:
            value StaticValue(cb_player_hp, cb_player_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#38D99A")
            right_bar Solid("#24304A")

    vbox:
        xpos 1070
        ypos 45
        xsize 760
        spacing 10
        text "[cb_enemy_name]" style "cb_small_text" xalign 1.0
        text "[cb_monster_hp] / [cb_monster_max_hp] HP":
            color "#FF8296"
            size 29
            bold True
            xalign 1.0
        bar:
            value StaticValue(cb_monster_hp, cb_monster_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#FF5F78")
            right_bar Solid("#24304A")
            xalign 1.0

        if boss_mechanic_text:
            text boss_mechanic_text:
                color boss_mechanic_color
                size 17
                bold True
                xalign 1.0
                text_align 1.0

    # Хот, projectile-ийн зам, мангас гурав нэг тасралтгүй arena-д байна.
    # Тусдаа frame/border ашиглахгүй тул хоёр тал нэг тулааны талбар мэт харагдана.
    add Solid("#000000"):
        xpos 50
        ypos 270
        xsize 1820
        ysize 350

    add team_city_image:
        xysize (640, 358)
        xcenter 430
        ycenter 445

    # Хотын төрлөөр сонгогдох хамгаалалтын зэвсэг city video дээр байна.
    add city_weapon_image:
        at cb_city_weapon_idle
        xysize (310, 180)
        xcenter 590
        ycenter 520

    text city_weapon_label:
        color "#C7D4F5"
        size 16
        bold True
        xcenter 590
        ycenter 600
        outlines [(2, "#07101FDD", 0, 0)]

    add cb_enemy_idle_image:
        at cb_monster_idle
        xysize (640, 358)
        xcenter 1490
        ycenter 445

    add Movie(channel="cb_monster_movie", size=(640, 358)):
        xcenter 1490
        ycenter 445

    # Асуулт болон хариултуудыг хоёр талаасаа зайтай, доод төв panel-д
    # байрлуулна. Сонголтыг үзэгч утаснаасаа хийсээр байна.
    frame:
        background Solid("#121B30EE")
        xpos 260
        ypos 620
        xsize 1400
        ysize 420
        padding (26, 20)

        vbox:
            xfill True
            spacing 8

            fixed:
                xfill True
                ysize 76

                if shown_question:
                    text shown_question:
                        color "#FFFFFF"
                        size 29
                        bold True
                        xalign 0.5
                        yalign 0.5
                        xmaximum 1080
                        text_align 0.5

                if voting_active:
                    text "[cb_remaining_seconds] секунд":
                        color "#FF899D"
                        size 25
                        bold True
                        xalign 1.0
                        yalign 0.5
                        text_align 1.0

            for choice_index, choice in enumerate(battle_choices):
                $ choice_letter = choice_letters[choice_index]
                $ choice_color = choice_colors[choice_index % len(choice_colors)]

                frame:
                    background Solid("#1A2540F5")
                    xfill True
                    yminimum 56
                    padding (12, 6)

                    fixed:
                        xfill True
                        ysize 44

                        frame:
                            background Solid(choice_color)
                            xysize (43, 43)
                            xpos 0
                            yalign 0.5
                            padding (0, 0)

                            text choice_letter:
                                color "#FFFFFF"
                                size 23
                                bold True
                                xalign 0.5
                                yalign 0.5

                        text choice:
                            color "#F6F7FF"
                            size 22
                            bold True
                            xalign 0.5
                            yalign 0.5
                            xmaximum 1120
                            text_align 0.5

            if voting_active and cb_connection_message:
                text cb_connection_message:
                    color "#FF899D"
                    size 18
                    xalign 0.5

    # Void-ийн тусгай round дээр deterministic glitch strip-үүд харагдана.
    if void_glitch_active:
        add Solid("#8D62FF68"):
            at cb_void_glitch_strip(0.0)
            xpos 0
            ypos 315
            xsize 1920
            ysize 5

        add Solid("#FF477A55"):
            at cb_void_glitch_strip(0.22)
            xpos 0
            ypos 535
            xsize 1920
            ysize 4

        add Solid("#7B4DFF44"):
            at cb_void_glitch_strip(0.46)
            xpos 0
            ypos 785
            xsize 1920
            ysize 7


# Voice уншиж байх preview болон санал авч буй round нь тусдаа top-level
# screen байна. Ижил screen/tag-ийг шууд hide -> call хийхэд Ren'Py өмнөх
# preview аргументыг хадгалж, polling timer-ийг асаахгүй үлдээж болдог.
screen crowd_battle_voice_preview(question):
    modal True

    on "show" action Function(cb_start_battle_idle)
    
    $ shown_question = (question or {}).get("question", "")
    $ shown_choices = (question or {}).get("choices", [])
    use crowd_battle_stage(shown_question, shown_choices, False)


screen crowd_battle_round(expected_round_id=None):
    modal True

    $ current_round = cb_battle.get("current_round") or {}
    $ guarded_round_id = expected_round_id or cb_round_guard_id

    on "show" action Function(cb_start_battle_idle)
    timer 0.25 repeat True action Function(cb_poll_round_action)

    if cb_round_can_finish(guarded_round_id):
        timer 0.10 action Return(current_round.get("result") or cb_round_result)

    use crowd_battle_stage(current_round.get("question", ""), current_round.get("choices", []), True)


screen crowd_round_result(result, final_question=False):
    modal True

    $ correct_count = result.get("correct_count", 0)
    $ wrong_count = result.get("wrong_count", 0)
    $ correct_percentage = result.get("correct_percentage", 0.0)
    $ wrong_percentage = result.get("wrong_percentage", 0.0)
    $ monster_damage = result.get("monster_damage", 0)
    $ player_damage = result.get("player_damage", 0)
    $ no_answer_penalty = bool(result.get("no_answer_penalty", False))
    $ monster_heal = result.get("monster_heal", 0)
    $ monster_damage_blocked = result.get("monster_damage_blocked", 0)
    $ mechanic_event = result.get("mechanic_event")
    $ duration_penalty = result.get("duration_penalty", 0)
    $ armor_combo = result.get("armor_combo", 0)
    $ armor_combo_target = result.get("armor_combo_target", 2)
    $ total_answers = result.get("total_answers", 0)
    $ team_city_image = getattr(store, "cb_team_city_image", "cb_team_city_futuristic")
    $ city_attack = cb_city_attack_media()
    $ city_weapon_image = city_attack["weapon"]
    $ city_projectile_image = city_attack["projectile"]
    $ city_weapon_label = city_attack["label"]
    $ city_attack_triggered = monster_damage > 0 or monster_damage_blocked > 0
    $ battle_finished = result.get("battle_status", "active") in ("victory", "defeat")
    $ next_part_text = "төгсгөлийн хэсэг" if battle_finished or final_question else "дараагийн асуулт"
    $ result_display_seconds = CB_ATTACK_RESULT_DISPLAY_SECONDS if player_damage > 0 else CB_RESULT_DISPLAY_SECONDS
    $ result_display_label = int(round(result_display_seconds))

    add Solid("#070B14")
    add Solid("#101A31") xysize (1920, 270)

    # Баг damage авбал attack-ийг нэг удаа тоглуулаад idle video-г
    # дараалалд оруулна. Screen хаагдахад movie channel-ийг цэвэрлэнэ.
    on "show" action Function(cb_start_battle_feedback, result)
    on "hide" action Function(cb_stop_battle_feedback)

    timer result_display_seconds action Return(True)
    if city_attack_triggered:
        timer 0.84 action Play("sound", "audio/cinematic_impact.ogg")

    vbox:
        xpos 90
        ypos 45
        xsize 760
        spacing 10
        text "ҮЗЭГЧДИЙН БАГ" style "cb_small_text"
        text "[cb_player_hp] / [cb_player_max_hp] HP":
            color "#7FF0BB"
            size 29
            bold True
        bar:
            value StaticValue(cb_player_hp, cb_player_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#38D99A")
            right_bar Solid("#24304A")

    vbox:
        xpos 1070
        ypos 45
        xsize 760
        spacing 10
        text "[cb_enemy_name]" style "cb_small_text" xalign 1.0
        text "[cb_monster_hp] / [cb_monster_max_hp] HP":
            color "#FF8296"
            size 29
            bold True
            xalign 1.0
        bar:
            value StaticValue(cb_monster_hp, cb_monster_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#FF5F78")
            right_bar Solid("#24304A")
            xalign 1.0

    # Result дээр ч хоёр тал ижил нэг arena дотор үлдэнэ.
    add Solid("#000000"):
        xpos 50
        ypos 270
        xsize 1820
        ysize 350

    if player_damage > 0:
        add team_city_image:
            at cb_team_hit_flash
            xysize (640, 358)
            xcenter 430
            ycenter 445
    else:
        add team_city_image:
            xysize (640, 358)
            xcenter 430
            ycenter 445

    if city_attack_triggered:
        add city_weapon_image:
            at cb_city_weapon_fire
            xysize (310, 180)
            xcenter 590
            ycenter 520
    else:
        add city_weapon_image:
            at cb_city_weapon_idle
            xysize (310, 180)
            xcenter 590
            ycenter 520

    text city_weapon_label:
        color "#C7D4F5"
        size 16
        bold True
        xcenter 590
        ycenter 600
        outlines [(2, "#07101FDD", 0, 0)]

    if player_damage > 0:
        text "-[player_damage] HP":
            at cb_damage_float
            xcenter 430
            ycenter 445
            color "#FF334F"
            size 68
            bold True
            outlines [(5, "#2A0008DD", 0, 0)]

    # Зөв хариултын damage эсвэл Colossus armor block үүсвэл хотын
    # projectile зүүн талаас monster руу нэг удаа ниснэ.
    if city_attack_triggered:
        add city_projectile_image:
            at cb_city_projectile_flight

    # Video decode эхлэхээс өмнө болон файл олдохгүй үед idle зураг харагдана.
    # Monster damage авсан бол зураг ба video хоёул ижил red-hit flash авна.
    if monster_damage > 0:
        add cb_enemy_idle_image:
            at cb_monster_idle, cb_monster_hit_flash
            xysize (640, 358)
            xcenter 1490
            ycenter 445

        add Movie(channel="cb_monster_movie", size=(640, 358)):
            at cb_monster_hit_flash
            xcenter 1490
            ycenter 445
    else:
        add cb_enemy_idle_image:
            at cb_monster_idle
            xysize (640, 358)
            xcenter 1490
            ycenter 445

        add Movie(channel="cb_monster_movie", size=(640, 358)):
            xcenter 1490
            ycenter 445

    if monster_damage > 0:
        text "-[monster_damage] HP":
            at cb_city_damage_float
            xcenter 1490
            ycenter 445
            color "#FF3B5C"
            size 68
            bold True
            outlines [(5, "#2A0008DD", 0, 0)]

    if monster_heal > 0:
        text "+[monster_heal] HP":
            at cb_damage_float
            xcenter 1585
            ycenter 520
            color "#66F2B4"
            size 56
            bold True
            outlines [(4, "#03251ADD", 0, 0)]
    elif mechanic_event == "colossus_armor_block":
        text "ARMOR BLOCK":
            at cb_result_pop
            xcenter 1490
            ycenter 500
            color "#FFD36D"
            size 43
            bold True
            outlines [(4, "#2A1D00DD", 0, 0)]
    elif mechanic_event == "colossus_armor_break":
        text "ARMOR BREAK!":
            at cb_result_pop
            xcenter 1490
            ycenter 520
            color "#59E6A8"
            size 45
            bold True
            outlines [(4, "#03251ADD", 0, 0)]

    frame:
        at cb_result_pop
        background Solid("#121B30F7")
        xpos 260
        ypos 650
        xsize 1400
        ysize 370
        padding (46, 28)

        vbox:
            spacing 12
            xfill True

            text "АСУУЛТЫН ҮР ДҮН":
                color "#F6F7FF"
                size 34
                bold True
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                vbox:
                    spacing 3
                    text "ЗӨВ" color "#59E6A8" size 23 bold True xalign 0.5
                    text "[correct_percentage]%" color "#FFFFFF" size 47 bold True xalign 0.5
                    text "[correct_count] хариулт · Мангас -[monster_damage] HP" color "#59E6A8" size 20 xalign 0.5

                vbox:
                    spacing 3
                    if no_answer_penalty:
                        text "ХАРИУЛТГҮЙ" color "#FF5F78" size 23 bold True xalign 0.5
                        text "MAX" color "#FFFFFF" size 47 bold True xalign 0.5
                        text "0 хариулт · Хот -[player_damage] HP" color "#FF5F78" size 20 xalign 0.5
                    else:
                        text "БУРУУ" color "#FF8296" size 23 bold True xalign 0.5
                        text "[wrong_percentage]%" color "#FFFFFF" size 47 bold True xalign 0.5
                        text "[wrong_count] хариулт · Баг -[player_damage] HP" color "#FF8296" size 20 xalign 0.5

            if no_answer_penalty:
                text "ХЭН Ч ХАРИУЛААГҮЙ · ХОТ MAX DAMAGE АВЛАА":
                    color "#FF5F78"
                    size 23
                    bold True
                    xalign 0.5
            elif mechanic_event == "devourer_heal" and monster_heal > 0:
                text "DEVOURER · +[monster_heal] HP НӨХӨВ":
                    color "#D57CFF"
                    size 22
                    bold True
                    xalign 0.5
            elif mechanic_event == "colossus_armor_block":
                text "COLOSSUS ARMOR · [monster_damage_blocked] DAMAGE ХААЛАА · COMBO [armor_combo]/[armor_combo_target]":
                    color "#FFD36D"
                    size 22
                    bold True
                    xalign 0.5
            elif mechanic_event == "colossus_armor_break":
                text "ARMOR BREAK! · COMBO [armor_combo]/[armor_combo_target]":
                    color "#59E6A8"
                    size 25
                    bold True
                    xalign 0.5
            elif mechanic_event == "void_glitch":
                text "VOID GLITCH · ЭНЭ ROUND-ЫН ХУГАЦАА -[duration_penalty] СЕК":
                    color "#D69CFF"
                    size 22
                    bold True
                    xalign 0.5

            text "Нийт хариулт: [total_answers]" style "cb_small_text" xalign 0.5

            text "[result_display_label] секундын дараа [next_part_text] руу автоматаар шилжинэ.":
                color "#8999FF"
                size 20
                xalign 0.5
                text_align 0.5


screen crowd_creators_round(question_number, question_total, expected_round_id=None, question_duration=15):
    modal True

    $ current_round = cb_battle.get("current_round") or {}
    $ guarded_round_id = expected_round_id or cb_round_guard_id

    add Solid("#070B14")

    # Серверийн хугацаа, хариултын төлөвийг шинэчилнэ.
    timer 0.25 repeat True action Function(cb_poll_round_action)

    # Бүгд хариулсан ЭСВЭЛ duration дууссан үед return хийнэ.
    if cb_round_can_finish(guarded_round_id):
        timer 0.10 action Return(True)
    
    frame:
        background Solid("#121B30F7")
        xalign 0.5
        yalign 0.5
        xsize 1500
        padding (60, 42)

        vbox:
            spacing 18
            xfill True

            text "CREATORS' QUESTION · [question_number]/[question_total]":
                color "#8999FF"
                size 24
                bold True
                xalign 0.5

            text "[cb_remaining_seconds] секунд":
                color "#FF899D"
                size 30
                bold True
                xalign 0.5

            text current_round.get("question", ""):
                color "#FFFFFF"
                size 38
                bold True
                text_align 0.5
                xalign 0.5

            # 1-р асуулт: role бүрийг 4 + 3 зурагтай карт болгоно.
            if question_number == 1:
                vbox:
                    spacing 12
                    xalign 0.5

                    for row_start in range(0, len(current_round.get("choices", [])), 4):
                        hbox:
                            spacing 16
                            xalign 0.5

                            for choice in current_round.get("choices", [])[row_start:row_start + 4]:
                                $ role_image = CB_ROLE_PREVIEW_DATA.get(choice)

                                frame:
                                    background Solid("#18233BF5")
                                    xsize 300
                                    ysize 230
                                    padding (10, 8)

                                    vbox:
                                        spacing 4
                                        xalign 0.5

                                        if role_image:
                                            add role_image:
                                                xysize (180, 180)
                                                xalign 0.5

                                        text choice:
                                            color "#F6F7FF"
                                            size 22
                                            bold True
                                            xalign 0.5
                                            text_align 0.5

            # 2-р асуулт: BG хавтасны cinematic бүрийг жижиг preview болгоно.
            elif question_number == 2:
                hbox:
                    spacing 18
                    xalign 0.5

                    for choice in current_round.get("choices", []):
                        $ preview_image = CB_WORLD_PREVIEW_DATA.get(choice)

                        frame:
                            background Solid("#18233BF5")
                            xsize 330
                            ysize 235
                            padding (14, 14)

                            vbox:
                                spacing 10
                                xalign 0.5

                                if preview_image:
                                    add preview_image:
                                        xysize (300, 169)
                                        xalign 0.5

                                text choice:
                                    color "#F6F7FF"
                                    size 23
                                    bold True
                                    xalign 0.5
                                    text_align 0.5

            # 3-р асуулт: location бүрийг 3 + 2 зурагтай карт болгоно.
            elif question_number == 3:
                vbox:
                    spacing 12
                    xalign 0.5

                    for row_start in range(0, len(current_round.get("choices", [])), 3):
                        hbox:
                            spacing 16
                            xalign 0.5

                            for choice in current_round.get("choices", [])[row_start:row_start + 3]:
                                $ location_image = CB_LOCATION_PREVIEW_DATA.get(choice)

                                frame:
                                    background Solid("#18233BF5")
                                    xsize 400
                                    ysize 255
                                    padding (8, 8)

                                    vbox:
                                        spacing 6
                                        xalign 0.5

                                        if location_image:
                                            add location_image:
                                                xysize (200, 200)
                                                xalign 0.5

                                        text choice:
                                            color "#F6F7FF"
                                            size 22
                                            bold True
                                            xalign 0.5
                                            text_align 0.5

            # 4-р асуулт: 7 Citizen зургийг 4 + 3 сонголтын карт болгоно.
            elif question_number == 4:
                vbox:
                    spacing 12
                    xalign 0.5

                    for row_start in range(0, len(current_round.get("choices", [])), 4):
                        hbox:
                            spacing 16
                            xalign 0.5

                            for choice in current_round.get("choices", [])[row_start:row_start + 4]:
                                $ citizen_preview = CB_CITIZEN_PREVIEW_DATA.get(choice) or {}
                                $ citizen_image = citizen_preview.get("image")
                                $ citizen_crop = citizen_preview.get("crop")

                                frame:
                                    background Solid("#18233BF5")
                                    xsize 330
                                    ysize 205
                                    padding (12, 10)

                                    vbox:
                                        spacing 7
                                        xalign 0.5

                                        if citizen_image:
                                            add citizen_image:
                                                crop citizen_crop
                                                xysize (230, 135)
                                                xalign 0.5

                                        text choice:
                                            color "#F6F7FF"
                                            size 21
                                            bold True
                                            xalign 0.5
                                            text_align 0.5

            # Бусад creators асуултын layout өөрчлөгдөхгүй.
            else:
                vbox:
                    spacing 12
                    xalign 0.5

                    for choice in current_round.get("choices", []):
                        text choice:
                            color "#D7DCEF"
                            size 28
                            xalign 0.5



screen crowd_creators_result(question, result):
    modal True
    default auto_seconds = CB_RESULT_DISPLAY_SECONDS

    $ latest_round = cb_battle.get("current_round") or {}
    $ latest_result = result or latest_round.get("result") or {}
    $ choices = question.get("choices", [])
    $ counts = latest_result.get("choice_counts", latest_round.get("choice_counts", []))
    $ total_answers = max(0, int(latest_result.get("total_answers", latest_round.get("total_answers", 0))))
    $ top_indices = latest_result.get("top_choice_indices", [])
    $ winner_labels = [choices[index] for index in top_indices if 0 <= index < len(choices)]
    $ winner_text = ", ".join(winner_labels)
    add Solid("#070B14")
    add Solid("#6F7CFF18")

    # Result-ийг дөрвөн секунд харуулаад дараагийн үйл явдал руу орно.
    timer 1.0 repeat True action If(
        auto_seconds > 1,
        SetScreenVariable("auto_seconds", auto_seconds - 1),
        Return(True)
    )

    frame:
        at cb_result_pop
        background Solid("#121B30F7")
        xalign 0.5
        yalign 0.5
        xsize 1400
        padding (65, 42)

        vbox:
            spacing 18
            xfill True

            text "САНАЛ АСУУЛГЫН ҮР ДҮН":
                style "cb_title_text"
                xalign 0.5

            text question.get("question", ""):
                color "#FFFFFF"
                size 32
                bold True
                text_align 0.5
                xalign 0.5

            vbox:
                spacing 12
                xfill True

                for index, choice in enumerate(choices):
                    $ count = counts[index] if index < len(counts) else 0
                    $ percentage = int(round(100.0 * count / total_answers)) if total_answers else 0

                    hbox:
                        spacing 18
                        xfill True

                        text choice:
                            color "#D7DCEF"
                            size 24
                            xsize 780

                        text "[count] · [percentage]%":
                            color "#8999FF"
                            size 24
                            bold True
                            xalign 1.0
                            xsize 360
                            text_align 1.0

            text "Нийт оролцогч: [total_answers] · Нийт санал: [total_answers]":
                style "cb_small_text"
                xalign 0.5

            if winner_text:
                text "Хамгийн олон санал: [winner_text]":
                    color "#59E6A8"
                    size 25
                    bold True
                    xalign 0.5

            text "[auto_seconds] секундын дараа автоматаар үргэлжилнэ.":
                color "#8999FF"
                size 23
                xalign 0.5
                text_align 0.5


screen crowd_battle_break(victory):
    modal True

    $ team_city_image = getattr(store, "cb_team_city_image", "cb_team_city_futuristic")
    $ city_attack = cb_city_attack_media()
    $ city_weapon_image = city_attack["weapon"]
    $ city_weapon_label = city_attack["label"]

    add Solid("#070B14")
    add Solid("#101A31") xysize (1920, 270)

    on "show" action Function(cb_prepare_battle_break, victory)
    on "hide" action Function(cb_stop_battle_break)
    timer CB_BREAK_START_DELAY action Function(cb_play_battle_break, victory)
    timer CB_BREAK_SCREEN_SECONDS action Return(True)

    vbox:
        xpos 90
        ypos 45
        xsize 760
        spacing 10
        text "ҮЗЭГЧДИЙН БАГ" style "cb_small_text"
        text "[cb_player_hp] / [cb_player_max_hp] HP":
            color "#7FF0BB"
            size 29
            bold True
        bar:
            value StaticValue(cb_player_hp, cb_player_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#38D99A")
            right_bar Solid("#24304A")

    vbox:
        xpos 1070
        ypos 45
        xsize 760
        spacing 10
        text "[cb_enemy_name]" style "cb_small_text" xalign 1.0
        text "[cb_monster_hp] / [cb_monster_max_hp] HP":
            color "#FF8296"
            size 29
            bold True
            xalign 1.0
        bar:
            value StaticValue(cb_monster_hp, cb_monster_max_hp)
            xsize 700
            ysize 28
            left_bar Solid("#FF5F78")
            right_bar Solid("#24304A")
            xalign 1.0

    # Нэг shared arena. Ялагдсан талын break movie зөвхөн өөрийн талд тоглоно.
    add Solid("#000000"):
        xpos 50
        ypos 270
        xsize 1820
        ysize 350

    add team_city_image:
        xysize (640, 358)
        xcenter 430
        ycenter 445

    if victory:
        # Хот ялсан тул зэвсэг нь үлдэж, мангас өөрийн die video-г тоглуулна.
        add city_weapon_image:
            at cb_city_weapon_idle
            xysize (310, 180)
            xcenter 590
            ycenter 520

        text city_weapon_label:
            color "#C7D4F5"
            size 16
            bold True
            xcenter 590
            ycenter 600
            outlines [(2, "#07101FDD", 0, 0)]

        add cb_enemy_idle_image:
            xysize (640, 358)
            xcenter 1490
            ycenter 445

        add Movie(channel="cb_break_movie", size=(640, 360)):
            xcenter 1490
            ycenter 445
    else:
        # Хот ялагдсан үед weapon-ийг огт зурахгүй. 0.30 секундын дараа
        # city break video эхлэх тул зэвсэг сүйрлээс түрүүлж алга болно.
        add Movie(channel="cb_break_movie", size=(640, 360)):
            xcenter 430
            ycenter 445

        add cb_enemy_idle_image:
            at cb_monster_idle
            xysize (640, 358)
            xcenter 1490
            ycenter 445

        add Movie(channel="cb_monster_movie", size=(640, 358)):
            xcenter 1490
            ycenter 445

    frame:
        background Solid("#121B30EE")
        xcenter 960
        ypos 650
        xsize 1400
        ysize 180
        padding (30, 24)

        vbox:
            xfill True
            spacing 10

            if victory:
                text "FINAL STRIKE · МАНГАС ЯЛАГДЛАА":
                    color "#59E6A8"
                    size 38
                    bold True
                    xalign 0.5
            else:
                text "WORLD FALLEN · ХОТ ЯЛАГДЛАА":
                    color "#FF8296"
                    size 38
                    bold True
                    xalign 0.5

            text "[cb_battle_end_reason]":
                style "cb_small_text"
                xalign 0.5


screen crowd_battle_ending(victory):
    modal True
    add Solid("#070B14")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        if victory:
            text "ЯЛАЛТ!" color "#59E6A8" size 100 bold True xalign 0.5
            text "Үзэгчдийн баг [cb_enemy_name]-г яллаа." style "cb_body_text" xalign 0.5
        else:
            text "ЯЛАГДАЛ" color "#FF8296" size 100 bold True xalign 0.5
            text "Ертөнцийг хамгаалж чадсангүй." style "cb_body_text" xalign 0.5

        text "[cb_battle_end_reason]":
            style "cb_small_text"
            xalign 0.5

        hbox:
            spacing 20
            xalign 0.5
            textbutton "ДАХИН ТОГЛОХ":
                style "cb_button"
                action Return("restart")
            textbutton "ГАРАХ":
                style "cb_button"
                action Return("quit")


screen crowd_connection_error(message):
    modal True
    add Solid("#070B14EE")

    frame:
        background Solid("#191426F7")
        xalign 0.5
        yalign 0.5
        xsize 1050
        padding (60, 45)

        vbox:
            spacing 24
            text "ХОЛБОЛТЫН АЛДАА" color "#FF8296" size 45 bold True xalign 0.5
            text message style "cb_body_text" text_align 0.5 xalign 0.5
            hbox:
                spacing 20
                xalign 0.5
                textbutton "ДАХИН ОРОЛДОХ":
                    style "cb_button"
                    action Return("retry")
