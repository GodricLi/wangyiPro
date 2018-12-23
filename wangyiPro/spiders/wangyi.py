# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy_redis.spiders import RedisSpider
from wangyiPro.items import WangyiproItem


class WangyiSpider(RedisSpider):
    """爬取网易新闻基于文字的新闻数据（国内，国际，军事，航空）"""
    name = 'wangyi'
    # allowed_domains = ['www.news.163.com']
    # start_urls = ['https://news.163.com']
    redis_key = 'wangyi'

    def __init__(self):
        # 实例化一个浏览器对象,访问动态加载的数据需要使用
        self.bro = webdriver.Chrome(executable_path='D:\StudyData\Python\Spider\chromedriver')

    def closed(self, spider):
        # 必须在整个爬虫结束后关闭浏览器
        print('spider end')
        self.bro.quit()

    def parse(self, response):
        # 先找到所有rul
        head_list = response.xpath('//div[@class="ns_area list"]/ul/li')

        # 根据索引选取对应的url
        index = [3, 4, 6, 7]  # 需要爬取的url对应的索引
        url_list = []
        for i in index:
            url_list.append(head_list[i])

        # 获取四个板块的url和标题
        for li in url_list:
            title = li.xpath('./a/text()').extract_first()
            url = li.xpath('./a/@href').extract_first()
            # print(url + ':' + title)

            # 对每个板块对应的url发起请求，获取页面数据（标题，缩略图，关键字，发布时间，url）
            yield scrapy.Request(url=url, callback=self.parse_second, meta={'title': title})

    def parse_second(self, response):
        div_list = response.xpath('//div[@class="data_row news_article clearfix "]')
        print(len(div_list))  # 访问网页新闻对应的url时，数据是动态加载的，

        # 获取paser传入的title
        title = response.meta['title']

        for div in div_list:
            news_title = div.xpath('.//div[@class="news_title"]/h3/a/text()').extract_first()
            news_url = div.xpath('.//div[@class="news_title"]/h3/a/@href').extract_first()
            img_url = div.xpath('./a/img/@src').extract_first()
            tag_list = div.xpath('.//div[@class="news_tag"]//text()').extract()
            tags=[]
            for t in tag_list:
                t=t.strip(' \n \t')
                tags.append(t)
            tag="-".join(tags)
            # print(news_title+','+news_url)

            item = WangyiproItem()
            item['news_title'] = news_title
            item['news_url'] = news_url
            item['img_url'] = img_url
            item['tag'] = tag
            item['title'] = title

            # 对url发起请求，获取对应页面数据
            yield scrapy.Request(url=news_url, callback=self.get_content, meta={'item': item})

    def get_content(self, response):
        # 获取传递过来的item
        item = response.meta['item']
        # 解析数据
        content_list = response.xpath('//div[@class="post_text"]/p/text()').extract()
        content = ''.join(content_list)
        item['content'] = content
        yield item
