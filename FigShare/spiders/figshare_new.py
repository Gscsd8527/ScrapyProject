import scrapy
import redis
from scrapy_redis.spiders import RedisSpider
import json
import re


pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=9, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class FigshareSpider(RedisSpider):
    name = 'figshare_new'
    # allowed_domains = ['www.figshar.com']
    # start_urls = ['http://www.figshar.com/']
    redis_key = 'figshare:url'

    def make_requests_from_url(self, url):
        # print(url, type(url))
        # url = 'https://figshare.com/articles/dataset/Table_1_Leukemia_With_TCF3-ZNF384_Rearrangement_as_a_Distinct_Subtype_of_Disease_With_Distinct_Treatments_Perspectives_From_A_Case_Report_and_Literature_Review_docx/15066030'
        id = url.split('/')[-1]
        citation_url = f'https://stats.figshare.com/total/article/{id}'
        return scrapy.Request(url=citation_url, method='GET', meta={'redis_url': url}, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        redis_url = response.meta.get('redis_url')
        text = response.text
        body_json = json.loads(text)
        temp_json = {
            'url': redis_url,
            'citation_url': response.url,
            **body_json,
            'body': body_json,

        }
        yield temp_json
