# -*- coding:utf-8 -*-
import pymongo
import NLPtools
import re

conn = pymongo.Connection('114.55.139.104', 27017)
db = conn.olympic

source_info = db.source
html_info = db.html

def PrecessHtml(doc):
    # delete all Tags and Js,Css's function)
    dTag = re.compile(r'<[^>]+>', re.S)
    dJs = re.compile(r'<script.*?/script>', re.S)
    dJS = re.compile(r'<SCRIPT.*?/SCRIPT>', re.S)
    dCss = re.compile(r'<style.*?/style>', re.S)
    preText = dJs.sub('', doc)
    preText = dJS.sub('', preText)
    preText = dCss.sub('', preText)
    preText = dTag.sub('', preText.encode('utf-8')).replace('\t', '').replace(' ', '').replace('&nbs','').replace('\r','')
    return preText

if __name__ == '__main__':
    for document in html_info.find():
        if document['page'] != None:
            pText = PrecessHtml(document['page'])
            setences  = preText.split('\n')
            for setence in setences:
                seg, pos = NLPtools.word_segment(setence)



