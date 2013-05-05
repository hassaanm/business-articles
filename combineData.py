#!/usr/local/bin/python
import sys
import json


def combineDicts(dict1, dict2):
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

def getJSON(fileName):
    f = open(fileName)
    jsonData = json.load(f)
    f.close()
    return jsonData

def writeJSON(jsonData, fileName):
    f = open(fileName, 'w')
    json.dump(jsonData, f)
    f.close()

json1 = getJSON(sys.argv[1])
json2 = getJSON(sys.argv[2])
json3 = getJSON(sys.argv[3])

combinedJSON = combineDicts(combineDicts(json1, json2), json3)
writeJSON(combinedJSON, sys.argv[4])
