import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from constants import *

# dpi of figure
DPI=500
# number of previous values to calculate average
TREND_ACCURACY=150

def plot_func(*args):
    iterations = []
    scores = []
    averages = []
    if len(args) > 0:
        file_name = args[0]
        file_image = file_name.replace('data/data', 'images/image')
        file_image = file_image.replace('csv', 'png')
    else:
        file_name = FILE_DATA
        file_image = FILE_IMAGE
    #max_s = 0
    #max_a = 0
    namea = file_name.split('_')
    change = len(namea) >= 9 and namea[2] == '15' and namea[6] == '1.0' and namea[8].split('.')[0] == '5'
    with open(file_name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            iterations.append(float(row[0]))
            scores.append(float(row[1]))
            #max_s = int(max(max_s, int(row[1])))
            # calculating trend
            averages.append(np.mean(scores[-TREND_ACCURACY:]))
            #max_a = max(max_a, np.mean(scores[-TREND_ACCURACY:]))
            #du 15 di 1.0 sz 5
            if change and len(iterations) == 7000 and namea[4] != '1e-05':
                break;
    plt.xlim(len(iterations) + 150)
    plt.gca().invert_xaxis()
    plt.xlabel('Iterations')
    plt.ylabel('Scores')
    plt.title("Results for: " + file_image.replace('images/image_',''))
    # plotting real values
    plt.plot(iterations, scores, 'r.')
    # plotting trend
    plt.plot(iterations, averages, "b")
    plt.savefig(file_image, dpi=DPI)
    plt.clf()
    #print(max_s)
    #print(max_a)

if __name__ == '__main__':
    plot_func()
