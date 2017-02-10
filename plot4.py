import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import glob

# dpi of figure
DPI=500
# number of previous values to calculate average
TREND_ACCURACY=1000

colors = ["#000000", "#0000FF", "#A52A2A", "#7FFF00", "#DC143C", "#006400", "#FF8C00", "#FF1493", "#FFD700", "#808080", "#669900", "#ff66ff"]
indices = ["6 step","4 steps","1 steps"]
col = {}
notplotlr = []#['0.4', '0.7']
files = {"data/data_du_50_lr_0.8_di_1.0_sz_5.csv":2, "data/data_du_50_lr_0.8_di_1.0_sz_5_4steps_new.csv":1, "data/data_du_50_lr_0.8_di_1.0_sz_5_6steps.csv":0}

def add_to_plot(file_name, i):
	iterations = []
	scores = []
	averages = []
	av = 0
	
	with open(file_name, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			if av >= 150:
				break;
			iterations.append(float(row[0]))
			scores.append(float(row[1]))
			# calculating trend
			av = np.mean(scores[-TREND_ACCURACY:])
			averages.append(av)
			if len(iterations) == 7000:
				break;
	col[indices[files[file_name]]]=[iterations,averages,colors[i%len(colors)]]
i=0
for file in glob.glob('data/data_*'):
	if file in files:
		add_to_plot(file, i)
		i+=1


for idx in indices:
	plt.plot(col[idx][0], col[idx][1], col[idx][2], label=idx, linewidth=2)
plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=.5)
plt.xlabel('Iterations')
plt.ylabel('Scores')
plt.savefig("images2/plot4_TA"+str(TREND_ACCURACY)+"without"+str(notplotlr)+".png", dpi=DPI)
