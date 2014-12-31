# -*- coding: utf-8 -*-
import scrapy
import re
import tldextract
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http.request import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.spiders import CrawlSpider
from caxy.items import CaxyItem

class DevknowsSpider(CrawlSpider):
    name = "devknows"
    #no of seconds to delay between requests
    download_delay = 5
    DEPTH_LIMIT=1
    retry_enabled=False
    redirect_enabled=False
    handle_httpstatus_list = [200]

    def __init__(self, id=None, c=None, *args, **kwargs):
        super(DevknowsSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        #Following next link and passing response of next page result to parse_page
        self.rules =(
        Rule (SgmlLinkExtractor(allow=('', ),restrict_xpaths=("//ul[@class='pagination']/li[7]/a[@class='prevnext']",)), callback='parse_page', follow= True),
    )

	# Adding URLs that need to be crawled/parsed
    start_urls = ['http://www.dexknows.com/local/finance/insurance/insurance_agents_and_brokers/geo/c-chicago-il/','http://www.dexknows.com/local/health_care/dentistry/general_dentists/geo/c-chicago-il','http://www.dexknows.com/local/health_care/health_care_centers/health_care_clinics/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/hvac_contractors/geo/c-chicago-il','http://www.dexknows.com/local/energy_and_environment/sanitation/geo/c-chicago-il','http://www.dexknows.com/local/automotive/vehicle_service_and_repair/auto_parts/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/plumbers/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/landscape_contractors/geo/c-chicago-il','http://www.dexknows.com/local/automotive/vehicle_sales/auto_dealers/geo/c-chicago-il','http://www.dexknows.com/local/health_care/health_care_equipment_and_supplies/medical_supply/geo/c-chicago-il','http://www.dexknows.com/local/real_estate/real_estate_services/real_estate_agents_and_brokers/geo/c-chicago-il','http://www.dexknows.com/local/food_and_beverage/restaurants/geo/c-chicago-il','http://www.dexknows.com/local/automotive/automotive_services/auto_wrecking_and_salvage/geo/c-chicago-il','http://www.dexknows.com/local/personal_care/beauty_salons/geo/c-chicago-il','http://www.dexknows.com/local/real_estate/property/rental_property/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/general_contractors/geo/c-chicago-il','http://www.dexknows.com/local/transportation/storage/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/fences/geo/c-chicago-il','http://www.dexknows.com/local/real_estate/facilities_management/landscape_services/geo/c-chicago-il','http://www.dexknows.com/local/automotive/automotive_services/towing_services/geo/c-chicago-il','http://www.dexknows.com/local/business/employment_services/geo/c-chicago-il','http://www.dexknows.com/local/health_care/alternative_health_care/chiropractors/geo/c-chicago-il','http://www.dexknows.com/local/automotive/vehicle_service_and_repair/general_auto_service/geo/c-chicago-il','http://www.dexknows.com/local/health_care/health_care_services/funeral_homes/geo/c-chicago-il','http://www.dexknows.com/local/automotive/vehicle_service_and_repair/auto_body_and_paint/geo/c-chicago-il','http://www.dexknows.com/local/real_estate/facilities_management/pest_control/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/tree_service/geo/c-chicago-il','http://www.dexknows.com/local/construction/building_equipment_and_supplies/doors/geo/c-chicago-il','http://www.dexknows.com/local/home_and_garden/furniture/geo/c-chicago-il','http://www.dexknows.com/local/construction/contractors/roofers/geo/c-chicago-il','http://www.dexknows.com/local/construction/building_equipment_and_supplies/glass/geo/c-chicago-il','http://www.dexknows.com/local/technology/internet_service_providers/geo/c-chicago-il','http://www.dexknows.com/local/retail/florists/geo/c-chicago-il','http://www.dexknows.com/local/law/lawyers/general_practice_lawyers/geo/c-chicago-il','http://www.dexknows.com/local/law/lawyers/family_and_divorce_lawyers/geo/c-chicago-il','http://www.dexknows.com/local/pets/veterinarians/geo/c-chicago-il','http://www.dexknows.com/local/real_estate/facilities_management/cleaning_services/geo/c-chicago-il','http://www.dexknows.com/local/travel_and_tourism/hotels_and_lodging/geo/c-chicago-il','http://www.dexknows.com/local/health_care/doctors/general_practitioners/geo/c-chicago-il','http://www.dexknows.com/local/energy_and_environment/recycling/geo/c-chicago-il']

    start_urls = ['http://www.dexknows.com/local/health_care/doctors/general_practitioners/geo/c-chicago-il']





    def parse_page(self, response):
        content = response.xpath("//div[@class='listingWrapper']/div[@id='listContent']/div[@id='mapPin']/div[@id='listingBlock']/div[@class='listing']")
        urls=[]
        for c in content:
            url=c.xpath("div[@class='details clearfix']/div[@class='website']/a/@href").extract()
            if len(url)>0:
                print url
                url=tldextract.extract(url[0])
                urls.append(url)

        return self.parse_urls(urls)

	# Getting response from scrapy after crawling Start URL
    def parse_start_url(self, response):
        content = response.xpath("//div[@class='listingWrapper']/div[@id='listContent']/div[@id='mapPin']/div[@id='listingBlock']/div[@class='listing']")
        urls=[]
        for c in content:
            url=c.xpath("div[@class='details clearfix']/div[@class='website']/a/@href").extract()
            if len(url)>0:
                url=tldextract.extract(url[0])
                urls.append(url)

        return self.parse_urls(urls)


    def parse_urls(self,urls):
        for url in urls:
            #Opening all urls with /user appended and sending response to check_drupal
            print url
            #yield Request("http://"+url.domain+"."+url.suffix+"/user", callback = self.check_drupal)

    def check_drupal(self,response):
        #Checking response code if 200 then it's a Drupal site and its saved in json file if 404,302 then its not saved
        if response.status == 200:
            if '/user' in response.request.url:
                content=response.xpath("//html").extract()
                if "drupal.js" in content[0]:
                    item = CaxyItem()
                    item["url"]=response.request.url
                    return item

    def spider_closed(self, spider):
        yield Request("http://"+url.domain+"."+url.suffix+"/user", callback = self.check_drupal)

    def cleanhtml(self,raw_html):
        #Checking HTML and removing any tags found in it.
        cleanr =re.compile('<.*?>')
        cleantext = re.sub(cleanr,'', raw_html)
        return cleantext
