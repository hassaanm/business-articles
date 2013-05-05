#!/usr/local/bin/python
import csv
import sys
import time
import json
import urllib2
from subprocess import call

NYT_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q='
NYT_FILTER = '&sort=newest'
NYT_API_KEY = '&api-key=b33980a491a537ae5a602cfe34fa575c:12:67633897'

# read CSV file
def getCompanies(csvFile):
    fileLines = []
    with open(csvFile, 'r') as f:
        fileContents = csv.reader(f)
        for line in fileContents:
            fileLines.append(line)
    header = {name.lower():i for (i, name) in enumerate(fileLines[0])}
    data = fileLines[1:]

    companies = [row[header['name']].rstrip() for row in data]
    symbols = [row[header['symbol']].rstrip() for row in data]

    return companies, symbols

# download urls and write to files
def downloadURLs(companies, symbols, fileName):
    data = {}
    track = 0
    for company, symbol in zip(companies, symbols):
        # try to download data
        try:
            company = company.replace(' ', '+')
            url = NYT_URL + company.replace('&#39;', "'") + NYT_FILTER + NYT_API_KEY
            jsonRawData = urllib2.urlopen(url)
            jsonData = json.load(jsonRawData)
            for article in jsonData['response']['docs']:
                if article['section_name'] == 'Business Day' or article['section_name'] == 'Technology' or article['section_name'] == 'Your Money':
                    webURL = article['web_url']
                    if webURL != None:
                        if webURL in data:
                            data[article['web_url']] += [symbol]
                        else:
                            data[article['web_url']] = [symbol]
        except:
            print 'No data for', company, symbol

        # to show progress of download
        if track % 100 == 0:
            print float(track) / len(companies)
        track += 1

        # sleep to stay within api requirements of 10/second
        time.sleep(0.1)

    with open(fileName, 'w') as outfile:
        json.dump(data, outfile)

# download data and write to files
def downloadData(companies, symbols, fileName):
    data = {}
    track = 0
    for company, symbol in zip(companies, symbols):
        # try to download data
        try:
            articles = {}
            company = company.replace(' ', '+')
            url = NYT_URL + company.replace('&#39;', "'") + NYT_FILTER + NYT_API_KEY
            jsonRawData = urllib2.urlopen(url)
            jsonData = json.load(jsonRawData)
            for article in jsonData['response']['docs']:
                if article['section_name'] == 'Business Day' or article['section_name'] == 'Technology' or article['section_name'] == 'Your Money':
                    articleText = ''
                    if article['headline']['main'] != None:
                        articleText += article['headline']['main'] + ' '
                    if article['lead_paragraph'] != None:
                        articleText += article['lead_paragraph'] + ' '
                    if article['abstract'] != None:
                        articleText += article['abstract'] + ' '
                    articles[article['pub_date']] = articleText
            if (len(articles) > 0):
                data[symbol] = articles
        except:
            print 'No data for', company, symbol

        # to show progress of download
        if track % 100 == 0:
            print float(track) / len(companies)
        track += 1

        # sleep to stay within api requirements of 10/second
        time.sleep(0.1)

    with open(fileName, 'w') as outfile:
        json.dump(data, outfile)

# get arguments
csvFile = sys.argv[2]
articleFile = csvFile.replace('.csv', '_Articles.json')
urlFile = csvFile.replace('.csv', '_URLs.json')

# get companies and symbols for csvFile
companies, symbols = getCompanies(csvFile)

if sys.argv[1].lower() == 'data':
    # download articles for companies
    downloadData(companies, symbols, articleFile)
elif sys.argv[1].lower() == 'url':
    # download article URLs for companies
    downloadURLs(companies, symbols, urlFile)
else:
    print 'Incorrect use'
