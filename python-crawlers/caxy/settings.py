# -*- coding: utf-8 -*-

# Scrapy settings for caxy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'caxy'

SPIDER_MODULES = ['caxy.spiders']
NEWSPIDER_MODULE = 'caxy.spiders'

COOKIES_ENABLED=False

RETRY_ENABLED = False

DOWNLOAD_TIMEOUT = 40

CONCURRENT_REQUESTS = 5

LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 2

#USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'

ITEM_PIPELINES = {'caxy.pipelines.JsonWriterPipeline':300,}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Caxy (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'caxy.comm.rotate_useragent.RotateUserAgentMiddleware' :400,
}

'''
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'caxy.comm.rotate_useragent.RotateUserAgentMiddleware' :400,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        'caxy.middlewares.ProxyMiddleware': 100,
    }

PROXY_LIST = 'list.txt'
'''