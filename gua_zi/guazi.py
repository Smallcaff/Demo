# coding=utf-8
import requests
import json
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import pymongo
# 写入文件时，需加上此三行代码，默认以utf8写入
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class GuaziSpider(object):
    """瓜子二手车车辆信息抓取"""
    count = 1
    def __init__(self):
        self.f = open("gua_zi.json","a")
        self.base_url = "https://www.guazi.com"
        self.headers = {
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Connection" : "keep-alive",
            "Cookie" : "uuid=e95e85fa-0422-47e8-b77c-75d0ffbfcc61; ganji_uuid=4194986112782835716777; 0d0315cf-6e34-4abb-b537-c04fda535e13_views=14; a190b93b-8d22-410b-d5f5-a014dfbf0d55_views=23; da34f7bb-5a25-4f30-d6e1-38fff59cbb51_views=22; 2475e833-67ed-48fa-850e-f941f7e18b65_views=33; b81a652f-7519-4b10-caef-cf8d4fcbd225_views=29; antipas=6O70q34u663O6498N1Jb032I01428; -_views=6; cityDomain=www; Hm_lvt_e6e64ec34653ff98b12aab73ad895002=1504249143,1504313470,1504313693,1504494430; Hm_lpvt_e6e64ec34653ff98b12aab73ad895002=1504497119; clueSourceCode=10103000312%2300; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22e95e85fa-0422-47e8-b77c-75d0ffbfcc61%22%2C%22sessionid%22%3A%22e1971e94-5642-42e5-ee56-35899633ec94%22%7D; preTime=%7B%22last%22%3A1504497850%2C%22this%22%3A1501145288%2C%22pre%22%3A1501145288%7D; sessionid=e1971e94-5642-42e5-ee56-35899633ec94; e95e85fa-0422-47e8-b77c-75d0ffbfcc61_views=130; e1971e94-5642-42e5-ee56-35899633ec94_views=3; lg=1",
            "Host" : "www.guazi.com",
            "Referer" : "https://www.guazi.com/sh/buy/",
            "Upgrade-Insecure-Requests" : "1",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        }
        # 创建mongo客户端
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        # 连接数据库
        self.db = self.client['guazi']
        # 创建表
        self.sheet = self.db['guazi_info']
        # self.proxy = {"http" : "mr_mao_hacker:sffqry9r@122.114.214.159:16816"}

    def parse_page(self, url):
        """发送每页的请求"""
        response = requests.get(url, headers=self.headers)
        html = response.content
        # with open("h.html","w") as f:
        #     f.write(html)
        # print response.url,response.status_code
        soup = BeautifulSoup(html, "lxml")
        # 获取每辆车信息所在的li标签
        li_list = soup.select('ul[class="carlist clearfix js-top"] li')
        # print li_list
        # 如果响应的url和请求的url不一样，那么就是超过了总页数，页面会重定向到最后一页
        if response.url != url:
            return
        self.load_page(li_list)

    def load_page(self, li_list):
        # n = 1
        for li in li_list:
            # 创建一个空字典，用来保存每辆车的信息
            item = {}
            # 获取汽车名字
            item['car_name'] = li.find('div', class_='t').get_text()
            # 获取汽车链接
            item['car_link'] = self.base_url + li.find('a', class_='car-a').get("href")
            # 获取汽车价格
            item['car_price'] = li.select('div[class="t-price"] p')[0].get_text()
            # 获取汽车上牌地
            item['car_location'] = li.find('div',class_='t-i').get_text().split("|")[2]
            # 获取汽车里程数
            item['car_mileage'] = li.find('div',class_='t-i').get_text().split("|")[1]
            # 获取汽车上牌时间
            item['car_license'] = li.find('div',class_='t-i').get_text().split("|")[0]

            # 将数据入库
            print "[LOG]-正在插入第%s条数据"%GuaziSpider.count
            self.sheet.insert(dict(item))
            print "[LOG]-第%s条数据插入完成"%GuaziSpider.count
            GuaziSpider.count+=1
            # content = json.dumps(item, ensure_ascii=False) + ",\n"
            # print "[LOG]-正在写入第%s行数据......"%n
            # self.f.write(content)
            # print "[LOG]-第%s行数据写入完成"%n
            # n+=1

    def main(self):
        """启动爬虫的主函数"""
        # 拼接每页的链接，缺点是没有实时性，不能根据网站自己更新抓取
        link_list = ["https://www.guazi.com/www/buy/o"+str(i)+"/#bread/buy/" for i in range(1,3600)]
        # print len(link_list)
        # 创建线程池
        pool = Pool(8)
        pool.map(self.parse_page, link_list)
        pool.close()
        pool.join()
        # 程序运行结束关闭文件
        self.f.close()

if __name__ == "__main__":
    g = GuaziSpider()
    g.main()

