# Scrapy settings for nytimesScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'nytimesScraper'

SPIDER_MODULES = ['nytimesScraper.spiders']
NEWSPIDER_MODULE = 'nytimesScraper.spiders'

DOWNLOAD_DELAY = 0.0

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nytimesScraper (+http://www.yourdomain.com)'
