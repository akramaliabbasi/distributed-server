# -*- coding: utf-8 -*-
import scrapy
import re
import tldextract
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.spiders import CrawlSpider
from caxy.items import CaxyItem

class GoogleSpider(CrawlSpider):
    name = "google"
    #no of seconds to delay between requests
    download_delay = 5
    DEPTH_LIMIT=1
    retry_enabled=False
    redirect_enabled=False

	# Adding URLs that need to be crawled/parsed
    start_urls = ['https://www.google.com/search?q=construction+chicago']

    #Following next link and passing response of next page result to parse_page
    '''
    rules =(
        Rule (SgmlLinkExtractor(allow=('', ),restrict_xpaths=('//a[@id="pnnext"]',)), callback='parse_page', follow= True),
    )
    '''

    def parse_page(self, response):
        sel = response
        #selecting text inside the cite tag
        content = sel.xpath('//cite')
        urls=[]
        for c in content:
            text=c.extract().encode("UTF-8")

            #Extracting content & removing HTML tags and extracting only domain name from urls
            url=tldextract.extract(self.cleanhtml(text))
            #Checking if extracted text is a URL or not
            if(url.suffix!=""):
                urls.append(url)

        #Passing extracted URLs to parse_urls
        return self.parse_urls(urls)
        sys.exit()

	# Getting response from scrapy after crawling Start URL
    def parse_start_url(self, response):
        sel = response
        content = sel.xpath('//cite')
        urls=[]
        for c in content:
            text=c.extract().encode("UTF-8")
            url=tldextract.extract(self.cleanhtml(text))
            if(url.suffix!=""):
                urls.append(url)

        return self.parse_urls(urls)


    def parse_urls(self,urls):
        for url in urls:
            print url
            #Opening all urls with /user appended and sending response to check_drupal
            yield Request("http://"+url.domain+"."+url.suffix+"/user", callback = self.check_drupal)

    def check_drupal(self,response):
        #Checking response code if 200 then it's a Drupal site and its saved in json file if 404,302 then its not saved
        if response.status == 200:
            if '/user' in response.request.url:
                item = CaxyItem()
                item["url"]=response.request.url
                return item

    def cleanhtml(self,raw_html):
        #Checking HTML and removing any tags found in it.
        cleanr =re.compile('<.*?>')
        cleantext = re.sub(cleanr,'', raw_html)
        return cleantext
