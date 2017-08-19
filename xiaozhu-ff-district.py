#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' xiaozhuduanzu_fangzi_fangdong_info v2.0 '

__author__ = 'Xiao Zhuangzhuang'

import requests
import lxml.html
import re
import csv

full_url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'
full_district_url = 'http://bj.xiaozhu.com/{}-duanzufang-p{}-8/'

def getSource(url):
    '''
    获取网页源代码。
    :param url:
    :return: String
    '''
    content = requests.get(url)
    content.encoding = 'UTF-8'  # 强制修改编码,防止Windows下出现乱码
    return content.content

def get_fangzi_fangdong_info(source):
    '''
    在full页面上和each界面上获取该城市每个房子的相关信息。 item字典用于保存房子的信息。
    :param source:
    :return: [item1,item2, item3,...]
    '''
    selector = lxml.html.fromstring(source)
    page_list = selector.xpath('//div[@id="page_list"]/ul/li')
    item_list = []


    def writefzPic(pic_list, fangzi_id):
        for each in pic_list:
            pic = requests.get(each)
            fp = open('pic\\' + 'fz' + str(fangzi_id) + '.jpg', 'wb')
            fp.write(pic.content)

    def writefdPic(pic_list, fangzi_id, fangdong_id):
        for each in pic_list:
            pic = requests.get(each)
            fp = open('pic\\' + 'fz' + str(fangzi_id) + 'fd' + str(fangdong_id) + '.jpg', 'wb')
            fp.write(pic.content)

    for each in page_list:
        item = {}
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
        item['fangzi_address'] = each_selector.xpath('//div[@class="pho_info"]/p/@title')[0]
        item['fangzi_pic'] = each_selector.xpath('//div[@class ="pho_show_big"]/div/img/@src')
        print(item['fangzi_pic'])
        writefzPic(item['fangzi_pic'],item['fangzi_id'])
        item['fangzi_area'] = each_selector.xpath('//li[@class ="border_none"]/p/text()')[0].replace(' ', '').replace('\n', '')
        item['fangzi_units'] = each_selector.xpath('//li[@class ="border_none"]/p/text()')[1].replace(' ', '').replace('\n', '')
        item['fangzi_description'] = each_selector.xpath('//*[@id="introducePart"]/div[1]/div[2]/div[1]/p/text()')
        item['fangzi_inner'] = each_selector.xpath('//*[@id="introducePart"]/div[2]/div[2]/div[1]/p/text()')
        item['fangzi_transportation'] = each_selector.xpath('//*[@id="introducePart"]/div[3]/div[2]/div[1]/p/text()')
        item['fangzi_around'] = each_selector.xpath('//*[@id="introducePart"]/div[4]/div[2]/div[1]/p/text()')
        item['fangzi_introitem'] = each_selector.xpath('//div[@class="intro_item_content"]/ul[@class="pt_list clearfix"]/li/text()')
        item['fangzi_shouldknow'] = each_selector.xpath('//div[@class="info_text_mid"]/ul[@class="check_con clearfix"]/li/text()')
        item['fangzi_otherfee'] = each_selector.xpath('//*[@id="rulesPart"]/div[1]/p/text()')[0].replace(' ', '').replace('\n', '')
        item['fangdong_name'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/h6/a/text()')[0]
        item['fangdong_sex'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/h6/span/@class')[0]
        item['fangdong_identify'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/p/span/text()')
        item['fangdong_pic'] = each_selector.xpath('//div[@class="js_box clearfix"]/div/a/img/@src')
        item['fangdong_zmscore'] = each_selector.xpath('//span[@class="zm_ico zm_credit"]/text()')
        print(item['fangdong_pic'])
        writefdPic(item['fangdong_pic'], item['fangzi_id'], item['fangdong_id'])

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
            item['fangdong_fangzinum'] = each_fangdong_selector.xpath('//li[@class="nav_bg2"]/span/text()')[0]
            item['fangdong_ordersum'] = each_fangdong_selector.xpath('//li[@class="nav_bg4"]/span/text()')[0]
            item['fangdong_replyratio'] = each_fangdong_selector.xpath('//ul[@class="infor_ul"]/li/strong/text()')[0]
            item['fangdong_confirmtime'] = each_fangdong_selector.xpath('//ul[@class="infor_ul"]/li/strong/text()')[1]
            item['fangdong_orderratio'] = each_fangdong_selector.xpath('//ul[@class="infor_ul"]/li/strong/text()')[2]

        item_list.append(item)
    return item_list

def writeData(item_list):
    with open('bj_bydistrict.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['fangzi_latlng', 'fangzi_url','fangzi_id', 'fangzi_title', 'fangzi_price', 'fangdong_url','fangdong_id', 'fangzi_text', 'fangzi_comment_about',
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
    for j in ['chaoyang','haidian','dongcheng','fengtai','changping','xicheng','daxing','tongzhou','shunyi','fangshan','miyun','shijingshan','huairou','yanqing','pinggu','yanjiao','mentougou']:
        for i in range(1, 14):
            pageLink = full_district_url.format(j,i)
            print(pageLink)
            source = getSource(pageLink)
            item_list += get_fangzi_fangdong_info(source)
    writeData(item_list)