define N = Character(
    _("Nova"),
    color="#a6f9ff",
    callback=cb_nova_portrait_callback,
)
define Monster = DynamicCharacter(
    "cb_enemy_name",
    color="#ff6677",
    callback=cb_monster_portrait_callback,
)
define C = Character(_("Creators"), color="#6aff7e")
