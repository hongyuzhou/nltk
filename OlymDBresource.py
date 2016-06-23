# -*- coding:utf-8 -*-

import pymongo
import NLPtools
import re
import SearchEnginClient

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
    loop = 0
    start = 0
    while start <= html_info.count():
        try:
            for document in html_info.find().skip(start):
                try:
                    if document['page'] != None:
                        pText = PrecessHtml(document['page'])
                        setences = pText.split('\n')
                        newSetence = ''
                        for setence in setences:
                            if setence != '':
                                seg, pos = NLPtools.word_segment(setence)                              
                                for ss in seg:
                                    newSetence += (ss.encode('utf-8') + ' ')
                                newSetence += '\n'
                        SearchEnginClient.startIndex(newSetence)
                    loop += 1
                    print loop
                except Exception, e:
                    print e
                    continue
        except Exception, e:
            continue
        finally:
            start = loop
            print start

    # loop = 15174
    # for document in html_info.find().skip(15173):
    #     try:
    #         if loop >= 15174:
    #             if document['page'] != None:
    #                 toWrite = open('/home/hongyz/chatBotContent/page' + str(loop) + '.txt', 'w+')
    #                 pText = PrecessHtml(document['page'])
    #                 setences  = pText.split('\n')
    #                 for setence in setences:
    #                     if setence != '':
    #                         seg, pos = NLPtools.word_segment(setence)
    #                         newSetence = ''
    #                         for ss in seg:
    #                             newSetence += (ss.encode('utf-8') + ' ')
    #                         toWrite.write(newSetence + '\n')
    #                 toWrite.close()
    #     except:
    #         continue
    #     finally:
    #         loop += 1
    #         print loop

