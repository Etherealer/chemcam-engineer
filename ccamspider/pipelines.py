# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.files import FilesPipeline

from ccamspider import settings


class FileDownloadPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        request_list = super(FileDownloadPipeline, self).get_media_requests(item, info)
        for obj in request_list:
            obj.item = item
        return request_list

    def file_path(self, request, response=None, info=None, *, item=None):
        category = request.item.get('category')
        files_store = settings.FILES_STORE
        category_path = os.path.join(files_store, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        file_name = request.url.split("/")[-1]
        file_path = os.path.join(category_path, file_name)
        return file_path
