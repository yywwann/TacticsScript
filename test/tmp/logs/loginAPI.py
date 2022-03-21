# -*- coding:UTF-8 -*-

import requests
import time

# from jsonpath import jsonpath

'''
1: ok, 可以使用
-4: code过期
-3: code在线数量上限
-2: code不存在
-1: 网络连接失败
'''


class noBBLogin(object):
    def __init__(self, url, cdkey_code, cdkeylog_temp_link_code):
        self.url = url
        self.cdkey_code = cdkey_code
        self.cdkey_id = 0
        self.cdkeylog_temp_link_code = cdkeylog_temp_link_code
        self.cdkeylog_id = 0
        self.update_flag = 1
        self.log_params = {
            "cdkey_id": self.cdkey_id,
            "login_time": self.get_current_time(),
            "logout_time": self.get_current_time(),
            "temp_link_code": self.cdkeylog_temp_link_code,
            "status": 0,
        }

    def login(self):
        print("#-----start login--------#")
        self.update_flag = 0
        status_code, cdkey = self.get_cdkeys(cdkey_code=self.cdkey_code)
        # 确认网络连接
        if status_code == -1 or status_code != 200:
            return -1

        # 检查验证码是否存在
        if cdkey is []:
            return -2

        cdkey = cdkey[0]
        self.cdkey_id = cdkey['id']
        # print(cdkey)
        # 检查是否达到同时在线人数上限
        if cdkey['available_nums'] == cdkey['online_nums']:
            return -3

        # 检查验证码是否过期
        status_code = self.check_time(cdkey['expire_time'])
        if status_code == -1 or status_code == -4:
            return status_code

        # put
        params = cdkey
        params['online_nums'] = params['online_nums'] + 1
        status_code, cdkey = self.put_cdkeys(params)
        if status_code == -1 or status_code != 200:
            return -1

        # post logs
        self.log_params['cdkey_id'] = self.cdkey_id
        status_code, cdkey = self.post_cdkeylogs(self.log_params)
        if status_code == -1 or status_code != 201:
            return -1
        # print(status_code)
        self.cdkeylog_id = cdkey['id']
        self.log_params['id'] = self.cdkeylog_id

        return 1

    def heart_beat(self):
        print("#-----start heart_beat--------#")
        # status_code, cdkeylog = self.get_cdkeylogs(cdkeylog_id=self.cdkeylog_id)
        # if status_code == -1 or status_code != 200:
        #     return -1

        self.log_params["logout_time"] = self.get_current_time()
        status_code, cdkey = self.put_cdkeylogs(self.log_params)
        if status_code == -1 or status_code != 200:
            return -1

        return 1

    def logout(self):
        print("#-----start logout--------#")
        self.update_flag = 1
        status_code, cdkey = self.get_cdkeys(cdkey_id=self.cdkey_id)
        if status_code == -1 or status_code != 200:
            return -1

        params = cdkey
        params['online_nums'] = max(0, params['online_nums'] - 1)
        status_code, cdkey = self.put_cdkeys(params)
        if status_code == -1 or status_code != 200:
            return -1

        # status_code, cdkeylog = self.get_cdkeylogs(cdkeylog_id=self.cdkeylog_id)
        # if status_code == -1 or status_code != 200:
        #     return -1

        # params = cdkeylog
        self.log_params["logout_time"] = self.get_current_time()
        self.log_params["status"] = 1
        status_code, cdkey = self.put_cdkeylogs(self.log_params)
        if status_code == -1 or status_code != 200:
            return -1

        return 1

    def get_cdkeys(self, cdkey_code=None, cdkey_id=None):
        params = {}
        headers = {}
        if cdkey_code is not None:
            url = self.url + 'cdkeys/?format=json&code=' + cdkey_code
            try:
                res = requests.request('get', url, json=params, headers=headers)
                # print('> get_cdkeys by code: ', res.json())
                return res.status_code, res.json()
            except:
                return -1, []
        elif cdkey_id is not None:
            url = self.url + 'cdkeys/' + str(cdkey_id) + '/?format=json'
            try:
                res = requests.request('get', url, json=params, headers=headers)
                # print('> get_cdkeys by id: ', res.json())
                return res.status_code, res.json()
            except:
                return -1, []
        else:
            url = self.url + 'cdkeys/?format=json'
            try:
                res = requests.request('get', url, json=params, headers=headers)
                # print('> get_cdkeys by id: ', res.json())
                return res.status_code, res.json()
            except:
                return -1, []

    def put_cdkeys(self, params=None):
        headers = {}
        url = self.url + 'cdkeys/' + str(params['id']) + '/'
        try:
            res = requests.request('put', url, json=params, headers=headers)
            # print('> put_cdkeys: ', res.json())
            return res.status_code, res.json()
        except:
            return -1, []

    def post_cdkeylogs(self, params):
        headers = {}
        url = self.url + 'cdkeylogs/'
        try:
            res = requests.request('post', url, json=params, headers=headers)
            # print('> post_cdkeylogs: ', res.json())
            return res.status_code, res.json()
        except:
            return -1, []

    def get_cdkeylogs(self, cdkeylog_id=None, param=None):
        if param is None:
            param = ""
        params = {}
        headers = {}
        if cdkeylog_id is not None:
            url = self.url + 'cdkeylogs/' + str(cdkeylog_id) + '/?format=json'
            try:
                res = requests.request('get', url, json=params, headers=headers)
                # print('> get_cdkeylogs: ', res.json())
                return res.status_code, res.json()
            except:
                return -1, []
        else:
            url = self.url + 'cdkeylogs/' + param + '&format=json'
            try:
                res = requests.request('get', url, json=params, headers=headers)
                # print('> get_cdkeylogs: ', res.json())
                return res.status_code, res.json()
            except:
                return -1, []

    def put_cdkeylogs(self, params=None):
        headers = {}
        url = self.url + 'cdkeylogs/' + str(params['id']) + '/'
        try:
            res = requests.request('put', url, json=params, headers=headers)
            # print('> put_cdkeylogs: ', res.json())
            return res.status_code, res.json()
        except:
            return -1, []

    def get_beijin_time(self):
        """
        联网获取北京时间
        :return: 北京时间时间戳
        """
        try:
            # 设置头信息，没有访问会错误400！！！
            hea = {"User-Agent": "Mozilla/5.0"}
            # 设置访问地址，我们分析到的；
            url = r"http://time1909.beijing-time.org/time.asp"
            # 用requests get这个地址，带头信息的；
            r = requests.get(url=url, headers=hea)
            # 检查返回的通讯代码，200是正确返回；
            if r.status_code == 200:
                # 定义result变量存放返回的信息源码；
                result = r.text
                # self.go_text("> 当前时间为" + str(result))
                # 通过;分割文本；
                data = result.split(";")
                # self.go_text("> 当前时间为" + str(data))
                # ======================================================
                # 以下是数据文本处理：切割、取长度，最最基础的东西就不描述了；
                year = data[1][len("nyear") + 3: len(data[1])]
                month = data[2][len("nmonth") + 3: len(data[2])]
                day = data[3][len("nday") + 3: len(data[3])]
                # wday = data[4][len("nwday")+1 : len(data[4])-1]
                hrs = data[5][len("nhrs") + 3: len(data[5])]
                minute = data[6][len("nmin") + 3: len(data[6])]
                sec = data[7][len("nsec") + 3: len(data[7])]
                # ======================================================
                # 这个也简单把切割好的变量拼到beijinTimeStr变量里；
                beijin_time_str = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
                # 把时间打印出来看看；
                # print(beijin_time_str)
                # self.go_text("> 当前时间为" + str(beijin_time_str))
                # 将beijinTimeStr转为时间戳格式；
                beijin_time = time.mktime(time.strptime(beijin_time_str, "%Y/%m/%d %X"))
                # 返回时间戳；
                return beijin_time
        except:
            return -1

    @staticmethod
    def RCF3339_to_mktime(RCF3339_time):
        year = RCF3339_time[0:4]
        month = RCF3339_time[5:7]
        day = RCF3339_time[8:10]
        hrs = RCF3339_time[11:13]
        minute = RCF3339_time[14:16]
        sec = RCF3339_time[17:19]
        mktime_time = "%s/%s/%s %s:%s:%s" % (year, month, day, hrs, minute, sec)
        mktime_time = time.mktime(time.strptime(mktime_time, "%Y/%m/%d %X"))
        return mktime_time

    def check_time(self, expire_time):
        beijin_time = self.get_beijin_time()
        if beijin_time == -1:
            return -1
        # print("北京时间:", beijin_time)
        # print("过期时间", expire_time)
        expire_time = self.RCF3339_to_mktime(expire_time)
        # print("过期时间", expire_time)
        if beijin_time > expire_time:
            return -4
        return 1

    @staticmethod
    def get_current_time():
        strtime = time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.localtime())
        return strtime


    # vipTime = '2020-11-30 10:00:00'
        # 检查脚本是否过期
    # isVIP = self.check_vip(vipTime)
    # if isVIP == -1:
    #     self.stop()
    #     return
    #
    # def check_vip(self, TIME):
    #     """
    #     检查脚本是否过期
    #     :param TIME: string类型 格式 'YYYY-MM-DD hh:mm:ss'
    #     :return: -1表示过期， 1表示没过期
    #     """
    #     beijinTime = self.get_beijin_time()
    #     if beijinTime == -1:
    #         # print("请连接网络")
    #         self.go_text("$ 请连接网络")
    #         return -1
    #     # print(beijinTime)
    #     vip = TIME
    #     timeArray = time.strptime(vip, "%Y-%m-%d %H:%M:%S")
    #
    #     timeStamp = int(time.mktime(timeArray))
    #     # print(timeStamp)
    #     if (beijinTime > timeStamp):
    #         # print("该脚本已过期，请联系QQ1489514329获取新脚本")
    #         # time.sleep(10)
    #         # exit()
    #         self.go_text("$ 该脚本已过期，请加QQ群237967793获取最新脚本")
    #         self.go_text("$ 或者从百度网盘链接:https://pan.baidu.com/s/1JeIKOCtov_RShm8eZpBirA  提取码:78oc 下载最新版本")
    #         return -1
    #     self.go_text("> 该脚本还在有效期内，马上开始脚本")
    #     return 1

if __name__ == "__main__":

    # cdkey_code = input()
    login_check = noBBLogin('cccccccccchy_1', "xxx")
    # login_check.post_cdkeylogs(6, 'ttt')
    # print(login_check.login())
    # time.sleep(10)
    # print(login_check.logout())
    # login_check = noBBLogin('cccccccccchy_4')
    print(login_check.get_current_time())
    print(time.time())
    print(login_check.RCF3339_to_mktime(login_check.get_current_time()))

