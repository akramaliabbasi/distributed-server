# -*- coding: utf-8 -*-
import scrapy
import tldextract
import urllib2
import re
from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider
from caxy.items import CaxyItem

class DrupalhospitalsSpider(CrawlSpider):
    name = "drupalhospitals"

	# Adding URLs that need to be crawled/parsed
    start_urls = ['http://www.ushospital.info/Alabama.htm','http://www.ushospital.info/Alaska.htm','http://www.ushospital.info/Arizona.htm','http://www.ushospital.info/Arkansas.htm','http://www.ushospital.info/Arkansas.htm','http://www.ushospital.info/California.htm','http://www.ushospital.info/Colorado.htm','http://www.ushospital.info/Connecticut.htm','http://www.ushospital.info/Delaware.htm','http://www.ushospital.info/Florida.htm','http://www.ushospital.info/Georgia.htm','http://www.ushospital.info/Hawaii.htm','http://www.ushospital.info/Idaho.htm','http://www.ushospital.info/Illinois.htm','http://www.ushospital.info/Indiana.htm','http://www.ushospital.info/Iowa.htm','http://www.ushospital.info/Kansas.htm','http://www.ushospital.info/Kentucky.htm','http://www.ushospital.info/Louisiana.htm','http://www.ushospital.info/Maine.htm','http://www.ushospital.info/Maryland.htm','http://www.ushospital.info/Massachusetts.htm','http://www.ushospital.info/Michigan.htm','http://www.ushospital.info/Mississippi.htm','http://www.ushospital.info/Missouri.htm','http://www.ushospital.info/Montana.htm','http://www.ushospital.info/Nebraska.htm','http://www.ushospital.info/Nevada.htm','http://www.ushospital.info/New-Hampshire.htm','http://www.ushospital.info/New-Jersey.htm','http://www.ushospital.info/New-Mexico.htm','http://www.ushospital.info/New-York.htm','http://www.ushospital.info/North-Carolina.htm','http://www.ushospital.info/North-Dakota.htm','http://www.ushospital.info/Ohio.htm','http://www.ushospital.info/Oklahoma.htm','http://www.ushospital.info/Oregon.htm','http://www.ushospital.info/Pennsylvania.htm','http://www.ushospital.info/Puerto-Rico.htm','http://www.ushospital.info/Rhode-Island.htm','http://www.ushospital.info/South-Carolina.htm','http://www.ushospital.info/South-Dakota.htm','http://www.ushospital.info/Tennessee.htm','http://www.ushospital.info/Texas.htm','http://www.ushospital.info/Utah.htm','http://www.ushospital.info/Vermont.htm','http://www.ushospital.info/Virgin-Islands.htm','http://www.ushospital.info/Virginia.htm','http://www.ushospital.info/Washington.htm','http://www.ushospital.info/Washington-DC.htm','http://www.ushospital.info/West-Virginia.htm','http://www.ushospital.info/Wisconsin.htm','http://www.ushospital.info/Wyoming.htm','http://www.ushospital.info/Guam.htm']
    
	# Getting response from scrapy after crawling each url
    def parse(self, response):

        # Checking which URL scrapy crawled and adding conditions related to that site.
       
        urls = []   

        #Defining the section of the page where board members are
        content=response.xpath("//ul")
        for c in content:
            ul=c.xpath("li")
            for li in ul:
                url=li.xpath("a[1]/@href").extract()
                url=tldextract.extract(url[0])
                urls.append(url)
                
        return self.parse_urls(urls)


    def parse_urls(self,urls):
        for url in urls:
            print "http://"+url.domain+"."+url.suffix+"/user"
            #Opening all urls with /user appended and sending response to check_drupal
            yield Request("http://"+url.domain+"."+url.suffix+"/user", callback = self.check_drupal)

    def check_drupal(self,response):
        #Checking response code if 200 then it's a Drupal site and its saved in json file if 404,302 then its not saved
        if response.status == 200:
            if '/user' in response.request.url:
                content=response.xpath("//html").extract()
                if "drupal.js" in content[0]:
                    item = CaxyItem()
                    item["version"]=self.check_drupal_version(response.request.url)
                    item["url"]=response.request.url
                    return item
                    
                    
    #Checking if changelog.txt file exists and extracting drupal version from it
    def check_drupal_version(self,url):
        req=urllib2.urlopen(url.replace("/user", "/CHANGELOG.txt").strip())

        #If 200 status code then it means file exists on remote server
        if req.getcode()==200:
            #Checking if its a drupal changelog file or some other
            content=req.read(150)

            if "drupal" in content.lower():
                #Extracting Drupal version text from changelog file
                regex = re.compile("Drupal [0-9.]+\,")
                content=regex.findall(content)[0]

                #Extracting version no from text
                return float(''.join(ele for ele in content if ele.isdigit() or ele == '.'))                
    