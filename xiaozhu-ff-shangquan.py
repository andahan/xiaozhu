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
        item['shangquan_url'] = url
        item['shangquan_name'] = re.findall('xiaozhu.com/(.*?)_', item['shangquan_url'])[0]
        item['shangquan_name'] = urllib.parse.unquote(item['shangquan_name'])
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
    with open('wh_ff_byshangquan.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['shangquan_url','shangquan_name','fangzi_latlng', 'fangzi_url','fangzi_id', 'fangzi_title', 'fangzi_price', 'fangdong_url','fangdong_id', 'fangzi_text', 'fangzi_comment_about',
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
    for j in ['http://wh.xiaozhu.com/%E4%B8%AD%E5%8D%97_uw1lmd-duanzufang-p{}-20/?putkey=%E4%B8%AD%E5%8D%97','http://wh.xiaozhu.com/%E8%A1%97%E9%81%93%E5%8F%A3_uw1lyd-duanzufang-p{}-20/?putkey=%E8%A1%97%E9%81%93%E5%8F%A3','http://wh.xiaozhu.com/%E9%92%9F%E5%AE%B6%E6%9D%91_uw1lxd-duanzufang-p{}-20/?putkey=%E9%92%9F%E5%AE%B6%E6%9D%91','http://wh.xiaozhu.com/%E6%B2%8C%E5%8F%A3_uw1lwd-duanzufang-p{}-20/?putkey=%E6%B2%8C%E5%8F%A3','http://wh.xiaozhu.com/%E6%AD%A6%E6%B1%89%E5%A4%A9%E5%9C%B0_uw1lvd-duanzufang-p{}-20/?putkey=%E6%AD%A6%E6%B1%89%E5%A4%A9%E5%9C%B0','http://wh.xiaozhu.com/%E8%A5%BF%E5%8C%97%E6%B9%96_uw1lud-duanzufang-p{}-20/?putkey=%E8%A5%BF%E5%8C%97%E6%B9%96','http://wh.xiaozhu.com/%E6%AD%A6%E6%B1%89%E5%B9%BF%E5%9C%BA_uw1ltd-duanzufang-p{}-20/?putkey=%E6%AD%A6%E6%B1%89%E5%B9%BF%E5%9C%BA','http://wh.xiaozhu.com/%E5%B9%BF%E5%9F%A0%E5%B1%AF_uw1lsd-duanzufang-p{}-20/?putkey=%E5%B9%BF%E5%9F%A0%E5%B1%AF','http://wh.xiaozhu.com/%E6%B1%9F%E6%B1%89%E8%B7%AF_uw1lrd-duanzufang-p{}-20/?putkey=%E6%B1%9F%E6%B1%89%E8%B7%AF','http://wh.xiaozhu.com/%E7%8E%8B%E5%AE%B6%E6%B9%BE_uw1lqd-duanzufang-p{}-20/?putkey=%E7%8E%8B%E5%AE%B6%E6%B9%BE','http://wh.xiaozhu.com/%E5%85%89%E8%B0%B7%E6%AD%A5%E8%A1%8C%E8%A1%97_uw1lpd-duanzufang-p{}-20/?putkey=%E5%85%89%E8%B0%B7%E6%AD%A5%E8%A1%8C%E8%A1%97','http://wh.xiaozhu.com/%E5%8F%B8%E9%97%A8%E5%8F%A3_uw1lod-duanzufang-p{}-20/?putkey=%E5%8F%B8%E9%97%A8%E5%8F%A3','http://wh.xiaozhu.com/%E5%BE%90%E4%B8%9C_uw1lnd-duanzufang-p{}-20/?putkey=%E5%BE%90%E4%B8%9C','http://wh.xiaozhu.com/%E8%8F%B1%E8%A7%92%E6%B9%96_uw1lzd-duanzufang-p{}-20/?putkey=%E8%8F%B1%E8%A7%92%E6%B9%96']:
        for i in range(1, 14):
            pageLink = j.format(i)
            print(pageLink)
            item_list += get_fangzi_fangdong_info(pageLink)
    writeData(item_list)