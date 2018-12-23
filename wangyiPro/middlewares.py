# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time, random
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
]


class UA(UserAgentMiddleware):
    """单独给UA池封装一个类，
    继承from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware"""

    def process_request(self, request, spider):
        ua = random.choice(user_agents)  # 随机选取一个ua
        # 拦截当前请求，设置ua
        request.headers.setdefault('User-Agent', ua)


proxy_http = [
    '178.18.65.194:53680',
    '212.46.220.214:80',
    '203.95.221.222:59838',
    '58.240.172.110:3128',
]
proxy_https = [
    '185.132.133.98:1080',
    '59.127.168.43:3128',
    '96.9.74.139:43732',
    '160.119.104.69:49327',
]


class Proxy(object):
    """批量对拦截的请求进行ip更换"""

    def process_request(self, request, spider):
        # ip = request.meta['proxy']
        # request.url:http://www.xxx.com
        head = request.url.split(':')[0]

        # 对拦截到的请求头进行判断：https，http
        if head == 'http':
            ip = random.choice(proxy_http)
            request.meta['proxy'] = 'http://' + ip
        else:
            ip = random.choice(proxy_https)
            request.meta['proxy'] = 'https://' + ip


class WangyiproSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WangyiproDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        """
        此方法能够拦截到相应对象（下载器传给Spider的响应对象），
        将拦截到的响应对象的页面数据篡改后返回给Spider
        :param request:响应对象对应的请求对象
        :param response:拦截到的响应对象
        :param spider:爬虫文件中爬虫类的实例
        :return:
        """
        # print(request.url)
        # 修改拦截到的数据并返回
        if request.url in ['http://news.163.com/domestic/', 'http://news.163.com/world/', 'http://news.163.com/air/',
                           'http://war.163.com/']:  # 主页数据不用获取
            # selenium实例化的浏览器对象访问request.url
            spider.bro.get(url=request.url)

            # 滚轮滑动致浏览器最下方
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            spider.bro.execute_script(js)

            # 2秒钟加载动态数据时间
            time.sleep(2)

            # 拿到访问页面的数据
            page_text = spider.bro.page_source

            # spider.bro.current_url本次访问的url
            return HtmlResponse(url=spider.bro.current_url, body=page_text,
                                encoding='utf-8', request=request)

        else:
            return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
