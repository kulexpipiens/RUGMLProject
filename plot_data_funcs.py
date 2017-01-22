from constants import *
import csv

def writeCsv(score):
    iteration = getIteration()
    with open(FILE_DATA, 'a') as csvfile:
        writer = csv.writer(csvfile)
        aList = [str(iteration), str(score)]
        writer.writerow(aList)
    printIteration()

def getIteration():
    with open(FILE_ITERATIONS, 'r') as csvfile:
        reader = csv.reader(csvfile)
        lastrow = reader.__next__()
        return lastrow[0]

def printIteration(*args):
    if len(args) > 0:
        iteration = 1
    else:
        iteration = int(getIteration()) + 1
    with open(FILE_ITERATIONS, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(iteration)])

def cleanCsv():
    f = open(FILE_DATA, "w+")
    f.close()
