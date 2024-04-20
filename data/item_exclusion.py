# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/metadata/item_exclusion.py

"""
This file offers lists of items related to the removal of useless items
during certain randomizer settings.
"""

exclude_due_to_settings = {
    "startwith_bluehouse_open": [
        "Odd Key"
    ],
    "startwith_forest_open": [
        "Forest Pass"
    ],
    "magical_seeds_required": {
        0: [
            "Magical Seed",
            "Magical Seed",
            "Magical Seed",
            "Magical Seed",
        ],
        1: [
            "Magical Seed",
            "Magical Seed",
            "Magical Seed",
        ],
        2: [
            "Magical Seed",
            "Magical Seed",
        ],
        3: [
            "Magical Seed",
        ],
    },
    "shorten_bowsers_castle": [
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Bowser Castle Key",
        "Bowser Castle Key",
    ],
    "boss_rush": [
        "Prison Key",
        "Prison Key",
    ],
    "always_speedyspin": [
        "Speedy Spin",
    ],
    "always_ispy": [
        "I Spy",
    ],
    "always_peekaboo": [
        "Peekaboo",
    ],
    "do_randomize_dojo": [
        "First Degree Card",
        "Second Degree Card",
        "Third Degree Card",
        "Fourth Degree Card",
        "Diploma",
    ],
    "do_progressive_badges": [
        "Mini Smash Charge",
        "Smash Charge",
        "Super Smash Charge",
        "Mini Jump Charge",
        "Jump Charge",
        "Super Jump Charge",
        "Power Jump",
        "Super Jump",
        "Mega Jump",
        "Power Smash",
        "Super Smash",
        "Mega Smash",
        "Quake Hammer",
        "Power Quake",
        "Mega Quake"
    ],
    "partner_upgrade_shuffle": [
        "Ultra Stone",
        "Nothing",  # Goombario 1
        "Nothing",  # Goombario 2
        "Nothing",  # Kooper 1
        "Nothing",  # Kooper 2
        "Nothing",  # Bombette 1
        "Nothing",  # Bombette 2
        "Nothing",  # Parakarry 1
        "Nothing",  # Parakarry 2
        "Nothing",  # Watt 1
        "Nothing",  # Watt 2
        "Nothing",  # Sushie 1
        "Nothing",  # Sushie 2
        "Nothing",  # Lakilester 1
        "Nothing",  # Lakilester 2
        "Nothing",  # Bow 1
        "Nothing",  # Bow 2
    ]
}

exclude_from_taycet_placement = [
    "Koopasta",  # 0x0B5
    "Cake",  # 0x0C1
    "Mistake",  # 0x0C2
    "Koopa Tea",  # 0x0C3
    "Kooky Cookie",  # 0x0D3
    "Nutty Cake",  # 0x0D6
]
