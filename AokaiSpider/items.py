# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from AokaiSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT

areas = ["华南", "华北", "东北", "华东", "华中", "西北", "西南"]

class AokaispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def area_convert(value):
    if value == None or value == "":
        return ""
    for area in areas:
        if value.__contains__(area):
            return area
        else:
            return value

def check_none(value):
    return value if value != None or value != "" else ""

def return_value(value):
    return value

class CostPriceItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class CostPriceItem(scrapy.Item):
    price_type = scrapy.Field()                 # 价格类型
    breed = scrapy.Field()                      # 品种
    spec = scrapy.Field()
    brand = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    updown = scrapy.Field()
    product_unit = scrapy.Field()
    release_date = scrapy.Field()
    release_date_str = scrapy.Field()

    def get_insert_sql(self, base_id):
        insert_sql = """
            INSERT INTO t_price_factory(base_id, price, release_date,release_date_str, updown, product_unit)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (str(base_id) , self["price"], self["release_date"], self["release_date_str"] , self["updown"],\
                  self["product_unit"])
        return insert_sql, params

    def get_update_sql(self, id):
        update_sql = """
            UPDATE t_price_factory SET price = %s , updown = %s WHERE id = %s
        """
        params = (self["price"], self["updown"], str(id))
        return update_sql, params

    def query_base_id_sql(self):
        sql = """
            SELECT * FROM t_price_factory_base WHERE price_type ='24' AND (product_varieties = %s OR product_name = %s) AND product_spec = %s AND \
            enterprise_name = %s AND (sales_area = %s OR sales_provinces = %s) LIMIT 1
        """
        params = (self["breed"], self["breed"], self["spec"], self["brand"] , self["area"], self["area"])
        return sql, params

    def query_existed_sql(self, base_id):
        sql = """
            SELECT * FROM t_price_factory WHERE base_id = %s AND release_date_str = %s LIMIT 1
        """
        params = (base_id, self["release_date_str"])
        return sql, params

import time

class MarketPriceItem(scrapy.Item):
    breed = scrapy.Field()                      # 品种
    spec = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    updown = scrapy.Field()
    release_date = scrapy.Field()
    release_date_str = scrapy.Field()

    def get_insert_sql(self, base_id):
        tbl_name = "t_analysis_price_" + self["breed"].lower()
        insert_sql = "INSERT INTO `"+ tbl_name+ "`(base_id, price, up_down, date_time, date_time_str, last_access) VALUES (%s, %s, %s, %s, %s, %s) "

        params = (str(base_id) , self["price"], self["updown"], self["release_date"], self["release_date_str"], str(1000*time.localtime(int(time.time()))))
        return insert_sql, params

    def get_update_sql(self, id):
        tbl_name = "t_analysis_price_" + self["breed"].lower()
        update_sql = "UPDATE `"+ tbl_name+ "` SET price = %s , up_down = %s WHERE id = %s"

        params = (self["price"], self["updown"], str(id))
        return update_sql, params

    def query_base_id_sql(self):
        sql = """
            SELECT * FROM t_price_base WHERE breed = %s  AND spec = %s AND brand = %s AND  city = %s LIMIT 1
        """
        params = (self["breed"], self["spec"], self["brand"], self["area"])
        return sql, params

    def query_existed_sql(self, base_id):
        tbl_name = "t_analysis_price_" + self["breed"].lower()
        sql = "SELECT * FROM `"+ tbl_name+ "` WHERE base_id = %s AND date_time_str = %s LIMIT 1"

        params = (str(base_id), self["release_date_str"])
        return sql, params


