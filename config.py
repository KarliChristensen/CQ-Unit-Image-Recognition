# config.py

# --------------------------------------------- App Configuration ---------------------------------------------

HOTKEY_START = 'ctrl+e'
HOTKEY_INTERRUPT_RESET = 'ctrl+s'
HOTKEY_TERMINATE = 'ctrl+escape'

OUTPUT_JSON_FILES = {
    "melee infantry": "melee_infantry_units.json",
    "ranged infantry": "ranged_infantry_units.json",
    "cavalry": "cavalry_units.json"
}

# --------------------------------------------- Main Attribute Configuration ---------------------------------------------

UNIT_NAME_REGION = (760, 140, 465, 60)
UNIT_TIER_REGION = (760, 190, 320, 40)
ICON_REGION = (599, 140, 134, 134)
TYPE_REGION = (840, 240, 480, 40)
STAR_COLOR = (210, 210, 210)  # RGB for #D2D2D2
STAR_Y_COORDINATE = 22
STAR_START_X_COORDINATE = 16
STAR_X_OFFSETS = [8, 19]
MAX_POSSIBLE_STARS = 5
MAX_LEVEL_REGION = (790, 405, 55, 25)

# --------------------------------------------- Basic Attribute Configuration ---------------------------------------------

BASIC_NUMBERS_REGION = (1400, 440, 130, 240)

# --------------------------------------------- Attack Attribute Configuration ---------------------------------------------

ATTACK_NUMBERS_REGION = (1400, 740, 130, 240)

# --------------------------------------------- Defence Attribute Configuration ---------------------------------------------

DEFENCE_NUMBERS_REGION = (1400, 1020, 130, 180)

# --------------------------------------------- Unit Specific Attribute Configuration ---------------------------------------------

BOX_GREY_HEX = "#8C8C8C"
BOX_GREY_RGB = tuple(int(BOX_GREY_HEX[i:i+2], 16) for i in (1, 3, 5))
BOX_COLOR_TOLERANCE = 10       
    
FORMATION_POTENTIAL_REGIONS = [  
        (1730, 777, 63, 63),  
        (1815, 777, 63, 63),  
        (1901, 777, 63, 63),  
        (1987, 777, 63, 63),
    ]

ORDERS_POTENTIAL_REGIONS = [  
        (2157, 775, 65, 65), 
        (2242, 775, 65, 65), 
        (2327, 775, 65, 65),
        (2412, 775, 65, 65),
    ]

UNIT_TRAIT_POTENTIAL_REGIONS = [
        (2163, 501, 325, 25),  
        (2163, 534, 325, 25),
        (2163, 567, 325, 25),
        (2163, 600, 325, 25),
        (2163, 633, 325, 25),
    ]
    
UNIT_TRAIT_TARGET_COLORS_RGB = [
        (133, 183, 85),  
        (159, 160, 160),
        (174, 53, 26), 
        (198, 57, 25),
    ]
UNIT_TRAIT_COLOR_TOLERANCE = 20

# --- Terrain ---

TERRAIN_Y_LINE = (1860)
TERRAIN_X_START = (495)
TERRAIN_X_OFFSET = (40)
TERRAIN_BOX = (80, 25)           

# --------------------------------------------- Navigation Configuration ---------------------------------------------

VETERANCY_TAB_COORDINATES = (1707, 323)
DETAILS_TAB_COORDINATES = (2582, 1353)
ATTRIBUTES_TAB_COORDINATES = (1400, 315)
