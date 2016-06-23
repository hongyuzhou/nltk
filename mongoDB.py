# -*- coding:utf-8 -*-
import pymongo
import NLPtools
import chunking
import re

conn = pymongo.Connection('114.55.139.104', 27017)
db = conn.olympic

source_collection = db.source
html_collection = db.html

rs = open('result2', 'a')
# wr = open('item','w')


def htmlPrecess(doc):
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


loop = 1

for doc in html_collection.find():
    try:
        if doc['page'] != None:
            preText = htmlPrecess(doc['page'])
            setences  = preText.split('\n')
            for setence in setences:
                # text = chunking.get_text_for_nltk(setence)
                player_res, item_res, place_res = chunking.build_relations_by_keyword(setence)
                # for relation in player_res:
                #     # print relation, loop
                #     rs.write(relation.encode('utf-8') + '\n')
                #     rs.flush()
                #     print relation, loop
                for relation in item_res:
                    # print relation, loop
                    # rs.write(relation.encode('utf-8') + '\n')
                    rs.write(relation + '\n')
                    rs.flush()
                    print relation, loop
                # for relation in place_res:
                #     # print relation, loop
                #     rs.write(relation.encode('utf-8') + '\n')
                #     rs.flush()
                #     print relation, loop

    except UnicodeDecodeError:
        # print 'UnicodeDecodeError' + 'link ' + str(loop)
        continue

    except TypeError:
        # print 'TypeError:' + 'link ' + str(loop)
        # print doc['page']
        continue
    except:
        continue
    finally:
        loop += 1
        print loop

    # if loop <= 5000:
    #     if doc['page'] != None:
    #         preText = htmlPrecess(doc['page'])
    #         # print preText
    #         setences  = preText.split('\n')
    #         for setence in setences:
    #             if re.search(r'\d{4}年.{6}奥运会的.{6}比赛', setence) != None:
    #                 wr.write(setence + '\n')
    #                 wr.flush()
    # loop += 1
    # print loop

