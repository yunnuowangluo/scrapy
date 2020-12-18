# -*- coding: utf-8 -*-
# 欢迎关注微信公众号“码上”，了解更多教程信息
# website: https://www.05dt.com/
# github: https://github.com/05dt/scrapy


import scrapy
from ..items import BookItem

class BooksSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识
    name = "books"

    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # 提取数据
        # 每一本书的信息在<article class="product_pod"> </article>元素中，我们使用css()方法找到所有这样的article元素，并依次迭代
        # 以下是 改动部分
        for sel in response.css('article.product_pod'):
            book = BookItem()
            book['name'] = sel.xpath('./h3/a/@title').extract_first()
            book['price'] = sel.css('p.price_color::text').extract_first()

            yield book

        # 以上是 改动部分


        # 提取翻页链接
        # 下一页next按钮的url 在 ul.pager > li.next > a 元素的 href 属性中
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 如果找到下一页的url，得到绝对路径，构造新的Request对象
            # 使用urljoin()方法构建完整的绝对URL
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)