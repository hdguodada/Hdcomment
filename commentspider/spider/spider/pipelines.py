# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class HotelImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
            item["hotel_front_img_path"] = image_file_path
        return item


class Save_to_Mysql(object):
    def process_item(self, item, spider):
        for k, v in item.items():
            if v == '':
                item[k] = None
        item.save_to_mysql()
        return item