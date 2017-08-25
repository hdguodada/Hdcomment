# -*- coding: utf-8 -*-
import scrapy
from ..items import ElongItem
from urllib.parse import urljoin
from scrapy import Request
from datetime import datetime
from commentspider.models import WhereFrom, HotelIndex



class CtripSpider(scrapy.Spider):
    name = 'ctrip'
    base_url = 'https://hotels.ctrip.com'
    base_next_url = 'http://hotels.ctrip.com/hotel/D1096_755/p{0}'
    comment_base_url = 'http://hotels.ctrip.com//hotel/dianping/{0}_p{1}t0.html'
    allowed_domains = ['hotels.ctrip.com']
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }



    def start_requests(self):
        return [scrapy.Request(url='http://hotels.ctrip.com/hotel/D1096_755/p1', headers=self.headers, callback=self.parse)]

    def parse(self, response):
        for hotel in response.css('#hotel_list .searchresult_list2'):
            ctrip_item = ElongItem()
            front_url = ['http:' + hotel.css('.hotel_pic a img::attr(src)').extract()[0]]
            hotel_id = hotel.css('.searchresult_info_name h2::attr(data-id)').extract()[0]
            ctrip_item['hotel_id'] = hotel_id
            ctrip_item['hotel_name'] = hotel.css('.searchresult_info_name a::attr(title)').extract()[0]
            ctrip_item['hotel_front_img_url'] =  front_url
            print('a')
            ctrip_item['wherefrom'] = WhereFrom.objects.get(name='ctrip')
            yield ctrip_item
            yield Request(url=self.comment_base_url.format(hotel_id, 1), meta={'hotel_id': hotel_id}, headers=self.headers, callback=self.parse_item)
        if 'index' in response.meta.keys():
            if response.css('.c_down_nocurrent') == []:
                index = response.meta.get('index')
                index += 1
                next_url = self.base_next_url.format(index)
                print('b')
                yield Request(url=next_url, headers=self.headers, meta={'index': index}, callback=self.parse, dont_filter=True)
        else:
            index = 2
            next_url = self.base_next_url.format(index)
            print('c')
            yield Request(url=next_url, headers=self.headers, meta={'index': index}, callback=self.parse, dont_filter=True)
            print('ok')

    def parse_item(self, response):
        pass



