from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import re
import itertools
import threading
import time
import sys
import os

done = False

def animate():
    for c in itertools.cycle(['     (ㄴ˙∇˙)ㄱ', '.    (ㄱ˙∇˙)ㄴ', '..   (ㄴ˙∇˙)ㄱ', '...  (ㄱ˙∇˙)ㄴ']):
        if done:
            break
        # sys.stdout.write('\r Loading' + c)
        # sys.stdout.flush()
        print('\b'*23, 'Loading', c, end='')
        time.sleep(0.4)


def Price(s):
    return 2000+500*(ord(s)-97) if s != 'f' else 5000


def Prtc(n):
    print('  -%s\n' % n, end='')


def Prtm(l):
    if l == 'N/A':
        print('   ', l)
        return
    if str(type(l[0])) == "<class 'list'>":
        for i in l:
            print('    [{}원]'.format(i[0]), i[1].replace(']', '').replace(')', '').replace('amp;', ''))
    else:
        print('    [{}원]'.format(l[0]), l[1].replace(']', '').replace(')', '').replace('amp;', ''))


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
        print('  아워홈')
        Prtc('가마')
        Prtm(Sorted[day])
        Prtc('InterChef')
        Prtm(Sorted[7+day])
        print()
        print('  919동')
        Prtm(Sorted[56+day])
    else:
        IE = 0 if t == '점심' else 1
        print('  아워홈')
        Prtc('가마')
        Prtm(Sorted[14+day+21*IE])
        Prtc('InterChef')
        Prtm(Sorted[21+day+21*IE])
        print()
        print('  919동')
        Prtm(Sorted[63+day+7*IE])


t = threading.Thread(target=animate)
t.start()

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

done = True

print('\b'*22, 'Done!!                  ')

def Rmain(dt):
    tt = ttn(dt.hour)
    print('', '='*48)
    print(dt.strftime("      %Y년 %m월 %d일 기숙사 식당 "), end='')
    print(nts(tt), '메뉴')
    print('', '='*48)
    print()
    Main(nts(tt))
    print()
    print('', '='*48)

Rmain(dt)
a = input(' Press Enter to Exit / Type "N" to See Next Meal: ')

def PN(a, dt):
    h = dt.hour
    if a == 'N' or a == 'n':
        return 6*(2*(ttn(h)//2+ttn(h)+1))-h
    if a == 'P' or a == 'p':
        return -6*(ttn(h)%3)-h
    return 0


while PN(a, dt):
    os.system('cls')
    dt += datetime.timedelta(hours=PN(a, dt))
    Rmain(dt)
    a = input(' Press Enter to Exit / Type "N" to See Next Meal: ')