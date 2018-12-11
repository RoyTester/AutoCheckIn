# coding:utf-8
import re
import requests
import warnings

warnings.filterwarnings('ignore')


class CheckIn:
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/63.0.3239.132 Safari/537.36'
    }

    def __init__(self, email, password, url):
        self.postDict = {
            'email': email,
            'passwd': password
        }
        self.login_url = '{}/auth/login'.format(url)
        self.checkin_url = '{}/user/checkin'.format(url)
        self.user_url = '{}/user'.format(url)

    def login(self):
        r = self.session.post(self.login_url, headers=self.headers, data=self.postDict, verify=False)
        data = r.json()
        return data['msg']

    def checkin(self):
        """签到
        :param self:
        :return:
        """
        r = self.session.post(self.checkin_url, headers=self.headers, verify=False)
        data = r.json()
        return data['msg']

    def info(self):
        """显示剩余流量
        :return:
        """
        r = self.session.get(self.user_url, headers=self.headers, verify=False)
        tmp = re.findall(r'legendText:"(.*)",', r.text)
        return tmp

    def crack(self):
        print(self.login(), self.checkin(), self.info())


if __name__ == '__main__':
    try:
        c = CheckIn(email='email', password='password', url='url')
        c.crack()
    except ConnectionError as e:
        print('确保站点可访问', e)
