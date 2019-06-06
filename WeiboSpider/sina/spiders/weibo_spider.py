#!/usr/bin/env python
# encoding: utf-8

import datetime
import requests
import re
from lxml import etree
from scrapy import Spider, FormRequest
from scrapy.selector import Selector
from scrapy.http import Request
from sina.config import KeyWordList

from sina.items import Weibo_Information
from sina.config import KeyWordList, TimeList


class Spider(Spider):
    name = "SinaSpider"
    max_page = 100
    #  keyword 关键字    hasor=1 原创
    def start_requests(self):
        for keyword in KeyWordList: # 6
            for query_date in TimeList:  #
                for page in range(1, self.max_page + 1):   # 2
                    url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={keyword}&advancedfilter=1&hasori=1&starttime={starttime}&endtime={endtime}&sort=time&page={page}'
                    yield Request(url=url.format(page=str(page), keyword=keyword, starttime=query_date, endtime=query_date), callback=self.parse_information)

    def parse_information(self, response):
        keyword = response.xpath('.//input[@name="keyword"]/@value').extract_first()
        weibos = response.xpath('//div[@class="c" and contains(@id, "M_")]')
        for item in weibos:
            try:
                weibo_information = Weibo_Information()
                text = ''
                nickname = item.xpath('.//a[@class="nk"]/text()').extract_first()
                idNum = item.xpath('.//a[@class="nk"]/@href').extract_first()
                idNum = re.findall('\d+', idNum)[0]
                # print('<span class="kt">{keyword}</span>'.format(keyword=self.keyword))
                format_item = re.sub('<span class="kt">{keyword}</span>'.format(keyword=keyword), keyword, item.extract())
                format_item = format_item.replace(':', '')
                format_item = Selector(text=format_item).xpath('.//span[@class="ctt"]/text()').extract()
                for line in format_item:
                    text += line
                time_and_termi = item.xpath('.//span[@class="ct"]/text()').extract_first()
                pub_time = time_and_termi[:12]
                termial = time_and_termi[15:] if len(time_and_termi[15:]) != 0 else 'iPhone客户端'
                weibo_information['_id'] = idNum
                weibo_information['NickName'] = nickname
                weibo_information['Text'] = text
                weibo_information['PupTime'] = pub_time
                weibo_information['Terminal'] = termial
                weibo_information['Token'] = keyword
                yield weibo_information
            except Exception as e:
                self.logger.info(e)
                pass


    # def parse_tweets(self, response):
    #     """ 抓取微博数据 """
    #     selector = Selector(response)
    #     ID = re.findall('(\d+)/profile', response.url)[0]
    #     divs = selector.xpath('body/div[@class="c" and @id]')
    #     for div in divs:
    #         try:
    #             tweetsItems = TweetsItem()
    #             id = div.xpath('@id').extract_first()  # 微博ID
    #             content = div.xpath('div/span[@class="ctt"]//text()').extract()  # 微博内容
    #             cooridinates = div.xpath('div/a/@href').extract()  # 定位坐标
    #             like = re.findall('赞\[(\d+)\]', div.extract())  # 点赞数
    #             transfer = re.findall('转发\[(\d+)\]', div.extract())  # 转载数
    #             comment = re.findall('评论\[(\d+)\]', div.extract())  # 评论数
    #             others = div.xpath('div/span[@class="ct"]/text()').extract()  # 求时间和使用工具（手机或平台）
    #
    #             tweetsItems["_id"] = ID + "-" + id
    #             tweetsItems["ID"] = ID
    #             if content:
    #                 tweetsItems["Content"] = " ".join(content).strip('[位置]')  # 去掉最后的"[位置]"
    #             if cooridinates:
    #                 cooridinates = re.findall('center=([\d.,]+)', cooridinates[0])
    #                 if cooridinates:
    #                     tweetsItems["Co_oridinates"] = cooridinates[0]
    #             if like:
    #                 tweetsItems["Like"] = int(like[0])
    #             if transfer:
    #                 tweetsItems["Transfer"] = int(transfer[0])
    #             if comment:
    #                 tweetsItems["Comment"] = int(comment[0])
    #             if others:
    #                 others = others[0].split('来自')
    #                 tweetsItems["PubTime"] = others[0].replace(u"\xa0", "")
    #                 if len(others) == 2:
    #                     tweetsItems["Tools"] = others[1].replace(u"\xa0", "")
    #             yield tweetsItems
    #         except Exception as e:
    #             self.logger.info(e)
    #             pass
    #
    #     url_next = selector.xpath('body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="下页"]/@href').extract()
    #     if url_next:
    #         yield Request(url=self.host + url_next[0], callback=self.parse_tweets, dont_filter=True)
    #
    # def parse_relationship(self, response):
    #     """ 打开url爬取里面的个人ID """
    #     selector = Selector(response)
    #     if "/follow" in response.url:
    #         ID = re.findall('(\d+)/follow', response.url)[0]
    #         flag = True
    #     else:
    #         ID = re.findall('(\d+)/fans', response.url)[0]
    #         flag = False
    #     urls = selector.xpath('//a[text()="关注他" or text()="关注她"]/@href').extract()
    #     uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
    #     for uid in uids:
    #         relationshipsItem = RelationshipsItem()
    #         relationshipsItem["fan_id"] = ID if flag else uid
    #         relationshipsItem["followed_id"] = uid if flag else ID
    #         yield relationshipsItem
    #         yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)
    #
    #     next_url = selector.xpath('//a[text()="下页"]/@href').extract()
    #     if next_url:
    #         yield Request(url=self.host + next_url[0], callback=self.parse_relationship, dont_filter=True)
