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
