import os

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ccamspider.items import FileItem


def isFile(url):
    if url.endswith('/'):
        return False
    else:
        return True


class ChemcamSpider(scrapy.Spider):
    name = "chemcam"

    allowed_domains = ["pds-geosciences.wustl.edu"]
    base_url = "https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/"
    start_urls = ["https://pds-geosciences.wustl.edu/msl/msl-m-chemcam-libs-4_5-rdr-v1/mslccm_1xxx/"]

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        item_list = sel.re(r'<a.*?href="(.*?)">.*?</a>')
        name_list = sel.re(r'<a.*?href=".*?">(.*?)</a>')
        item_list = [item_list[index] for index, item in enumerate(name_list) if item != '[To Parent Directory]']

        urls = [response.urljoin(item) for item in item_list if isFile(item)]
        if len(urls) != 0:
            files = FileItem()
            category, _ = os.path.split(urls[0])
            category = os.path.relpath(category, self.base_url)
            files['file_urls'] = urls
            files['category'] = category
            yield files

        for item in item_list:
            if not isFile(item):
                url = response.urljoin(item)
                yield Request(url=url, dont_filter=True)
