# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 汽车的具体品牌
    car_brand = scrapy.Field()
    # 汽车的具体型号
    car_type = scrapy.Field()
    # 汽车详细配置型号
    car_configuration = scrapy.Field()
    # 汽车的价格
    car_price = scrapy.Field()

