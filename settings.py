import math


# screen setting
size = 25
s_size = 10
num = 42
RES = num * size, num * size
RES2 = 2 * num * size, num * size
FPS = 60

# player setting
PLAYER_POS = 3, 7
PLAYER_ANGLE = 0
PLAYER_SPEED = 3
PLAYER_ROT_SPEED = 0.002
PlAYER_SIZE_SCALE = 300
PLATER_VIEW = 10

# ray casting setting
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = num * size // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 42

# floor setting
FLOOR_COLOR = (240, 200, 180)

# 3D distance setting
SCREEN_DIST = 0.5 * num * size / math.tan(HALF_FOV)
SCALE = num * size // NUM_RAYS

# texture setting
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

