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

class UsdirectorySpider(CrawlSpider):
    name = "usdirectory"
    #no of seconds to delay between requests
    download_delay = 5
    DEPTH_LIMIT=1
    retry_enabled=False
    redirect_enabled=False

	# Adding URLs that need to be crawled/parsed
    start_urls = ['http://www.usdirectory.com/yellow-pages/Illinois/chicago/all_1.htm']

    #Following next link and passing response of next page result to parse_page

    rules =(
        Rule (SgmlLinkExtractor(allow=('', ),restrict_xpaths=("//div[@class='counter']/a[@class='counter_pic'][1]",)), callback='parse_page', follow= True),
    )



    def parse_page(self, response):
        content = response.xpath("//div[@id='all_results']/div[@id='holder_result2']/a")
        if len(content)==0:
            content=response.xpath("//div[@id='all_results']/div[@id='holder_result2']/span[@class='result_item']")

        urls=[]
        for c in content:
            url=c.xpath("span[@class='text2_1 url']/span[@class='underline']/text()").extract()
            if len(url)==0:
                url=c.xpath("span[@class='url']/a/@href").extract()

            if len(url)>0:
                url=tldextract.extract(url[0])
                print url
                urls.append(url)

        return self.parse_urls(urls)

	# Getting response from scrapy after crawling Start URL
    def parse_start_url(self, response):
        content = response.xpath("//div[@id='all_results']/div[@id='holder_result2']/a")
        if len(content)==0:
            content=response.xpath("//div[@id='all_results']/div[@id='holder_result2']/span[@class='result_item']")

        urls=[]
        for c in content:
            url=c.xpath("span[@class='text2_1 url']/span[@class='underline']/text()").extract()
            if len(url)==0:
                url=c.xpath("span[@class='url']/a/@href").extract()

            if len(url)>0:
                url=tldextract.extract(url[0])
                print url
                urls.append(url)

        return self.parse_urls(urls)


    def parse_urls(self,urls):
        for url in urls:
            #Opening all urls with /user appended and sending response to check_drupal
            yield Request("http://"+url.domain+"."+url.suffix+"/user", callback = self.check_drupal)

    def check_drupal(self,response):
        #Checking response code if 200 then it's a Drupal site and its saved in json file if 404,302 then its not saved
        if response.status == 200:
            if '/user' in response.request.url:
                content=response.xpath("//html").extract()
                if "drupal.js" in content[0]:
                    item = CaxyItem()
                    item["url"]=response.request.url
                    return item

    def cleanhtml(self,raw_html):
        #Checking HTML and removing any tags found in it.
        cleanr =re.compile('<.*?>')
        cleantext = re.sub(cleanr,'', raw_html)
        return cleantext
