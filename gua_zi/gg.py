# coding=utf-8
import requests
import json
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class GuaziSpider(object):
    def __init__(self):
        self.f = open("gua_zi.json", "a")
        self.base_url = "https://www.guazi.com"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Connection": "keep-alive",
            "Cookie": "uuid=e95e85fa-0422-47e8-b77c-75d0ffbfcc61; ganji_uuid=4194986112782835716777; 0d0315cf-6e34-4abb-b537-c04fda535e13_views=14; a190b93b-8d22-410b-d5f5-a014dfbf0d55_views=23; da34f7bb-5a25-4f30-d6e1-38fff59cbb51_views=22; antipas=31J638658439N328DE440Y839R; 2475e833-67ed-48fa-850e-f941f7e18b65_views=33; -_views=5; cityDomain=sh; clueSourceCode=10103000312%2300; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%25e4%25ba%258c%25e6%2589%258b%25e8%25bd%25a6%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22e95e85fa-0422-47e8-b77c-75d0ffbfcc61%22%2C%22sessionid%22%3A%22b81a652f-7519-4b10-caef-cf8d4fcbd225%22%7D; preTime=%7B%22last%22%3A1504313705%2C%22this%22%3A1501145288%2C%22pre%22%3A1501145288%7D; lg=1; Hm_lvt_e6e64ec34653ff98b12aab73ad895002=1504239434,1504249143,1504313470,1504313693; Hm_lpvt_e6e64ec34653ff98b12aab73ad895002=1504313707; sessionid=b81a652f-7519-4b10-caef-cf8d4fcbd225; e95e85fa-0422-47e8-b77c-75d0ffbfcc61_views=101; b81a652f-7519-4b10-caef-cf8d4fcbd225_views=4",
            "Host": "www.guazi.com",
            "Referer": "https://www.guazi.com/sh/buy/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        }

    def parse_page(self, url):
        """处理每一页"""
        response = requests.get(url, headers=self.headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        li_list = soup.select('ul[class="carlist clearfix js-top"] li')
        if response.url != url:
            return
        for li in li_list:
            item = {}
            # 获取汽车名字
            item['car_name'] = li.find('div', class_='t').get_text()
            # 获取汽车链接
            item['car_link'] = self.base_url + li.find('a', class_='car-a').get("href")
            # 获取汽车价格
            item['car_price'] = li.select('div[class="t-price"] p')[0].get_text()
            # 获取汽车上牌地
            item['car_location'] = li.find('div', class_='t-i').get_text().split("|")[2]
            # 获取汽车里程数
            item['car_mileage'] = li.find('div', class_='t-i').get_text().split("|")[1]
            # 获取汽车上牌时间
            item['car_license'] = li.find('div', class_='t-i').get_text().split("|")[0]
            # car_parameter = scrapy.Field()

            content = json.dumps(item, ensure_ascii=False) + ",\n"
            self.f.write(content)


    def main(self):
        link_list = ["https://www.guazi.com/www/buy/o" + str(i) + "/#bread/buy/" for i in range(1, 3500)]
        pool = Pool(16)
        pool.map(self.parse_page, link_list)

        pool.close()
        pool.join()

    def close_spider(self):
        self.f.close()


if __name__ == "__main__":
    g = GuaziSpider()
    g.main()

