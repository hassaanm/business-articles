from scrapy.spider import BaseSpider
from scrapy.exceptions import DropItem
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from nytimesScraper.items import Article

import re
import json

class NYTSpider(CrawlSpider):
    name = 'nytimes'
    allowed_domains = ['nytimes.com']

    f = open('All_URLs.json')
    company = json.load(f)
    f.close()
    start_urls = company.keys()

    rules = [Rule(SgmlLinkExtractor(allow=r'pagewanted=\d+',tags='//a[@class="next"]'), 'parse_link')]

    def parse_link(self, response):
        x = HtmlXPathSelector(response)

        article = Article()
        article['url'] = response.url
        article['title'] = x.select('//title/text()').extract()
        article['company'] = NYTSpider.company[self.baseURL(response.url)] if self.baseURL(response.url) in NYTSpider.company else ""
        article['text'] = self.extractText(x.select('//div[@class="articleBody"]//text()').extract()) \
                        + self.extractText(x.select('//div[@id="articleBody"]//text()').extract()) \
                        + self.extractText(x.select('string(//div[@class="entry-content"])').extract())
        article['date'] = self.extractDate(x.select('//meta[@name="pdate"]').extract())

        if len(article['company']) == 0 or len(article['text']) == 0:
            raise DropItem('Missing company and/or text: %s' % article)

        return article

    def parse_start_url(self, response):
        return self.parse_link(response)

    def baseURL(self, url):
        url = re.sub('\?pagewanted=\d+', '', url)
        url = re.sub('\?_r=\d', '', url)
        url = re.sub('&pagewanted=\d+', '', url)
        url = re.sub('&_r=\d', '', url)
        url = re.sub('pagewanted=\d+', '', url)
        url = re.sub('_r=\d', '', url)
        return url

    def extractText(self, body):
        texts = []
        for text in body:
            '''cleanText = text
            while '<' in cleanText:
                openTag = cleanText.find('<')
                closeTag = cleanText.find('>')
                cleanText = cleanText[:openTag] + cleanText[closeTag+1:]
            cleanText = cleanText.strip()
            if len(cleanText) > 0:
                texts.append(cleanText)'''
            if len(text.strip()) > 100:
                texts.append(text.strip())
        return ' '.join(texts)

    def extractDate(self, dateTags):
        for dateTag in dateTags:
            if 'content=' in dateTag:
                spot = dateTag.find('content=') + 9
                date = dateTag[spot:spot+8]
                date = date[:4] + '-' + date[4:6] + '-' + date[6:]
            return date
        return '2013-01-01'
