# get the address for the given option using its key type (0xAF), area, map, and index


#    Name                        id    area     map    index   default val
rom_option_table = {
    "StartingMap":              (1,      0,      0,      0,     65796),
    "StartingCoins":            (2,      0,      0,      1,     50),
    "StartingLevel":            (3,      0,      0,      2,     1),
    "StartingMaxHP":            (4,      0,      0,      3,     10),
    "StartingMaxFP":            (5,      0,      0,      4,     5),
    "StartingMaxBP":            (6,      0,      0,      5,     3),
    "StartingItem0":            (7,      0,      0,      16,    0),
    "StartingItem1":            (8,      0,      0,      17,    0),
    "StartingItem2":            (9,      0,      0,      18,    0),
    "StartingItem3":            (10,     0,      0,      19,    0),
    "StartingItem4":            (11,     0,      0,      20,    0),
    "StartingItem5":            (12,     0,      0,      21,    0),
    "StartingItem6":            (13,     0,      0,      22,    0),
    "StartingItem7":            (14,     0,      0,      23,    0),
    "StartingItem8":            (15,     0,      0,      24,    0),
    "StartingItem9":            (16,     0,      0,      25,    0),
    "StartingItemA":            (17,     0,      0,      26,    0),
    "StartingItemB":            (18,     0,      0,      27,    0),
    "StartingItemC":            (19,     0,      0,      28,    0),
    "StartingItemD":            (20,     0,      0,      29,    0),
    "StartingItemE":            (21,     0,      0,      30,    0),
    "StartingItemF":            (22,     0,      0,      31,    0),
    "StartingStarPower":        (23,     0,      0,      32,    0),
    "PartnerUpgradeShuffle":    (24,     0,      0,      78,    0),
    "PartnersAlwaysUsable":     (25,     0,      0,      79,    1),
    "StartWithGoombario":       (26,     0,      0,      64,    1),
    "StartWithKooper":          (27,     0,      0,      65,    0),
    "StartWithBombette":        (28,     0,      0,      66,    0),
    "StartWithParakarry":       (29,     0,      0,      67,    0),
    "StartWithBow":             (30,     0,      0,      68,    0),
    "StartWithWatt":            (31,     0,      0,      69,    0),
    "StartWithSushie":          (32,     0,      0,      70,    0),
    "StartWithLakilester":      (33,     0,      0,      71,    0),
    "StartingBoots":            (34,     0,      0,      72,    0),
    "StartingHammer":           (35,     0,      0,      73,    0),
    "MagicalSeedsRequired":     (36,     1,      0,      0,     4),
    "PrologueOpen":             (37,     1,      0,      1,     0),
    "BlueHouseOpen":            (38,     1,      0,      2,     0),
    "MtRuggedOpen":             (39,     1,      0,      3,     0),
    "ForeverForestOpen":        (40,     1,      0,      4,     1),
    "ToyboxOpen":               (41,     1,      0,      5,     0),
    "WhaleOpen":                (42,     1,      0,      6,     0),
    "Ch7BridgeVisible":         (43,     1,      0,      7,     1),
    "ShuffleItems":             (44,     1,      0,      8,     1),
    "IncludeShops":             (45,     1,      0,      9,     1),
    "IncludePanels":            (46,     1,      0,      10,    1),
    "ShuffleDungeonRooms":      (47,     1,      0,      11,    0),
    "ShuffleDungeonEntrances":  (48,     1,      0,      12,    0),
    "ShuffleEntrancesByAll":    (49,     1,      0,      13,    0),
    "MatchEntranceTypes":       (50,     1,      0,      14,    1),
    "PeachCastleReturnPipe":    (51,     1,      0,      15,    1),
    "CookWithoutFryingPan":     (52,     1,      0,      16,    0),
    "RandomFormations":         (53,     1,      0,      17,    1),
    "GearShuffleMode":          (54,     1,      0,      18,    0),
    "BossShuffleMode":          (55,     1,      0,      19,    0),
    "SeedGoal":                 (56,     1,      0,      20,    0),
    "StarWaySpiritsNeededCnt":  (57,     1,      0,      21,    7),
    "StarWaySpiritsNeededEnc":  (58,     1,      0,      22,    255),
    "StarWayPowerStarsNeeded":  (59,     1,      0,      23,    0),
    "StarBeamSpiritsNeeded":    (60,     1,      0,      24,    0),
    "StarBeamPowerStarsNeeded": (61,     1,      0,      25,    0),
    "StarBeamArea":             (62,     1,      0,      26,    5),
    "StarHuntTotal":            (63,     1,      0,      27,    0),
    "SkipQuiz":                 (64,     1,      1,      0,     0),
    "QuizmoAlwaysAppears":      (65,     1,      1,      1,     0),
    "CapEnemyXP":               (66,     2,      0,      0,     1),
    "XPMultiplier":             (67,     2,      0,      1,     2),
    "DoubleDamage":             (68,     2,      0,      2,     0),
    "QuadrupleDamage":          (69,     2,      0,      3,     0),
    "OHKO":                     (70,     2,      0,      4,     0),
    "NoSaveBlocks":             (71,     2,      0,      5,     0),
    "NoHeartBlocks":            (72,     2,      0,      6,     0),
    "NoHealingItems":           (73,     2,      0,      7,     0),
    "AllowPhysicsGlitches":     (74,     2,      0,      8,     0),
    "ProgressiveScaling":       (75,     2,      0,      9,     1),
    "ChallengeMode":            (76,     2,      0,      10,    0),
    "BadgeSynergy":             (77,     2,      0,      11,    0),
    "DropStarPoints":           (78,     2,      0,      12,    1),
    "MirrorMode":               (79,     2,      0,      13,    0),
    "HiddenBlockMode":          (80,     4,      0,      1,     1),
    "BlocksMatchContent":       (81,     4,      0,      2,     1),
    "CutsceneMode":             (82,     4,      0,      3,     1),
    "AlwaysSpeedySpin":         (83,     4,      0,      4,     1),
    "AlwaysISpy":               (84,     4,      0,      5,     0),
    "AlwaysPeekaboo":           (85,     4,      0,      6,     1),
    "SkipEpilogue":             (86,     4,      0,      7,     0),
    "BowsersCastleMode":        (87,     4,      0,      8,     0),
    "FoliageItemHints":         (88,     4,      0,      9,     1),
    "HiddenPanelVisibility":    (89,     4,      0,      10,    0),
    "FastTextSkip":             (90,     4,      0,      16,    0),
    "EnabledCheckBits":         (91,     4,      0,      32,    65535),
    "EnabledShopBits":          (92,     4,      0,      33,    65535),
    "PlandomizerActive":        (93,     4,      0,      34,    0),
    "PawnsEnabled":             (94,     5,      0,      0,     1),
    "MultiworldEnabled":        (95,     5,      0,      1,     0),
    "ColorMode":                (96,     6,      5,      0,     0),
    "Box5ColorA":               (97,     6,      5,      1,     3957749759),
    "Box5ColorB":               (98,     6,      5,      2,     2388272639),
    "CoinColor":                (99,     6,      5,      3,     0),
    "RomanNumerals":            (100,     6,      5,      4,     0),
    "RandomText":               (101,    6,      5,      5,     0),
    "Widescreen":               (102,    6,      5,      6,     0),
    "RandomPitch":              (103,    7,      0,      0,     0),
    "MuteDangerBeeps":          (104,    7,      0,      1,     0),
    "RandomChoice":             (105,    10,     0,      0,     0),
    "ItemChoiceA":              (106,    10,     0,      1,     138),
    "ItemChoiceB":              (107,    10,     0,      2,     140),
    "ItemChoiceC":              (108,    10,     0,      3,     128),
    "ItemChoiceD":              (109,    10,     0,      4,     136),
    "ItemChoiceE":              (110,    10,     0,      5,     154),
    "ItemChoiceF":              (111,    10,     0,      6,     130),
    "ItemChoiceG":              (112,    10,     0,      7,     133),
    "RandomQuiz":               (113,    3,      7,      128,   1)
}

ap_to_rom_option_table = {
    # General
    "BlocksMatchContent": "",  # always true
    "HiddenBlockMode": "hidden_block_mode",
    "AllowPhysicsGlitches": "",
    "BadgeSynergy": "badge_synergy",

    # QOL
    "AlwaysSpeedySpin": "always_speedy_spin",
    "AlwaysISpy": "always_ispy",
    "AlwaysPeekaboo": "always_peekaboo",
    "CutsceneMode": "cutscene_mode",
    "FastTextSkip": "",
    "SkipEpilogue": "skip_epilogue",
    "PeachCastleReturnPipe": "",
    "FoliageItemHints": "foliage_item_hints",
    "HiddenPanelVisibility": "visible_hidden_panels",
    "MuteDangerBeeps": "mute_danger_beeps",

    # Difficulty and enemies
    "ProgressiveScaling": "",
    "ChallengeMode": "",  # NYI, always false
    "CapEnemyXP": "cap_enemy_xp",
    "XPMultiplier": "enemy_xp_multiplier",
    "DoubleDamage": "",  # damage multiplier == 2
    "QuadrupleDamage": "",  # damage multiplier == 4
    "OHKO": "one_hit_ko",
    "NoSaveBlocks": "no_save_blocks",
    "NoHeartBlocks": "no_heart_blocks",
    "NoHealingItems": "no_healing_items",
    "DropStarPoints": "drop_star_points",
    "RandomFormations": "formation_shuffle",

    # Item Placement
    "ShuffleItems": "",
    "IncludeShops": "include_shops",
    "IncludePanels": "shuffle_hidden_panels",

    # Item Pool Modification
    "GearShuffleMode": "gear_shuffle_mode",
    "PartnerUpgradeShuffle": "partner_upgrades",

    # Map Check Tracker (auto-calculated bits for trackers to use)
    "EnabledCheckBits": "",
    "EnabledShopBits": "",
    "PlandomizerActive": "",

    # Item Misc
    "CookWithoutFryingPan": "cook_without_frying_pan",
    "RandomChoice": "mystery_shuffle",
    "ItemChoiceA": "",
    "ItemChoiceB": "",
    "ItemChoiceC": "",
    "ItemChoiceD": "",
    "ItemChoiceE": "",
    "ItemChoiceF": "",
    "ItemChoiceG": "",

    # Starting setup
    "StartingMap": "",
    "StartingLevel": "",  # calculated based on the next 3
    "StartingMaxHP": "starting_hp",
    "StartingMaxFP": "starting_fp",
    "StartingMaxBP": "starting_bp",
    "StartingStarPower": "starting_sp",
    "StartingBoots": "",
    "StartingHammer": "",
    "StartingCoins": "starting_coins",

    "StartingItem0": "",  # not currently doable?
    "StartingItem1": "",
    "StartingItem2": "",
    "StartingItem3": "",
    "StartingItem4": "",
    "StartingItem5": "",
    "StartingItem6": "",
    "StartingItem7": "",
    "StartingItem8": "",
    "StartingItem9": "",
    "StartingItemA": "",
    "StartingItemB": "",
    "StartingItemC": "",
    "StartingItemD": "",
    "StartingItemE": "",
    "StartingItemF": "",

    # Partners
    "StartWithGoombario": "start_with_goombario",
    "StartWithKooper": "start_with_kooper",
    "StartWithBombette": "start_with_bombette",
    "StartWithParakarry": "start_with_parakarry",
    "StartWithBow": "start_with_bow",
    "StartWithWatt": "start_with_watt",
    "StartWithSushie": "start_with_sushie",
    "StartWithLakilester": "start_with_lakilester",

    "PartnersAlwaysUsable": "partners_always_usable",

    # Pre-opened areas
    "MagicalSeedsRequired": "magical_seeds",
    "PrologueOpen": "open_prologue",
    "BlueHouseOpen": "open_blue_house",
    "MtRuggedOpen": "open_mt_rugged",
    "ForeverForestOpen": "open_forest",
    "ToyboxOpen": "open_toybox",
    "WhaleOpen": "open_whale",
    "Ch7BridgeVisible": "ch7_bridge_visible",

    # Goal Settings
    "SeedGoal": "seed_goal",
    "StarWaySpiritsNeededCnt": "star_way_spirits",
    "StarWaySpiritsNeededEnc": "",
    "StarWayPowerStarsNeeded": "star_way_power_stars",
    "StarBeamSpiritsNeeded": "star_beam_spirits",
    "StarBeamPowerStarsNeeded": "star_beam_power_stars",
    "BowsersCastleMode": "bowser_castle_mode",
    "StarHuntTotal": "total_power_stars",
    "StarBeamArea": "",

    # Entrance Shuffle
    "ShuffleDungeonRooms": "",  # NYI, always false
    "ShuffleDungeonEntrances": "shuffle_dungeon_entrances",
    "ShuffleEntrancesByAll": "",  # NYI, always false
    "MatchEntranceTypes": "",  # NYI, always true
    "BossShuffleMode": "boss_shuffle",

    # Quizmo Quizzes
    "RandomQuiz": "",  # always true
    "QuizmoAlwaysAppears": "quizmo_always_appears",
    "SkipQuiz": "skip_quiz",

    # Multiplayer
    "PawnsEnabled": "",
    "MultiworldEnabled": "",

    # Cosmetics
    "ColorMode": "",
    "Box5ColorA": "",
    "Box5ColorB": "",
    "CoinColor": "coin_palette",

    # Joke options
    "RomanNumerals": "roman_numerals",
    "RandomText": "random_text",
    "RandomPitch": "random_pitch",
    "MirrorMode": "mirror_mode",

    "Widescreen": "",
}
