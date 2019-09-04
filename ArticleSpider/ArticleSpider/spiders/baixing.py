import scrapy
import re
from scrapy.http import Request # 下载
from urllib import parse
from ArticleSpider.items import FangItem, ArticleItemLoader


class BaiXing(scrapy.Spider):
    name = "baixing" # 定义蜘蛛名

    headers = {
        "HOST": "beijing.baixing.com",
        "Referer": "http://beijing.baixing.com",
        "User-Agent": ""
    }

    def start_requests(self): # 由此方法通过下面链接爬取页面

        # 定义爬取的连接
        urls = [
            'http://beijing.baixing.com/zhengzu/?grfy=1',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) # 爬取到页面如何处理，提交给parse方法处理
    def parse_detail(self, response):
        fang_item = FangItem()

        item_loader = ArticleItemLoader(item=FangItem(), response=response)
        # item_loader.add_css("name", ".zf_mftel")
        # item_loader.add_css("phone", ".zf_mftel")
        fang_item['name'] = response.css(".zf_mfname::text").extract_first()

        fang_item['phone'] = response.css(".zf_mftel::text").extract_first()
        addressArr = response.css(".link-under::text").extract()

        fang_item['address'] = addressArr[1] + " - " + addressArr[2] + " - " + addressArr[0]
        yield fang_item

    def parse(self, response):
        # 1. 获取文章列表野种的文章url
        # 2. 获取下一月的url交给scrapy进行下载

        post_urls = response.css(".title a::attr(href)").extract()
        for post_url in post_urls:
           # print("=====================")
           # meta 传递参数 是一个数组 meta
           # 取参 response.meta.get("参数", "")
           yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail) # 下载详情url
           #print(post_url)

        # 提取下一页并交个scrapy下载
        next_urls = response.css(".fanye a::text").extract()
        next_urls_href = response.css(".fanye a::attr(href)").extract()
        print (next_urls)
        for index in range(len(next_urls)):
            if next_urls[index] == '下一页':
                yield Request(url=parse.urljoin(response.url, next_urls_href[index]), callback=self.parse)

        size = len(next_urls)
        if next_urls_href[size-1] == next_urls_href[size-2]:
            print ("下载完成。。。。。。。。")
        '''
         start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        就是这么个流程，似不似很简单呀？
        '''
        # 处理urls

        # fang_selector = response.xpath('//*[@class="list hiddenMap rel"]')
        #
        # print('=================================')
        # print(len(fang_selector))
        # print('=================================')
