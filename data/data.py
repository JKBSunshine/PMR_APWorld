# https://github.com/icebound777/PMR-SeedGenerator/blob/main/docs/RAMLocations.md
from ..data.ItemList import item_table


# RDRAM Addresses
MODE_ADDRESS = 0x0A08F1  # Game Mode, checks if you're in a state to send/receive stuff
UIR_START_ADDRESS = 0x356B00  # Unique Item Registry
PD_START_ADDRESS = 0x10F290  # Player Data

# Location data
AREA_ADDRESS = 0x0740AB
MAP_ADDRESS = 0x0740B1

# ModByte Data
MB_START_ADDRESS = 0x356000
STAR_SPIRITS_COUNT = 0x356090
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
TABLE_ADDRESS = 0x1D00000
AUTH_ADDRESS = 0x1D00000 - 16

# ROM and RAM values
MAGIC_VALUE = b'PMDB'
GAME_MODE_WORLD = 4


def get_uir_address(name):
    item_id = item_table[name][2]
    return hex(UIR_START_ADDRESS + item_id)


def get_pd_address(name):
    return hex(PD_START_ADDRESS + name)


def get_mb_address(name):
    return hex(MB_START_ADDRESS + name)


def get_flag_value(flag_id, flag_bytes) -> bool:
    flag_offset = int(flag_id / 32) * 4
    flag_remainder = flag_id % 32

    byte_index = 3 - int(flag_remainder / 8)
    value = 2 ** (flag_remainder % 8)

    byte_start = flag_offset + byte_index

    for index, byte in enumerate(flag_bytes):
        if index == byte_start:
            return byte & value == value
    return False


# Location (spoiler log name)                    | Flag type and ID
# -----------------------------------------------+---------------------
checks_table = {
    "GR Forest Clearing Hidden Panel":                           ("GF",   0x056),

    "GR Goomba Village Bush Bottom Right":                       ("GF",   0x02F),
    "GR Goomba Village Goompa Koopa Koot Favor":                 ("GF",   0x064),
    "GR Goomba Village Goompa Gift":                             ("MF",   0x1000),
    "GR Goomba Village Goombaria Dolly Reward":                  ("MF",   0x1001),
    "GR Goomba Village Goompa Letter Reward":                    ("MF",   0x1002),
    "GR Goomba Village Goompapa Letter Reward 1":                ("MF",   0x1003),
    "GR Goomba Village Goompapa Letter Reward 2":                ("MF",   0x1004),
    "GR Goomba Village On The Balcony":                          ("GF",   0x02E),
    "GR Goomba Village Goombario Partner":                       ("MF",   0x1006),
    "GR Goomba Village Goomnut Tree":                            ("MF",   0x1005),

    "GR Behind the Village On Ledge":                            ("GF",   0x04A),
    "GR Behind the Village In Tree":                             ("GF",   0x049),

    "GR Bottom of the Cliff Hidden Panel":                       ("GF",   0x058),
    "GR Bottom of the Cliff Above Stone Block":                  ("GF",   0x034),
    "GR Bottom of the Cliff Floating Coin 1":                    ("GF",   0x038),
    "GR Bottom of the Cliff Floating Coin 2":                    ("GF",   0x039),
    "GR Bottom of the Cliff Floating Coin 3":                    ("GF",   0x03A),
    "GR Bottom of the Cliff Floating Coin 4":                    ("GF",   0x03B),
    "GR Bottom of the Cliff Upper Ledge":                        ("GF",   0x031),
    "GR Bottom of the Cliff In Tree":                            ("GF",   0x035),
    "GR Bottom of the Cliff Block On Ground":                    ("GF",   0x032),

    "GR Jr. Troopa's Playground Bush Right":                      ("GF",   0x03E),
    "GR Jr. Troopa's Playground Bush Bottom Right":               ("GF",   0x03F),
    "GR Jr. Troopa's Playground Bush Top 1":                      ("GF",   0x040),
    "GR Jr. Troopa's Playground Bush Top 2":                      ("GF",   0x041),
    "GR Jr. Troopa's Playground Bush Center":                     ("GF",   0x042),
    "GR Jr. Troopa's Playground Bush Top Left":                   ("GF",   0x043),
    "GR Jr. Troopa's Playground In Hammer Bush":                  ("MF",   0x1007),
    "GR Jr. Troopa's Playground In MultiCoinBlock":               ("GF",   0x046),
    "GR Jr. Troopa's Playground In Tree Left":                    ("GF",   0x03C),
    "GR Jr. Troopa's Playground In Tree Top":                     ("GF",   0x03D),
    "GR Jr. Troopa's Playground In Tree Right":                   ("GF",   0x01E),

    "GR Goomba Road 1 Yellow Block Left":                        ("GF",   0x04D),
    "GR Goomba Road 1 Yellow Block Right":                       ("GF",   0x04E),

    "GR Goomba Road 2 On the Sign":                              ("GF",   0x04F),
    "GR Goomba Road 2 Red Block":                                ("GF",   0x050),

    "GR Goomba King's Castle Hidden Panel":                       ("GF",   0x05A),
    "GR Goomba King's Castle In Tree Left Of Fortress":           ("GF",   0x052),
    "GR Goomba King's Castle In Tree Right Of Cliff":             ("GF",   0x053),
    "GR Goomba King's Castle Hidden Yellow Block":                ("GF",   0x051),

    "GR Toad Town Entrance Chest On Roof":                       ("GF",   0x054),
    "GR Toad Town Entrance Yellow Block":                        ("GF",   0x055),

    "GR Mario's House Luigi Koopa Koot Favor":                    ("GF",   0x063),

    # Toad Town

    "TT Gate District Dojo: Chan":                               ("MF",   0x100B),
    "TT Gate District Dojo: Lee":                                ("MF",   0x100C),
    "TT Gate District Dojo: Master 1":                           ("MF",   0x100D),
    "TT Gate District Dojo: Master 2":                           ("MF",   0x100E),
    "TT Gate District Dojo: Master 3":                           ("MF",   0x100F),
    "TT Gate District Russ T. Dictionary Reward":                ("GF",   0x0F4),
    "TT Gate District Russ T. Letter Reward":                    ("MF",   0x1008),
    "TT Gate District Miss T. Letter Reward":                    ("MF",   0x1009),
    "TT Gate District Radio Trade Event 1 Reward":               ("MF",   0x100A),
    "TT Gate District Hidden Panel":                             ("GF",   0x127),
    "TT Gate District Sushie Island":                            ("GF",   0x12D),
    "TT Gate District Shop Item 1":                              ("MF",   0x1010),
    "TT Gate District Shop Item 2":                              ("MF",   0x1011),
    "TT Gate District Shop Item 3":                              ("MF",   0x1012),
    "TT Gate District Shop Item 4":                              ("MF",   0x1013),
    "TT Gate District Shop Item 5":                              ("MF",   0x1014),
    "TT Gate District Shop Item 6":                              ("MF",   0x1015),

    "TT Plaza District Rowf's Calculator Reward":                 ("MF",   0x1016),
    "TT Plaza District Postmaster MailBag Reward":               ("GF",   0x10A),
    "TT Plaza District Merlon Letter Reward":                    ("MF",   0x1017),
    "TT Plaza District Minh T. Letter Reward":                   ("MF",   0x1018),
    "TT Plaza District Merlon House Stomping":                   ("GF",   0x0FF),
    "TT Plaza District Rowf's Shop Set 1 - 1":                    ("GF",   0x680),
    "TT Plaza District Rowf's Shop Set 1 - 2":                    ("GF",   0x681),
    "TT Plaza District Rowf's Shop Set 1 - 3":                    ("GF",   0x682),
    "TT Plaza District Rowf's Shop Set 1 - 4":                    ("GF",   0x683),
    "TT Plaza District Rowf's Shop Set 2 - 1":                    ("GF",   0x684),
    "TT Plaza District Rowf's Shop Set 2 - 2":                    ("GF",   0x685),
    "TT Plaza District Rowf's Shop Set 2 - 3":                    ("GF",   0x686),
    "TT Plaza District Rowf's Shop Set 3 - 1":                    ("GF",   0x687),
    "TT Plaza District Rowf's Shop Set 3 - 2":                    ("GF",   0x688),
    "TT Plaza District Rowf's Shop Set 3 - 3":                    ("GF",   0x689),
    "TT Plaza District Rowf's Shop Set 4 - 1":                    ("GF",   0x68A),
    "TT Plaza District Rowf's Shop Set 4 - 2":                    ("GF",   0x68B),
    "TT Plaza District Rowf's Shop Set 4 - 3":                    ("GF",   0x68C),
    "TT Plaza District Rowf's Shop Set 5 - 1":                    ("GF",   0x68D),
    "TT Plaza District Rowf's Shop Set 5 - 2":                    ("GF",   0x68E),
    "TT Plaza District Rowf's Shop Set 5 - 3":                    ("GF",   0x68F),
    "TT Plaza District In Tree":                                 ("GF",   0x12E),

    "TT Southern District Bub-ulb Gift":                         ("GF",   0x11B),
    "TT Southern District Tayce T. Frying Pan Reward":           ("MF",   0x1019),
    "TT Southern District Fice T. Letter Reward":                ("MF",   0x101A),
    "TT Southern District Fice T. Forest Pass":                  ("MF",   0x10AE),
    "TT Southern District Hidden Panel":                         ("GF",   0x129),
    "TT Southern District Inside Blue House":                    ("GF",   0x084),

    "TT Station District Dane T. Letter Reward 1":               ("MF",   0x101B),
    "TT Station District Dane T. Letter Reward 2":               ("MF",   0x101C),
    "TT Station District Hidden Panel":                          ("GF",   0x12A),

    "TT Residental District Storeroom Item 1":                   ("GF",   0x12F),
    "TT Residental District Storeroom Item 2":                   ("GF",   0x130),
    "TT Residental District Storeroom Item 3":                   ("GF",   0x121),
    "TT Residental District Storeroom Item 4":                   ("GF",   0x131),
    "TT Residental District Shop Item 1":                        ("MF",   0x101D),
    "TT Residental District Shop Item 2":                        ("MF",   0x101E),
    "TT Residental District Shop Item 3":                        ("MF",   0x101F),
    "TT Residental District Shop Item 4":                        ("MF",   0x1020),
    "TT Residental District Shop Item 5":                        ("MF",   0x1021),
    "TT Residental District Shop Item 6":                        ("MF",   0x1022),

    "TT Port District Poet Gift":                                ("GF",   0x125),
    "TT Port District Poet Melody Reward":                       ("GF",   0x126),
    "TT Port District Fishmael Letter Reward":                   ("MF",   0x1023),
    "TT Port District Radio Trade Event 3 Reward":               ("MF",   0x1024),
    "TT Port District Hidden Panel":                             ("GF",   0x12C),
    "TT Port District In MultiCoinBlock":                        ("GF",   0x132),

    # Toad Town Tunnels

    "TTT Hall to Blooper 1 (B1) Hidden Block":                    ("GF",   0x198),
    "TTT Hall to Blooper 1 (B1) In MultiCoinBlock":               ("GF",   0x199),

    "TTT Blooper Boss 1 (B1) Blooper Fight Reward":               ("GF",   0x18F),

    "TTT Short Elevator Room (B1) Yellow Block Center":           ("GF",   0x190),
    "TTT Short Elevator Room (B1) Yellow Block Left":             ("GF",   0x191),
    "TTT Short Elevator Room (B1) Yellow Block Right":            ("GF",   0x192),

    "TTT Spring Room (B2) Chest On Ledge":                        ("GF",   0x193),

    "TTT Elevator Attic Room (B2) On Parakarry Ledge":            ("GF",   0x194),
    "TTT Elevator Attic Room (B2) In SuperBlock":                 ("GF",   0x1B1),

    "TTT Metal Block Room (B3) In SuperBlock":                    ("GF",   0x1B3),

    "TTT Blue Pushblock Room (B2) Hidden Block Left":             ("GF",   0x195),
    "TTT Blue Pushblock Room (B2) Hidden Block Center":           ("GF",   0x196),
    "TTT Blue Pushblock Room (B2) Hidden Block Right":            ("GF",   0x197),
    "TTT Blue Pushblock Room (B2) In SuperBlock":                 ("GF",   0x1B2),

    "TTT Room with Spikes (B2) Yellow Block":                     ("GF",   0x19A),

    "TTT Winding Path (Spiny Room) Hidden Block Center":          ("GF",   0x1A0),
    "TTT Winding Path (Spiny Room) Hidden Block Right":           ("GF",   0x1A1),
    "TTT Winding Path (Spiny Room) Hidden Block Left":            ("GF",   0x1A2),
    "TTT Winding Path (Spiny Room) Yellow Block":                 ("GF",   0x1A3),

    "TTT Hall to Ultra Boots (B3) Hidden Block":                  ("GF",   0x1A4),
    "TTT Hall to Ultra Boots (B3) Yellow Block Left":             ("GF",   0x1A5),
    "TTT Hall to Ultra Boots (B3) Yellow Block Right":            ("GF",   0x1A6),

    "TTT Ultra Boots Room (B3) In Big Chest":                     ("GF",   0x1A7),

    "TTT Bridge to Shiver City (B2) Yellow Block 1":              ("GF",   0x19B),
    "TTT Bridge to Shiver City (B2) Yellow Block 2":              ("GF",   0x19C),
    "TTT Bridge to Shiver City (B2) Yellow Block 3":              ("GF",   0x19D),
    "TTT Bridge to Shiver City (B2) Yellow Block 4":              ("GF",   0x19E),
    "TTT Bridge to Shiver City (B2) Yellow Block 5":              ("GF",   0x19F),

    "TTT Frozen Room (B3) In SuperBlock":                         ("GF",   0x1B4),

    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 1":               ("MF",   0x102C),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 2":               ("MF",   0x102D),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 3":               ("MF",   0x102E),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 4":               ("MF",   0x102F),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 5":               ("MF",   0x1030),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 6":               ("MF",   0x1031),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 7":               ("MF",   0x1032),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 8":               ("MF",   0x1033),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 9":               ("MF",   0x1034),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 10":              ("MF",   0x1035),
    "TTT Rip Cheato's Home (B3) Rip Cheato Offer 11":              ("MF",   0x1036),

    "TTT Under the Toad Town Pond In SuperBlock":                 ("GF",   0x1B5),

    # Shooting Star Summit

    "SSS Shooting Star Path Hidden Panel":                        ("GF",   0x21A),

    "SSS Merluvlee's House Merluvlee Koopa Koot Favor":            ("GF",   0x219),
    "SSS Merluvlee's House Merlow Letter Reward":                  ("MF",   0x102B),
    "SSS Merluvlee's House Hidden Panel":                          ("GF",   0x21C),
    "SSS Merluvlee's House Merlow's Badges 1":                      ("GF",   0x6EB),
    "SSS Merluvlee's House Merlow's Badges 2":                      ("GF",   0x6EC),
    "SSS Merluvlee's House Merlow's Badges 3":                      ("GF",   0x6ED),
    "SSS Merluvlee's House Merlow's Badges 4":                      ("GF",   0x6EE),
    "SSS Merluvlee's House Merlow's Badges 5":                      ("GF",   0x6EF),
    "SSS Merluvlee's House Merlow's Badges 6":                      ("GF",   0x6F0),
    "SSS Merluvlee's House Merlow's Badges 7":                      ("GF",   0x6F1),
    "SSS Merluvlee's House Merlow's Badges 8":                      ("GF",   0x6F2),
    "SSS Merluvlee's House Merlow's Badges 9":                      ("GF",   0x6F3),
    "SSS Merluvlee's House Merlow's Badges 10":                     ("GF",   0x6F4),
    "SSS Merluvlee's House Merlow's Badges 11":                     ("GF",   0x6F5),
    "SSS Merluvlee's House Merlow's Badges 12":                     ("GF",   0x6F6),
    "SSS Merluvlee's House Merlow's Badges 13":                     ("GF",   0x6F7),
    "SSS Merluvlee's House Merlow's Badges 14":                     ("GF",   0x6F8),
    "SSS Merluvlee's House Merlow's Badges 15":                     ("GF",   0x6F9),
    "SSS Merluvlee's House Merlow's Rewards 1":                     ("MF",   0x10A8),
    "SSS Merluvlee's House Merlow's Rewards 2":                     ("MF",   0x10A9),
    "SSS Merluvlee's House Merlow's Rewards 3":                     ("MF",   0x10AA),
    "SSS Merluvlee's House Merlow's Rewards 4":                     ("MF",   0x10AB),
    "SSS Merluvlee's House Merlow's Rewards 5":                     ("MF",   0x10AC),
    "SSS Merluvlee's House Merlow's Rewards 6":                     ("MF",   0x10AD),

    "SSS Shooting Star Summit Hidden Panel":                      ("GF",   0x21B),
    "SSS Shooting Star Summit Behind The Summit":                 ("GF",   0x220),

    "SSS Star Haven Shop Item 1":                                 ("MF",   0x1025),
    "SSS Star Haven Shop Item 2":                                 ("MF",   0x1026),
    "SSS Star Haven Shop Item 3":                                 ("MF",   0x1027),
    "SSS Star Haven Shop Item 4":                                 ("MF",   0x1028),
    "SSS Star Haven Shop Item 5":                                 ("MF",   0x1029),
    "SSS Star Haven Shop Item 6":                                 ("MF",   0x102A),

    "SSS Star Sanctuary Gift of the Stars":                       ("MF", 0x81),

    # Koopa Region

    "KR Pleasant Path Entry Red Block Center":                   ("GF",   0x253),
    "KR Pleasant Path Entry Yellow Block Left":                  ("GF",   0x252),
    "KR Pleasant Path Entry Yellow Block Right":                 ("GF",   0x254),

    "KR Pleasant Path Bridge Kooper Island":                     ("GF",   0x244),
    "KR Pleasant Path Bridge Behind Fence":                      ("GF",   0x267),
    "KR Pleasant Path Bridge In MultiCoinBlock":                 ("GF",   0x258),
    "KR Pleasant Path Bridge Yellow Block":                      ("GF",   0x255),

    "KR Pleasant Crossroads Hidden Panel":                       ("GF",   0x260),
    "KR Pleasant Crossroads Behind Peg":                         ("GF",   0x268),
    "KR Pleasant Crossroads Brick Block Puzzle":                 ("GF",   0x256),

    "KR Path to Fortress 1 Hidden Panel":                        ("GF",   0x261),
    "KR Path to Fortress 1 Hidden Block":                        ("GF",   0x257),
    "KR Path to Fortress 1 X On Ground 1":                       ("GF",   0x246),
    "KR Path to Fortress 1 X On Ground 2":                       ("GF",   0x247),
    "KR Path to Fortress 1 X On Ground 3":                       ("GF",   0x248),
    "KR Path to Fortress 1 X On Ground 4":                       ("GF",   0x249),
    "KR Path to Fortress 1 X On Ground 5":                       ("GF",   0x24A),
    "KR Path to Fortress 1 On Brick Block":                      ("GF",   0x245),

    "KR Path to Fortress 2 In Tree":                             ("GF",   0x251),

    "KR Koopa Village 1 Bush Far Left":                          ("GF",   0x24C),
    "KR Koopa Village 1 Bush Left Front":                        ("GF",   0x24D),
    "KR Koopa Village 1 Bush Infront Of Tree":                   ("MF",   0x1049),
    "KR Koopa Village 1 Bush Second From Right":                 ("GF",   0x24F),
    "KR Koopa Village 1 Bush Second From Left (Koopa Koot Favor)": ("GF",   0x263),
    "KR Koopa Village 1 Bush Far Right (Koopa Koot Favor)":      ("GF",   0x264),
    "KR Koopa Village 1 Mort T. Letter Reward":                  ("MF",   0x1037),
    "KR Koopa Village 1 Koover Letter Reward 1":                 ("MF",   0x1038),
    "KR Koopa Village 1 Koover Letter Reward 2":                 ("MF",   0x1039),
    "KR Koopa Village 1 Hidden Panel":                           ("GF",   0x25E),
    "KR Koopa Village 1 Shop Item 1":                            ("MF",   0x103A),
    "KR Koopa Village 1 Shop Item 2":                            ("MF",   0x103B),
    "KR Koopa Village 1 Shop Item 3":                            ("MF",   0x103C),
    "KR Koopa Village 1 Shop Item 4":                            ("MF",   0x103D),
    "KR Koopa Village 1 Shop Item 5":                            ("MF",   0x103E),
    "KR Koopa Village 1 Shop Item 6":                            ("MF",   0x103F),

    "KR Koopa Village 2 Bush Far Left":                          ("MF",   0x104A),
    "KR Koopa Village 2 Bush Far Right":                         ("MF",   0x10A7),
    "KR Koopa Village 2 Kolorado's Wife (Koopa Koot Favor)":      ("GF",   0x265),
    "KR Koopa Village 2 Koopa Koot Silver Credit":               ("MF",   0x1040),
    "KR Koopa Village 2 Koopa Koot Gold Credit":                 ("MF",   0x1041),
    "KR Koopa Village 2 Kolorado Artifact Reward":               ("GF",   0x312),
    "KR Koopa Village 2 Kolorado Letter Reward":                 ("MF",   0x1042),
    "KR Koopa Village 2 Push Block Puzzle":                      ("GF",   0x243),
    "KR Koopa Village 2 Koopa Koot Reward 1":                    ("GF",   0x6AD),
    "KR Koopa Village 2 Koopa Koot Reward 2":                    ("GF",   0x6B0),
    "KR Koopa Village 2 Koopa Koot Reward 3":                    ("GF",   0x6B3),
    "KR Koopa Village 2 Koopa Koot Reward 4":                    ("GF",   0x6B6),
    "KR Koopa Village 2 Koopa Koot Reward 5":                    ("GF",   0x6B9),
    "KR Koopa Village 2 Koopa Koot Reward 6":                    ("GF",   0x6BC),
    "KR Koopa Village 2 Koopa Koot Reward 7":                    ("GF",   0x6BF),
    "KR Koopa Village 2 Koopa Koot Reward 8":                    ("GF",   0x6C2),
    "KR Koopa Village 2 Koopa Koot Reward 9":                    ("GF",   0x6C5),
    "KR Koopa Village 2 Koopa Koot Reward 10":                   ("GF",   0x6C8),
    "KR Koopa Village 2 Koopa Koot Reward 11":                   ("GF",   0x6CB),
    "KR Koopa Village 2 Koopa Koot Reward 12":                   ("GF",   0x6CE),
    "KR Koopa Village 2 Koopa Koot Reward 13":                   ("GF",   0x6D1),
    "KR Koopa Village 2 Koopa Koot Reward 14":                   ("GF",   0x6D4),
    "KR Koopa Village 2 Koopa Koot Reward 15":                   ("GF",   0x6D7),
    "KR Koopa Village 2 Koopa Koot Reward 16":                   ("GF",   0x6DA),
    "KR Koopa Village 2 Koopa Koot Reward 17":                   ("GF",   0x6DD),
    "KR Koopa Village 2 Koopa Koot Reward 18":                   ("GF",   0x6E0),
    "KR Koopa Village 2 Koopa Koot Reward 19":                   ("GF",   0x6E3),
    "KR Koopa Village 2 Koopa Koot Reward 20":                   ("GF",   0x6E6),
    "KR Koopa Village 2 Kooper Partner":                         ("MF",   0x1043),

    "KR Behind Koopa Village On Stump":                          ("GF",   0x242),

    "KR Fuzzy Forest Fuzzy Battle Reward":                       ("MF",   0x1044),

    # Koopa Bros Fortress

    "KBF Fortress Exterior Chest Behind Fortress":                ("GF",   0x281),
    "KBF Fortress Exterior Chest On Ledge":                       ("GF",   0x282),

    "KBF Left Tower Top Of Tower":                                ("GF",   0x27E),
    "KBF Left Tower Koopa Troopa Reward":                         ("GF",   0x285),

    "KBF Central Hall Left Cell":                                 ("GF",   0x286),
    "KBF Central Hall Right Cell":                                ("GF",   0x287),
    "KBF Central Hall Center Cell":                               ("GF",   0x27F),

    "KBF Jail Bombette Partner":                                  ("MF",   0x1045),

    "KBF Dungeon Fire Room On The Ground":                        ("GF",   0x288),

    "KBF Battlement Block Behind Rock":                           ("GF",   0x280),

    # Mt Rugged

    "MR Train Station Bush 1":                                   ("GF",   0x2C5),
    "MR Train Station Bush 2":                                   ("GF",   0x2C6),
    "MR Train Station Bush 3":                                   ("GF",   0x2C7),
    "MR Train Station Bush Top":                                 ("MF",   0x1047),
    "MR Train Station Parakarry Partner":                        ("MF",   0x1048),
    "MR Train Station In SuperBlock":                            ("GF",   0x2D1),

    "MR Mt Rugged 1 On Slide 1":                                 ("GF",   0x2B3),
    "MR Mt Rugged 1 On Slide 2":                                 ("GF",   0x2B4),
    "MR Mt Rugged 1 On Slide 3":                                 ("GF",   0x2B5),
    "MR Mt Rugged 1 Hurting Whacka":                             ("MF",   0x1046),
    "MR Mt Rugged 1 Yellow Block":                               ("GF",   0x2CB),

    "MR Mt Rugged 2 Hidden Panel":                               ("GF",   0x2CD),
    "MR Mt Rugged 2 Parakarry Ledge":                            ("GF",   0x2AE),
    "MR Mt Rugged 2 Kooper Ledge":                               ("GF",   0x2C1),

    "MR Mt Rugged 3 Bub-ulb Gift":                               ("GF",   0x2CC),
    "MR Mt Rugged 3 On Scaffolding":                             ("GF",   0x2AF),

    "MR Mt Rugged 4 Hidden Cave Chest":                          ("GF",   0x2B1),
    "MR Mt Rugged 4 Slide Ledge":                                ("GF",   0x2C2),
    "MR Mt Rugged 4 Left Ledge Center":                          ("GF",   0x2B0),
    "MR Mt Rugged 4 Left Ledge Right":                           ("GF",   0x2B8),
    "MR Mt Rugged 4 Left Ledge 3":                               ("GF",   0x2B9),
    "MR Mt Rugged 4 Left Ledge 4":                               ("GF",   0x2BA),
    "MR Mt Rugged 4 Left Ledge 5":                               ("GF",   0x2BB),
    "MR Mt Rugged 4 Left Ledge 6":                               ("GF",   0x2BC),
    "MR Mt Rugged 4 Left Ledge 7":                               ("GF",   0x2BD),
    "MR Mt Rugged 4 Bottom Left 1":                              ("GF",   0x2B6),
    "MR Mt Rugged 4 Bottom Left 2":                              ("GF",   0x2B7),
    "MR Mt Rugged 4 Yellow Block Top Left":                      ("GF",   0x2BE),
    "MR Mt Rugged 4 Yellow Block Floating":                      ("GF",   0x2BF),
    "MR Mt Rugged 4 Yellow Block Top Right":                     ("GF",   0x2C0),

    "MR Suspension Bridge Bottom Of Cliff":                      ("GF",   0x2C3),

    # Dry Dry Desert

    "DDD N3W3 Yellow Block Left":                                 ("GF",   0x31D),
    "DDD N3W3 Yellow Block Right":                                ("GF",   0x31E),

    "DDD N3W1 Ruins Entrance Radio Trade Event 2 Reward":         ("MF",   0x1054),

    "DDD N3E2 Pokey Army Behind Cactus":                          ("GF",   0x33F),

    "DDD N3E3 In Tree":                                           ("GF",   0x345),
    "DDD N3E3 In MultiCoinBlock":                                 ("GF",   0x330),

    "DDD N2W3 Hidden Block":                                      ("GF",   0x31F),

    "DDD N2E1 (Tweester A) Yellow Block Left":                    ("GF",   0x320),
    "DDD N2E1 (Tweester A) Yellow Block Right":                   ("GF",   0x321),
    "DDD N2E1 (Tweester A) In MultiCoinBlock":                    ("GF",   0x331),

    "DDD N1W3 Special Block Hit Block":                           ("GF",   0x322),
    "DDD N1W3 Special Block Hit Block Plenty":                    ("GF",   0x323),
    "DDD N1W3 Special Block Hit Block Very Much":                 ("GF",   0x324),

    "DDD N1W1 Yellow Block 1":                                    ("GF",   0x325),
    "DDD N1W1 Yellow Block 2":                                    ("GF",   0x326),
    "DDD N1W1 Yellow Block 3":                                    ("GF",   0x327),
    "DDD N1W1 Yellow Block 4":                                    ("GF",   0x328),
    "DDD N1W1 Yellow Block Center":                               ("GF",   0x329),

    "DDD N1E1 Palm Trio Hidden Block":                            ("GF",   0x32A),

    "DDD N1E2 In MultiCoinBlock Center":                          ("GF",   0x332),
    "DDD N1E2 In MultiCoinBlock Bottom Right":                    ("GF",   0x333),

    "DDD N1E3 In Tree":                                           ("GF",   0x346),

    "DDD W3 Kolorado's Camp In Tree":                              ("GF",   0x340),

    "DDD Center (Tweester C) Hidden Panel":                       ("GF",   0x31C),

    "DDD E1 Nomadimouse Nomadimouse Letter Reward":               ("MF",   0x1055),
    "DDD E1 Nomadimouse In Tree":                                 ("GF",   0x347),

    "DDD E2 In Tree Far Left":                                    ("GF",   0x348),

    "DDD E3 Outside Outpost In Tree (Far Left)":                  ("GF",   0x349),
    "DDD E3 Outside Outpost In Tree (Second From Left)":          ("GF",   0x34A),
    "DDD E3 Outside Outpost In Tree (Fourth From Right)":         ("GF",   0x34B),
    "DDD E3 Outside Outpost In Tree (Far Right)":                 ("GF",   0x341),

    "DDD S1W3 In MultiCoinBlock Top Left":                        ("GF",   0x334),

    "DDD S1 Yellow Block":                                        ("GF",   0x32B),

    "DDD S1E2 Small Bluffs On Brick Block":                       ("GF",   0x343),
    "DDD S1E2 Small Bluffs Ontop Of Bluffs":                      ("GF",   0x342),

    "DDD S1E3 North of Oasis Hidden Block":                       ("GF",   0x32D),
    "DDD S1E3 North of Oasis Tree Bottom Left":                   ("GF",   0x34C),
    "DDD S1E3 North of Oasis Yellow Block":                       ("GF",   0x32C),

    "DDD S2W1 In MultiCoinBlock Top":                             ("GF", 0x335),

    "DDD S2E2 West of Oasis Behind Bush":                         ("GF",   0x344),
    "DDD S2E2 West of Oasis In Tree":                             ("GF",   0x34D),
    "DDD S2E2 West of Oasis In MultiCoinBlock":                   ("GF",   0x336),

    "DDD S2E3 Oasis In Fruit Tree (Left)":                        ("MF",   0x1056),
    "DDD S2E3 Oasis In Fruit Tree (Right)":                       ("MF",   0x1057),
    "DDD S2E3 Oasis In Tree (Far Left)":                          ("GF",   0x34E),
    "DDD S2E3 Oasis In Tree (Front Right)":                       ("GF",   0x34F),
    "DDD S2E3 Oasis In SuperBlock":                               ("GF",   0x33D),

    "DDD S3W2 Hidden AttackFX Hidden Block":                      ("GF",   0x32E),

    "DDD S3E1 Yellow Block":                                      ("GF",   0x32F),

    "DDD S3E3 South of Oasis In Tree (Far Right)":                ("GF",   0x350),
    "DDD S3E3 South of Oasis In MultiCoinBlock Top Left":         ("GF",   0x337),
    "DDD S3E3 South of Oasis In MultiCoinBlock Top Right":        ("GF",   0x338),
    "DDD S3E3 South of Oasis In MultiCoinBlock Right":            ("GF",   0x339),
    "DDD S3E3 South of Oasis In MultiCoinBlock Left":             ("GF",   0x33A),
    "DDD S3E3 South of Oasis In MultiCoinBlock Bottom Left":      ("GF",   0x33B),
    "DDD S3E3 South of Oasis In MultiCoinBlock Bottom Right":     ("GF",   0x33C),

    # Dry Dry Outpost

    "DDO Outpost 1 Composer Lyrics Reward":                       ("GF",   0x2F2),
    "DDO Outpost 1 Store Legend":                                 ("GF",   0x2F6),
    "DDO Outpost 1 Little Mouser Letter Reward":                  ("MF",   0x104B),
    "DDO Outpost 1 Shop Item 1":                                  ("MF",   0x104C),
    "DDO Outpost 1 Shop Item 2":                                  ("MF",   0x104D),
    "DDO Outpost 1 Shop Item 3":                                  ("MF",   0x104E),
    "DDO Outpost 1 Shop Item 4":                                  ("MF",   0x104F),
    "DDO Outpost 1 Shop Item 5":                                  ("MF",   0x1050),
    "DDO Outpost 1 Shop Item 6":                                  ("MF",   0x1051),
    "DDO Outpost 1 In Red Tree":                                  ("GF",   0x2F8),

    "DDO Outpost 2 Merlee Request (Koopa Koot Favor)":            ("GF",   0x2F7),
    "DDO Outpost 2 Moustafa Gift":                                ("MF",   0x1052),
    "DDO Outpost 2 Mr. E. Letter Reward":                         ("MF",   0x1053),
    "DDO Outpost 2 Hidden Panel":                                 ("GF",   0x2F4),
    "DDO Outpost 2 Toad House Roof":                              ("GF",   0x2F5),

    # Dry Dry Ruins

    "DDR Sarcophagus Hall 1 In Sarcophagus":                      ("GF",   0x694),

    "DDR Sand Drainage Room 1 On The Ground":                     ("GF",   0x367),

    "DDR Sand Drainage Room 2 In The Sand":                       ("GF",   0x375),
    "DDR Sand Drainage Room 2 On Ledge":                          ("GF",   0x36A),

    "DDR Pyramid Stone Room On Pedestal":                         ("GF",   0x372),

    "DDR Sarcophagus Hall 2 Pokey Gauntlet Reward":               ("GF",   0x36B),
    "DDR Sarcophagus Hall 2 Behind Hammer Block":                 ("GF",   0x374),

    "DDR Super Hammer Room In Big Chest":                         ("GF",   0x384),
    "DDR Super Hammer Room Hidden Chest":                         ("GF",   0x385),

    "DDR Vertical Shaft In SuperBlock":                           ("GF",   0x387),

    "DDR Diamond Stone Room On Pedestal":                         ("GF",   0x373),

    "DDR Sand Drainage Room 3 On Ledge":                          ("GF",   0x377),

    "DDR Lunar Stone Room On Pedestal":                           ("GF",   0x371),

    # Forever Forest

    "FOR Tree Face (Bub-ulb) Bub-ulb Gift":                       ("GF",   0x3A2),
    "FOR Bee Hive (HP Plus) Central Block":                       ("GF",   0x39D),
    "FOR Flowers Appear (FP Plus) Central Block":                 ("GF",   0x39E),
    "FOR Outside Boo's Mansion In Bush (Back Right)":              ("MF",   0x1058),
    "FOR Outside Boo's Mansion Yellow Block":                      ("GF",   0x3A7),
    "FOR Exit to Gusty Gulch Hidden Panel":                       ("GF",   0x3A5),

    # Boo's Mansion

    "BM Foyer From Franky (Koopa Koot Favor)":                   ("GF",   0x3BF),
    "BM Foyer Franky Letter Reward":                             ("MF",   0x1059),
    "BM Foyer Hidden Panel":                                     ("GF",   0x3C1),

    "BM Basement Stairs Hidden Panel":                           ("GF",   0x3C4),

    "BM Basement In Crate":                                      ("GF",   0x3C5),
    "BM Basement Igor Letter Reward":                            ("MF",   0x105A),
    "BM Basement Shop Item 1":                                   ("MF",   0x105B),
    "BM Basement Shop Item 2":                                   ("MF",   0x105C),
    "BM Basement Shop Item 3":                                   ("MF",   0x105D),
    "BM Basement Shop Item 4":                                   ("MF",   0x105E),
    "BM Basement Shop Item 5":                                   ("MF",   0x105F),
    "BM Basement Shop Item 6":                                   ("MF",   0x1060),

    "BM Super Boots Room In Big Chest":                          ("GF",   0x3C7),
    "BM Super Boots Room In Crate":                              ("GF",   0x3CA),
    "BM Super Boots Room Hidden Panel":                          ("GF",   0x3CC),

    "BM Pot Room In Crate 1":                                    ("MF",   0x1061),
    "BM Pot Room In Crate 2":                                    ("MF",   0x1062),

    "BM Library In Crate":                                       ("GF",   0x3D0),
    "BM Library On Bookshelf":                                   ("GF",   0x3CF),

    "BM Record Player Room In Chest":                            ("GF",   0x3D2),

    "BM Record Room Hidden Panel":                               ("GF",   0x3D4),
    "BM Record Room Beat Boo Game":                              ("GF",   0x3D3),

    "BM Lady Bow's Room Bow Partner":                             ("MF",   0x1063),

    # Gusty Gulch

    "GG Ghost Town 1 From Boo (Koopa Koot Favor)":               ("GF",   0x3F7),
    "GG Ghost Town 1 Yellow Block In House":                     ("GF",   0x3EF),

    "GG Wasteland Ascent 1 On Rock":                             ("GF",   0x3ED),
    "GG Wasteland Ascent 1 Infront Of Branch":                   ("GF",   0x3EE),
    "GG Wasteland Ascent 1 Yellow Block 1":                      ("GF",   0x3EA),
    "GG Wasteland Ascent 1 Yellow Block 2":                      ("GF",   0x3EB),
    "GG Wasteland Ascent 1 Yellow Block Right":                  ("GF",   0x3EC),

    "GG Wasteland Ascent 2 Behind Rock":                         ("GF",   0x3FB),
    "GG Wasteland Ascent 2 In MultiCoinBlock":                   ("GF",   0x3F2),
    "GG Wasteland Ascent 2 Yellow Block Left":                   ("GF",   0x3F0),
    "GG Wasteland Ascent 2 Yellow Block Right":                  ("GF",   0x3F1),

    # Tubba's Castle

    "TC Covered Tables Room (1F) On Table":                      ("GF",   0x41F),

    "TC Study (1F) On Table":                                    ("GF",   0x41A),

    "TC Table/Clock Room (1/2F) On Table":                       ("GF",   0x412),

    "TC Basement In Chest":                                      ("GF",   0x418),

    "TC Stairs to Basement In SuperBlock":                       ("GF",   0x416),

    "TC Spike Trap Room (2F) In Chest":                          ("GF",   0x421),

    "TC Hidden Bedroom (2F) In Hidden Room":                     ("GF",   0x422),
    "TC Hidden Bedroom (2F) On Bed 1":                           ("GF",   0x423),
    "TC Hidden Bedroom (2F) On Bed 2":                           ("GF",   0x424),
    "TC Hidden Bedroom (2F) On Bed 3":                           ("GF",   0x425),
    "TC Hidden Bedroom (2F) On Bed 4":                           ("GF",   0x426),
    "TC Hidden Bedroom (2F) On Bed 5":                           ("GF",   0x427),
    "TC Hidden Bedroom (2F) On Bed 6":                           ("GF",   0x428),

    "TC Stairs to Third Floor Yellow Block":                     ("GF",   0x429),

    "TC Sleeping Clubbas Room (3F) On Pedestal":                 ("GF",   0x42D),

    # Shy Guys Toybox

    "SGT BLU Station Hidden Panel":                               ("GF",   0x4A6),
    "SGT BLU Station Hidden Block":                               ("GF",   0x45D),

    "SGT BLU Anti-Guy Hall In Chest":                             ("GF",   0x49F),
    "SGT BLU Anti-Guy Hall Hidden Block":                         ("GF",   0x4A1),
    "SGT BLU Anti-Guy Hall Yellow Block":                         ("GF",   0x4A0),

    "SGT BLU Large Playroom Hidden Block 1":                      ("GF",   0x456),
    "SGT BLU Large Playroom Hidden Block 2":                      ("GF",   0x457),
    "SGT BLU Large Playroom Calculator Thief 1":                  ("GF",   0x454),
    "SGT BLU Large Playroom Calculator Thief 2":                  ("MF",   0x1064),
    "SGT BLU Large Playroom Shy Guy 2":                           ("MF",   0x1065),
    "SGT BLU Large Playroom Shy Guy 3":                           ("MF",   0x1066),
    "SGT BLU Large Playroom Shy Guy 4":                           ("MF",   0x1067),
    "SGT BLU Large Playroom Shy Guy 5":                           ("MF",   0x1068),

    "SGT BLU Block City In Chest":                                ("GF",   0x45F),
    "SGT BLU Block City Infront Of Chest":                        ("GF",   0x44E),
    "SGT BLU Block City Midair 1":                                ("GF",   0x463),
    "SGT BLU Block City Midair 2":                                ("GF",   0x464),
    "SGT BLU Block City Midair 3":                                ("GF",   0x465),
    "SGT BLU Block City Midair 4":                                ("GF",   0x466),
    "SGT BLU Block City Midair 5":                                ("GF",   0x467),
    "SGT BLU Block City Midair 6":                                ("GF",   0x468),
    "SGT BLU Block City Midair 7":                                ("GF",   0x469),
    "SGT BLU Block City Midair 8":                                ("GF",   0x46A),
    "SGT BLU Block City On Building":                             ("GF",   0x46C),
    "SGT BLU Block City Behind Building Block":                   ("GF",   0x46D),
    "SGT BLU Block City Yellow Block 1":                          ("GF",   0x460),
    "SGT BLU Block City Yellow Block 2":                          ("GF",   0x461),
    "SGT BLU Block City Yellow Block On Ledge":                   ("GF",   0x462),

    "SGT PNK Station In Chest":                                   ("GF",   0x472),
    "SGT PNK Station Hidden Panel":                               ("GF",   0x4A7),
    "SGT PNK Station Hidden Block":                               ("GF",   0x473),

    "SGT PNK Tracks Hallway In MultiCoinBlock":                   ("GF",   0x4A5),
    "SGT PNK Tracks Hallway Yellow Block South":                  ("GF",   0x4A2),
    "SGT PNK Tracks Hallway Yellow Block North 1":                ("GF",   0x4A3),
    "SGT PNK Tracks Hallway Yellow Block North 2":                ("GF",   0x4A4),

    "SGT PNK Gourmet Guy Crossing Hidden Block Right":            ("GF",   0x470),
    "SGT PNK Gourmet Guy Crossing Hidden Block Left":             ("GF",   0x471),
    "SGT PNK Gourmet Guy Crossing Gourmet Guy Reward":            ("GF",   0x452),
    "SGT PNK Gourmet Guy Crossing Yellow Block 1":                ("GF",   0x46E),
    "SGT PNK Gourmet Guy Crossing Yellow Block 2":                ("GF",   0x46F),

    "SGT PNK Playhouse In Chest (Far Right)":                     ("GF",   0x476),
    "SGT PNK Playhouse In Chest (Top Left)":                      ("GF",   0x477),
    "SGT PNK Playhouse In Chest (Right)":                         ("GF",   0x478),
    "SGT PNK Playhouse Infront Of Chest (Right)":                 ("GF",   0x44F),
    "SGT PNK Playhouse Yellow Block":                             ("GF",   0x475),

    "SGT GRN Station Hidden Panel":                               ("GF",   0x4A8),
    "SGT GRN Station Hidden Block":                               ("GF",   0x479),

    "SGT GRN Treadmills/Slot Machine In Chest":                   ("GF",   0x47B),
    "SGT GRN Treadmills/Slot Machine Infront Of Chest":           ("GF",   0x450),
    "SGT GRN Treadmills/Slot Machine On Treadmill 1":             ("GF",   0x47E),
    "SGT GRN Treadmills/Slot Machine On Treadmill 2":             ("GF",   0x47F),
    "SGT GRN Treadmills/Slot Machine On Treadmill 3":             ("GF",   0x480),
    "SGT GRN Treadmills/Slot Machine On Treadmill 4":             ("GF",   0x481),
    "SGT GRN Treadmills/Slot Machine On Treadmill 5":             ("GF",   0x482),
    "SGT GRN Treadmills/Slot Machine On Treadmill 6":             ("GF",   0x483),
    "SGT GRN Treadmills/Slot Machine Hidden Room Center":         ("GF",   0x496),
    "SGT GRN Treadmills/Slot Machine Hidden Room 1":              ("GF",   0x488),
    "SGT GRN Treadmills/Slot Machine Hidden Room 2":              ("GF",   0x489),
    "SGT GRN Treadmills/Slot Machine Hidden Room 3":              ("GF",   0x48D),
    "SGT GRN Treadmills/Slot Machine Hidden Room 4":              ("GF",   0x48E),
    "SGT GRN Treadmills/Slot Machine Hidden Room 5":              ("GF",   0x492),
    "SGT GRN Treadmills/Slot Machine Hidden Room 6":              ("GF",   0x493),
    "SGT GRN Treadmills/Slot Machine Defeat Shy Guy":             ("GF",   0x47D),
    "SGT GRN Treadmills/Slot Machine In MultiCoinBlock":          ("GF",   0x497),

    "SGT RED Station Hidden Panel":                               ("GF",   0x4A9),
    "SGT RED Station Hidden Block":                               ("GF",   0x498),

    "SGT RED Moving Platforms Hidden Block Center":               ("GF",   0x49A),
    "SGT RED Moving Platforms Hidden Block Right":                ("GF",   0x49D),
    "SGT RED Moving Platforms Hidden Block Left":                 ("GF",   0x49E),
    "SGT RED Moving Platforms In SuperBlock":                     ("GF",   0x4AA),
    "SGT RED Moving Platforms In MultiCoinBlock":                 ("GF",   0x499),
    "SGT RED Moving Platforms Yellow Block 1":                    ("GF",   0x49C),
    "SGT RED Moving Platforms Yellow Block 2":                    ("GF",   0x49B),

    "SGT RED Lantern Ghost Watt Partner":                         ("MF",   0x1069),

    "SGT RED Boss Barricade Hidden Block Left":                   ("GF",   0x45B),
    "SGT RED Boss Barricade On Brick Block":                      ("GF",   0x45C),
    "SGT RED Boss Barricade Yellow Block Right":                  ("GF",   0x45A),

    # Jade Jungle

    "JJ Whale Cove Over Flower 1":                               ("GF",   0x4C0),
    "JJ Whale Cove Over Flower 2":                               ("GF",   0x4C1),
    "JJ Whale Cove Behind Bush":                                 ("GF",   0x4C3),
    "JJ Whale Cove In Palm Tree":                                ("MF",   0x106A),

    "JJ Beach Hidden Block Left":                                ("GF",   0x4DE),
    "JJ Beach Hidden Block Right":                               ("GF",   0x4DF),
    "JJ Beach On The Rocks":                                     ("GF",   0x4C6),
    "JJ Beach Over Flower 1":                                    ("GF",   0x4C5),
    "JJ Beach Over Flower 2":                                    ("GF",   0x4FD),
    "JJ Beach In Palm Tree 1":                                   ("MF",   0x106B),
    "JJ Beach In Palm Tree 2":                                   ("MF",   0x106C),
    "JJ Beach In Palm Tree 3":                                   ("MF",   0x106D),
    "JJ Beach In Palm Tree 4":                                   ("MF",   0x106E),
    "JJ Beach In Palm Tree 5":                                   ("MF",   0x106F),
    "JJ Beach In Palm Tree 6 One-Off":                           ("GF",   0x4E4),
    "JJ Beach In Palm Tree 6 Replenishing":                      ("MF",   0x1070),

    "JJ Village Cove Village Leader Reward":                     ("MF",   0x1071),
    "JJ Village Cove Hidden Panel":                              ("GF",   0x4F5),
    "JJ Village Cove In Palm Tree Left":                         ("MF",   0x1072),
    "JJ Village Cove In Palm Tree Right":                        ("MF",   0x1073),

    "JJ Village Buildings Kolorado Volcano Vase Reward":         ("GF",   0x4FB),
    "JJ Village Buildings Yellow Yoshi Food Reward":             ("MF",   0x107A),
    "JJ Village Buildings Red Yoshi Kid Letter Reward":          ("MF",   0x107B),
    "JJ Village Buildings Shop Item 1":                          ("MF",   0x1074),
    "JJ Village Buildings Shop Item 2":                          ("MF",   0x1075),
    "JJ Village Buildings Shop Item 3":                          ("MF",   0x1076),
    "JJ Village Buildings Shop Item 4":                          ("MF",   0x1077),
    "JJ Village Buildings Shop Item 5":                          ("MF",   0x1078),
    "JJ Village Buildings Shop Item 6":                          ("MF",   0x1079),
    "JJ Village Buildings In Palm Tree":                         ("MF",   0x107C),

    "JJ Path to the Volcano Raphael Gift":                       ("MF",   0x107E),
    "JJ Path to the Volcano Behind Tree":                        ("GF",   0x4D9),

    "JJ SE Jungle (Quake Hammer) Bush (Bottom Right)":           ("GF",   0x4F0),
    "JJ SE Jungle (Quake Hammer) Bush (Bottom Left)":            ("GF",   0x4D7),
    "JJ SE Jungle (Quake Hammer) Red Block":                     ("GF",   0x4D6),
    "JJ SE Jungle (Quake Hammer) In Tree (Right)":               ("GF",   0x4E5),

    "JJ Sushi Tree In Volcano Chest":                            ("GF",   0x4CC),
    "JJ Sushi Tree On Island":                                   ("GF",   0x4CD),
    "JJ Sushi Tree Sushie Partner":                              ("MF",   0x107D),
    "JJ Sushi Tree In Island Tree":                              ("GF",   0x4CB),

    "JJ SW Jungle (Super Block) Bush (Top Right)":               ("GF",   0x4F1),
    "JJ SW Jungle (Super Block) Bush (Bottom Left)":             ("GF",   0x4F2),
    "JJ SW Jungle (Super Block) Hidden Block":                   ("GF",   0x4E1),
    "JJ SW Jungle (Super Block) Underwater 1":                   ("GF",   0x4FF),
    "JJ SW Jungle (Super Block) Underwater 2":                   ("GF",   0x500),
    "JJ SW Jungle (Super Block) Underwater 3":                   ("GF",   0x501),
    "JJ SW Jungle (Super Block) In SuperBlock":                  ("GF",   0x4FE),
    "JJ SW Jungle (Super Block) In Tree (Top)":                  ("GF",   0x4E8),
    "JJ SW Jungle (Super Block) In Tree (Right)":                ("GF",   0x4E9),

    "JJ NW Jungle (Large Ledge) Bush 1":                         ("GF",   0x4F3),
    "JJ NW Jungle (Large Ledge) Bush 2":                         ("GF",   0x4F4),
    "JJ NW Jungle (Large Ledge) In Tree On Ledge":               ("GF",   0x4EA),
    "JJ NW Jungle (Large Ledge) In Tree Right":                  ("GF",   0x4EB),

    "JJ Western Dead End Underwater":                            ("GF",   0x502),

    "JJ NE Jungle (Raven Statue) Underwater":                    ("GF",   0x4D8),
    "JJ NE Jungle (Raven Statue) In Tree (Top Left)":            ("GF",   0x4E6),

    "JJ Small Jungle Ledge In Tree":                             ("GF",   0x4E7),

    "JJ Deep Jungle 1 Hidden Block":                             ("GF",   0x4E2),
    "JJ Deep Jungle 1 In Tree (Vine)":                           ("GF",   0x4DA),
    "JJ Deep Jungle 1 In Tree (Hit)":                            ("GF",   0x4EC),

    "JJ Deep Jungle 2 (Block Puzzle) Hidden Block":              ("GF",   0x4E3),
    "JJ Deep Jungle 2 (Block Puzzle) In Tree (Left)":            ("GF",   0x4ED),

    "JJ Deep Jungle 3 Tree Vine Second Left":                    ("GF",   0x4DB),
    "JJ Deep Jungle 3 Tree Vine Far Right":                      ("GF",   0x4DC),

    "JJ Deep Jungle 4 (Ambush) Hidden Panel":                    ("GF",   0x4F6),
    "JJ Deep Jungle 4 (Ambush) In Tree (Right)":                 ("GF",   0x4EE),

    "JJ Great Tree Vine Ascent End Of Vine":                     ("GF",   0x4DD),

    # Mt Lavalava

    "MLL Central Cavern On Stone Pillar":                         ("GF",   0x532),
    "MLL Central Cavern On Brick Block":                          ("GF",   0x533),
    "MLL Central Cavern Yellow Block 1":                          ("GF",   0x534),
    "MLL Central Cavern Yellow Block 2":                          ("GF",   0x535),
    "MLL Central Cavern Yellow Block 3":                          ("GF",   0x536),
    "MLL Central Cavern Yellow Block 4":                          ("GF",   0x537),

    "MLL Fire Bar Bridge In SuperBlock":                          ("GF",   0x530),

    "MLL Flowing Lava Puzzle Hidden Block":                       ("GF",   0x520),

    "MLL Ultra Hammer Room In Big Chest":                         ("GF",   0x523),

    "MLL Dizzy Stomp Room In Chest":                              ("GF",   0x52C),

    "MLL Zipline Cavern Hidden Panel":                            ("GF",   0x53A),
    "MLL Zipline Cavern In SuperBlock":                           ("GF",   0x531),

    "MLL Boss Antechamber Hidden Panel":                          ("GF",   0x53B),

    "MLL Boss Room Yellow Block Left":                            ("GF",   0x538),
    "MLL Boss Room Yellow Block Right":                           ("GF",   0x539),

    # Flower Fields

    "FLO (NE) Elevators Stomp On Ledge":                          ("GF",   0x56C),
    "FLO (NE) Elevators Leftside Vine":                           ("MF",   0x108B),
    "FLO (NE) Elevators In SuperBlock":                           ("GF",   0x57B),

    "FLO (NE) Fallen Logs Hidden Block":                          ("GF",   0x56E),
    "FLO (NE) Fallen Logs In The Flowers":                        ("GF",   0x56D),

    "FLO (East) Triple Tree Path Leftmost Vine":                  ("MF",   0x1086),
    "FLO (East) Triple Tree Path Tree Puzzle Reward":             ("GF",   0x566),

    "FLO (East) Petunia's Field Petunia Gift":                     ("MF",   0x107F),
    "FLO (East) Petunia's Field Hidden Panel":                     ("GF",   0x57C),
    "FLO (East) Petunia's Field In Tree 1":                        ("MF",   0x1080),
    "FLO (East) Petunia's Field In Tree 2":                        ("MF",   0x1081),

    "FLO (East) Old Well Well Reward":                            ("GF",   0x570),

    "FLO (SE) Briar Platforming In The Flowers":                  ("GF",   0x565),
    "FLO (SE) Briar Platforming Left Side Vine":                  ("MF",   0x1083),
    "FLO (SE) Briar Platforming In SuperBlock":                   ("GF",   0x57A),
    "FLO (SE) Briar Platforming In Tree 1":                       ("MF",   0x1084),
    "FLO (SE) Briar Platforming In Tree 2":                       ("MF",   0x1085),

    "FLO (SE) Water Level Room Hidden Panel":                     ("GF",   0x57E),
    "FLO (SE) Water Level Room Hidden Block":                     ("GF",   0x572),
    "FLO (SE) Water Level Room In Tree 1":                        ("MF",   0x108C),
    "FLO (SE) Water Level Room In Tree 2":                        ("MF",   0x108D),
    "FLO (SE) Water Level Room Yellow Block":                     ("GF",   0x571),

    "FLO (SE) Lily's Fountain Lily Reward For WaterStone":         ("MF",   0x1087),
    "FLO (SE) Lily's Fountain In Tree":                            ("GF",   0x567),

    "FLO (SW) Path to Crystal Tree Hidden Panel":                 ("GF",   0x57F),
    "FLO (SW) Path to Crystal Tree Central Vine":                 ("MF",   0x108E),
    "FLO (SW) Path to Crystal Tree In Tree 1":                    ("MF",   0x108F),
    "FLO (SW) Path to Crystal Tree In Tree 2":                    ("MF",   0x1090),

    "FLO (SW) Posie and Crystal Tree Posie Gift 1":               ("MF",   0x1082),
    "FLO (SW) Posie and Crystal Tree Posie Gift 2":               ("GF",   0x55E),

    "FLO (West) Path to Maze Upper Hidden Block":                 ("GF",   0x581),
    "FLO (West) Path to Maze Lower Hidden Block":                 ("GF",   0x580),

    "FLO (West) Maze In MultiCoinBlock":                          ("GF",   0x568),

    "FLO (West) Rosie's Trellis Rosie Gift":                       ("MF",   0x1088),

    "FLO (NW) Bubble Flower On Ledge":                            ("GF",   0x56B),
    "FLO (NW) Bubble Flower Right Vine":                          ("MF",   0x108A),

    "FLO (NW) Lakilester Cage Under Rock":                        ("GF",   0x569),
    "FLO (NW) Lakilester In The Flowers":                         ("GF",   0x56A),
    "FLO (NW) Lakilester Lakilester Partner":                     ("MF",   0x1089),

    "FLO Cloudy Climb On Cloud":                                  ("GF",   0x56F),

    # Shiver Region

    "SR Shiver City Center Toad House Breakfast":                ("MF",   0x1093),
    "SR Shiver City Center Snowmen Gift 1":                      ("GF",   0x5A0),
    "SR Shiver City Center Snowmen Gift 2":                      ("GF",   0x5A1),
    "SR Shiver City Center Snowmen Gift 3":                      ("GF",   0x5A2),
    "SR Shiver City Center Snowmen Gift 4":                      ("GF",   0x5A3),
    "SR Shiver City Center Snowmen Gift 5":                      ("GF",   0x5A4),
    "SR Shiver City Center Shop Item 1":                         ("MF",   0x1094),
    "SR Shiver City Center Shop Item 2":                         ("MF",   0x1095),
    "SR Shiver City Center Shop Item 3":                         ("MF",   0x1096),
    "SR Shiver City Center Shop Item 4":                         ("MF",   0x1097),
    "SR Shiver City Center Shop Item 5":                         ("MF",   0x1098),
    "SR Shiver City Center Shop Item 6":                         ("MF",   0x1099),

    "SR Shiver City Mayor Area Chest In House":                  ("GF",   0x59B),
    "SR Shiver City Mayor Area Mayor Penguin Gift":              ("MF",   0x1091),
    "SR Shiver City Mayor Area Mayor Penguin Letter Reward":     ("MF",   0x1092),
    "SR Shiver City Mayor Area Hidden Panel":                    ("GF",   0x59C),

    "SR Shiver City Pond Area In Frozen Pond":                   ("GF",   0x5BA),

    "SR Shiver Snowfield Hidden Panel":                          ("GF",   0x5A5),
    "SR Shiver Snowfield Behind Tree Right":                     ("GF",   0x5A7),
    "SR Shiver Snowfield In Tree Left":                          ("GF",   0x5A6),

    "SR Path to Starborn Valley Hidden Block":                   ("GF",   0x5AA),
    "SR Path to Starborn Valley Behind Icicle":                  ("GF",   0x5A9),

    "SR Starborn Valley Merle Gift":                             ("MF",   0x109A),
    "SR Starborn Valley Frost T. Letter Reward":                 ("MF",   0x109B),

    "SR Shiver Mountain Passage Hidden Block":                   ("GF",   0x5B0),

    "SR Shiver Mountain Hills Bottom Path":                      ("MF",   0x109C),
    "SR Shiver Mountain Hills In SuperBlock":                    ("GF",   0x5B1),

    "SR Shiver Mountain Tunnel Socket 1":                        ("MF",   0x109D),
    "SR Shiver Mountain Tunnel Socket 2":                        ("MF",   0x109E),
    "SR Shiver Mountain Tunnel Socket 3":                        ("MF",   0x109F),

    "SR Shiver Mountain Peaks Left Ledge":                       ("GF",   0x5B8),
    "SR Shiver Mountain Peaks Red Block":                        ("GF",   0x5B7),

    "SR Merlar's Sanctuary On Pedestal":                          ("GF",   0x599),

    # Crystal Palace

    "CP Blue Key Room In Chest":                                 ("GF",   0x5D5),

    "CP Red Key Room In Chest":                                  ("GF",   0x5D4),

    "CP Reflected Save Room Yellow Block":                       ("GF",   0x5DA),

    "CP Shooting Star Room On The Ground":                       ("GF",   0x5DB),

    "CP P-Down, D-Up Room In Chest":                             ("GF",   0x5DD),

    "CP Star Piece Cave On The Ground":                          ("GF",   0x5E2),

    "CP Blue Mirror Hall 2 In MultiCoinBlock Front":             ("GF",   0x5E0),
    "CP Blue Mirror Hall 2 In MultiCoinBlock Back":              ("GF",   0x5E1),

    "CP Triple Dip Room In Chest":                               ("GF",   0x5ED),

    "CP Huge Statue Room Hidden Panel":                          ("GF",   0x5E6),
    "CP Huge Statue Room Yellow Block":                          ("GF",   0x5E5),

    "CP Palace Key Room In Chest":                               ("GF",   0x5E9),

    "CP Small Statue Room Hidden Panel":                         ("GF",   0x5E8),
    "CP Small Statue Room Hidden Block":                         ("GF",   0x5E7),

    "CP P-Up, D-Down Room In Chest":                             ("GF",   0x5EA),

    # Bowser's Castle

    "BC Front Door Exterior Red Block":                          ("GF",   0x61D),

    "BC Lower Jail In Crate 1":                                  ("GF",   0x617),
    "BC Lower Jail In Crate 2":                                  ("GF",   0x618),

    "BC Outside Lower Jail Defeat Koopatrol Reward":             ("GF",   0x60D),
    "BC Outside Lower Jail Yellow Block":                        ("GF",   0x60B),

    "BC Lava Key Room In Chest":                                 ("GF",   0x613),

    "BC Lava Channel 3 On Island 1":                             ("GF",   0x611),
    "BC Lava Channel 3 On Island 2":                             ("GF",   0x612),

    "BC Dark Cave 1 Yellow Block":                               ("GF",   0x609),

    "BC Dark Cave 2 Yellow Block":                               ("GF",   0x60A),

    "BC East Upper Jail Defeat Koopatrol Reward":                ("GF",   0x627),

    "BC Item Shop Shop Item 1":                                  ("MF",   0x10A0),
    "BC Item Shop Shop Item 2":                                  ("MF",   0x10A1),
    "BC Item Shop Shop Item 3":                                  ("MF",   0x10A2),
    "BC Item Shop Shop Item 4":                                  ("MF",   0x10A3),
    "BC Item Shop Shop Item 5":                                  ("MF",   0x10A4),
    "BC Item Shop Shop Item 6":                                  ("MF",   0x10A5),

    "BC Left Water Puzzle Top Left Ledge":                       ("GF",   0x632),

    "BC Right Water Puzzle Hidden Block":                        ("GF",   0x637),

    "BC Room with Hidden Door 1 Hidden Block":                   ("GF",   0x62E),
    "BC Room with Hidden Door 1 Yellow Block":                   ("GF",   0x62D),

    "BC Hidden Key Room On The Ground":                          ("GF",   0x630),

    "BC Battlement On Ledge":                                    ("GF",   0x622),
    "BC Battlement Yellow Block Left":                           ("GF",   0x61F),
    "BC Battlement Yellow Block Center":                         ("GF",   0x620),
    "BC Battlement Yellow Block Right":                          ("GF",   0x621),

    "BC West Upper Jail Defeat Koopatrol Reward":                ("GF",   0x62A),

    "BC Ultra Shroom Room On The Ground":                        ("GF",   0x62C),

    "BC Castle Key Room On The Ground":                          ("GF",   0x62B),

    # Peach's Castle

    "PC Guest Room (1F) In Chest":                               ("GF",   0x1E7),

    "PC Library (2F) Upper Level":                               ("GF",   0x1F8),
    "PC Library (2F) Between Bookshelves":                       ("GF",   0x1E4),

    "PC Storeroom (2F) On The Ground":                           ("GF",   0x1E6),

    # Peach's Castle Grounds

    "PCG Ruined Castle Grounds Muss T. Letter Reward":            ("MF",   0x10A6),
    "PCG Hijacked Castle Entrance Hidden Block":                  ("GF",   0x66B),

}
