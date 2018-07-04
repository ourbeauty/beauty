# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

import pymysql


class BeautyspiderPipeline(object):

    def process_item(self, item, spider):
        first_cla = ['当季流行妆容', '底妆专区', '眼妆专区', '唇妆专区',
                     '卸妆清洁', '优雅日常妆', '甜蜜约会妆', '干练职业妆', '派对女王妆']
        sec_cla = ['瓷感轻妆', '雾面妆感', '浓密眼妆', '点睛魔捧', '梦露唇膏', '粉底霜/液',
                   '粉饼/蜜粉', '遮瑕笔', '腮红/胭脂', '气垫BB霜', '睫毛膏', '眼线', '眼影',
                   '眉笔', '唇膏', '唇彩', '护唇膏']

        index = first_cla.index(item['c_name'])

        code1 = index * 1000
        code2 = code1 + 1 + sec_cla.index(item['c2_name']) if item['c2_name'] in sec_cla else 0
        # print(item)
        # print(code1, code2)
        item['c_name'] = code1
        item['c2_name'] = code2
        item['g_class'] = item['g_class'] if item['g_class'] else 0
        # print(item)

        client = MongoClient('47.106.81.203', 27017)
        db = client.beauty
        db.detail.insert(dict(item))

        conn = pymysql.connect(host='47.106.81.203',
                               user='root',
                               password='admin@123',
                               db='beautytest',
                               port=3306)
        cursor = conn.cursor()

        s = ''
        for info in item['g_info']:
            s = s + info + ','
        item['g_info'] = s

        s = ''
        for info in item['g_pics']:
            s = s + info + ','
        item['g_pics'] = s

        s = ''
        for i, n in item['g_goodprops'].items():
            s = str(i) + str(n) + ','
        item['g_goodprops'] = s

        if item['g_class']:
            s = ''
            for x, y in item['g_class'].items():
                s = str(x) + str(y) + ','
            item['g_class'] = s

        sql = "INSERT INTO goods(c_code,c2_code,g_name,g_desc,g_info," \
              "g_mktprice,g_price,g_class,g_goodsprops,g_pics) VALUES " \
              "('%d','%d','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  item['c_name'], item['c2_name'], str(item['g_name']), str(item['g_desc']), str(item['g_info']),
                  str(item['g_mktprice']), str(item['g_price']), str(item['g_class']), str(item['g_goodprops']),
                  str(item['g_pics']))
        try:
            cursor.execute(sql)
            conn.commit()
            print('保存完成!')
        except Exception as e:

            conn.rollback()
            print(e)
            print('回滚!')
        conn.close()

        # return item
