# -*- coding: utf-8 -*-
# 欢迎关注微信公众号“码上”，了解更多教程信息
# website: https://www.05dt.com/
# github: https://github.com/05dt/scrapy


# -*- coding: utf-8 -*-

import scrapy

class BooksSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识
    name = "books"

    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # 提取数据
        # 每一本书的信息在<article class="product_pod"> </article>元素中，我们使用css()方法找到所有这样的article元素，并依次迭代
        for book in response.css('article.product_pod'):
            # 书名信息在 article > h3 > a 元素的title属性里
            name = book.xpath('./h3/a/@title').extract_first()

            # 书的价格信息在<p class="price_color">£23.88</p>的TEXT中
            price = book.css('p.price_color::text').extract_first()

            yield{
                '书名': name,
                '价格': price,
            }

        # 提取翻页链接
        # 下一页next按钮的url 在 ul.pager > li.next > a 元素的 href 属性中
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 如果找到下一页的url，得到绝对路径，构造新的Request对象
            # 使用urljoin()方法构建完整的绝对URL
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)