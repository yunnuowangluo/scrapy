# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PriceConverterPipeline:
    
    # 英镑对人民币汇率（2020年12月16日更新）
    exchange_rate = 8.8001

    def process_item(self, item, spider):
        # 提取 item 的 price 字段（如£51.77）
        # 去掉前面英镑符号 £ ，转换为 float 类型，乘以汇率
        price = float(item['价格'][1:]) * self.exchange_rate

        # 保留2位小数，赋值回 item 的 price 字段
        item['价格'] = '￥%.2f' % price

        return item




from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['书名']
        if name in self.book_set:
            raise DropItem('Duplicate book found:%s' % item)

        self.book_set.add(name)
        return item




from scrapy.item import Item
import pymongo

class MongoDBPipeline(object):

    # 直接定义方式
    # DB_URI = 'mongodb://localhost:27017/'
    # DB_NAME = 'scrapy_data'

    # 配置文件方式
    # 类方法（不需要实例化类就可以被类本身调用）
    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URI = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017/')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data2')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item