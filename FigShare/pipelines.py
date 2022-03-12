# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import redis
import json


pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=9, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class FigsharePipeline:
    def process_item(self, item, spider):
        # print('入库', type(item))
        try:
            lines = json.dumps(dict(item), ensure_ascii=False)
            # print('lines = ', lines)
            r.rpush('figshare_new', lines)
        except:
            with open('data.json', 'a+', encoding='utf-8') as f:
                # print(list(item.keys()))
                f.write('{}\n'.format(json.dumps(item, ensure_ascii=False)))


