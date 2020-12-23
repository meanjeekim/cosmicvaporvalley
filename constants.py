from enum import Enum

TITLE = 'Cosmic Vapor Valley'
SCREEN_SIZE = WIDTH, HEIGHT = 896, 704
TILESIZE = 64
FPS = 60

FIRSTHOUR = 6           # as in the day starts at 6AM
HOUR_INTERVAL = 3000    # 7 seconds per hour
LIGHT_ALPHA = 0
ALPHA_INCR = 10

class CATEGORY(Enum):
    TOOL = 1
    SEED = 2
    CROP = 3
    