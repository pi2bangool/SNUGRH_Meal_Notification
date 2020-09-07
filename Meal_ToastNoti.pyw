from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import re
import time
from win10toast import ToastNotifier

toast = ToastNotifier()
title = ''
body = ''


def Price(s):
    return 2000+500*(ord(s)-97) if s != 'f' else 5000


def Prtm(l):
    global body
    if l == 'N/A':
        return
    if type(l[0]) is list:
        for i in l:
            body += '[{}원] '.format(i[0]) + i[1].replace(']', '').replace(')', '').replace('amp;', '').replace('(#', '') + '\n'
    else:
        body += '[{}원] '.format(l[0]) + l[1].replace(']', '').replace(')', '').replace('amp;', '').replace('(#', '') + '\n'


def ttn(h):
    if h <= 9:
        return 0
    elif h <= 13:
        return 1
    else:
        return 2

def nts(n):
    if n == 0:
        return '아침'
    elif n == 1:
        return '점심'
    else:
        return '저녁'


def Main(t):
    if t == '아침':
        Prtm(Sorted[day])
        Prtm(Sorted[7+day])
        Prtm(Sorted[56+day])
    else:
        IE = 0 if t == '점심' else 1
        Prtm(Sorted[14+day+21*IE])
        Prtm(Sorted[21+day+21*IE])
        Prtm(Sorted[63+day+7*IE])


def Rmain(dt):
    global title
    tt = ttn(dt.hour)
    title = "기숙사 식당 " + nts(tt) + " 메뉴 " + dt.strftime("(%Y.%m.%d.)")
    Main(nts(tt))

dt = datetime.datetime.now()
day = (dt.weekday()+1)%7
Hour = dt.hour

html = urlopen("https://dorm.snu.ac.kr/dk_board/facility/food.php")  

bsObject = BeautifulSoup(html, "html.parser") 

menu = bsObject.select('table.t_col > tbody > tr > td > ul')
Sorted = []
for i in menu:
    s = str(i)
    if len(s) > 10:
        mean = [Price(s[21]), s[30:-18]]
        if mean[1].count('<'):
            if s.count('00원'):
                p = s.find('원')
                try:
                    pri = int(s[p-4:p])
                except ValueError:
                    pri = 0
            else:
                pri = Price(s[21])
            pos = mean[1][mean[1].find('<')+29]
            srt = re.split('</span></li>\n<li class="menu_c"><span>|</span></li>\n<li class="menu_d"><span>|</span></li>\n<li class="menu_e"><span>|</span></li>\n<li class="menu_f"><span>', mean[1])
            if len(srt) > 1:
                mean = [[pri, srt[0]], [Price(pos), srt[1]]]
        Sorted.append(mean)
    else:
        Sorted.append('N/A')


Rmain(dt)
toast.show_toast(title, body, duration=7, icon_path="alarm_icon.ico")