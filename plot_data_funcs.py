import csv

def writeCsv(score):
    iteration = getIteration()
    with open('data/data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        aList = [str(iteration), str(score)]
        writer.writerow(aList)
    printIteration()

def getIteration():
    with open('data/iteration.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        lastrow = reader.next()
        return lastrow[0]

def printIteration(*args):
    if len(args) > 0:
        iteration = 1
    else:
        iteration = int(getIteration()) + 1
    with open('data/iteration.csv', 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(iteration)])

def cleanCsv():
    f = open('data/data.csv', "w+")
    f.close()
