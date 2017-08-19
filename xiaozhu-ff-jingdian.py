#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' xiaozhuduanzu_fangzi_fangdong_info v2.0 '

__author__ = 'Xiao Zhuangzhuang'

import requests
import lxml.html
import re
import csv
import urllib.parse

full_url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'
full_district_url = 'http://bj.xiaozhu.com/{}-duanzufang-p{}-8/'

'''
在使用本程序之前，先要替换该城市所对应的jingdian url，
改存放文件名字。
然后执行一次。
'''

def get_fangzi_fangdong_info(url):
    '''
    在full页面上和each界面上获取该城市每个房子的相关信息。 item字典用于保存房子的信息。
    :param source:
    :return: [item1,item2, item3,...]
    '''
    source = requests.get(url).content
    selector = lxml.html.fromstring(source)
    page_list = selector.xpath('//div[@id="page_list"]/ul/li')
    item_list = []

    for each in page_list:
        item = {}
        item['jingdian_url'] = url
        item['jingdian_name'] = re.findall('xiaozhu.com/(.*?)_', item['jingdian_url'])[0]
        item['jingdian_name'] = urllib.parse.unquote(item['jingdian_name'])
        item['fangzi_latlng'] = each.xpath('@latlng')[0]
        item['fangzi_url'] = each.xpath('a/@href')[0]
        item['fangzi_id'] = re.findall('fangzi.(.*?).html', item['fangzi_url'])[0]
        item['fangzi_title'] = each.xpath('a/img/@title')[0]
        item['fangzi_price'] = each.xpath('div/span[@class="result_price"]/i/text()')[0]
        item['fangdong_url'] = each.xpath('div/span[@class ="result_img"]/a/@href')[0]
        item['fangdong_id'] = re.findall('fangdong.(.*?)/', item['fangdong_url'])[0]
        item['fangzi_text'] = each.xpath('div/div/em/text()')[0]
        item['fangzi_text'] = ''.join(item['fangzi_text']).replace('                            ', '').replace('\n', '')
        item['fangzi_comment_about'] = each.xpath('div/div/em/span[@class ="commenthref"]/text()')[0]
        item['fangzi_comment_about'] = ''.join(item['fangzi_comment_about']).replace(' ', '').replace('\n', '')
        # each 界面--每个房子的界面
        each_source = requests.get(item['fangzi_url']).content
        each_selector = lxml.html.fromstring(each_source)
        item['fangzi_address'] = each_selector.xpath('//div[@class="pho_info"]/p/@title')
        item['fangzi_pic'] = each_selector.xpath('//div[@class ="pho_show_big"]/div/img/@src')[0]
        item['fangzi_area'] = each_selector.xpath('//li[@class ="border_none"]/p/text()')[0].replace(' ', '').replace('\n', '')
        item['fangzi_units'] = each_selector.xpath('//li[@class ="border_none"]/p/text()')[1].replace(' ', '').replace('\n', '')
        item['fangzi_description'] = each_selector.xpath('//*[@id="introducePart"]/div[1]/div[2]/div[1]/p/text()')
        item['fangzi_inner'] = each_selector.xpath('//*[@id="introducePart"]/div[2]/div[2]/div[1]/p/text()')
        item['fangzi_transportation'] = each_selector.xpath('//*[@id="introducePart"]/div[3]/div[2]/div[1]/p/text()')
        item['fangzi_around'] = each_selector.xpath('//*[@id="introducePart"]/div[4]/div[2]/div[1]/p/text()')
        item['fangzi_introitem'] = each_selector.xpath('//div[@class="intro_item_content"]/ul[@class="pt_list clearfix"]/li/text()')
        item['fangzi_shouldknow'] = each_selector.xpath('//div[@class="info_text_mid"]/ul[@class="check_con clearfix"]/li/text()')
        item['fangzi_otherfee'] = each_selector.xpath('//*[@id="rulesPart"]/div[1]/p/text()')[0].replace(' ', '').replace('\n', '')
        item['fangdong_pic'] = each_selector.xpath('//div[@class="member_pic"]/a/@href')[0]
        item['fangdong_name'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/h6/a/text()')[0]
        item['fangdong_sex'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/h6/span/@class')[0]
        item['fangdong_identify'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/p/span/text()')
        item['fangdong_zmscore'] = each_selector.xpath('//span[@class="zm_ico zm_credit"]/text()')

        # each 界面--每个房东的界面
        each_fangdong_source = requests.get(item['fangdong_url']).content
        each_fangdong_selector = lxml.html.fromstring(each_fangdong_source)
        fangdong_noexistHtml = each_fangdong_selector.xpath('//p[@class ="fd_p"]/text()')

        if fangdong_noexistHtml:
            item['fangdong_fangzinum'] = each_fangdong_selector.xpath('//div[@class="fd_infor"]/ul/li/span/strong/text()')[0]
            item['fangdong_replyratio'] = each_fangdong_selector.xpath('//div[@class="fd_infor"]/ul/li/span/strong/text()')[1]
            item['fangdong_confirmtime'] = each_fangdong_selector.xpath('//div[@class="fd_infor"]/ul/li/span/strong/text()')[3]
            item['fangdong_ordersum'] = each_fangdong_selector.xpath('//div[@class="fd_infor"]/ul/li/span/strong/text()')[4]
            item['fangdong_orderratio'] = each_fangdong_selector.xpath('//div[@class="fd_infor"]/ul/li/span/strong/text()')[5]
        else:
            item['fangdong_fangzinum'] = each_fangdong_selector.xpath('//li[@class="nav_bg2"]/span/text()')
            item['fangdong_ordersum'] = each_fangdong_selector.xpath('//li[@class="nav_bg4"]/span/text()')[0]
            item['fangdong_replyratio'] = each_fangdong_selector.xpath('//ul[@class="infor_ul"]/li/strong/text()')[0]
            item['fangdong_confirmtime'] = each_fangdong_selector.xpath('//ul[@class="infor_ul"]/li/strong/text()')[1]
            item['fangdong_orderratio'] = each_fangdong_selector.xpath('//ul[@class="infor_ul"]/li/strong/text()')[2]

        item_list.append(item)
    return item_list

def writeData(item_list):
    with open('sanya_ff_byjingdian.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['jingdian_url','jingdian_name','fangzi_latlng', 'fangzi_url','fangzi_id', 'fangzi_title', 'fangzi_price', 'fangdong_url','fangdong_id', 'fangzi_text', 'fangzi_comment_about',
                                               'fangzi_address','fangzi_pic','fangzi_area','fangzi_units',
                                               'fangzi_description', 'fangzi_inner', 'fangzi_transportation', 'fangzi_around','fangzi_introitem', 'fangzi_shouldknow','fangzi_otherfee',
                                               'fangdong_pic','fangdong_name','fangdong_sex','fangdong_identify','fangdong_zmscore',
                                               'fangdong_fangzinum','fangdong_replyratio','fangdong_confirmtime','fangdong_ordersum','fangdong_orderratio'])
        writer.writeheader()
        for each in item_list:
            print(each)
            writer.writerow(each)

if __name__ == '__main__':
    item_list = []
    for j in ['http://sanya.xiaozhu.com/%E4%BA%9A%E9%BE%99%E6%B9%BE_uw1jed-duanzufang-p{}-20/?putkey=%E4%BA%9A%E9%BE%99%E6%B9%BE','http://sanya.xiaozhu.com/%E8%9C%88%E6%94%AF%E6%B4%B2%E5%B2%9B_uw1jfd-duanzufang-p{}-20/?putkey=%E8%9C%88%E6%94%AF%E6%B4%B2%E5%B2%9B','http://sanya.xiaozhu.com/%E5%A4%A7%E4%B8%9C%E6%B5%B7_uw1jgd-duanzufang-p{}-20/?putkey=%E5%A4%A7%E4%B8%9C%E6%B5%B7','http://sanya.xiaozhu.com/%E4%B8%89%E4%BA%9A%E6%B9%BE_uw1jhd-duanzufang-p{}-20/?putkey=%E4%B8%89%E4%BA%9A%E6%B9%BE','http://sanya.xiaozhu.com/%E5%A4%A9%E6%B6%AF%E6%B5%B7%E8%A7%92_uw1jid-duanzufang-p{}-20/?putkey=%E5%A4%A9%E6%B6%AF%E6%B5%B7%E8%A7%92','http://sanya.xiaozhu.com/%E9%B9%BF%E5%9B%9E%E5%A4%B4_uw1jjd-duanzufang-p{}-20/?putkey=%E9%B9%BF%E5%9B%9E%E5%A4%B4','http://sanya.xiaozhu.com/%E5%87%A4%E5%87%B0%E5%B2%9B_uw1jkd-duanzufang-p{}-20/?putkey=%E5%87%A4%E5%87%B0%E5%B2%9B','http://sanya.xiaozhu.com/%E5%A4%A7%E5%B0%8F%E6%B4%9E%E5%A4%A9_uw1jld-duanzufang-p{}-20/?putkey=%E5%A4%A7%E5%B0%8F%E6%B4%9E%E5%A4%A9','http://sanya.xiaozhu.com/%E7%BE%8E%E4%B8%BD%E4%B9%8B%E5%86%A0_uw1jmd-duanzufang-p{}-20/?putkey=%E7%BE%8E%E4%B8%BD%E4%B9%8B%E5%86%A0','http://sanya.xiaozhu.com/%E7%99%BD%E9%B9%AD%E5%85%AC%E5%9B%AD_uw1jnd-duanzufang-p{}-20/?putkey=%E7%99%BD%E9%B9%AD%E5%85%AC%E5%9B%AD','http://sanya.xiaozhu.com/%E8%9D%B4%E8%9D%B6%E8%B0%B7_uw1jod-duanzufang-p{}-20/?putkey=%E8%9D%B4%E8%9D%B6%E8%B0%B7','http://sanya.xiaozhu.com/%E7%83%AD%E5%B8%A6%E5%A4%A9%E5%A0%82%E6%A3%AE%E6%9E%97%E5%85%AC%E5%9B%AD_uw1jpd-duanzufang-p{}-20/?putkey=%E7%83%AD%E5%B8%A6%E5%A4%A9%E5%A0%82%E6%A3%AE%E6%9E%97%E5%85%AC%E5%9B%AD','http://sanya.xiaozhu.com/%E6%B5%B7%E5%BA%95%E4%B8%96%E7%95%8C_uw1jqd-duanzufang-p{}-20/?putkey=%E6%B5%B7%E5%BA%95%E4%B8%96%E7%95%8C','http://sanya.xiaozhu.com/%E5%87%A4%E5%87%B0%E5%B2%AD%E5%85%AC%E5%9B%AD_uw1jrd-duanzufang-p{}-20/?putkey=%E5%87%A4%E5%87%B0%E5%B2%AD%E5%85%AC%E5%9B%AD','http://sanya.xiaozhu.com/%E8%90%BD%E7%AC%94%E6%B4%9E_uw1jsd-duanzufang-p{}-20/?putkey=%E8%90%BD%E7%AC%94%E6%B4%9E','http://sanya.xiaozhu.com/%E8%A5%BF%E5%B2%9B_10m0ovd-duanzufang-p{}-20/?putkey=%E8%A5%BF%E5%B2%9B','http://sanya.xiaozhu.com/%E5%B4%96%E5%B7%9E%E5%8F%A4%E5%9F%8E_10m0ppd-duanzufang-p{}-20/?putkey=%E5%B4%96%E5%B7%9E%E5%8F%A4%E5%9F%8E']:
        for i in range(1, 14):
            pageLink = j.format(i)
            print(pageLink)
            item_list += get_fangzi_fangdong_info(pageLink)
    writeData(item_list)