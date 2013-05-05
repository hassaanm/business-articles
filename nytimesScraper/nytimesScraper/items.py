# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Article(Item):
    url = Field()
    title = Field()
    text = Field()
    company = Field()
    date = Field()
