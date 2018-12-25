# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class BkzufangPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='127.0.0.1',
            db='test',
            port=3306,
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=False
        )
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        sql = "insert into bkzf(company,rental,addr,mianji,geshi,price) VALUE (%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql,(
                item['company'],
                item['rental'],
                item['addr'],
                item['mianji'],
                item['geshi'],
                item['price'],
            ))
            self.connect.commit()
        except Exception as e:
            print(e)
        return item
