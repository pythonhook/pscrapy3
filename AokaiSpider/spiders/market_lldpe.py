# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from AokaiSpider.items import CostPriceItemLoader, CostPriceItem, MarketPriceItem
import time
from AokaiSpider.utils import zhesu

class MarketLLDPESpider(scrapy.Spider):
    name = 'market-lldpe'
    breed = "LLDPE"
    allowed_domains = ['www.ex-cp.com']
    start_urls = ["http://www.ex-cp.com/plastic/list-50-1.html"]
    total_pages = 0
    strat_page = 1

    def parse(self, response):
        """
        """
        post_nodes = response.css(".catlist_li")
        cur_date = time.strftime('%Y-%m-%d', time.localtime(time.time()));
        for post_node in post_nodes:
            post_url = post_node.css("a::attr(href)").extract_first("")
            post_date = "2018-" + zhesu.date_time_convert(post_node.css("a::attr(title)").extract_first(""))
            if post_date == cur_date:
                yield Request(url=post_url, callback = self.parse_detail)


    def parse_detail(self, response):
        print("market_current_detail_page:" + response.url)
        trs = response.css("tbody tr")
        date_time_str = "2018-" + zhesu.date_time_convert(response.css("#title::text").extract_first(""))
        date_time = int(time.mktime(time.strptime(date_time_str,'%Y-%m-%d')))
        for tr in trs[1:]:
            tds = tr.css("td")
            market_item = MarketPriceItem()
            market_item["breed"] = self.breed
            market_item["spec"] = tds[0].css("td::text").extract_first("").strip()
            market_item["brand"] = tds[1].css("td::text").extract_first("").strip()
            market_item["area"] = tds[2].css("td::text").extract_first("").strip()
            market_item["price"] = tds[3].css("td::text").extract_first("").strip()
            market_item["updown"] = zhesu.market_updown_convert(tds[4].css("td::text").extract_first("").strip())
            market_item["release_date"] = date_time*1000
            market_item["release_date_str"] = date_time_str
            if market_item["spec"] == None or market_item["brand"] == None or market_item["spec"] == "" or market_item["brand"] == "":
                continue
            yield market_item

    def get_page(self, url):
        url = url[url.rindex("/") + 1:]
        attrs = url.replace(".html", "").split("-")
        return  attrs[len(attrs) - 1]