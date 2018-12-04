# -*- coding: utf-8 -*-
import schedule
import os
import sys
import time
import subprocess
from scrapy import cmdline

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#成本价品种
cost_scrapies = ["cost-abs", "cost-pp", "cost-lldpe", "cost-hdpe", "cost-pvc", "cost-ps", "cost-ldpe"]
#市场价品种
market_scrapies = ["market-abs", "market-pp", "market-hdpe", "market-ldpe", "market-lldpe", "market-ps", \
                   "market-pvc"]

# cmdline.execute(["scrapy", "crawl", "market-abs"])


def cost_crawl_work():
    for s in cost_scrapies:
        subprocess.Popen('scrapy crawl ' + s )


def market_crawl_work():
    for s in market_scrapies:
        subprocess.Popen('scrapy crawl ' + s )

if __name__=='__main__':
    schedule.every().day.at("11:48").do(cost_crawl_work)

    schedule.every().day.at("11:44").do(market_crawl_work)

    while True:
        schedule.run_pending()
        time.sleep(1)
