from pymongo import *
import pandas as pd
'''
查询方法：
    find_one()返回满足条件的文档集中第一条数据，类型为字典
                如果没有查询结果返回None
    方法find()返回满足条件的所有文档，类型为Cursor对象，可以使用for...in遍历，每项为字典对象
            如果没有查询结果返一个空的Cursor对象
'''

WeiBoAccounts = [
    {'username': 'xxxxx@sina.com', 'password': '111111'},
]

import time
import datetime
def select():
    accountList = []
    j = 0
    try:
        client = MongoClient(host="localhost", port=27017)
        db = client.Sina    # 使用demo数据库
#         # #  查看哪些账号不符合规范
#         # res = db.userAccount.find()
#         # for item in res:
#         #     if len(item['cookie']) != 5:
#         #         for i in range(len(WeiBoAccounts)):
#         #             if item['_id'] == WeiBoAccounts[i]['username']:
#         #                 print(WeiBoAccounts[i])
#
#         # 查询哪些账号没有存进mongodb
#         # res = db.userAccount.find()
#         # for item in res:
#         #     accountList.append(item['_id'])
#         #
#         # for i in range(len(WeiBoAccounts)):
#         #     j += 1
#         #     if WeiBoAccounts[i]['username'] not in accountList:
#         #         print(WeiBoAccounts[i])
#         # print(j)
#
        count = db.weibo_information.count()
        print('日期：%s' % (datetime.datetime.now()))
        print(count)
        time.sleep(60)
        select()

    except Exception as e:
        print(e)

#  生成日期
# import datetime
#
# # version_2
# start = '2017-08-01'
# end = '2018-02-01'
# # version_1
# # start = '2018-02-02'
# # end = '2018-08-01'
#
# datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
# dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
#
# while datestart < dateend:
#     datestart += datetime.timedelta(days=1)
#     print(datestart.strftime('%Y%m%d'))



# from sina.config import KeyWordList
# for item in range(len(KeyWordList)):
#     print(KeyWordList[item])


# def merge(self, intervals):
#     out = []
#     for i in sorted(intervals, key=lambda i : i.start):
#         if out and i.start <= out[-1].end:
#             out[-1].end = max(out[-1].end, i.end)
#         else:
#             out += i,
#     return out
import re

def data_tocsv():
    labels = {'开心':'happy', '伤心':'sad', '厌恶':'disgust', '生气':'anger', '惊讶':'surprise', '害怕':'fear'}

    try:
        for key, value in sorted(labels.items()):
            list = []
            client = MongoClient(host="localhost", port=27017)
            db = client.Sina
            count = db.weibo_information.find({'Token': key})
            for item in count:
                if len(item['Text']) > 250:
                    continue
                line = []
                token = item["Token"]
                # token = token.strip()
                line.append(token)
                text = item['Text']
                # text = text.encode('unicode_escape')
                text = re.sub('200b', '', text)
                # text = re.sub('\\n', '', text)
                # text = text.decode('utf-8')
                line.append(text)
                list.append(line)
            result = pd.DataFrame(data=list, columns=['sentiment', 'review'])
            result.to_csv('E:/'+value+'_1.csv', sep='\t', index=False, encoding='utf-8')


    except Exception as e:
        print(e)
#
# def demo():
#     str = 'Monster-\xe5\x88\x98\xe5\xae\xaa\xe5\x8d\x8eHenry-Lau \xe2\x80\x8b'
#     print(str.replace('\xe2\x80\x8b','').encode('gbk'))
#
#
#
if __name__ == '__main__':
    data_tocsv()