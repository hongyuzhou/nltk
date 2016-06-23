# -*- coding:utf-8 -*-

import pymongo
import NLPtools
import re
import SearchEnginClient

conn = pymongo.Connection('121.199.68.185')
db = conn.weibo

_SORT = [('_id', 1)]
cond = {'status' : {'$gte' : -1},'_id':{'$gt':1463328000000000}}
_NEWS_FIELDS = {
    '_id' : 1,
    'did' : 1,
    'news.title' : 1,
    'news.content': 1,
    'news.url': 1
}


def clean_content(text):
    dTag = re.compile(r'<[^>]+>', re.S)
    preText = dTag.sub('', text).replace('\t', '').replace('\r','').replace(' ','')
    return preText

def segemnt_process(text):
    newText = ''
    if text != '':
        seg, pos = NLPtools.word_segment(text)                              
        for ss in seg:
            newText += (ss.encode('utf-8') + ' ')
    return newText


for news in db.infos.find(cond, fields=_NEWS_FIELDS, sort=_SORT):
    try:
        Info = []

        _id = long(news['_id'])
        Info.append(_id)

        url = news['news']['url']
        Info.append(url)

        title = segemnt_process(news['news']['title'].encode('utf-8').replace(' ',''))
        Info.append(title)

        content = segemnt_process(clean_content(news['news']['content'].encode('utf-8')))        
        Info.append(content)
        SearchEnginClient.startIndex(Info)

    except Exception, e:
        print e
        continue
    
