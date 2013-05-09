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

def removeTags(text, openTag, closeTag):
    flag = True
    while openTag in text and closeTag in text and flag:
        start = text.find(openTag)
        end = text.find(closeTag)
        if start < end:
            text = text[:start] + text[end+1:]
        else:
            flag = False
    return text.replace(openTag, '').replace(closeTag, '')

def cleanText(text):
    return ' '.join(removeTags(removeTags(text, '<', '>'), '{', '}').replace("&", "and").split())

def writeClassifier(jsonData, fileName):
    f = open(fileName, 'w')
    f.write("<dataset>\n")

    size = len(jsonData.keys())
    for article in jsonData.keys():
        articleReturn = jsonData[article]
        articleText = cleanText(article.strip().encode('utf8'))
        f.write('\t<item label="' + getLabel(articleReturn) + '">\n')
        f.write("\t\t<content>" + articleText + "</content>\n")
        f.write("\t</item>\n")

    f.write("</dataset>\n")
    f.close()

def splitData(jsonData, testPercentage):
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
