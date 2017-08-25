# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import os
import sys
sys.path.append('/home/yumo/myproject/Hdcomment/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hdcomment.settings")
import django
django.setup()
import scrapy
from commentspider.models import HotelIndex, HotelDetail
import time
import re
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ElongItem(scrapy.Item):
    """
    elong的所有横店酒店，包含酒店名，酒店的id，酒店的封面图url和存储路径
    """
    hotel_name = scrapy.Field()
    hotel_id = scrapy.Field()
    hotel_front_img_url = scrapy.Field()
    hotel_front_img_path = scrapy.Field()
    wherefrom = scrapy.Field()

    def save_to_mysql(self):
        hotel_name = self['hotel_name']
        hotel_id = self['hotel_id']
        hotel_front_img_url = self['hotel_front_img_url']
        hotel_front_img_path = self['hotel_front_img_path']
        wherefrom = self['wherefrom']
        print('d')
        HotelIndex.objects.create(
            hotel_name=hotel_name,
            hotel_id=hotel_id,
            hotel_front_img_path=hotel_front_img_path,
            hotel_front_img_url=hotel_front_img_url[0], wherefrom=wherefrom)


def date_time(value):
    createtime = time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime(
            value / 1000))
    return createtime




def remove_biaoqing(value):
    pattern = re.compile(r'[\u4e00-\u9af5]+')
    a = re.match(pattern, value)
    if a:
        return a.group(0)


class ElongDetailItem(scrapy.Item):
    """
    艺龙的酒店评论item
    """
    guest_nickname = scrapy.Field()
    guest_content = scrapy.Field()
    create_time = scrapy.Field()
    commentExt_roomNum = scrapy.Field()
    commentExt_roomTypeId = scrapy.Field()
    commentExt_roomTypeName = scrapy.Field()
    commentExt_checkInTime = scrapy.Field()
    replys_replyId = scrapy.Field()
    replys_content = scrapy.Field()
    replys_createTime = scrapy.Field()
    hotel = scrapy.Field()
    wherefrom = scrapy.Field()

    def save_to_mysql(self):
        guest_nickname = self['guest_nickname']
        guest_content = self['guest_content']
        create_time = self['create_time']
        commentExt_roomNum = self['commentExt_roomNum']
        commentExt_roomTypeId = self['commentExt_roomTypeId']
        commentExt_roomTypeName = self['commentExt_roomTypeName']
        commentExt_checkInTime = self['commentExt_checkInTime']
        hotel = self['hotel']
        wherefrom = self['wherefrom']
        if 'replys_replyId' in self.keys():
            replys_replyId = self['replys_replyId']
            replys_content = self['replys_content']
            replys_createTime = self['replys_createTime']
            HotelDetail.objects.create(
                guest_nickname=guest_nickname,
                guest_content=guest_content,
                create_time=create_time,
                commentExt_roomNum=commentExt_roomNum,
                commentExt_roomTypeId=commentExt_roomTypeId,
                commentExt_roomTypeName=commentExt_roomTypeName,
                commentExt_checkInTime=commentExt_checkInTime,
                replys_replyId=replys_replyId,
                replys_content=replys_content,
                replys_createTime=replys_createTime,
                hotel=hotel,
                wherefrom=wherefrom)
        else:
            HotelDetail.objects.create(
                guest_nickname=guest_nickname,
                guest_content=guest_content,
                create_time=create_time,
                commentExt_roomNum=commentExt_roomNum,
                commentExt_roomTypeId=commentExt_roomTypeId,
                commentExt_roomTypeName=commentExt_roomTypeName,
                commentExt_checkInTime=commentExt_checkInTime,
                hotel=hotel,
                wherefrom=wherefrom)


