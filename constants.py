from enum import Enum
class Algorithm(Enum):
    QLEARNING = "qlearning"
    SARSA = "sarsa"
    QVLEARNING = "qvlearning"

FPS_GLOBAL = 0
PLAY_SOUNDS = False
SHOW_SCREEN = False
SIZE = 5 # 5 for our qvalues 10 for original
DUMPING_RATE = 50 # Number of iterations to dump Q values to JSON after
DISCOUNT = 1.0
REWARD = {0: 1, 1: -1000} # Reward function
LEARNING_RATE = 0.8
ALGORITHM = Algorithm.QVLEARNING
DEBUGGING = False
STEPS = 4
LAMBDA = 0.9

STEPS_STR = '_' + str(STEPS) + 'steps' if STEPS > 1 else ''
ALGORITHM_STR = '_' + ALGORITHM.value if ALGORITHM != Algorithm.QLEARNING else ''


TAG = '_du_' + str(DUMPING_RATE) + '_lr_' + str(LEARNING_RATE) + '_di_' + str(DISCOUNT) + '_sz_' + str(SIZE) + STEPS_STR + ALGORITHM_STR #'0test'#
FILE_QVALUES = 'data/qvalues' + TAG + '.json'
FILE_ITERATIONS = 'data/iteration' + TAG + '.csv'
FILE_DATA = 'data/data' + TAG + '.csv'
FILE_IMAGE = 'images/image' + TAG + '.png'
FILE_VVALUES = 'data/vvalues' + TAG + '.json'

