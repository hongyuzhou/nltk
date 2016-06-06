# -*- coding:utf-8 -*-

import chunking
import re

of = open('result1','r')
toWrite = open('result2','a')

loop = 1

# for ff in of.readline():
#     seg = ff.strip().split('#')
#     try:
#         name = seg[0]
#         # place = seg[length-1].split(':')[1]
#         # time = seg[1].split(':')[1]
#         item = seg[1]
#         toWrite.write(r1 + '\n')
#     except Exception, e:
#         continue
#     finally:
#         pass


def fun(string1,stirng2):
    m1 = int(string1[0:1])
    d1 = int(string1[4:6])
    m2 = int(stirng2[0:1])
    d2 = int(stirng2[4:6])
    if m1 == m2:
        return str(d2-d1+1)
    else:
        return str(32-d1+d2)
        


for ff in of:
    m = re.search(r'\d{4}年.{6}奥运会的.{6}比赛', ff)
    if m != None:
        itemInfo = m.group().replace('的','')
        if re.search(r'(\d月\d{,2}日)(―|到|-)(\d{,2}日)',ff) != None:
            tt = re.search(r'(\d月\d{,2}日)(―|到|-)(\d{,2}日)',ff)
            startTime = tt.group(1)
            endTime = tt.group(3)
            dis = str(int(endTime[0:2]) - int(startTime[4:6])) + '天'
            schedule = startTime + '-' + endTime
            r1 = '<' + itemInfo + '\t' + schedule + '\t' + '项目赛程>'
            r2 = '<' + itemInfo + '\t' + dis + '\t' + '项目持续天数>'
            toWrite.write(r1 + '\n')
            toWrite.write(r2 + '\n')
            continue
        if re.search(r'\d月\d{,2}日',ff) != None:
            tt = re.findall(r'\d月\d{,2}日',ff)
            startTime = tt[0]
            endTime = tt[1]
            dis = fun(startTime,endTime) + '天'
            schedule = startTime + '-' + endTime
            r1 = '<' + itemInfo + '\t' + schedule + '\t' + '项目赛程>'
            r2 = '<' + itemInfo + '\t' + dis + '\t' + '项目持续天数>'
            toWrite.write(r1 + '\n')
            toWrite.write(r2 + '\n')
            continue