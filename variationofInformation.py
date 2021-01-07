import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import seaborn as sns; sns.set(style="white", color_codes=True)
import csv
import scipy.stats

def varInfo(hist):
    hist = np.array([i for i in hist if i != 0])
    numBins = len(hist)
    uniform = np.ones(numBins)
    hist=hist/hist.sum()
    uniform = uniform/uniform.sum()
    mix_list = list(map(np.average, zip(hist, uniform)))


    dist = []
    for i in range(len(mix_list)):


        if hist[i] == 0:
            firstTerm = 0
            secondTerm = 0

        else:
            firstTerm = hist[i]*np.log2(hist[i]/mix_list[i])
            secondTerm = uniform[i]*np.log2(uniform[i]/mix_list[i])


        dist.append((firstTerm+secondTerm)/2)


    infoDistance = np.sqrt(sum(dist))


    return infoDistance


def main():

    abs_file_path = "C:/Users/Richard/Downloads/seaStarTrails5ht.csv"
    with open(abs_file_path, newline='') as csvfile:
        totalData = list(csv.reader(csvfile))


    seaStarID = list(np.array(totalData)[1:,2])
    positionX = list(np.array(totalData)[1:,4])
    positionY = list(np.array(totalData)[1:,5])
    time = list(np.array(totalData)[1:,7])

    numSeaStars = len(set(seaStarID))
    seaStars = set(seaStarID)
    filteredSeaStars = []
    for i in seaStars:
        counts = seaStarID.count(i)
        if counts > 99:
            filteredSeaStars.append(int(i))

    filteredSeaStars = sorted(filteredSeaStars)



    positionX = np.array(positionX)
    positionY = np.array(positionY)
    time = np.array(time)

    aggregatePositionX = []
    aggregatePositionY = []
    aggregateTime = []

    for a in filteredSeaStars:
        pos = []
        for b in range(len(seaStarID)):
            if seaStarID[b] == str(a):
                pos.append(b)

        tempPosX = positionX[pos]
        tempPosY = positionY[pos]
        tempTime = time[pos]
        tempPosX = list(tempPosX)
        tempPosY = list(tempPosY)
        tempTime = list(tempTime)

        for c in range(len(tempTime)):
            tempPosX[c] = float(tempPosX[c])
            tempPosY[c] = float(tempPosY[c])
            tempTime[c] = float(tempTime[c])

        aggregatePositionX.append(tempPosX)
        aggregatePositionY.append(tempPosY)
        aggregateTime.append(tempTime)

    aggregateDiffX = []
    aggregateDiffY = []
    aggregateDiffT = []
    aggregateSpeed = []
    aggregateDirection = []
    maxSpeed = 0
    maxDirection = 0
    for i in range(len(aggregatePositionX)):
        diffX = []
        diffY = []
        diffT = []
        speed = []
        direction = [0]
        for j in range(1,len(aggregatePositionX[i])):
            x = aggregatePositionX[i][j]-aggregatePositionX[i][j-1]
            y = aggregatePositionY[i][j] - aggregatePositionY[i][j - 1]
            t = aggregateTime[i][j] - aggregateTime[i][j - 1]
            delta = 0
            if x < 0:
                delta = 1
            eps = 1
            if y < 0:
                eps = -1

            diffX.append(x)
            diffY.append(y)
            diffT.append(t)

            speed.append(np.sqrt((x/t)**2+(y/t)**2))

            try:
                direction.append(np.arctan(y/x) + eps*delta*np.pi)

            except ZeroDivisionError:
                if y == 0:
                    direction.append(direction[-1])

                else:
                    direction.append(np.pi/2 + eps*delta*np.pi)

        aggregateDiffX.append(diffX)
        aggregateDiffY.append(diffY)
        aggregateDiffT.append(diffT)
        aggregateSpeed.append(speed)
        aggregateDirection.append(direction[1:])
        if max(speed) > maxSpeed:
            maxSpeed = max(speed)

        if max(direction) > maxDirection:
            maxDirection = max(direction)

    print(aggregateDirection[3])
    print(aggregateSpeed[3])
    print(maxSpeed, maxDirection)
    #sns.distplot(aggregateDirection[3], kde=False)

    fig, axes = plt.subplots(2, len(aggregateDiffX))

    fig.suptitle('Histograms of Motion')


    variationMetricSpeed = []
    variationMetricDirection = []
    for s in range(len(aggregateDiffX)):
        sns.distplot(aggregateDirection[s], kde=False, ax=axes[0,s])
        sns.distplot(aggregateSpeed[s], kde=False, ax=axes[1,s])
        directionHist, directionBins = np.histogram(aggregateDirection[s], bins=6, range=(-np.pi,np.pi), density=True)
        speedHist, speedBins = np.histogram(aggregateSpeed[s], bins=50, range=(0,500), density=True)
        variationMetricSpeed.append(varInfo(speedHist))
        variationMetricDirection.append(varInfo(directionHist))


    plt.show()

    fig2 = sns.distplot(variationMetricSpeed)
    plt.show()
    fig3 = sns.distplot(variationMetricDirection)
    plt.show()

    print(scipy.stats.describe(variationMetricSpeed))
    print(scipy.stats.describe(variationMetricDirection))



main()