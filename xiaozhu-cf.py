#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' xiaozhuduanzu_review_reviewer_info v2.0 '

__author__ = 'Xiao Zhuangzhuang'

import requests
import lxml.html
import re
import csv
import glob
import pandas as pd

def get_comment_fangke_info(url):
    fangzi_id = re.findall('fangzi.(.*?).html', url)[0]
    fangzi_city = re.findall('http://(.*?).xiaozhu', url)[0]
    item_list = []
    for page in range(0, 5):
        comment_url = "http://" + fangzi_city + ".xiaozhu.com/ajax.php?op=Ajax_GetDetailComment&lodgeId=" + fangzi_id + "&cityDomain=undefined&p=" + str(page)
        content = requests.get(comment_url).content
        content = content.decode('utf-8')  # python3
        selector = lxml.html.fromstring(content)
        page_list = selector.xpath('//div[@class="dp_box clearfix mt_10"]/div')

        for each in page_list:
            item = {}
            item['fangzi_city'] = fangzi_city
            item['fangzi_id'] = fangzi_id
            item['fangke_url'] = each.xpath('h6/a/@href')[0]
            item['fangke_id'] = re.findall('fangke.(.*?)/', item['fangke_url'])[0]
            item['fangke_name'] = each.xpath('h6/a/span/text()')[0]
            item['comment_checkintime'] = each.xpath('h6/i/text()')
            item['comment_content'] = each.xpath('text()')[1]
            item['comment_content'] = ''.join(item['comment_content']).replace(' ', '').replace('\n', '')
            # # 每个fangke的界面
            each_source = requests.get(item['fangke_url']).content
            each_selector = lxml.html.fromstring(each_source)
            item['fangke_identify'] = each_selector.xpath('//ul[@class="fk_yz_ul"]/li/strong/text()')
            item['fangke_regtime'] = each_selector.xpath('//ul[@class ="fk_person"]/li/text()')[1]
            item_list.append(item)

    return item_list

def writeData(item_list):
    with open('city_sh.csv', 'a', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['fangzi_city','fangzi_id','fangke_url','fangke_id','fangke_name','comment_checkintime','comment_content','fangke_identify','fangke_regtime'])
        writer.writeheader()
        for each in item_list:
            writer.writerow(each)

if __name__ == '__main__':
    item_list = []
    # 获取指定目录下的xlsx，并打开操作
    for file in glob.glob(r"C:/Users/anhan/pythonfiles/xiaozhu/data-doing/*.xlsx"):
        df = pd.read_excel(file)
        urlList = df["fangzi_url"]
        for url in urlList:
            print(url)
            item_list += get_comment_fangke_info(url)
    writeData(item_list)




