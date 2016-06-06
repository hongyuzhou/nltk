# -*- coding:utf-8 -*-

import nltk
import NLPtools
import re

grammer = """
        BornDate: {<nr><wp>?<wkz>?<t>+}
        Hometown: {<nr><vshi><ns>+<n>}
        MajorItem: {<vn><n><nr>}
        PersonBestRe: {<>}
        ItemWorldRe: {<>}
        ItemRule: {<>}
        ItemTime: {<>}
        HostCity: {<>}
        HostGym: {<>}
        """

# player_info = []
# item_info = []
# place_info = []

def get_text_for_nltk(doc):
    se, pos = NLPtools.word_segment(doc)
    text = []
    for i in range(len(se)):
        if se[i] != u'　' and se[i] != u'\r' and se[i] != u'\n':
            text.append((se[i], pos[i]))
    return text

def fund_chunks(text, grammer):
    cp = nltk.RegexpParser(grammer)
    return cp.parse(text)


def build_relations_by_keyword(text):
    player_info = []
    item_info = []
    place_info = []
    # host_city_find(place_info, text)
    # word_recordKeeper_find(player_info, text)
    # major_item_find(player_info,text)
    item_schedule_find(item_info,text)
    return player_info, item_info, place_info


def major_item_find(ll, text):
    if re.search('运动员',text) != None:
        grammer = """
            MajorItem: {<vn><n><nr>}
        """
        pText = get_text_for_nltk(text)
        res = fund_chunks(pText, grammer)
        for subtree in res.subtrees():
            if subtree.label() == 'MajorItem':
                if subtree[1][0] == u'运动员':
                    name = subtree[2][0]
                    item = subtree[0][0]
                    r = u'<' + name + u'\t' + item + u'\t' + u'参赛项目' + u'>'
                    ll.append(r)


def personal_best_record_find(ll, subtree):
    if subtree[len(subtree)-2][0] == u'世界' and subtree[len(subtree)-1][0] == u'纪录':
        name = subtree[0][0]
        item = u''
        for t in range(2,len(subtree)-2):
            item += subtree[t][0]
        r = u'<' + name + u'\t' + item + u'\t' + u'破世界纪录' + u'>'
        ll.append(r)


# extract for item
def word_recordKeeper_find(ll,text):
    if re.search('世界纪录保持者',text) != None:
        grammer = """
            recordKeeper: 
            {<n>*<m><q><n>*<n><n><n><nr>} 
            }<w.*>{   
            {<nr.*><vshi><.*>+<n><n><n>} 
             
        """
        pText = get_text_for_nltk(text)
        res = fund_chunks(pText, grammer)
        for subtree in res.subtrees():
            if subtree.label() == 'recordKeeper':
                string = u''
                for tt in range(1,len(subtree)):
                    string += subtree[tt][0]
                # print subtree[0][0]
                if u'世界纪录保持者' in string:
                    if subtree[len(subtree)-3][0] == u'世界' and subtree[len(subtree)-2][0] == u'纪录' and subtree[len(subtree)-1][0] == u'保持者':
                        if re.search(u'世界纪录保持者',string).span()[0]>10:
                            continue
                        name = subtree[0][0]
                        item = ''
                        for t in range(2,len(subtree)-3):
                            if subtree[t][1] != u'ude1':
                                item += subtree[t][0]
                        r = u'<' + name + u'\t' + item + u'\t' + u'现在或曾经的世界纪录保持者' + u'>'
                        ll.append(r)
                    else:
                        name = subtree[len(subtree)-1][0]
                        item = ''
                        for ii in range(len(subtree)):
                            if subtree[ii][0] != u'世界':
                                item += subtree[ii][0]
                            else:
                                break
                        r = u'<' + name + u'\t' + item + u'\t' + u'现在或曾经的世界纪录保持者' + u'>'
                        ll.append(r)



def item_world_record_find():
    return


def item_rule_find():
    return


def item_time_find():
    return


# extract for place
def host_city_find(ll, text):
    if re.search('举办地',text) != None:
        grammer = """
            hostPalce: {<ns.*><p.*|vshi|v>*<m><q><nz>*<n><.*>*<n>}
        """
        pText = get_text_for_nltk(text)
        res = fund_chunks(pText, grammer)
        for subtree in res.subtrees():
            if subtree.label() == 'hostPalce':
                string = u''
                num = ''
                for tt in range(2,len(subtree)-1):
                    string += subtree[tt][0]
                if u'奥运会' in string or u'奥林匹克运动会' in string:
                    place = subtree[0][0]
                    for tt in range(len(subtree)):
                        if subtree[tt][1] == u'm':
                            num = subtree[tt][0]
                            break
                    r = u'<' + place + u'\t' + num + u'届' + u'\t' + u'举办地' + u'>'
                    ll.append(r)


def host_gymnasium_find():
    return

def OlymInfo_find(ll, text):
    if re.search('吉祥物',text) != None:
        grammer = """
            Lucky: {<ns|nsf><n><ude1><n><.*>*<wd><vshi><m><.*>*<nr|nrf>+<.*>*<ude1><n><wd|wj>}
        """ 
        pText = get_text_for_nltk(text)
        res = fund_chunks(pText, grammer)
        for subtree in res.subtrees():
            if subtree.label() == 'Lucky':
                if subtree[1][0] == u'奥运会' and subtree[3][0] == u'吉祥物':
                    olym = subtree[0][0] + u'奥运会'
                    name = []
                    luckyName = ''
                    nameNum = 0
                    for ii in range(len(subtree))[::-1]:
                        if subtree[ii][1] == u'nr' or subtree[ii][1] == u'nrf':
                            name.append(subtree[ii][0])
                        if subtree[ii][1] == u'm' and subtree[ii-1][1] == u'vshi':
                            if subtree[ii][0] == u'一':
                                nameNum = 1
                            elif subtree[ii][0] == u'二' or subtree[ii][0] == u'两':
                                nameNum = 2
                            elif subtree[ii][0] == u'三' or subtree[ii][0] == u'':
                                nameNum = 3
                            elif subtree[ii][0] == u'四':
                                nameNum = 4
                            elif subtree[ii][0] == u'五':
                                nameNum = 5
                            else:
                                nameNum = int(subtree[ii][0])
                            break
                    for jj in range(nameNum):
                        if jj != nameNum-1:
                            luckyName += name[jj] + ', '
                        else:
                            luckyName += name[jj]
                    r = u'<' + olym + u'\t' + luckyName + u'\t' + u'吉祥物' + u'>'
                    ll.append(r)


def item_schedule_find(ll, text):
    
    def fun(string1,stirng2):
        m1 = int(string1[0:1])
        d1 = int(string1[4:6])
        m2 = int(stirng2[0:1])
        d2 = int(stirng2[4:6])
        if m1 == m2:
            return str(d2-d1+1)
        else:
            return str(32-d1+d2)

    m = re.search(r'\d{4}年.{6}奥运会的.{6}比赛', text)
    if m != None:
        itemInfo = m.group().replace('的','')
        if re.search(r'(\d月\d{,2}日)(―|到|-)(\d{,2}日)',text) != None:
            tt = re.search(r'(\d月\d{,2}日)(―|到|-)(\d{,2}日)',text)
            startTime = tt.group(1)
            endTime = tt.group(3)
            dis = str(int(endTime[0:2]) - int(startTime[4:6])) + '天'
            schedule = startTime + '-' + endTime
            r1 = '<' + itemInfo + '\t' + schedule + '\t' + '项目赛程>'
            r2 = '<' + itemInfo + '\t' + dis + '\t' + '项目持续天数>'
            ll.append(r1)
            ll.append(r2)
            return
        if re.search(r'\d月\d{,2}日',text) != None:
            tt = re.findall(r'\d月\d{,2}日',text)
            startTime = tt[0]
            endTime = tt[1]
            dis = fun(startTime,endTime) + '天'
            schedule = startTime + '-' + endTime
            r1 = '<' + itemInfo + '\t' + schedule + '\t' + '项目赛程>'
            r2 = '<' + itemInfo + '\t' + dis + '\t' + '项目持续天数>'
            ll.append(r1)
            ll.append(r2)
            return


if __name__ == '__main__':
    # s1 = s.replace('\n','').replace('　','')
    #s2 = "28届奥运会在北京举办Beijing"
    s2 = "赛程与场馆：2004年雅典奥运会的足球比赛将在雅典、沃洛斯、塞萨洛尼基、伊拉克利翁和帕特雷五个城市举行，比赛将提前开始，8月11日就拉开序幕，到8月29日结束，决赛将在雅典举行。男子足球比赛将有16支参赛队伍，分预赛、四分之一决赛、半决赛和决赛四轮；女子比赛将有10支球队参赛，分四分之一决赛、半决赛和决赛三轮。"
    se, pos = NLPtools.word_segment(s2)
    text = []
    for i in range(len(se)):
        if se[i] != u'　' and se[i] != u'\r' and se[i] != u'\n':
            text.append((se[i], pos[i]))
    #     print se[i], pos[i]
    # print len(se),len(text)
    # print text
    # for n in text:
    #     print n[0],n[1]
    gg = """
            Lucky: {<ns|nsf><n><ude1><n><.*>*<wd><vshi><m><.*>*<nr|nrf>+<.*>*<ude1><n><wd|wj>}       
        """
    res = fund_chunks(text, gg)
    for le in res.leaves():
        print le[0],le[1]

    res.pprint()
    ll = []
    OlymInfo_find(ll, s2)
    print ll[0]
    # player_info, item_info, place_info = build_relations_by_chunking(text)
    # for i in player_info:
    #     print i


