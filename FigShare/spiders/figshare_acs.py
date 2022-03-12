import scrapy
import redis
from scrapy_redis.spiders import RedisSpider
import json
import re

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=9, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class FigshareSpider(RedisSpider):
    name = 'figshare_acs'
    # allowed_domains = ['www.figshar.com']
    # start_urls = ['http://www.figshar.com/']
    redis_key = 'figshare_acs:url'

    def make_requests_from_url(self, url):
        return scrapy.Request(url=url, method='GET', callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        text = response.text
        data_text = re.findall('function\(\) { window.apolloState = (.*?); }\(\)\);</script>', text)[0]
        data_json = json.loads(data_text)
        dataset_id = response.url.split('/')[-1]

        source = data_json['$ROOT_QUERY.domainData.branding']['name']
        keys = list(data_json.keys())
        # print(json.dumps(source))
        # data_field = re.findall(self.data_re, data_text)[0]
        # print('data的key值为', data_field)
        # data = data_json[data_field]
        for key in keys:
            if '$ROOT_QUERY' in key and str(dataset_id) in key and '"version":null' in key:
                print('data  key = ', key)
                data = data_json[key]
                break
        # print('keys = ', keys)
        # 类别
        categories = list()
        # 关键字
        keywords = list()
        # license
        licenses = list()
        # timeline
        timeline = list()
        # authors
        authors = list()
        # REFERENCES
        references = list()
        for key in keys:
            if 'categories' in key:
                categories.append(data_json[key])
            if 'keywords' in key:
                keywords.append(data_json[key])
            if 'license' in key:
                licenses.append(data_json[key])
            if 'timeline' in key:
                timeline.append(data_json[key])
            if 'authors' in key and 'elements' in key:
                authors.append(data_json[key])
            if 'references' in key:
                references.append(data_json[key])

        for _ in list(data.keys()):
            if 'limit' in _:
                data.pop(_)

        json_data = {
            **data,
            'source': source,
            'soucre_url': response.url,
            'categories': categories,
            'keywords': keywords,
            'license': licenses,
            'authors': authors,
            'references': references,
            'timeline': timeline,
            'data_source': json.dumps(data, ensure_ascii=False),
            'source_data': json.dumps(data_json, ensure_ascii=False)
        }
        url = json_data['url']
        baseUrl = json_data['baseUrl']
        if not url.startswith('http'):
            json_data['url'] = 'https://acs.figshare.com' + url
        if not url.startswith('http'):
            json_data['baseUrl'] = 'https://acs.figshare.com' + baseUrl

        yield json_data
