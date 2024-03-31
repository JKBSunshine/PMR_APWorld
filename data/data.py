# https://github.com/icebound777/PMR-SeedGenerator/blob/main/docs/RAMLocations.md

from ..data.ItemList import item_table


# RDRAM Addresses, leave off the initial 80
MODE_ADDRESS = 0x0A08F1  # Game Mode, checks if you're in a state to send/receive stuff
UIR_START_ADDRESS = 0x356B00  # Unique Item Registry
PD_START_ADDRESS = 0x10F290  # Player Data

# ModByte Data
MB_START_ADDRESS = 0x356000
ITM_RCV_SEQ = MB_START_ADDRESS + 0x134  # take 0x134 and 0x135 together as u16

KEY_RECV_BUFFER = 0x358400  # takes item IDs to add to Mario's inventory as u16

# Game Flags
GF_START_ADDRESS = 0x0DBC70
GF_END_ADDRESS = 0x0DBD77

# Mod Flags
MF_START_ADDRESS = 0x357000
MF_END_ADDRESS = 0x357228
GOAL_FLAG = 0x1100


# ROM Addresses
MAGIC_VALUE = b'PMDB'
TABLE_ADDRESS = 0x1D00000
AUTH_ADDRESS = 0x1D00000 - 16

GAME_MODE_WORLD = 4


def get_uir_address(name):
    item_id = item_table[name][2]
    return hex(UIR_START_ADDRESS + item_id)


def get_pd_address(name):
    return hex(PD_START_ADDRESS + name)


def get_mb_address(name):
    return hex(MB_START_ADDRESS + name)


def get_flag_value(flag_type, flag_id, bytes) -> bool:
    flag_offset = int(flag_id / 32) * 4
    flag_remainder = flag_id % 32

    hex_index = (7 - int(flag_remainder / 4)) % 2
    byte_index = 3 - int(flag_remainder / 8)
    value = 2 ** (flag_remainder % 8)

    match flag_type:
        case "GF":
            byte_start = flag_offset + byte_index
        case "MF":
            byte_start = flag_offset + byte_index

    for index, byte in enumerate(bytes):
        if index == byte_start:
            return byte & value == value

    return False

    # if addressvalue & value = value
    # return bytes[byte_start] & value == value
    # return bytes[byte_start] & value == value


# Location (spoiler log name)                    | Flag type and ID
# -----------------------------------------------+---------------------
checks_table = {
    "Forest Clearing Hidden Panel":                           ("GF",   0x056),

    "Goomba Village Bush Bottom Right":                       ("GF",   0x02F),
    "Goomba Village Goompa Koopa Koot Favor":                 ("GF",   0x064),
    "Goomba Village Goompa Gift":                             ("MF",   0x1000),
    "Goomba Village Goombaria Dolly Reward":                  ("MF",   0x1001),
    "Goomba Village Goompa Letter Reward":                    ("MF",   0x1002),
    "Goomba Village Goompapa Letter Reward 1":                ("MF",   0x1003),
    "Goomba Village Goompapa Letter Reward 2":                ("MF",   0x1004),
    "Goomba Village On The Balcony":                          ("GF",   0x02E),
    "Goomba Village Goombario Partner":                       ("MF",   0x1006),
    "Goomba Village Goomnut Tree":                            ("MF",   0x1005),

    "Behind the Village On Ledge":                            ("GF",   0x04A),
    "Behind the Village In Tree":                             ("GF",   0x049),

    "Bottom of the Cliff Hidden Panel":                       ("GF",   0x058),
    "Bottom of the Cliff Above Stone Block":                  ("GF",   0x034),
    "Bottom of the Cliff Floating Coin 1":                    ("GF",   0x038),
    "Bottom of the Cliff Floating Coin 2":                    ("GF",   0x039),
    "Bottom of the Cliff Floating Coin 3":                    ("GF",   0x03A),
    "Bottom of the Cliff Floating Coin 4":                    ("GF",   0x03B),
    "Bottom of the Cliff Upper Ledge":                        ("GF",   0x031),
    "Bottom of the Cliff In Tree":                            ("GF",   0x035),
    "Bottom of the Cliff Block On Ground":                    ("GF",   0x032),

    "Jr. Troopa's Playground Bush Right":                      ("GF",   0x03E),
    "Jr. Troopa's Playground Bush Bottom Right":               ("GF",   0x03F),
    "Jr. Troopa's Playground Bush Top 1":                      ("GF",   0x040),
    "Jr. Troopa's Playground Bush Top 2":                      ("GF",   0x041),
    "Jr. Troopa's Playground Bush Center":                     ("GF",   0x042),
    "Jr. Troopa's Playground Bush Top Left":                   ("GF",   0x043),
    "Jr. Troopa's Playground In Hammer Bush":                  ("MF",   0x1007),
    "Jr. Troopa's Playground In MultiCoinBlock":               ("GF",   0x046),
    "Jr. Troopa's Playground In Tree Left":                    ("GF",   0x03C),
    "Jr. Troopa's Playground In Tree Top":                     ("GF",   0x03D),
    "Jr. Troopa's Playground In Tree Right":                   ("GF",   0x01E),

    "Goomba Road 1 Yellow Block Left":                        ("GF",   0x04D),
    "Goomba Road 1 Yellow Block Right":                       ("GF",   0x04E),

    "Goomba Road 2 On the Sign":                              ("GF",   0x04F),
    "Goomba Road 2 Red Block":                                ("GF",   0x050),

    "Goomba King's Castle Hidden Panel":                       ("GF",   0x05A),
    "Goomba King's Castle In Tree Left Of Fortress":           ("GF",   0x052),
    "Goomba King's Castle In Tree Right Of Cliff":             ("GF",   0x053),
    "Goomba King's Castle Hidden Yellow Block":                ("GF",   0x051),

    "Toad Town Entrance Chest On Roof":                       ("GF",   0x054),
    "Toad Town Entrance Yellow Block":                        ("GF",   0x055),

    "Mario's House Luigi Koopa Koot Favor":                    ("GF",   0x063),

    # Toad Town

    "Gate District Dojo: Chan":                               ("MF",   0x100B),
    "Gate District Dojo: Lee":                                ("MF",   0x100C),
    "Gate District Dojo: Master 1":                           ("MF",   0x100D),
    "Gate District Dojo: Master 2":                           ("MF",   0x100E),
    "Gate District Dojo: Master 3":                           ("MF",   0x100F),
    "Gate District Russ T. Dictionary Reward":                ("GF",   0x0F4),
    "Gate District Russ T. Letter Reward":                    ("MF",   0x1008),
    "Gate District Miss T. Letter Reward":                    ("MF",   0x1009),
    "Gate District Radio Trade Event 1 Reward":               ("MF",   0x100A),
    "Gate District Hidden Panel":                             ("GF",   0x127),
    "Gate District Sushie Island":                            ("GF",   0x12D),
    "Gate District Shop Item 1":                              ("MF",   0x1010),
    "Gate District Shop Item 2":                              ("MF",   0x1011),
    "Gate District Shop Item 3":                              ("MF",   0x1012),
    "Gate District Shop Item 4":                              ("MF",   0x1013),
    "Gate District Shop Item 5":                              ("MF",   0x1014),
    "Gate District Shop Item 6":                              ("MF",   0x1015),

    "Plaza District Rowf's Calculator Reward":                 ("MF",   0x1016),
    "Plaza District Postmaster MailBag Reward":               ("GF",   0x10A),
    "Plaza District Merlon Letter Reward":                    ("MF",   0x1017),
    "Plaza District Minh T. Letter Reward":                   ("MF",   0x1018),
    "Plaza District Merlon House Stomping":                   ("GF",   0x0FF),
    "Plaza District Rowf's Shop Set 1 - 1":                    ("GF",   0x680),
    "Plaza District Rowf's Shop Set 1 - 2":                    ("GF",   0x681),
    "Plaza District Rowf's Shop Set 1 - 3":                    ("GF",   0x682),
    "Plaza District Rowf's Shop Set 1 - 4":                    ("GF",   0x683),
    "Plaza District Rowf's Shop Set 2 - 1":                    ("GF",   0x684),
    "Plaza District Rowf's Shop Set 2 - 2":                    ("GF",   0x685),
    "Plaza District Rowf's Shop Set 2 - 3":                    ("GF",   0x686),
    "Plaza District Rowf's Shop Set 3 - 1":                    ("GF",   0x687),
    "Plaza District Rowf's Shop Set 3 - 2":                    ("GF",   0x688),
    "Plaza District Rowf's Shop Set 3 - 3":                    ("GF",   0x689),
    "Plaza District Rowf's Shop Set 4 - 1":                    ("GF",   0x68A),
    "Plaza District Rowf's Shop Set 4 - 2":                    ("GF",   0x68B),
    "Plaza District Rowf's Shop Set 4 - 3":                    ("GF",   0x68C),
    "Plaza District Rowf's Shop Set 5 - 1":                    ("GF",   0x68D),
    "Plaza District Rowf's Shop Set 5 - 2":                    ("GF",   0x68E),
    "Plaza District Rowf's Shop Set 5 - 3":                    ("GF",   0x68F),
    "Plaza District In Tree":                                 ("GF",   0x12E),

    "Southern District Bub-ulb Gift":                         ("GF",   0x11B),
    "Southern District Tayce T. Frying Pan Reward":           ("MF",   0x1019),
    "Southern District Fice T. Letter Reward":                ("MF",   0x101A),
    "Southern District Fice T. Forest Pass":                  ("MF",   0x10AE),
    "Southern District Hidden Panel":                         ("GF",   0x129),
    "Southern District Inside Blue House":                    ("GF",   0x084),

    "Station District Dane T. Letter Reward 1":               ("MF",   0x101B),
    "Station District Dane T. Letter Reward 2":               ("MF",   0x101C),
    "Station District Hidden Panel":                          ("GF",   0x12A),

    "Residental District Storeroom Item 1":                   ("GF",   0x12F),
    "Residental District Storeroom Item 2":                   ("GF",   0x130),
    "Residental District Storeroom Item 3":                   ("GF",   0x121),
    "Residental District Storeroom Item 4":                   ("GF",   0x131),
    "Residental District Shop Item 1":                        ("MF",   0x101D),
    "Residental District Shop Item 2":                        ("MF",   0x101E),
    "Residental District Shop Item 3":                        ("MF",   0x101F),
    "Residental District Shop Item 4":                        ("MF",   0x1020),
    "Residental District Shop Item 5":                        ("MF",   0x1021),
    "Residental District Shop Item 6":                        ("MF",   0x1022),

    "Port District Poet Gift":                                ("GF",   0x125),
    "Port District Poet Melody Reward":                       ("GF",   0x126),
    "Port District Fishmael Letter Reward":                   ("MF",   0x1023),
    "Port District Radio Trade Event 3 Reward":               ("MF",   0x1024),
    "Port District Hidden Panel":                             ("GF",   0x12C),
    "Port District In MultiCoinBlock":                        ("GF",   0x132),

    # Toad Town Tunnels

    "Hall to Blooper 1 (B1) Hidden Block":                    ("GF",   0x198),
    "Hall to Blooper 1 (B1) In MultiCoinBlock":               ("GF",   0x199),

    "Blooper Boss 1 (B1) Blooper Fight Reward":               ("GF",   0x18F),

    "Short Elevator Room (B1) Yellow Block Center":           ("GF",   0x190),
    "Short Elevator Room (B1) Yellow Block Left":             ("GF",   0x191),
    "Short Elevator Room (B1) Yellow Block Right":            ("GF",   0x192),

    "Spring Room (B2) Chest On Ledge":                        ("GF",   0x193),

    "Elevator Attic Room (B2) On Parakarry Ledge":            ("GF",   0x194),
    "Elevator Attic Room (B2) In SuperBlock":                 ("GF",   0x1B1),

    "Metal Block Room (B3) In SuperBlock":                    ("GF",   0x1B3),

    "Blue Pushblock Room (B2) Hidden Block Left":             ("GF",   0x195),
    "Blue Pushblock Room (B2) Hidden Block Center":           ("GF",   0x196),
    "Blue Pushblock Room (B2) Hidden Block Right":            ("GF",   0x197),
    "Blue Pushblock Room (B2) In SuperBlock":                 ("GF",   0x1B2),

    "Room with Spikes (B2) Yellow Block":                     ("GF",   0x19A),

    "Winding Path (Spiny Room) Hidden Block Center":          ("GF",   0x1A0),
    "Winding Path (Spiny Room) Hidden Block Right":           ("GF",   0x1A1),
    "Winding Path (Spiny Room) Hidden Block Left":            ("GF",   0x1A2),
    "Winding Path (Spiny Room) Yellow Block":                 ("GF",   0x1A3),

    "Hall to Ultra Boots (B3) Hidden Block":                  ("GF",   0x1A4),
    "Hall to Ultra Boots (B3) Yellow Block Left":             ("GF",   0x1A5),
    "Hall to Ultra Boots (B3) Yellow Block Right":            ("GF",   0x1A6),

    "Ultra Boots Room (B3) In Big Chest":                     ("GF",   0x1A7),

    "Bridge to Shiver City (B2) Yellow Block 1":              ("GF",   0x19B),
    "Bridge to Shiver City (B2) Yellow Block 2":              ("GF",   0x19C),
    "Bridge to Shiver City (B2) Yellow Block 3":              ("GF",   0x19D),
    "Bridge to Shiver City (B2) Yellow Block 4":              ("GF",   0x19E),
    "Bridge to Shiver City (B2) Yellow Block 5":              ("GF",   0x19F),

    "Frozen Room (B3) In SuperBlock":                         ("GF",   0x1B4),

    "Rip Cheato's Home (B3) Rip Cheato Offer 1":               ("MF",   0x102C),
    "Rip Cheato's Home (B3) Rip Cheato Offer 2":               ("MF",   0x102D),
    "Rip Cheato's Home (B3) Rip Cheato Offer 3":               ("MF",   0x102E),
    "Rip Cheato's Home (B3) Rip Cheato Offer 4":               ("MF",   0x102F),
    "Rip Cheato's Home (B3) Rip Cheato Offer 5":               ("MF",   0x1030),
    "Rip Cheato's Home (B3) Rip Cheato Offer 6":               ("MF",   0x1031),
    "Rip Cheato's Home (B3) Rip Cheato Offer 7":               ("MF",   0x1032),
    "Rip Cheato's Home (B3) Rip Cheato Offer 8":               ("MF",   0x1033),
    "Rip Cheato's Home (B3) Rip Cheato Offer 9":               ("MF",   0x1034),
    "Rip Cheato's Home (B3) Rip Cheato Offer 10":              ("MF",   0x1035),
    "Rip Cheato's Home (B3) Rip Cheato Offer 11":              ("MF",   0x1036),

    "Under the Toad Town Pond In SuperBlock":                 ("GF",   0x1B5),

    # Shooting Star Summit

    "Shooting Star Path Hidden Panel":                        ("GF",   0x21A),

    "Merluvlee's House Merluvlee Koopa Koot Favor":            ("GF",   0x219),
    "Merluvlee's House Merlow Letter Reward":                  ("MF",   0x102B),
    "Merluvlee's House Hidden Panel":                          ("GF",   0x21C),
    "Merluvlee's House Merlow's Badges 1":                      ("GF",   0x6EB),
    "Merluvlee's House Merlow's Badges 2":                      ("GF",   0x6EC),
    "Merluvlee's House Merlow's Badges 3":                      ("GF",   0x6ED),
    "Merluvlee's House Merlow's Badges 4":                      ("GF",   0x6EE),
    "Merluvlee's House Merlow's Badges 5":                      ("GF",   0x6EF),
    "Merluvlee's House Merlow's Badges 6":                      ("GF",   0x6F0),
    "Merluvlee's House Merlow's Badges 7":                      ("GF",   0x6F1),
    "Merluvlee's House Merlow's Badges 8":                      ("GF",   0x6F2),
    "Merluvlee's House Merlow's Badges 9":                      ("GF",   0x6F3),
    "Merluvlee's House Merlow's Badges 10":                     ("GF",   0x6F4),
    "Merluvlee's House Merlow's Badges 11":                     ("GF",   0x6F5),
    "Merluvlee's House Merlow's Badges 12":                     ("GF",   0x6F6),
    "Merluvlee's House Merlow's Badges 13":                     ("GF",   0x6F7),
    "Merluvlee's House Merlow's Badges 14":                     ("GF",   0x6F8),
    "Merluvlee's House Merlow's Badges 15":                     ("GF",   0x6F9),
    "Merluvlee's House Merlow's Rewards 1":                     ("MF",   0x10A8),
    "Merluvlee's House Merlow's Rewards 2":                     ("MF",   0x10A9),
    "Merluvlee's House Merlow's Rewards 3":                     ("MF",   0x10AA),
    "Merluvlee's House Merlow's Rewards 4":                     ("MF",   0x10AB),
    "Merluvlee's House Merlow's Rewards 5":                     ("MF",   0x10AC),
    "Merluvlee's House Merlow's Rewards 6":                     ("MF",   0x10AD),

    "Shooting Star Summit Hidden Panel":                      ("GF",   0x21B),
    "Shooting Star Summit Behind The Summit":                 ("GF",   0x220),

    "Star Haven Shop Item 1":                                 ("MF",   0x1025),
    "Star Haven Shop Item 2":                                 ("MF",   0x1026),
    "Star Haven Shop Item 3":                                 ("MF",   0x1027),
    "Star Haven Shop Item 4":                                 ("MF",   0x1028),
    "Star Haven Shop Item 5":                                 ("MF",   0x1029),
    "Star Haven Shop Item 6":                                 ("MF",   0x102A),

    # Koopa Region

    "Pleasant Path Entry Red Block Center":                   ("GF",   0x253),
    "Pleasant Path Entry Yellow Block Left":                  ("GF",   0x252),
    "Pleasant Path Entry Yellow Block Right":                 ("GF",   0x254),

    "Pleasant Path Bridge Kooper Island":                     ("GF",   0x244),
    "Pleasant Path Bridge Behind Fence":                      ("GF",   0x267),
    "Pleasant Path Bridge In MultiCoinBlock":                 ("GF",   0x258),
    "Pleasant Path Bridge Yellow Block":                      ("GF",   0x255),

    "Pleasant Crossroads Hidden Panel":                       ("GF",   0x260),
    "Pleasant Crossroads Behind Peg":                         ("GF",   0x268),
    "Pleasant Crossroads Brick Block Puzzle":                 ("GF",   0x256),

    "Path to Fortress 1 Hidden Panel":                        ("GF",   0x261),
    "Path to Fortress 1 Hidden Block":                        ("GF",   0x257),
    "Path to Fortress 1 X On Ground 1":                       ("GF",   0x246),
    "Path to Fortress 1 X On Ground 2":                       ("GF",   0x247),
    "Path to Fortress 1 X On Ground 3":                       ("GF",   0x248),
    "Path to Fortress 1 X On Ground 4":                       ("GF",   0x249),
    "Path to Fortress 1 X On Ground 5":                       ("GF",   0x24A),
    "Path to Fortress 1 On Brick Block":                      ("GF",   0x245),

    "Path to Fortress 2 In Tree":                             ("GF",   0x251),

    "Koopa Village 1 Bush Far Left":                          ("GF",   0x24C),
    "Koopa Village 1 Bush Left Front":                        ("GF",   0x24D),
    "Koopa Village 1 Bush Infront Of Tree":                   ("MF",   0x1049),
    "Koopa Village 1 Bush Second From Right":                 ("GF",   0x24F),
    "Koopa Village 1 Bush Second From Left (Koopa Koot Favor)": ("GF",   0x263),
    "Koopa Village 1 Bush Far Right (Koopa Koot Favor)":      ("GF",   0x264),
    "Koopa Village 1 Mort T. Letter Reward":                  ("MF",   0x1037),
    "Koopa Village 1 Koover Letter Reward 1":                 ("MF",   0x1038),
    "Koopa Village 1 Koover Letter Reward 2":                 ("MF",   0x1039),
    "Koopa Village 1 Hidden Panel":                           ("GF",   0x25E),
    "Koopa Village 1 Shop Item 1":                            ("MF",   0x103A),
    "Koopa Village 1 Shop Item 2":                            ("MF",   0x103B),
    "Koopa Village 1 Shop Item 3":                            ("MF",   0x103C),
    "Koopa Village 1 Shop Item 4":                            ("MF",   0x103D),
    "Koopa Village 1 Shop Item 5":                            ("MF",   0x103E),
    "Koopa Village 1 Shop Item 6":                            ("MF",   0x103F),

    "Koopa Village 2 Bush Far Left":                          ("MF",   0x104A),
    "Koopa Village 2 Bush Far Right":                         ("MF",   0x10A7),
    "Koopa Village 2 Kolorado's Wife (Koopa Koot Favor)":      ("GF",   0x265),
    "Koopa Village 2 Koopa Koot Silver Credit":               ("MF",   0x1040),
    "Koopa Village 2 Koopa Koot Gold Credit":                 ("MF",   0x1041),
    "Koopa Village 2 Kolorado Artifact Reward":               ("GF",   0x312),
    "Koopa Village 2 Kolorado Letter Reward":                 ("MF",   0x1042),
    "Koopa Village 2 Push Block Puzzle":                      ("GF",   0x243),
    "Koopa Village 2 Koopa Koot Reward 1":                    ("GF",   0x6AD),
    "Koopa Village 2 Koopa Koot Reward 2":                    ("GF",   0x6B0),
    "Koopa Village 2 Koopa Koot Reward 3":                    ("GF",   0x6B3),
    "Koopa Village 2 Koopa Koot Reward 4":                    ("GF",   0x6B6),
    "Koopa Village 2 Koopa Koot Reward 5":                    ("GF",   0x6B9),
    "Koopa Village 2 Koopa Koot Reward 6":                    ("GF",   0x6BC),
    "Koopa Village 2 Koopa Koot Reward 7":                    ("GF",   0x6BF),
    "Koopa Village 2 Koopa Koot Reward 8":                    ("GF",   0x6C2),
    "Koopa Village 2 Koopa Koot Reward 9":                    ("GF",   0x6C5),
    "Koopa Village 2 Koopa Koot Reward 10":                   ("GF",   0x6C8),
    "Koopa Village 2 Koopa Koot Reward 11":                   ("GF",   0x6CB),
    "Koopa Village 2 Koopa Koot Reward 12":                   ("GF",   0x6CE),
    "Koopa Village 2 Koopa Koot Reward 13":                   ("GF",   0x6D1),
    "Koopa Village 2 Koopa Koot Reward 14":                   ("GF",   0x6D4),
    "Koopa Village 2 Koopa Koot Reward 15":                   ("GF",   0x6D7),
    "Koopa Village 2 Koopa Koot Reward 16":                   ("GF",   0x6DA),
    "Koopa Village 2 Koopa Koot Reward 17":                   ("GF",   0x6DD),
    "Koopa Village 2 Koopa Koot Reward 18":                   ("GF",   0x6E0),
    "Koopa Village 2 Koopa Koot Reward 19":                   ("GF",   0x6E3),
    "Koopa Village 2 Koopa Koot Reward 20":                   ("GF",   0x6E6),
    "Koopa Village 2 Kooper Partner":                         ("MF",   0x1043),

    "Behind Koopa Village On Stump":                          ("GF",   0x242),

    "Fuzzy Forest Fuzzy Battle Reward":                       ("MF",   0x1044),

    # Koopa Bros Fortress

    "Fortress Exterior Chest Behind Fortress":                ("GF",   0x281),
    "Fortress Exterior Chest On Ledge":                       ("GF",   0x282),

    "Left Tower Top Of Tower":                                ("GF",   0x27E),
    "Left Tower Koopa Troopa Reward":                         ("GF",   0x285),

    "Central Hall Left Cell":                                 ("GF",   0x286),
    "Central Hall Right Cell":                                ("GF",   0x287),
    "Central Hall Center Cell":                               ("GF",   0x27F),

    "Jail Bombette Partner":                                  ("MF",   0x1045),

    "Dungeon Fire Room On The Ground":                        ("GF",   0x288),

    "Battlement Block Behind Rock":                           ("GF",   0x280),

    # Mt Rugged

    "Train Station Bush 1":                                   ("GF",   0x2C5),
    "Train Station Bush 2":                                   ("GF",   0x2C6),
    "Train Station Bush 3":                                   ("GF",   0x2C7),
    "Train Station Bush Top":                                 ("MF",   0x1047),
    "Train Station Parakarry Partner":                        ("MF",   0x1048),
    "Train Station In SuperBlock":                            ("GF",   0x2D1),

    "Mt Rugged 1 On Slide 1":                                 ("GF",   0x2B3),
    "Mt Rugged 1 On Slide 2":                                 ("GF",   0x2B4),
    "Mt Rugged 1 On Slide 3":                                 ("GF",   0x2B5),
    "Mt Rugged 1 Hurting Whacka":                             ("MF",   0x1046),
    "Mt Rugged 1 Yellow Block":                               ("GF",   0x2CB),

    "Mt Rugged 2 Hidden Panel":                               ("GF",   0x2CD),
    "Mt Rugged 2 Parakarry Ledge":                            ("GF",   0x2AE),
    "Mt Rugged 2 Kooper Ledge":                               ("GF",   0x2C1),

    "Mt Rugged 3 Bub-ulb Gift":                               ("GF",   0x2CC),
    "Mt Rugged 3 On Scaffolding":                             ("GF",   0x2AF),

    "Mt Rugged 4 Hidden Cave Chest":                          ("GF",   0x2B1),
    "Mt Rugged 4 Slide Ledge":                                ("GF",   0x2C2),
    "Mt Rugged 4 Left Ledge Center":                          ("GF",   0x2B0),
    "Mt Rugged 4 Left Ledge Right":                           ("GF",   0x2B8),
    "Mt Rugged 4 Left Ledge 3":                               ("GF",   0x2B9),
    "Mt Rugged 4 Left Ledge 4":                               ("GF",   0x2BA),
    "Mt Rugged 4 Left Ledge 5":                               ("GF",   0x2BB),
    "Mt Rugged 4 Left Ledge 6":                               ("GF",   0x2BC),
    "Mt Rugged 4 Left Ledge 7":                               ("GF",   0x2BD),
    "Mt Rugged 4 Bottom Left 1":                              ("GF",   0x2B6),
    "Mt Rugged 4 Bottom Left 2":                              ("GF",   0x2B7),
    "Mt Rugged 4 Yellow Block Top Left":                      ("GF",   0x2BE),
    "Mt Rugged 4 Yellow Block Floating":                      ("GF",   0x2BF),
    "Mt Rugged 4 Yellow Block Top Right":                     ("GF",   0x2C0),

    "Suspension Bridge Bottom Of Cliff":                      ("GF",   0x2C3),

    # Dry Dry Desert

    "N3W3 Yellow Block Left":                                 ("GF",   0x31D),
    "N3W3 Yellow Block Right":                                ("GF",   0x31E),

    "N3W1 Ruins Entrance Radio Trade Event 2 Reward":         ("MF",   0x1054),

    "N3E2 Pokey Army Behind Cactus":                          ("GF",   0x33F),

    "N3E3 In Tree":                                           ("GF",   0x345),
    "N3E3 In MultiCoinBlock":                                 ("GF",   0x330),

    "N2W3 Hidden Block":                                      ("GF",   0x31F),

    "N2E1 (Tweester A) Yellow Block Left":                    ("GF",   0x320),
    "N2E1 (Tweester A) Yellow Block Right":                   ("GF",   0x321),

    "N1W3 Special Block Hit Block":                           ("GF",   0x322),
    "N1W3 Special Block Hit Block Plenty":                    ("GF",   0x323),
    "N1W3 Special Block Hit Block Very Much":                 ("GF",   0x324),

    "N1W1 Yellow Block 1":                                    ("GF",   0x325),
    "N1W1 Yellow Block 2":                                    ("GF",   0x326),
    "N1W1 Yellow Block 3":                                    ("GF",   0x327),
    "N1W1 Yellow Block 4":                                    ("GF",   0x328),
    "N1W1 Yellow Block Center":                               ("GF",   0x329),

    "N1E1 Palm Trio Hidden Block":                            ("GF",   0x32A),

    "N1E2 In MultiCoinBlock Center":                          ("GF",   0x332),
    "N1E2 In MultiCoinBlock Bottom Right":                    ("GF",   0x333),

    "N1E3 In Tree":                                           ("GF",   0x346),

    "W3 Kolorado's Camp In Tree":                              ("GF",   0x340),

    "Center (Tweester C) Hidden Panel":                       ("GF",   0x31C),

    "E1 Nomadimouse Nomadimouse Letter Reward":               ("MF",   0x1055),
    "E1 Nomadimouse In Tree":                                 ("GF",   0x347),

    "E2 In Tree Far Left":                                    ("GF",   0x348),

    "E3 Outside Outpost In Tree (Far Left)":                  ("GF",   0x349),
    "E3 Outside Outpost In Tree (Second From Left)":          ("GF",   0x34A),
    "E3 Outside Outpost In Tree (Fourth From Right)":         ("GF",   0x34B),
    "E3 Outside Outpost In Tree (Far Right)":                 ("GF",   0x341),

    "S1W3 In MultiCoinBlock Top Left":                        ("GF",   0x334),

    "S1 Yellow Block":                                        ("GF",   0x32B),

    "S1E2 Small Bluffs On Brick Block":                       ("GF",   0x343),
    "S1E2 Small Bluffs Ontop Of Bluffs":                      ("GF",   0x344),

    "S1E3 North of Oasis Hidden Block":                       ("GF",   0x32D),
    "S1E3 North of Oasis Tree Bottom Left":                   ("GF",   0x34C),
    "S1E3 North of Oasis Yellow Block":                       ("GF",   0x32C),

    "S2E2 West of Oasis Behind Bush":                         ("GF",   0x344),
    "S2E2 West of Oasis In Tree":                             ("GF",   0x34D),
    "S2E2 West of Oasis In MultiCoinBlock":                   ("GF",   0x336),

    "S2E3 Oasis In Fruit Tree (Left)":                        ("MF",   0x1056),
    "S2E3 Oasis In Fruit Tree (Right)":                       ("MF",   0x1057),
    "S2E3 Oasis In Tree (Far Left)":                          ("GF",   0x34E),
    "S2E3 Oasis In Tree (Front Right)":                       ("GF",   0x34F),

    "S3W2 Hidden AttackFX Hidden Block":                      ("GF",   0x32E),

    "S3E1 Yellow Block":                                      ("GF",   0x32F),

    "S3E3 South of Oasis In Tree (Far Right)":                ("GF",   0x350),
    "S3E3 South of Oasis In MultiCoinBlock Top Left":         ("GF",   0x337),
    "S3E3 South of Oasis In MultiCoinBlock Top Right":        ("GF",   0x338),
    "S3E3 South of Oasis In MultiCoinBlock Right":            ("GF",   0x339),
    "S3E3 South of Oasis In MultiCoinBlock Left":             ("GF",   0x33A),
    "S3E3 South of Oasis In MultiCoinBlock Bottom Left":      ("GF",   0x33B),
    "S3E3 South of Oasis In MultiCoinBlock Bottom Right":     ("GF",   0x33C),

    # Dry Dry Outpost

    "Outpost 1 Composer Lyrics Reward":                       ("GF",   0x2F2),
    "Outpost 1 Store Legend":                                 ("GF",   0x2F6),
    "Outpost 1 Little Mouser Letter Reward":                  ("MF",   0x104B),
    "Outpost 1 Shop Item 1":                                  ("MF",   0x104C),
    "Outpost 1 Shop Item 2":                                  ("MF",   0x104D),
    "Outpost 1 Shop Item 3":                                  ("MF",   0x104E),
    "Outpost 1 Shop Item 4":                                  ("MF",   0x104F),
    "Outpost 1 Shop Item 5":                                  ("MF",   0x1050),
    "Outpost 1 Shop Item 6":                                  ("MF",   0x1051),
    "Outpost 1 In Red Tree":                                  ("GF",   0x2F8),

    "Outpost 2 Merlee Request (Koopa Koot Favor)":            ("GF",   0x2F7),
    "Outpost 2 Moustafa Gift":                                ("MF",   0x1052),
    "Outpost 2 Mr. E. Letter Reward":                         ("MF",   0x1053),
    "Outpost 2 Hidden Panel":                                 ("GF",   0x2F4),
    "Outpost 2 Toad House Roof":                              ("GF",   0x2F5),

    # Dry Dry Ruins

    "Sarcophagus Hall 1 In Sarcophagus":                      ("GF",   0x694),

    "Sand Drainage Room 1 On The Ground":                     ("GF",   0x367),

    "Sand Drainage Room 2 In The Sand":                       ("GF",   0x375),
    "Sand Drainage Room 2 On Ledge":                          ("GF",   0x36A),

    "Pyramid Stone Room On Pedestal":                         ("GF",   0x372),

    "Sarcophagus Hall 2 Pokey Gauntlet Reward":               ("GF",   0x36B),
    "Sarcophagus Hall 2 Behind Hammer Block":                 ("GF",   0x374),

    "Super Hammer Room In Big Chest":                         ("GF",   0x384),
    "Super Hammer Room Hidden Chest":                         ("GF",   0x385),

    "Vertical Shaft In SuperBlock":                           ("GF",   0x387),

    "Diamond Stone Room On Pedestal":                         ("GF",   0x373),

    "Sand Drainage Room 3 On Ledge":                          ("GF",   0x377),

    "Lunar Stone Room On Pedestal":                           ("GF",   0x371),

    # Forever Forest

    "Tree Face (Bub-ulb) Bub-ulb Gift":                       ("GF",   0x3A2),
    "Bee Hive (HP Plus) Central Block":                       ("GF",   0x39D),
    "Flowers Appear (FP Plus) Central Block":                 ("GF",   0x39E),
    "Outside Boo's Mansion In Bush (Back Right)":              ("MF",   0x1058),
    "Outside Boo's Mansion Yellow Block":                      ("GF",   0x3A7),
    "Exit to Gusty Gulch Hidden Panel":                       ("GF",   0x3A5),
    # Boo's Mansion
    "Foyer From Franky (Koopa Koot Favor)":                   ("GF",   0x3BF),
    "Foyer Franky Letter Reward":                             ("MF",   0x1059),
    "Foyer Hidden Panel":                                     ("GF",   0x3C1),

    "Basement Stairs Hidden Panel":                           ("GF",   0x3C4),

    "Basement In Crate":                                      ("GF",   0x3C5),
    "Basement Igor Letter Reward":                            ("MF",   0x105A),
    "Basement Shop Item 1":                                   ("MF",   0x105B),
    "Basement Shop Item 2":                                   ("MF",   0x105C),
    "Basement Shop Item 3":                                   ("MF",   0x105D),
    "Basement Shop Item 4":                                   ("MF",   0x105E),
    "Basement Shop Item 5":                                   ("MF",   0x105F),
    "Basement Shop Item 6":                                   ("MF",   0x1060),

    "Super Boots Room In Big Chest":                          ("GF",   0x3C7),
    "Super Boots Room In Crate":                              ("GF",   0x3CA),
    "Super Boots Room Hidden Panel":                          ("GF",   0x3CC),

    "Pot Room In Crate 1":                                    ("MF",   0x1061),
    "Pot Room In Crate 2":                                    ("MF",   0x1062),

    "Library In Crate":                                       ("GF",   0x3D0),
    "Library On Bookshelf":                                   ("GF",   0x3CF),

    "Record Player Room In Chest":                            ("GF",   0x3D2),

    "Record Room Hidden Panel":                               ("GF",   0x3D4),
    "Record Room Beat Boo Game":                              ("GF",   0x3D3),

    "Lady Bow's Room Bow Partner":                             ("MF",   0x1063),

    # Gusty Gulch

    "Ghost Town 1 From Boo (Koopa Koot Favor)":               ("GF",   0x3F7),
    "Ghost Town 1 Yellow Block In House":                     ("GF",   0x3EF),

    "Wasteland Ascent 1 On Rock":                             ("GF",   0x3ED),
    "Wasteland Ascent 1 Infront Of Branch":                   ("GF",   0x3EE),
    "Wasteland Ascent 1 Yellow Block 1":                      ("GF",   0x3EA),
    "Wasteland Ascent 1 Yellow Block 2":                      ("GF",   0x3EB),
    "Wasteland Ascent 1 Yellow Block Right":                  ("GF",   0x3EC),

    "Wasteland Ascent 2 Behind Rock":                         ("GF",   0x3FB),
    "Wasteland Ascent 2 In MultiCoinBlock":                   ("GF",   0x3F2),
    "Wasteland Ascent 2 Yellow Block Left":                   ("GF",   0x3F0),
    "Wasteland Ascent 2 Yellow Block Right":                  ("GF",   0x3F1),
    # Tubba's Castle
    "Covered Tables Room (1F) On Table":                      ("GF",   0x41F),

    "Study (1F) On Table":                                    ("GF",   0x41A),

    "Table/Clock Room (1/2F) On Table":                       ("GF",   0x412),

    "Basement In Chest":                                      ("GF",   0x418),

    "Stairs to Basement In SuperBlock":                       ("GF",   0x416),

    "Spike Trap Room (2F) In Chest":                          ("GF",   0x421),

    "Hidden Bedroom (2F) In Hidden Room":                     ("GF",   0x422),
    "Hidden Bedroom (2F) On Bed 1":                           ("GF",   0x423),
    "Hidden Bedroom (2F) On Bed 2":                           ("GF",   0x424),
    "Hidden Bedroom (2F) On Bed 3":                           ("GF",   0x425),
    "Hidden Bedroom (2F) On Bed 4":                           ("GF",   0x426),
    "Hidden Bedroom (2F) On Bed 5":                           ("GF",   0x427),
    "Hidden Bedroom (2F) On Bed 6":                           ("GF",   0x428),

    "Stairs to Third Floor Yellow Block":                     ("GF",   0x429),

    "Sleeping Clubbas Room (3F) On Pedestal":                 ("GF",   0x42D),

    # Shy Guys Toybox

    "BLU Station Hidden Panel":                               ("GF",   0x4A6),
    "BLU Station Hidden Block":                               ("GF",   0x45D),

    "BLU Anti-Guy Hall In Chest":                             ("GF",   0x49F),
    "BLU Anti-Guy Hall Hidden Block":                         ("GF",   0x4A1),
    "BLU Anti-Guy Hall Yellow Block":                         ("GF",   0x4A0),

    "BLU Large Playroom Hidden Block 1":                      ("GF",   0x456),
    "BLU Large Playroom Hidden Block 2":                      ("GF",   0x457),
    "BLU Large Playroom Calculator Thief 1":                  ("GF",   0x454),
    "BLU Large Playroom Calculator Thief 2":                  ("MF",   0x1064),
    "BLU Large Playroom Shy Guy 2":                           ("MF",   0x1065),
    "BLU Large Playroom Shy Guy 3":                           ("MF",   0x1066),
    "BLU Large Playroom Shy Guy 4":                           ("MF",   0x1067),
    "BLU Large Playroom Shy Guy 5":                           ("MF",   0x1068),

    "BLU Block City In Chest":                                ("GF",   0x45F),
    "BLU Block City Infront Of Chest":                        ("GF",   0x44E),
    "BLU Block City Midair 1":                                ("GF",   0x463),
    "BLU Block City Midair 2":                                ("GF",   0x464),
    "BLU Block City Midair 3":                                ("GF",   0x465),
    "BLU Block City Midair 4":                                ("GF",   0x466),
    "BLU Block City Midair 5":                                ("GF",   0x467),
    "BLU Block City Midair 6":                                ("GF",   0x468),
    "BLU Block City Midair 7":                                ("GF",   0x469),
    "BLU Block City Midair 8":                                ("GF",   0x46A),
    "BLU Block City On Building":                             ("GF",   0x46C),
    "BLU Block City Behind Building Block":                   ("GF",   0x46D),
    "BLU Block City Yellow Block 1":                          ("GF",   0x460),
    "BLU Block City Yellow Block 2":                          ("GF",   0x461),
    "BLU Block City Yellow Block On Ledge":                   ("GF",   0x462),

    "PNK Station In Chest":                                   ("GF",   0x472),
    "PNK Station Hidden Panel":                               ("GF",   0x4A7),
    "PNK Station Hidden Block":                               ("GF",   0x473),

    "PNK Tracks Hallway In MultiCoinBlock":                   ("GF",   0x4A5),
    "PNK Tracks Hallway Yellow Block South":                  ("GF",   0x4A2),
    "PNK Tracks Hallway Yellow Block North 1":                ("GF",   0x4A3),
    "PNK Tracks Hallway Yellow Block North 2":                ("GF",   0x4A4),

    "PNK Gourmet Guy Crossing Hidden Block Right":            ("GF",   0x470),
    "PNK Gourmet Guy Crossing Hidden Block Left":             ("GF",   0x471),
    "PNK Gourmet Guy Crossing Gourmet Guy Reward":            ("GF",   0x452),
    "PNK Gourmet Guy Crossing Yellow Block 1":                ("GF",   0x46E),
    "PNK Gourmet Guy Crossing Yellow Block 2":                ("GF",   0x46F),

    "PNK Playhouse In Chest (Far Right)":                     ("GF",   0x476),
    "PNK Playhouse In Chest (Top Left)":                      ("GF",   0x477),
    "PNK Playhouse In Chest (Right)":                         ("GF",   0x478),
    "PNK Playhouse Infront Of Chest (Right)":                 ("GF",   0x44F),
    "PNK Playhouse Yellow Block":                             ("GF",   0x475),

    "GRN Station Hidden Panel":                               ("GF",   0x4A8),
    "GRN Station Hidden Block":                               ("GF",   0x479),

    "GRN Treadmills/Slot Machine In Chest":                   ("GF",   0x47B),
    "GRN Treadmills/Slot Machine Infront Of Chest":           ("GF",   0x450),
    "GRN Treadmills/Slot Machine On Treadmill 1":             ("GF",   0x47E),
    "GRN Treadmills/Slot Machine On Treadmill 2":             ("GF",   0x47F),
    "GRN Treadmills/Slot Machine On Treadmill 3":             ("GF",   0x480),
    "GRN Treadmills/Slot Machine On Treadmill 4":             ("GF",   0x481),
    "GRN Treadmills/Slot Machine On Treadmill 5":             ("GF",   0x482),
    "GRN Treadmills/Slot Machine On Treadmill 6":             ("GF",   0x483),
    "GRN Treadmills/Slot Machine Hidden Room Center":         ("GF",   0x496),
    "GRN Treadmills/Slot Machine Hidden Room 1":              ("GF",   0x488),
    "GRN Treadmills/Slot Machine Hidden Room 2":              ("GF",   0x489),
    "GRN Treadmills/Slot Machine Hidden Room 3":              ("GF",   0x48D),
    "GRN Treadmills/Slot Machine Hidden Room 4":              ("GF",   0x48E),
    "GRN Treadmills/Slot Machine Hidden Room 5":              ("GF",   0x492),
    "GRN Treadmills/Slot Machine Hidden Room 6":              ("GF",   0x493),
    "GRN Treadmills/Slot Machine Defeat Shy Guy":             ("GF",   0x47D),
    "GRN Treadmills/Slot Machine In MultiCoinBlock":          ("GF",   0x497),

    "RED Station Hidden Panel":                               ("GF",   0x4A9),
    "RED Station Hidden Block":                               ("GF",   0x498),

    "RED Moving Platforms Hidden Block Center":               ("GF",   0x49A),
    "RED Moving Platforms Hidden Block Right":                ("GF",   0x49D),
    "RED Moving Platforms Hidden Block Left":                 ("GF",   0x49E),
    "RED Moving Platforms In SuperBlock":                     ("GF",   0x4AA),
    "RED Moving Platforms In MultiCoinBlock":                 ("GF",   0x499),
    "RED Moving Platforms Yellow Block 1":                    ("GF",   0x49C),
    "RED Moving Platforms Yellow Block 2":                    ("GF",   0x49B),

    "RED Lantern Ghost Watt Partner":                         ("MF",   0x1069),

    "RED Boss Barricade Hidden Block Left":                   ("GF",   0x45B),
    "RED Boss Barricade On Brick Block":                      ("GF",   0x45C),
    "RED Boss Barricade Yellow Block Right":                  ("GF",   0x45A),

    # Jade Jungle

    "Whale Cove Over Flower 1":                               ("GF",   0x4C0),
    "Whale Cove Over Flower 2":                               ("GF",   0x4C1),
    "Whale Cove Behind Bush":                                 ("GF",   0x4C3),
    "Whale Cove In Palm Tree":                                ("MF",   0x106A),

    "Beach Hidden Block Left":                                ("GF",   0x4DE),
    "Beach Hidden Block Right":                               ("GF",   0x4DF),
    "Beach On The Rocks":                                     ("GF",   0x4C6),
    "Beach Over Flower 1":                                    ("GF",   0x4C5),
    "Beach Over Flower 2":                                    ("GF",   0x4FD),
    "Beach In Palm Tree 1":                                   ("MF",   0x106B),
    "Beach In Palm Tree 2":                                   ("MF",   0x106C),
    "Beach In Palm Tree 3":                                   ("MF",   0x106D),
    "Beach In Palm Tree 4":                                   ("MF",   0x106E),
    "Beach In Palm Tree 5":                                   ("MF",   0x106F),
    "Beach In Palm Tree 6":                                   ("GF",   0x4E4),
    "Beach In Palm Tree 6 2":                                 ("MF",   0x1070),

    "Village Cove Village Leader Reward":                     ("MF",   0x1071),
    "Village Cove Hidden Panel":                              ("GF",   0x4F5),
    "Village Cove In Palm Tree Left":                         ("MF",   0x1072),
    "Village Cove In Palm Tree Right":                        ("MF",   0x1073),

    "Village Buildings Kolorado Volcano Vase Reward":         ("GF",   0x4FB),
    "Village Buildings Yellow Yoshi Food Reward":             ("MF",   0x107A),
    "Village Buildings Red Yoshi Kid Letter Reward":          ("MF",   0x107B),
    "Village Buildings Shop Item 1":                          ("MF",   0x1074),
    "Village Buildings Shop Item 2":                          ("MF",   0x1075),
    "Village Buildings Shop Item 3":                          ("MF",   0x1076),
    "Village Buildings Shop Item 4":                          ("MF",   0x1077),
    "Village Buildings Shop Item 5":                          ("MF",   0x1078),
    "Village Buildings Shop Item 6":                          ("MF",   0x1079),
    "Village Buildings In Palm Tree":                         ("MF",   0x107C),

    "Path to the Volcano Raphael Gift":                       ("MF",   0x107E),
    "Path to the Volcano Behind Tree":                        ("GF",   0x4D9),

    "SE Jungle (Quake Hammer) Bush (Bottom Right)":           ("GF",   0x4F0),
    "SE Jungle (Quake Hammer) Bush (Bottom Left)":            ("GF",   0x4D7),
    "SE Jungle (Quake Hammer) Red Block":                     ("GF",   0x4D6),
    "SE Jungle (Quake Hammer) In Tree (Right)":               ("GF",   0x4E5),

    "Sushi Tree In Volcano Chest":                            ("GF",   0x4CC),
    "Sushi Tree On Island":                                   ("GF",   0x4CD),
    "Sushi Tree Sushie Partner":                              ("MF",   0x107D),
    "Sushi Tree In Island Tree":                              ("GF",   0x4CB),

    "SW Jungle (Super Block) Bush (Top Right)":               ("GF",   0x4F1),
    "SW Jungle (Super Block) Bush (Bottom Left)":             ("GF",   0x4F2),
    "SW Jungle (Super Block) Hidden Block":                   ("GF",   0x4E1),
    "SW Jungle (Super Block) Underwater 1":                   ("GF",   0x4FF),
    "SW Jungle (Super Block) Underwater 2":                   ("GF",   0x500),
    "SW Jungle (Super Block) Underwater 3":                   ("GF",   0x501),
    "SW Jungle (Super Block) In SuperBlock":                  ("GF",   0x4FE),
    "SW Jungle (Super Block) In Tree (Top)":                  ("GF",   0x4E8),
    "SW Jungle (Super Block) In Tree (Right)":                ("GF",   0x4E9),

    "NW Jungle (Large Ledge) Bush 1":                         ("GF",   0x4F3),
    "NW Jungle (Large Ledge) Bush 2":                         ("GF",   0x4F4),
    "NW Jungle (Large Ledge) In Tree On Ledge":               ("GF",   0x4EA),
    "NW Jungle (Large Ledge) In Tree Right":                  ("GF",   0x4EB),

    "Western Dead End Underwater":                            ("GF",   0x502),

    "NE Jungle (Raven Statue) Underwater":                    ("GF",   0x4D8),
    "NE Jungle (Raven Statue) In Tree (Top Left)":            ("GF",   0x4E6),

    "Small Jungle Ledge In Tree":                             ("GF",   0x4E7),

    "Deep Jungle 1 Hidden Block":                             ("GF",   0x4E2),
    "Deep Jungle 1 In Tree (Vine)":                           ("GF",   0x4DA),
    "Deep Jungle 1 In Tree (Hit)":                            ("GF",   0x4EC),

    "Deep Jungle 2 (Block Puzzle) Hidden Block":              ("GF",   0x4E3),
    "Deep Jungle 2 (Block Puzzle) In Tree (Left)":            ("GF",   0x4ED),

    "Deep Jungle 3 Tree Vine Second Left":                    ("GF",   0x4DB),
    "Deep Jungle 3 Tree Vine Far Right":                      ("GF",   0x4DC),

    "Deep Jungle 4 (Ambush) Hidden Panel":                    ("GF",   0x4F6),
    "Deep Jungle 4 (Ambush) In Tree (Right)":                 ("GF",   0x4EE),

    "Great Tree Vine Ascent End Of Vine":                     ("GF",   0x4DD),

    # Mt Lavalava

    "Central Cavern On Stone Pillar":                         ("GF",   0x532),
    "Central Cavern On Brick Block":                          ("GF",   0x533),
    "Central Cavern Yellow Block 1":                          ("GF",   0x534),
    "Central Cavern Yellow Block 2":                          ("GF",   0x535),
    "Central Cavern Yellow Block 3":                          ("GF",   0x536),
    "Central Cavern Yellow Block 4":                          ("GF",   0x537),

    "Fire Bar Bridge In SuperBlock":                          ("GF",   0x530),

    "Flowing Lava Puzzle Hidden Block":                       ("GF",   0x520),

    "Ultra Hammer Room In Big Chest":                         ("GF",   0x523),

    "Dizzy Stomp Room In Chest":                              ("GF",   0x52C),

    "Zipline Cavern Hidden Panel":                            ("GF",   0x53A),
    "Zipline Cavern In SuperBlock":                           ("GF",   0x531),

    "Boss Antechamber Hidden Panel":                          ("GF",   0x53B),

    "Boss Room Yellow Block Left":                            ("GF",   0x538),
    "Boss Room Yellow Block Right":                           ("GF",   0x539),

    # Flower Fields

    "(NE) Elevators Stomp On Ledge":                          ("GF",   0x56C),
    "(NE) Elevators Leftside Vine":                           ("MF",   0x108B),
    "(NE) Elevators In SuperBlock":                           ("GF",   0x57B),

    "(NE) Fallen Logs Hidden Block":                          ("GF",   0x56E),
    "(NE) Fallen Logs In The Flowers":                        ("GF",   0x56D),

    "(East) Triple Tree Path Leftmost Vine":                  ("MF",   0x1086),
    "(East) Triple Tree Path Tree Puzzle Reward":             ("GF",   0x566),

    "(East) Petunia's Field Petunia Gift":                     ("MF",   0x107F),
    "(East) Petunia's Field Hidden Panel":                     ("GF",   0x57C),
    "(East) Petunia's Field In Tree 1":                        ("MF",   0x1080),
    "(East) Petunia's Field In Tree 2":                        ("MF",   0x1081),

    "(East) Old Well Well Reward":                            ("GF",   0x570),

    "(SE) Briar Platforming In The Flowers":                  ("GF",   0x565),
    "(SE) Briar Platforming Left Side Vine":                  ("MF",   0x1083),
    "(SE) Briar Platforming In SuperBlock":                   ("GF",   0x57A),
    "(SE) Briar Platforming In Tree 1":                       ("MF",   0x1084),
    "(SE) Briar Platforming In Tree 2":                       ("MF",   0x1085),

    "(SE) Water Level Room Hidden Panel":                     ("GF",   0x57E),
    "(SE) Water Level Room Hidden Block":                     ("GF",   0x572),
    "(SE) Water Level Room In Tree 1":                        ("MF",   0x108C),
    "(SE) Water Level Room In Tree 2":                        ("MF",   0x108D),
    "(SE) Water Level Room Yellow Block":                     ("GF",   0x571),

    "(SE) Lily's Fountain Lily Reward For WaterStone":         ("MF",   0x1087),
    "(SE) Lily's Fountain In Tree":                            ("GF",   0x567),

    "(SW) Path to Crystal Tree Hidden Panel":                 ("GF",   0x57F),
    "(SW) Path to Crystal Tree Central Vine":                 ("MF",   0x108E),
    "(SW) Path to Crystal Tree In Tree 1":                    ("MF",   0x108F),
    "(SW) Path to Crystal Tree In Tree 2":                    ("MF",   0x1090),

    "(SW) Posie and Crystal Tree Posie Gift 1":               ("MF",   0x1082),
    "(SW) Posie and Crystal Tree Posie Gift 2":               ("GF",   0x55E),

    "(West) Path to Maze Upper Hidden Block":                 ("GF",   0x581),
    "(West) Path to Maze Lower Hidden Block":                 ("GF",   0x580),

    "(West) Maze In MultiCoinBlock":                          ("GF",   0x568),

    "(West) Rosie's Trellis Rosie Gift":                       ("MF",   0x1088),

    "(NW) Bubble Flower On Ledge":                            ("GF",   0x56B),
    "(NW) Bubble Flower Right Vine":                          ("MF",   0x108A),

    "(NW) Lakilester Cage Under Rock":                        ("GF",   0x569),
    "(NW) Lakilester In The Flowers":                         ("GF",   0x56A),
    "(NW) Lakilester Lakilester Partner":                     ("MF",   0x1089),

    "Cloudy Climb On Cloud":                                  ("GF",   0x56F),

    # Shiver Region

    "Shiver City Center Toad House Breakfast":                ("MF",   0x1093),
    "Shiver City Center Snowmen Gift 1":                      ("GF",   0x5A0),
    "Shiver City Center Snowmen Gift 2":                      ("GF",   0x5A1),
    "Shiver City Center Snowmen Gift 3":                      ("GF",   0x5A2),
    "Shiver City Center Snowmen Gift 4":                      ("GF",   0x5A3),
    "Shiver City Center Snowmen Gift 5":                      ("GF",   0x5A4),
    "Shiver City Center Shop Item 1":                         ("MF",   0x1094),
    "Shiver City Center Shop Item 2":                         ("MF",   0x1095),
    "Shiver City Center Shop Item 3":                         ("MF",   0x1096),
    "Shiver City Center Shop Item 4":                         ("MF",   0x1097),
    "Shiver City Center Shop Item 5":                         ("MF",   0x1098),
    "Shiver City Center Shop Item 6":                         ("MF",   0x1099),

    "Shiver City Mayor Area Chest In House":                  ("GF",   0x59B),
    "Shiver City Mayor Area Mayor Penguin Gift":              ("MF",   0x1091),
    "Shiver City Mayor Area Mayor Penguin Letter Reward":     ("MF",   0x1092),
    "Shiver City Mayor Area Hidden Panel":                    ("GF",   0x59C),

    "Shiver City Pond Area In Frozen Pond":                   ("GF",   0x5BA),

    "Shiver Snowfield Hidden Panel":                          ("GF",   0x5A5),
    "Shiver Snowfield Behind Tree Right":                     ("GF",   0x5A7),
    "Shiver Snowfield In Tree Left":                          ("GF",   0x5A6),

    "Path to Starborn Valley Hidden Block":                   ("GF",   0x5AA),
    "Path to Starborn Valley Behind Icicle":                  ("GF",   0x5A9),

    "Starborn Valley Merle Gift":                             ("MF",   0x109A),
    "Starborn Valley Frost T. Letter Reward":                 ("MF",   0x109B),

    "Shiver Mountain Passage Hidden Block":                   ("GF",   0x5B0),

    "Shiver Mountain Hills Bottom Path":                      ("MF",   0x109C),
    "Shiver Mountain Hills In SuperBlock":                    ("GF",   0x5B1),

    "Shiver Mountain Tunnel Socket 1":                        ("MF",   0x109D),
    "Shiver Mountain Tunnel Socket 2":                        ("MF",   0x109E),
    "Shiver Mountain Tunnel Socket 3":                        ("MF",   0x109F),

    "Shiver Mountain Peaks Left Ledge":                       ("GF",   0x5B8),
    "Shiver Mountain Peaks Red Block":                        ("GF",   0x5B7),

    "Merlar's Sanctuary On Pedestal":                          ("GF",   0x599),

    # Crystal Palace

    "Blue Key Room In Chest":                                 ("GF",   0x5D5),

    "Red Key Room In Chest":                                  ("GF",   0x5D4),

    "Reflected Save Room Yellow Block":                       ("GF",   0x5DA),

    "Shooting Star Room On The Ground":                       ("GF",   0x5DB),

    "P-Down, D-Up Room In Chest":                             ("GF",   0x5DD),

    "Star Piece Cave On The Ground":                          ("GF",   0x5E2),

    "Blue Mirror Hall 2 In MultiCoinBlock Front":             ("GF",   0x5E0),
    "Blue Mirror Hall 2 In MultiCoinBlock Back":              ("GF",   0x5E1),

    "Triple Dip Room In Chest":                               ("GF",   0x5ED),

    "Huge Statue Room Hidden Panel":                          ("GF",   0x5E6),
    "Huge Statue Room Yellow Block":                          ("GF",   0x5E5),

    "Palace Key Room In Chest":                               ("GF",   0x5E9),

    "Small Statue Room Hidden Panel":                         ("GF",   0x5E8),
    "Small Statue Room Hidden Block":                         ("GF",   0x5E7),

    "P-Up, D-Down Room In Chest":                             ("GF",   0x5EA),

    # Bowser's Castle

    "Front Door Exterior Red Block":                          ("GF",   0x61D),

    "Lower Jail In Crate 1":                                  ("GF",   0x617),
    "Lower Jail In Crate 2":                                  ("GF",   0x618),

    "Outside Lower Jail Defeat Koopatrol Reward":             ("GF",   0x60D),
    "Outside Lower Jail Yellow Block":                        ("GF",   0x60B),

    "Lava Key Room In Chest":                                 ("GF",   0x613),

    "Lava Channel 3 On Island 1":                             ("GF",   0x611),
    "Lava Channel 3 On Island 2":                             ("GF",   0x612),

    "Dark Cave 1 Yellow Block":                               ("GF",   0x609),

    "Dark Cave 2 Yellow Block":                               ("GF",   0x60A),

    "East Upper Jail Defeat Koopatrol Reward":                ("GF",   0x627),

    "Item Shop Shop Item 1":                                  ("MF",   0x10A0),
    "Item Shop Shop Item 2":                                  ("MF",   0x10A1),
    "Item Shop Shop Item 3":                                  ("MF",   0x10A2),
    "Item Shop Shop Item 4":                                  ("MF",   0x10A3),
    "Item Shop Shop Item 5":                                  ("MF",   0x10A4),
    "Item Shop Shop Item 6":                                  ("MF",   0x10A5),

    "Left Water Puzzle Top Left Ledge":                       ("GF",   0x632),

    "Right Water Puzzle Hidden Block":                        ("GF",   0x637),

    "Room with Hidden Door 1 Hidden Block":                   ("GF",   0x62E),
    "Room with Hidden Door 1 Yellow Block":                   ("GF",   0x62D),

    "Hidden Key Room On The Ground":                          ("GF",   0x630),

    "Battlement On Ledge":                                    ("GF",   0x622),
    "Battlement Yellow Block Left":                           ("GF",   0x61F),
    "Battlement Yellow Block Center":                         ("GF",   0x620),
    "Battlement Yellow Block Right":                          ("GF",   0x621),

    "West Upper Jail Defeat Koopatrol Reward":                ("GF",   0x62A),

    "Ultra Shroom Room On The Ground":                        ("GF",   0x62C),

    "Castle Key Room On The Ground":                          ("GF",   0x62B),

    # Peach's Castle

    "Guest Room (1F) In Chest":                               ("GF",   0x1E7),

    "Library (2F) Upper Level":                               ("GF",   0x1F8),
    "Library (2F) Between Bookshelves":                       ("GF",   0x1E4),

    "Storeroom (2F) On The Ground":                           ("GF",   0x1E6),

    # Peach's Castle Grounds

    "Ruined Castle Grounds Muss T. Letter Reward":            ("MF",   0x10A6),
    "Hijacked Castle Entrance Hidden Block":                  ("GF",   0x66B),

}
