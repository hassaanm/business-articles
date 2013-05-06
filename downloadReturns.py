#!/usr/local/bin/python

import sys
import urllib
import urllib2
import json
import datetime

YAHOO_URL = 'http://query.yahooapis.com/v1/public/yql?env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json&diagnostics=true&q='

def getJSON(fileName):
    f = open(fileName)
    jsonData = json.load(f)
    f.close()
    return jsonData

def writeJSON(jsonData, fileName):
    f = open(fileName, 'w')
    json.dump(jsonData, f)
    f.close()

def fixSymbol(symbol) :
    if len(symbol) > 1 and symbol[-2] == "/":
        symbol = symbol[:-2] + "-" + symbol[-1]
    if '/' in symbol :
        symbol = symbol.split('/')[0]
    return symbol.replace('^', '-P').rstrip()

def getReturn(returns):
    firstDate = returns.keys()[0]
    lastDate = returns.keys()[0]

    for date in returns.keys():
        if date < firstDate:
            firstDate = date
        if date > lastDate:
            lastDate = date

    openPrice = float(returns[firstDate][0])
    closePrice = float(returns[lastDate][1])

    return (closePrice - openPrice) / openPrice

def getReturnForCompany(symbol, date, numOfDays):
    endDate = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=numOfDays)
    sym = fixSymbol(symbol)
    query = 'select * from yahoo.finance.historicaldata where symbol = "'+sym+'" and startDate = "'+str(date)+'" and endDate = "'+str(endDate.date())+'"'
    encoded_query = urllib.quote(query)
    url = YAHOO_URL + encoded_query
    jsonRawData = urllib2.urlopen(url)
    jsonData = json.load(jsonRawData)

    if jsonData["query"]["results"] == None:
        return 0.0

    if type(jsonData["query"]["results"]["quote"]) == type({}):
        quotes = [jsonData["query"]["results"]["quote"]]
    else:
        quotes = jsonData["query"]["results"]["quote"]

    returns = {}
    for data in quotes:
        returns[data["Date"]] = (data["Open"], data["Close"])
    return getReturn(returns)

def returnsJSON(jsonData, days):
    returns = {}

    for article in jsonData.keys():
        date = jsonData[article]["date"]
        companies = jsonData[article]["company"]
        articleReturns = []
        for company in companies:
            articleReturns.append(getReturnForCompany(company, date, days))
        articleReturn = sum(articleReturns) / len(articleReturns)
        returns[article] = articleReturn

    return returns

inputFile = sys.argv[1]
outputFile = sys.argv[2]
days = int(sys.argv[3])

jsonData = getJSON(inputFile)
writeJSON(returnsJSON(jsonData, days), outputFile)
