# -*- coding: utf-8 -*-
import sys
import io
import requests
import hashlib
import re

from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def md5(str):
    return hashlib.md5(str.encode('gb2312')).hexdigest()

class Jw:
    def __init__(self, jw_url, sc_code):
        #教务网地址
        self.__jw_url = jw_url
        #学校代码
        self.__sc_code = sc_code
        #登陆页面
        self.__login_url = self.__jw_url + '/_data/home_login.aspx'

    def getCheckCode(self):
        self.__session = requests.session()
        self.__session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'
        self.__session.headers['Referer'] = self.__jw_url
        self.__session.get(self.__login_url)
        self.__session.headers['Referer'] = self.__login_url
        response = self.__session.get(self.__login_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.__VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'}).attrs['value']
        yzm_response = self.__session.get(self.__jw_url + '/sys/ValidateCode.aspx')
        return yzm_response.content

    def login(self, stuid, passwd, code):
        data = {
            '__VIEWSTATE': self.__VIEWSTATE,
            'pcInfo': 'Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64;+rv:52.0)+Gecko/20100101+Firefox/52.0Windows+NT+6.1;+Win64;+x645.0+(Windows)+SN:NULL',
            'typeName': u'学生'.encode('gb2312'),
            'dsdsdsdsdxcxdfgfg': md5(stuid + md5(passwd)[0:30].upper() + self.__sc_code)[0:30].upper(),
            'fgfggfdgtyuuyyuuckjg': md5(md5(code.upper())[0:30].upper() + self.__sc_code)[0:30].upper(),
            'Sel_Type': 'STU',
            'txt_asmcdefsddsd': stuid,
            'txt_pewerwedsdfsdff': '',
            'txt_sdertfgsadscxcadsads': ''
        }
        login_response = self.__session.post(self.__login_url, data)
        login_html = login_response.text
        if 'MAINFRM.aspx' in login_html:
            return True
        return False

    def getScores(self, xnxq):
        scores = []
        self.__session.headers['Referer'] = self.__jw_url + '/xscj/c_ydcjrdjl.aspx'
        data = {
            'sel_xnxq': xnxq,
            'radCx': '1',
            'btn_search': u'检索'.encode('gb2312')
        }
        scores_response = self.__session.post(self.__jw_url + '/xscj/c_ydcjrdjl_rpt.aspx', data)
        soup = BeautifulSoup(scores_response.text, 'html.parser')
        tr = soup.find_all('tr')
        for i in range(2, len(tr)):
            score = []
            for td in tr[i].find_all('td'):
                score.append(td.get_text().strip())
            scores.append(score)
        return scores
    '''
    #有缺陷
    def getCoures(self):
        courses = []
        self.__session.headers['Referer'] = self.__jw_url + '/wsxk/stu_zxjg.aspx'
        courses_response = self.__session.get(self.__jw_url + '/wsxk/stu_zxjg_rpt.aspx')
        soup = BeautifulSoup(courses_response.text, 'html.parser')
        tr = soup.find_all('tr', attrs={'style' : 'background-color:#f4fffb;'})
        for i in range(8, len(tr)):
            course = []
            for td in tr[i].find_all('td'):
                course.append(td.get_text().strip())
            courses.append(course)
        return courses
    '''

jw = Jw('http://jw.zhku.edu.cn', '11347')
with open('CheckCode.jpg', 'wb') as fd:
    fd.write(jw.getCheckCode())
yzm = input('CheckCode: ')
#jw.login("账号", "密码",yzm)
for score in jw.getScores(xnxq="20161"):
    print(score)