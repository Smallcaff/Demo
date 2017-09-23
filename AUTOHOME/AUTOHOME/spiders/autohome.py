# -*- coding: utf-8 -*-
import scrapy

from ..items import AutohomeItem


class AutohomeSpider(scrapy.Spider):
    name = 'autohome'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['http://www.autohome.com.cn/shanghai/']

    def parse(self, response):
        # 拼接url
        for i in range(26):
            n = chr(i + ord('A'))
            url = 'http://www.autohome.com.cn/grade/carhtml/{}.html'.format(n)
            yield scrapy.Request(url=url, callback=self.parse_car)

    def parse_car(self, response):
        """
        抓取汽车品牌及链接
        """

        brand_list = response.xpath('//dl')
        for brand in brand_list:
            # 汽车品牌
            item = AutohomeItem()
            item['car_brand'] = brand.xpath('./dt/div/a/text()').extract()[0]
            a_list = brand.xpath('./dd/ul/li/h4/a')
            for a in a_list:
                # 汽车型号
                item['car_type'] = a.xpath('./text()').extract()[0]
                # 汽车链接
                car_link = "http:" + a.xpath('./@href').extract()[0]
                yield scrapy.Request(url=car_link, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        """
        详情页抓取汽车的详细信息
        """
        item = response.meta['item']
        li_list = response.xpath('//div[@class="interval01 interval-new"]/ul/li')
        # items = []
        for li in li_list:
            # 汽车详细配置
            item['car_configuration'] = li.xpath('./div[1]//p[1]/a/text()').extract()[0]
            # 汽车的价格
            if len(li.xpath('./div[3]/div/text()').extract()) == 1:
                item['car_price'] = li.xpath('./div[3]/div/text()').extract()[0].strip()
            else:
                item['car_price'] = li.xpath('./div[3]/div/text()').extract()[1].strip()
            # items.append(item)

            yield item








