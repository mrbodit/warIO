GAME_WIDTH = 800
GAME_HEIGHT = 800
HERO_RADIUS = 15
HERO_SPEED = 3
BULLET_SPEED = 6
BULLET_RADIUS = 9
NUMBER_OF_LAYERS = 3
NUMBER_OF_FRAMES = 1200
LAYERS = [14,14,3]
WEIGHTS_DOWN_CAP = -2
WEIGHTS_TOP_CAP = 2
BIASES_DOWN_CAP = -2
BIASES_TOP_CAP = 2
MUTATION_RATE = 5
STRINGS_AT_START = 6
NUMBER_OF_MATCHES = 5
WEIGHTS_LENGTH = LAYERS[0] * LAYERS[1] + LAYERS[1] * LAYERS[2] #+ LAYERS[2] * LAYERS[3]
BIASES_LENGTH = LAYERS[1] + LAYERS[2] #+ LAYERS[3]
AI_PATH = "D:\\projekty\\warIO\\ai\\2kontranadopadacza"