import json
from constants import *
from itertools import chain
from plot_data_funcs import cleanCsv, printIteration
import os

# Script to create Q-Value JSON file, initilazing with zeros
def initialize_data():
    qval = {}
    # X -> [-40,-30...120] U [140, 210 ... 490]
    # Y -> [-300, -290 ... 160] U [180, 240 ... 420]
    for x in chain(list(range(-40,140,SIZE)), list(range(140,421,70))):
        for y in chain(list(range(-300,180,SIZE)), list(range(180,421,60))):
            for v in range(-10,11):
                qval[str(x)+'_'+str(y)+'_'+str(v)] = [0,0]


    fd = open(FILE_QVALUES, 'w+')
    json.dump(qval, fd)
    fd.close()

    cleanCsv()
    printIteration(True)
