import json
from constants import *

class Bot(object):
    # The Bot class that applies the Qlearning logic to Flappy bird game
    # After every iteration (iteration = 1 game that ends with the bird dying) updates Q values
    # After every DUMPING_N iterations, dumps the Q values to the local JSON file
    def __init__(self):
        self.gameCNT = 0 # Game count of current run, incremented after every death
        self.DUMPING_N = DUMPING_RATE # Number of iterations to dump Q values to JSON after
        self.discount = DISCOUNT
        self.r = REWARD # Reward function
        self.lr = LEARNING_RATE
        self.load_qvalues()
        self.last_state = "420_240_0"
        self.last_action = 0
        self.moves = []

    def load_qvalues(self):
        # Load q values from a JSON file
        self.qvalues = {}
        try:
            fil = open(FILE_QVALUES, 'r')
        except IOError:
            return
        self.qvalues = json.load(fil)
        fil.close()

    def act(self, xdif, ydif, vel):
        # Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        state = self.map_state(xdif, ydif, vel)

        if self.qvalues[state][0] >= self.qvalues[state][1]:
            self.moves.append( [self.last_state, self.last_action, state, 0] ) # Add the experience to the history
            self.last_state = state # Update the last_state with the current state
            self.last_action = 0
            return 0
        else:
            self.moves.append( [self.last_state, self.last_action, state, 1] ) # Add the experience to the history
            self.last_state = state # Update the last_state with the current state
            self.last_action = 1
            return 1

    def get_last_state(self):
        return self.last_state
        
    def use_qlearning(self):
		#Update qvalues via iterating over experiences
        history = list(reversed(self.moves))

        #Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

        #Q-learning score updates
        t = 1
        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]
            if t == 1 or t==2:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) )
            #elif high_death_flag and act:
            #    self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) )
            #    high_death_flag = False
            else:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*max(self.qvalues[res_state]) )

            t += 1

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.moves = []  #clear history after updating strategies
        
    def use_sarsa(self):
		#Update qvalues via iterating over experiences
        history = list(reversed(self.moves))

        #Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

        #Q-learning score updates
        t = 1
        act = history[0][1]
        for exp in history:
            state = exp[0]
            res_state = exp[2]
            res_act = exp[3]
            if t == 1 or t==2:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*self.qvalues[res_state][res_act] )

            elif high_death_flag and act:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*self.qvalues[res_state][res_act] )
                high_death_flag = False

            else:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*self.qvalues[res_state][res_act] )

            t += 1
            act = res_act

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.moves = []  #clear history after updating strategies


    def update_scores(self):
        self.use_qlearning() if USE_QLEARNING else self.use_sarsa()

    def map_state(self, xdif, ydif, vel):
        # Map the (xdif, ydif, vel) to the respective state, with regards to the grids
        # The state is a string, "xdif_ydif_vel"

        # X -> [-40,-30...120] U [140, 210 ... 420]
        # Y -> [-300, -290 ... 160] U [180, 240 ... 420]
        if xdif < 140:
            xdif = int(xdif) - (int(xdif) % SIZE)
        else:
            xdif = int(xdif) - (int(xdif) % 70)

        if ydif < 180:
            ydif = int(ydif) - (int(ydif) % SIZE)
        else:
            ydif = int(ydif) - (int(ydif) % 60)

        return str(int(xdif))+'_'+str(int(ydif))+'_'+str(vel)

    def dump_qvalues(self):
        # Dump the qvalues to the JSON file
        if self.gameCNT % self.DUMPING_N == 0:
            fil = open(FILE_QVALUES, 'w')
            json.dump(self.qvalues, fil)
            fil.close()
            print('Q-values updated on local file.')
