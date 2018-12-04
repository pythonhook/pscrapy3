# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class AokaispiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        query_sql, query_params  = item.query_base_id_sql()
        cursor.execute(query_sql, query_params)
        results = cursor.fetchall();
        if len(results) > 0:
            existed_sql, existed_params = item.query_existed_sql(results[0]["id"])
            cursor.execute(existed_sql, existed_params)
            cost_prices = cursor.fetchall();

            if(len(cost_prices) > 0):
                update_sql, update_params = item.get_update_sql(cost_prices[0]["id"])
                print(update_sql)
                cursor.execute(update_sql, update_params)
            else:
                insert_sql, insert_params = item.get_insert_sql(results[0]["id"])
                print(insert_sql)
                cursor.execute(insert_sql, insert_params)



