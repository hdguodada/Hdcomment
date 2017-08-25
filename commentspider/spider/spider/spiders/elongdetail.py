# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ElongDetailItem, date_time, remove_biaoqing


from commentspider.models import HotelIndex, WhereFrom
from scrapy.http import Request


class ElongdetailSpider(scrapy.Spider):
    name = 'elongdetail'
    allowed_domains = ['http://elong.hotel.com']
    index = 1
    base_url = 'http://hotel.elong.com/ajax/detail/gethotelreviews/?hotelId={0}&pageIndex={1}'
    start_id = 91010014
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
    headers = {
        'Host':'hotel.elong.com',
        'Origin':'http://hotel.elong.com',
        'Referer':'http://hotel.elong.com/hengdian_jin_hua/',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }


    def parse(self, response):
        comment_detail = json.loads(response.text)
        if comment_detail['totalNumber'] != 0:

            if 'x' in response.meta.keys():
                x = response.meta.get('x')
                x += 1
                id = response.meta.get('hotel_id')
                url = self.base_url.format(id, x)
                yield Request(url=url, meta={'hotel_id': id, 'x': x}, headers=self.headers, callback=self.parse, dont_filter=True)
            else:
                x = 2
                id = response.meta.get('hotel_id')
                url = self.base_url.format(id, x)
                yield Request(url=url, meta={'hotel_id': id, 'x': x},headers=self.headers, callback=self.parse, dont_filter=True)

            for content in comment_detail['contents']:
                detail_item = ElongDetailItem()
                detail_item['guest_nickname'] = content['commentUser']['nickName']
                detail_item['guest_content'] = remove_biaoqing(content['content'])
                detail_item['create_time'] = date_time(content['createTime'])
                detail_item['commentExt_roomNum'] = content['commentExt']['order']['roomNum']
                detail_item['commentExt_roomTypeId'] = content['commentExt']['order']['roomTypeId']
                detail_item['commentExt_roomTypeName'] = content['commentExt']['order']['roomTypeName']
                detail_item['commentExt_checkInTime'] = date_time(content['commentExt']['order']['checkInTime'])
                if content['replys']:
                    detail_item['replys_replyId'] = content['replys'][0]['replyId']
                    detail_item['replys_content'] = content['replys'][0]['content']
                    detail_item['replys_createTime'] = date_time(content['replys'][0]['createTime'])
                detail_item['hotel'] = HotelIndex.objects.get(hotel_id=response.meta.get('hotel_id'))
                detail_item['wherefrom'] = WhereFrom.objects.get(name='elong')
                yield detail_item


    def parse_detail(self, response):
            pass


    def start_requests(self):
        hotelIds = HotelIndex.objects.all()
        hotelid_list = []
        for hotelid in hotelIds:
            hotelid_list.append(hotelid.hotel_id)
        for id in hotelid_list:
            yield Request(url=self.base_url.format(id, self.index), meta={'hotel_id': id}, headers=self.headers, callback=self.parse)


