#-*- coding: utf-8 -*-
import requests
import re
import hashlib
import math
import random

def md5(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()

def randomString(l):
    ss = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    maxPos = len(ss)
    pwd = ''
    for i in range(0, l):
        pwd = pwd + ss[(math.floor(random.random() * maxPos))]
    return pwd

class Jw:
    def __init__(self, jw_url):
        self.__jw_url = jw_url
        self.__session = requests.Session()
        self.__headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Referer' : self.__jw_url + '/_data/home_login.aspx'
        }
        response = self.__session.get(self.__jw_url + '/_data/home_login.aspx', headers=self.__headers)
        html = response.content.decode('GB2312')
        re_viewstate = re.compile(r'<input type="hidden" name="__VIEWSTATE" value="(.*?)"')
        m = re_viewstate.search(html)
        if m:
            self.__VIEWSTATE = m.group(1)

    def getCheckCode(self):
        response = self.__session.get(self.__jw_url + '/sys/ValidateCode.aspx', headers=self.__headers)
        return response.content

    def login(self, id, password, checkcode):
        data = {
            '__VIEWSTATE' : self.__VIEWSTATE,
            'pcInfo' : 'Mozilla/5.0+(Windows+NT+6.1;+Win64;+x64;+rv:52.0)+Gecko/20100101+Firefox/52.0Windows+NT+6.1;+Win64;+x645.0+(Windows)+SN:NULL',
            'typeName' : '学生'.encode('GB2312'),
            'dsdsdsdsdxcxdfgfg' : md5(id + md5(password)[0:30].upper() + '11347')[0:30].upper(),
            'fgfggfdgtyuuyyuuckjg' : md5(md5(checkcode.upper())[0:30].upper() + '11347')[0:30].upper(),
            'Sel_Type': 'STU',
            'txt_asmcdefsddsd' : id,
            'txt_pewerwedsdfsdff' : '',
            'txt_sdertfgsadscxcadsads' : ''
        }
        response = self.__session.post(self.__jw_url + '/_data/home_login.aspx', data, headers=self.__headers)
        return response.status_code

    def getScoreTable(self, **data):
        result = {}
        self.__headers['Referer'] = self.__jw_url + '/xscj/Stu_MyScore.aspx'
        response = self.__session.post(self.__jw_url + '/xscj/Stu_MyScore_rpt.aspx', data, headers=self.__headers)
        html = response.content.decode('GB2312')
        re_gpa = re.compile(r'平均学分绩点：(.*?)<')
        m = re_gpa.search(html)
        if m:
            result['gpa'] = m.group(1)
        re_img_url = re.compile(r"<img width='\d+' src='(.*?)'")
        img_url = re_img_url.findall(html)
        if img_url:
            img = []
            for url in img_url:
                response = self.__session.get(self.__jw_url + '/xscj/' + url, headers=self.__headers)
                img.append(response.content)
            result['img'] = img
        return result

    def getCourseTable(self, **data):
        result = {}
        self.__headers['Referer'] = self.__jw_url + '/znpk/Pri_StuSel.aspx'
        response = self.__session.get(self.__jw_url + '/znpk/Pri_StuSel.aspx', headers=self.__headers)
        html = response.content.decode('GB2312')
        re_hidyzm = re.compile(r'<input type="hidden" name="hidyzm" value="(.*?)"')
        m = re_hidyzm.search(html)
        if m:
            hidyzm = m.group(1)
        rs = randomString(15)
        data['px'] = '0'
        data['txt_yzm'] = ''
        data['hidyzm'] = hidyzm
        data['hidsjyzm'] = md5('11347' + data['Sel_XNXQ'] + rs).upper()
        response = self.__session.post(self.__jw_url + '/znpk/Pri_StuSel_rpt.aspx?m=' + rs, data, headers=self.__headers)
        html = response.content.decode('GB2312')
        re_kcsj = re.compile(r"<td align='left' width='1060px'>(.*?)<")
        kcsj = re_kcsj.findall(html)
        if kcsj:
            result['kcsj'] = kcsj
        re_img_url = re.compile(r"<img width='\d+' height='\d+' src='(.*?)'")
        img_url = re_img_url.findall(html)
        if img_url:
            self.__headers['Referer'] = self.__jw_url + '/znpk/Pri_StuSel_rpt.aspx?m=' + rs
            img = []
            for url in img_url:
                response = self.__session.get(self.__jw_url + '/znpk/' + url, headers=self.__headers)
                img.append(response.content)
            result['img'] = img
        return result


jw = Jw('http://jw.zhku.edu.cn')
with open('CheckCode.jpg', 'wb') as fd:
    fd.write(jw.getCheckCode())
yzm = input('CheckCode: ')
#jw.login('账号', '密码', yzm)
'''
img = jw.getScoreTable(SJ='1', SelXNXQ='0')
k = 1
for i in img:
    with open('ScoreTable' + str(k) + '.jpg', 'wb') as fd:
        fd.write(i)
    k = k + 1
'''
c = jw.getCourseTable(Sel_XNXQ='20161',rad='0')
img = c['img']
kcsj = c['kcsj']
print(kcsj)
k = 1
for i in img:
    with open('CourseTable' + str(k) + '.jpg', 'wb') as fd:
        fd.write(i)
    k += 1














