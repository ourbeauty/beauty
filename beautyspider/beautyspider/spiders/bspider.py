# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from beautyspider.items import BeautyItem


class BspiderSpider(CrawlSpider):
    name = 'bspider'
    allowed_domains = ['www.maxfactorcn.com']
    start_urls = ['http://www.maxfactorcn.com/']
    rules = (
        Rule(LinkExtractor(allow=(r'http://www.maxfactorcn.com/\?\.*.html'))),
        Rule(LinkExtractor(allow=(r'http://www.maxfactorcn.com/\?product-\d+.html')), callback='get_image_parse'),
    )

    def get_image_parse(self, response):
        class_id = response.xpath('//div[@class="Navigation"]/span[3]/a/text()').extract_first()
        zi_id = response.xpath('//div[@class="Navigation"]/span[5]/a/text()').extract_first()
        """如果zi_id为None则表示下面没有分类"""
        title = response.xpath('//h1[@class="goodsname"]/text()').extract_first()
        desc = response.xpath('//p[@class="brief"]/text()').extract_first()
        shi_price = response.xpath('//i[@class="mktprice1"]/text()').extract_first()
        sale_price = response.xpath('//span[@class="price1"]/text()').extract_first()
        goods_spec = response.xpath('//*[@id="goods-spec"]/table[2]/tr/td[2]/ul//li/a/img')
        pro_bgimg = response.xpath('//*[@id="goods-viewer"]/table/tr/td[1]/div/table/tr/td[2]/div/center/table/tr//td/a')
        pro_detail = response.xpath('//*[@id="goods-intro"]/div//img')
        goodprops = response.xpath('//*[@id="goods-viewer"]/table/tr/td[2]/form/ul[1]//li')
        goodprop = {}
        for props in goodprops:
            key = props.xpath('./span/text()').extract_first()
            value = props.xpath('./text()').extract_first()
            goodprop[key] = value
        items = BeautyItem()
        items['g_goodprops'] = goodprop
        items['c_name'] = class_id
        items['c2_name'] = zi_id
        items['g_name'] = title
        items['g_desc'] = desc
        items['g_mktprice'] = float(shi_price[2:])
        items['g_price'] = float(sale_price[2:])
        good = {}
        for goods_prop in goods_spec:
            value = goods_prop.xpath('./@src').extract_first()
            key = goods_prop.xpath('./@alt').extract_first()
            good[key] = value
        items['g_class'] = good
        bgs = []
        for bg in pro_bgimg:
            bgs.append(bg.xpath('./@imginfo').extract_first()[1:-1].split('\'')[-2])
        items['g_pics'] = bgs
        details = []
        for detail in pro_detail:
            details.append(detail.xpath('./@src').extract_first())
        items['g_info'] = details
        return items
