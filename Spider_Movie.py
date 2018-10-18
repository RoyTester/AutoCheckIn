#!/user/bin/env python
# -*- coding:utf-8 -*-
# author:ZRui
# datetime:2018/7/28 22:52
# software:PyCharm
import requests
import datetime

url = 'http://group.leying.com/cinema/play-info'
QueryString = {
    '.sig': 'd028afe46ebe3c8c201783d432682360',
    'cinema_id': '49',
    'city_id': '485',
    'client_id': 'c7fb1d30d16b6',
    'group': '20045',
    'pver': '6.0',
    'session_id': '5b5c9945a52a19318e05fc983ca31cbbe6305e48adbec',
    'source': '105001',
    'ver': '5.3.0',
    'width': '270',
}

re = requests.get(url, params=QueryString)
r = re.json()
data = r['data']['movie_data']
l_data = []
for i in range(len(data)):
    name = data[i]['movie_name']
    str = '{}.{}'.format(i+1, name)
    l_data.append(len(str.encode('gbk')) + 2)
length = max(l_data)
print("{:{s}^{l}}".format('☆', s='=', l=length*5-1))
print('{:^{l}}'.format(r['data']['cinema_data']['name'], l=length*5-9))
print('{:^{l}}'.format('正在上映', l=length*5-4))
print("{:{s}^{l}}".format('☆', s='=', l=length*5-1), '\n')
for i in range(len(data)):
    name = data[i]['movie_name']
    str = '{}.{}'.format(i+1, name)
    l = length - len(str.encode('gbk'))
    if (i+1) % 5 == 0:
        print('{}{}'.format(str, '\n'))
    else:
        # 两种输出对齐字符格式的方法
        print(str, end=' '*l)
        # len()中文与数字字母一样宽度为1，但print()中文占2字节/字母数字占1字节，因此用encode('gbk')方法算出适合宽度即
        # length = 实际需要的字节宽度 - gbk编码宽度 + len()字符宽度
        # print('{:<{l}}'.format(str, l=l+len(str)), end='')
print('\n')
def get_price(num):
    try:
        shows = data[int(num)]['shows']
        for j in shows:
            times = shows[j]
            # 字符串格式化为时间
            time_ = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
            d1 = time_(r['data']['today'])
            d2 = time_(j)
            delta = (d2 - d1).days
            if delta == 0:
                print('今天')
            elif delta == 1:
                print('明天')
            elif delta == 2:
                print('后天')
            else:
                print('日期：{}'.format(j))
            for k in range(len(times)):
                p = times[k]
                end_time = p['end_time']
                start_time = p['start_time']
                lg = p['language']
                media = p['media']
                price = p['nonmember_price']
                m_price = p['member_price']
                print('{}至{} {}{}：{}（会员价{}）'.format(start_time, end_time, lg, media, price, m_price))
    except:
        print('序号不存在！')
while True:
    num = input('查看票价请输入电影序号：')
    get_price(num)