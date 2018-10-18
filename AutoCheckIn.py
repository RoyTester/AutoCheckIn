# coding:utf-8

import requests
import warnings

warnings.filterwarnings('ignore')
s = requests.Session()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
file = 'AutoCheckIn.txt'


def url_check(url, data):
    r = s.post(url, headers=header, data=data, verify=False)
    # 某些站点域名采用user.前缀
    if r.status_code != requests.codes.ok:
        url = url[:7] + 'user.' + url[7:]
        url_check(url, data)
    else:
        print(r.json()['msg'])


def checkin():
    try:
        with open(str(file), 'r') as f:
            content = f.readlines()
        data = {
            'email': content[1].strip('\n'),
            'passwd': content[2].strip('\n'),
        }
        url = 'http://{}/auth/login'.format(content[0].strip('\n'))
        url_check(url, data)
        checkin_url = '{}/user/checkin'.format(url.rstrip('/auth/login'))
        url_check(checkin_url, data='')
    except IOError as e:
        print('检查同名文本是否存在', e)


if __name__ == '__main__':
    try:
        checkin()
    except ConnectionError as e:
        print('确保站点可访问', e)
