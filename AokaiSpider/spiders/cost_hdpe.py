# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from AokaiSpider.items import CostPriceItemLoader, CostPriceItem
import time
from AokaiSpider.utils import zhesu

class CostHdpeSpider(scrapy.Spider):
    name = 'cost-hdpe'
    breed = "HDPE"
    allowed_domains = ['www.ex-cp.com']
    start_urls = ["http://www.ex-cp.com/plastic/list-29-1.html"]
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

        # if self.total_pages == 0:
        #     common_url = response.css("#destoon_previous ::attr(value)").extract_first("")
        #     self.total_pages = int(self.get_page(common_url.strip()))
        #
        # c_page = 1 if int(self.get_page(response.url)) == None else int(self.get_page(response.url))
        # if c_page < self.total_pages:
        #     next_url = self.breed_url+ str(c_page + 1)+".html"
        #     print("ABS出厂价URL:" + next_url)
        #     yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        print("current_detail_page:" + response.url)
        trs = response.css("tbody tr")
        date_time_str = "2018-" + zhesu.date_time_convert(response.css("#title::text").extract_first(""))
        date_time = int(time.mktime(time.strptime(date_time_str,'%Y-%m-%d')))
        for tr in trs[1:]:
            tds = tr.css("td")
            cost_item = CostPriceItem()
            cost_item["breed"] = self.breed
            cost_item["spec"] = tds[0].css("td::text").extract_first("").strip()
            cost_item["brand"] = tds[1].css("td::text").extract_first("").strip()
            cost_item["area"] = zhesu.area_convert(tds[2].css("td::text").extract_first("").strip())
            cost_item["price"] = tds[3].css("td::text").extract_first("").strip()
            cost_item["updown"] = tds[4].css("td::text").extract_first("").strip()
            cost_item["product_unit"] = "元/吨"
            cost_item["release_date"] = date_time*1000
            cost_item["release_date_str"] = date_time_str
            if cost_item["spec"] == None or cost_item["brand"] == None or cost_item["spec"] == "" or cost_item["brand"] == "" \
                or cost_item["area"] == None or cost_item["area"] == "" :
                continue
            yield cost_item

    def get_page(self, url):
        url = url[url.rindex("/") + 1:]
        attrs = url.replace(".html", "").split("-")
        return  attrs[len(attrs) - 1]