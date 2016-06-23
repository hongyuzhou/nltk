# -*- coding:utf-8 -*-

import requests


def startIndex(LL):
    doc = {'id': LL[0], 'url':LL[1], 'title':LL[2], 'content':LL[3]}
    return requests.post('http://127.0.0.1:12000/index', data=doc)

def startSearch(keywords):
    query = {'keywords': keywords}
    r = requests.post('http://127.0.0.1:12000/search', data=query)
    return r.text


if __name__ == '__main__':
    #while True:
    print len(startSearch('韩国,明星').split('\n'))
