import json
from constants import *
import random
import math
from plot_data_funcs import getIteration

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

        # for changed policy to looking at more future steps
        self.possibilities = {}
	self.actual = ""
	self.sum = 0
        self.LENGTH_ACT = STEPS

        # for using QV-learning also load V-values
        if ALGORITHM == Algorithm.QVLEARNING: self.load_vvalues()

    ## loading V-values for QV-learning
    def load_vvalues(self):
        # Load q values from a JSON file
        self.vvalues = {}
        try:
            fil = open(FILE_VVALUES, 'r')
        except IOError:
            return
        self.vvalues = json.load(fil)
        fil.close()

    ## loading Q-values for all the algorithms
    def load_qvalues(self):
        # Load q values from a JSON file
        self.qvalues = {}
        try:
            fil = open(FILE_QVALUES, 'r')
        except IOError:
            return
        self.qvalues = json.load(fil)
        fil.close()

    ## recursion to generate all self.LENGTH_ACT possible future moves and Q-values sums
    def generate(self, i, xdif, ydif, vel):
        if i == self.LENGTH_ACT or xdif < -29:
            self.possibilities[self.actual] = self.sum
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

    ## return if the agent should flap or not deppending on policy and other parameters
    def not_flap(self, xdif, ydif, vel):
        if POLICY == Policy.EGREEDY:
            if not math.isnan(EPSILON):
                if 1 - EPSILON < random.random():
                    return random.randint(0,1) == 0
            else:
                if 1.0 / int(getIteration()) > random.random():
                    return random.randint(0,1) == 0
        self.generate(0, xdif, ydif, vel)

        max = float("-inf")
        out = 0
        for key, value in self.possibilities.iteritems():
            if max <= value:
                if max == value and out == 0:
                    continue
                max = value
                out = int(key[0])

        return True if out == 0 else False

    ## act deppending on policy and other parameters
    def act(self, xdif, ydif, vel):
        # Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        state = self.map_state(xdif, ydif, vel)
        self.possibilities = {}

        if self.not_flap(xdif, ydif, vel):
            self.moves.append( [self.last_state, self.last_action, state, 0] ) # Add the experience to the history
            self.last_state = state # Update the last_state with the current state
            self.last_action = 0
            return 0
        else:
            self.moves.append( [self.last_state, self.last_action, state, 1] ) # Add the experience to the history
            self.last_state = state # Update the last_state with the current state
            self.last_action = 1
            return 1

    ## return last state
    def get_last_state(self):
        return self.last_state

    ## using Q-learning algorithm for update Q-values        
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

    ## using Q-learning algorithm for update Q-values (but history is not reversed)
    def use_qlearningfl(self):
        #Update qvalues via iterating over experiences
        history = list(self.moves)

        #Flag if the bird died in the top pipe
        high_death_flag = 1 if int(history[0][2].split('_')[1]) > 120 and history[len(history) - min(STEPS+1, 5) - 1][1] == 1 else 0

        #Q-learning score updates
        size = len(history) - min(STEPS+1, 5) - high_death_flag
        t = 1
        r = range(1, size)
        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]
            if t in r:
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*max(self.qvalues[res_state]) )
            else:
                #print(str(max(self.qvalues[res_state])) == str(self.qvalues[res_state][exp[3]]) )
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) )

            t += 1

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.moves = []  #clear history after updating strategies

    ## updating V-values depending on parameters, and return new e-list
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

    ## using QV-learning algorithm for update Q-values  
    def use_qvlearning(self):
        #Update qvalues via iterating over experiences
        history = list(self.moves)

        #Flag if the bird died in the top pipe
        high_death_flag = 1 if int(history[0][2].split('_')[1]) > 120 and history[len(history) - min(STEPS+1, 5) - 1][1] == 1 else 0

        #QV-learning score updates
        size = len(history) - min(STEPS+1, 5) - high_death_flag
        t = 1
        r = range(1, size)

        e = {}
        for key, value in self.vvalues.iteritems():
            e[key] = 0

        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]
            if t in r:
                e = self.update_vvalues(self.r[0], res_state, state, e)
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*self.vvalues[res_state] )
            else:
                e = self.update_vvalues(self.r[1], res_state, state, e)
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*self.vvalues[res_state] )
            t += 1

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.dump_vvalues() # Dump v values (if game count % DUMPING_N == 0)
        self.moves = []  #clear history after updating strategies

    ## using SARSA algorithm for update Q-values         
    def use_sarsa(self):
        #Update qvalues via iterating over experiences
        history = list(self.moves)

        #Flag if the bird died in the top pipe
        high_death_flag = 1 if int(history[0][2].split('_')[1]) > 120 and history[len(history) - min(STEPS+1, 5) - 1][1] == 1 else 0

        #Sarsa score updates
        size = len(history) - min(STEPS+1, 5) - high_death_flag
        t = 1
        r = range(1, size)
        for exp in history:
            act = exp[1]
            state = exp[0]
            res_state = exp[2]
            res_act = exp[3]
            if t in r:
                #print(self.qvalues[res_state][res_act])
                #print(max(self.qvalues[res_state]))
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[0] + (self.discount)*self.qvalues[res_state][res_act] )
                #print(self.qvalues[state][act])
                
                #print(self.qvalues[state][act])
                #print((1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) ))
                #print("\n")
            else:
                #print(self.qvalues[res_state][res_act])
                #print(max(self.qvalues[res_state]))
                self.qvalues[state][act] = (1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*self.qvalues[res_state][res_act] )

                #print(self.qvalues[state][act])
                #print((1- self.lr) * (self.qvalues[state][act]) + (self.lr) * ( self.r[1] + (self.discount)*max(self.qvalues[res_state]) ))
                #print("\n")

            t += 1
            #act = res_act

        self.gameCNT += 1 #increase game count
        self.dump_qvalues() # Dump q values (if game count % DUMPING_N == 0)
        self.moves = []  #clear history after updating strategies


    def update_scores(self):
        switcher = {
            Algorithm.QLEARNING: self.use_qlearning,
            Algorithm.QLEARNINGFL: self.use_qlearningfl,
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
