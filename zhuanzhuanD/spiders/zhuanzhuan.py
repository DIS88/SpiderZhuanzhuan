import json
import scrapy
from zhuanzhuanD.items import ZhuanzhuandItem

iphone_children = {
    "iPhone 14": "101,10530,95637",
    "iPhone 14 Pro": "101,10530,95638",
    "iPhone 14 Pro Max": "101,10530,95639",
    "iPhone 14 Plus": "101,10530,95667",
    "iPhone 13": "101,10530,58384",
    "iPhone 13 Pro Max": "101,10530,58387",
    "iPhone 13 Pro": "101,10530,58386",
    "iPhone 13 mini": "101,10530,58383",
    "iPhone 12": "101,10530,31458",
    "iPhone 12 Pro Max": "101,10530,31469",
    "iPhone 12 Pro": "101,10530,31459",
    "iPhone 12 mini": "101,10530,31468",
    "iPhone 11": "101,10530,2193",
    "iPhone 11 Pro Max": "101,10530,2192",
    "iPhone 11 Pro": "101,10530,2191",
    "iPhone XR": "101,10530,2189",
    "iPhone X": "101,10530,2190",
    "iPhone Xs Max": "101,10530,2188",
    "iPhone Xs": "101,10530,2187",
    "iPhone 8 Plus": "101,10530,2195",
    "iPhone 8": "101,10530,2194",
    "iPhone SE (第二代)": "101,10530,11973",
    "iPhone SE": "101,10530,2200",
    "iPhone SE (第三代)": "101,10530,88797",
    "iPhone 7 Plus": "101,10530,2197",
    "iPhone 7": "101,10530,2196",
    "iPhone 6": "101,10530,2201",
    "iPhone 6s": "101,10530,2198",
    "iPhone 6s Plus": "101,10530,2199",
    "iPhone 6 Plus": "101,10530,2202",
    "iPhone 5s": "101,10530,2203",
}


PARAM = 'param={"pageIndex":%s,"pageSize":100,"filterItems":{"st3":[{"cmd":"pg_cate_brand_model=%s","style":"326"}]},"secondFrom":"","initFrom":"2_1_14275_0","channelPageName":"iPhone","tab":0,"rstmark":1671608495247,"labelIdList":""}'


class ZhuanzhuanSpider(scrapy.Spider):
    name = 'zhuanzhuan'
    allowed_domains = ['zhuanzhuan.com']
    start_url = 'https://app.zhuanzhuan.com/zzopen/ypmall/listData'

    model_page_index = {}
    def start_requests(self):
        # 这个方法默认会对start_urls 进行get请求
        # yield scrapy.Request(self.start_url,
        #                      method="POST",
        #                      body=PARAM % "101,10530,95637",
        #                      headers={"content-type": "application/x-www-form-urlencoded"},
        #                      callback=self.parse,
        #                      # meta={"model": model}
        #                      )

        for model, model_value in iphone_children.items():
            self.model_page_index[model] = 1
            yield scrapy.Request(self.start_url,
                                 method="POST",
                                 body=PARAM % (self.model_page_index[model], model_value),
                                 headers={"content-type": "application/x-www-form-urlencoded"},
                                 callback=self.parse,
                                 meta={"model": model, "model_value":model_value})

    def parse(self, response):
        data_list = json.loads(response.body)['respData']['datas']
        if len(data_list) == 0:
            return
        model = response.meta.get("model")
        model_value = response.meta.get("model_value")
        for data in data_list:
            item = ZhuanzhuandItem()
            item["title"] = data["title"]
            item["model"] = model
            item["cutPrice"] = data["cutPrice"]
            item["mainImg"] = data["mainImg"]
            item["price"] = data["price"]
            item["realPayPrice"] = data["realPayPrice"]
            yield item
        has_next = json.loads(response.body)['respData'].get("hasNext")
        if has_next:
            # if self.model_page_index[model] < 2:
            self.model_page_index[model] += 1
            yield scrapy.Request(self.start_url,
                                 method="POST",
                                 body=PARAM % (self.model_page_index[model], model),
                                 headers={"content-type": "application/x-www-form-urlencoded"},
                                 callback=self.parse,
                                 meta={"model": model, "model_value":model_value})