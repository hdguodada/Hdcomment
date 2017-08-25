# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import json
import re
from scrapy.http import Request
from ..items import ElongItem
from commentspider.models import WhereFrom


class ElongSpider(scrapy.Spider):
    name = 'elong'
    allowed_domains = ['hotel.elong.com']
    start_urls = [
        'http://hotel.elong.com/ajax/list/asyncsearch/?listRequest.cityID=1288&listRequest.pageIndex={0}'.format(1)]
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
    headers = {
        'Host': 'hotel.elong.com',
        'Origin': 'http://hotel.elong.com',
        'Referer': 'http://hotel.elong.com/hengdian_jin_hua/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    def start_requests(self):
        index = 1
        return [
            scrapy.Request(
                self.start_urls[0],
                meta={
                    'index': index},
                headers=self.headers,
                callback=self.parse)]

    def parse(self, response):
        hotellisthtml = json.loads(response.text).get(
            'value').get('hotelListHtml')
        soup = BeautifulSoup(hotellisthtml, "lxml")
        # 获得当前页酒店列表
        hotellist = soup.find_all(class_='h_item')
        for x in hotellist:
            # hotel_name = scrapy.Field()
            # hotel_id = scrapy.Field()
            # hotel_front_img_url = scrapy.Field()
            # hotel_front_img_path = scrapy.Field()
            Elong_item = ElongItem()
            Elong_item['hotel_id'] = re.sub(r'[^\d]+', '', x.a['href'])
            Elong_item['hotel_name'] = x.img['alt']
            Elong_item['hotel_front_img_url'] = [x.img['src']]
            Elong_item['wherefrom'] = WhereFrom.objects.get(name='elong')
            yield Elong_item
        if response.meta.get('index'):
            index = response.meta.get('index')
            index += 1
            if index <= 11:
                url = 'http://hotel.elong.com/ajax/list/asyncsearch/?listRequest.cityID=1288&listRequest.pageIndex={0}'.format(
                    index)
                yield Request(url=url, meta={'index': index}, callback=self.parse, dont_filter=True)
