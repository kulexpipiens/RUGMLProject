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

        self.possibilities = {}
	self.actual = ""
	self.sum = 0
        self.LENGTH_ACT = STEPS

        if ALGORITHM == Algorithm.QVLEARNING: self.load_vvalues()

    def load_vvalues(self):
        # Load q values from a JSON file
        self.vvalues = {}
        try:
            fil = open(FILE_VVALUES, 'r')
        except IOError:
            return
        self.vvalues = json.load(fil)
        fil.close()

    def load_qvalues(self):
        # Load q values from a JSON file
        self.qvalues = {}
        try:
            fil = open(FILE_QVALUES, 'r')
        except IOError:
            return
        self.qvalues = json.load(fil)
        fil.close()

    def generate(self, i, xdif, ydif, vel):
        if i == self.LENGTH_ACT or xdif < -29:
            self.possibilities[self.actual] = self.sum
            #print(self.sum)
            #print("xdif: " + str(xdif) + ", ydif: " + str(ydif) + ", vel: " + str(vel) + ", state: " + self.map_state(xdif, ydif, vel))
            return

        state = self.map_state(xdif, ydif, vel)

        self.actual += "0"
	self.sum += self.qvalues[state][0]
	n_vel = min(vel + 1, 10)
	self.generate(i + 1, xdif - 4, ydif - n_vel, n_vel)

	self.actual = self.actual[:-1]
	self.sum -= self.qvalues[state][0]

	self.actual += "1"
	self.sum += self.qvalues[state][1]
	self.generate(i + 1, xdif - 4, ydif + 9, -9)

	self.actual = self.actual[:-1]
	self.sum -= self.qvalues[state][1]

    def not_flap(self, xdif, ydif, vel):
        self.generate(0, xdif, ydif, vel)
        #print(self.possibilities)
        max = float("-inf")
        for key, value in self.possibilities.iteritems():
            #print(key + " "+str(value))
            if max <= value:
                if max == value and out == 0:
                    continue
                max = value
                out = int(key[0])
        #print(out)
        return True if out == 0 else False

    def act(self, xdif, ydif, vel):
        # Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        state = self.map_state(xdif, ydif, vel)
        self.possibilities = {}

        if self.not_flap(xdif, ydif, vel):
            self.moves.append( [self.last_state, self.last_action, state, 0] ) # Add the experience to the history
            #print("xdif: " + str(xdif) + ", ydif: " + str(ydif) + ", vel: " + str(vel) + ", state: " + state + ", action: 0")
            self.last_state = state # Update the last_state with the current state
            self.last_action = 0
            return 0
        else:
            self.moves.append( [self.last_state, self.last_action, state, 1] ) # Add the experience to the history
            #print("xdif: " + str(xdif) + ", ydif: " + str(ydif) + ", vel: " + str(vel) + ", state: " + state + ", action: 1")
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
        r = range(1, min(STEPS+1, 5))
        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]
            if t in r:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) )
            elif high_death_flag and act:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) )
                high_death_flag = False
            else:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*max(self.qvalues[res_state]) )

            t += 1

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.moves = []  #clear history after updating strategies

    def update_vvalues(self, reward, res_state, state, e):
        e_new = {}
        for key, value in e.iteritems():
            e_new[key] = 0

        for k,v in self.vvalues.iteritems():
            n = 1 if k == state else 0
            delta = reward + (self.discount * self.vvalues[res_state]) - self.vvalues[state]
            e_new[k] = (self.discount * LAMBDA * e[k]) + n
            self.vvalues[k] = self.vvalues[k] + (self.lr * delta * e_new[k])
        return e_new


    def use_qvlearning(self):
        #Update qvalues via iterating over experiences
        history = list(reversed(self.moves))

        #Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

        #Q-learning score updates
        t = 1
        r = range(1, min(STEPS+1, 5))

        e = {}
        for key, value in self.vvalues.iteritems():
            e[key] = 0

        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]
            if t in r:
                e = self.update_vvalues(self.r[1], res_state, state, e)
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*self.vvalues[res_state] )
            elif high_death_flag and act:
                e = self.update_vvalues(self.r[1], res_state, state, e)
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*self.vvalues[res_state] )
                high_death_flag = False
            else:
                e = self.update_vvalues(self.r[0], res_state, state, e)
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*self.vvalues[res_state] )

            t += 1

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.dump_vvalues()
        self.moves = []  #clear history after updating strategies
        
    def use_sarsa(self):
        #Update qvalues via iterating over experiences
        history = list(reversed(self.moves))

        #Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

        #Q-learning score updates
        t = 1
        r = range(1, min(STEPS+1, 5))
        act = history[0][1]
        for exp in history:
            state = exp[0]
            res_state = exp[2]
            res_act = exp[3]
            if t in r:
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
        switcher = {
            Algorithm.QLEARNING: self.use_qlearning,
            Algorithm.SARSA: self.use_sarsa,
            Algorithm.QVLEARNING: self.use_qvlearning
        }
        al = switcher.get(ALGORITHM)
        al()

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

    def dump_vvalues(self):
        if self.gameCNT % self.DUMPING_N == 0:
            fil = open(FILE_VVALUES, 'w')
            json.dump(self.vvalues, fil)
            fil.close()
            print('V-values updated on local file.')
