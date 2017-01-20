FPS_GLOBAL = 0
PLAY_SOUNDS = False
SHOW_SCREEN = False
SIZE = 10 # 5 for our qvalues 10 for original
DUMPING_RATE = 15 # Number of iterations to dump Q values to JSON after
DISCOUNT = 1.0
REWARD = {0: 1, 1: -1000} # Reward function
LEARNING_RATE = 0.7

TAG = '_du_' + str(DUMPING_RATE) + '_lr_' + str(LEARNING_RATE) + '_di_' + str(DISCOUNT) + '_sz_' + str(SIZE)
FILE_QVALUES = 'data/qvalues' + TAG + '.json'
FILE_ITERATIONS = 'data/iteration' + TAG + '.csv'
FILE_DATA = 'data/data' + TAG + '.csv'
FILE_IMAGE = 'images/image' + TAG + '.png'
