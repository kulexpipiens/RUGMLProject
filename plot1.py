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
indices = ["1.0", "0.99999","0.9","0.8","0.7","0.6","0.5","0.4","0.3","0.2","0.1","1e-05"]
col = {}
notplotlr = []#['0.4', '0.7']

def add_to_plot(file_name, i, lr):
	if lr in notplotlr: return
	iterations = []
	scores = []
	averages = []
	
	with open(file_name, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			iterations.append(float(row[0]))
			scores.append(float(row[1]))
			# calculating trend
			averages.append(np.mean(scores[-TREND_ACCURACY:]))
			#du 15 di 1.0 sz 5
			if len(iterations) == 20000:
				break;
	l = lr#'0.'+str(i+1)
	col[lr]=[iterations,averages,colors[i%len(colors)]]
	#if i == 9: l = '1.0'
	#plt.plot(iterations, averages, colors[i%len(colors)], label=l, linewidth=2)
i=0
for file in glob.glob('data/data_*'):
	namea = file.split('_')
	change = namea[2] == '15' and namea[6] == '1.0' and namea[8].split('.')[0] == '5' and len(namea) < 10
	if change:
		add_to_plot(file, i, namea[4])
		i+=1
for idx in indices:
	plt.plot(col[idx][0], col[idx][1], col[idx][2], label=idx, linewidth=2)
plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=.5)
plt.xlabel('Iterations')
plt.ylabel('Scores')
plt.savefig("images2/plot1_TA"+str(TREND_ACCURACY)+"without"+str(notplotlr)+"_new_new2.png", dpi=DPI)
