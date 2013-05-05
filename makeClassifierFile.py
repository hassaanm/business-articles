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

def fixSymbol(symbol) :
    if '/' in symbol :
        symbol = symbol.split('/')[0]
    return symbol.replace('^', '-P').rstrip()

def getReturns(symbol, date, numOfDays):
    endDate = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=numOfDays)
    sym = fixSymbol(symbol)
    query = 'select * from yahoo.finance.historicaldata where symbol = "'+sym+'" and startDate = "'+str(date)+'" and endDate = "'+str(endDate.date())+'"'
    encoded_query = urllib.quote(query)
    url = YAHOO_URL + encoded_query
    jsonRawData = urllib2.urlopen(url)
    jsonData = json.load(jsonRawData)
    print jsonData
  

inputFile = sys.argv[1]
outputFile = sys.argv[2]
days = int(sys.argv[3])

jsonData = getJSON(inputFile)
getReturns("GOOG", "2013-01-05", days)
