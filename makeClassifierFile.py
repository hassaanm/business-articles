#!/usr/local/bin/python

import sys
import json

def getJSON(fileName):
    f = open(fileName)
    jsonData = json.load(f)
    f.close()
    return jsonData

def getLabel(articleReturn):
    if articleReturn > 0.05:
        return "Really Good"
    elif articleReturn > 0.01:
        return "Good"
    elif articleReturn > -0.01:
        return "OK"
    elif articleReturn > -0.05:
        return "Bad"
    else:
        return "Really Bad"

def writeClassifier(jsonData, fileName):
    f = open(fileName, 'w')
    f.write("<dataset>\n")

    for article in jsonData.keys():
        articleReturn = jsonData[article]
        f.write('<item label="' + getLabel(articleReturn) + '">\n')
        f.write("<conten>" + article.trim() + "</content>\n")
        f.write("</item>\n")

    f.write("</dataset>\n")
    f.close()

def splitDate(jsonData, testPercentage):
    trainData = {}
    testData = {}

    trainPercentage = 1.0 - testPercentage
    count = 0
    size = float(len(jsonData.keys()))
    for article in jsonData.keys():
        percentage = count / size
        if percentage < trainPercentage:
            trainData[article] = jsonData[article]
        else:
            testData[article] = jsonData[article]
        count += 1

    return (trainData, testData)

inputFile = sys.argv[1]
trainFile = sys.argv[2]
testFile = sys.argv[3]
testPercentage = float(sys.argv[4])

jsonData = getJSON(inputFile)
trainData, testData = splitData(jsonData, testPercentage)
writeClassifier(trainData, trainFile)
writeClassifier(testData, testFile)
