# WeiboSpider-chinese-implicit-emotion-analysis

Use python language to implement web crawler. Sina weibo data were crawled to form Chinese implicit emotion analysis data set.

This is a sina weibo spider built by scrapy

The program needs to log into weibo with an account to get cookies, and then run the crawler. The database where cookies are stored is Redis.If you need to grab a lot of weibo data, need to maintain a large pool of accounts. That is, access to a large number of weibo accounts.

If you do need to grab a lot of data, you can contact me. Email: david_captain@sina.com

## Use the project：
Python version: Python 3.5
```bash
git clone https://github.com/L-Maybe/WeiboSpider-chinese-implicit-emotion-analysis.git

# First, get the cookie and store it in the database.
python cookie.py

# run spider
python run.py
```

## The purpose of this project is to construct Chinese implicit emotion analysis data set. Six basic emotions are used as keywords to crawl data.

## Flow chart for data set construction.

![image](https://github.com/L-Maybe/WeiboSpider-chinese-implicit-emotion-analysis/blob/master/crawler.png)