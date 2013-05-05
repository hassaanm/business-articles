#!/usr/local/bin/python
import sys
import json


def combineURLDicts(dict1, dict2):
    newDict = {}
    for key in dict1.keys():
        if key not in dict2:
            newDict[key] = dict1[key]
        else:
            newDict[key] = dict1[key] + dict2[key]
    for key in dict2.keys():
        if key not in dict1:
            newDict[key] = dict2[key]
    return newDict

def addDataDict(dataDict, articleDict):
    for company in articleDict.keys():
        for date in articleDict[company]:
            article = articleDict[company][date]
            if article in dataDict:
                dataDict[article]["company"] += [company]
            else:
                dataDict[article] = {"date": date[:10], "company": [company]}
    return dataDict

def getJSON(fileName):
    f = open(fileName)
    jsonData = json.load(f)
    f.close()
    return jsonData

def writeJSON(jsonData, fileName):
    f = open(fileName, 'w')
    json.dump(jsonData, f)
    f.close()

json1 = getJSON(sys.argv[2])
json2 = getJSON(sys.argv[3])
json3 = getJSON(sys.argv[4])
finalJsonFile = sys.argv[5]

if (sys.argv[1] == "data"):
    combinedJSON = addDataDict(addDataDict(addDataDict({}, json1), json2), json3)
elif (sys.argv[1] == "url"):
    combinedJSON = combineURLDicts(combineURLDicts(json1, json2), json3)

writeJSON(combinedJSON, finalJsonFile)
