# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time
import pyautogui as auto
import random
import requests
from system_hotkey import SystemHotkey
import os
import ctypes
# import qdarkstyle
import style
import source
# import base64
import loginAPI


os.environ["QT_API"] = "pyqt5"

noBB_version = "不多BB" + source.VERSION


class TS(QThread):
    strsin = pyqtSignal(str)
    isEnable = pyqtSignal()

    def __init__(self, group, ffturn, hero1, hero2, hero3, hero4, hero5, hero6, hero7, hero8, temp_link_code, rest):
        super(TS, self).__init__()
        self.DEBUG = source.DEBUG
        self.vip_time = source.vip_time
        self.debug_time = 0
        self.BASE_PATH = source.BASE_PATH
        self.ASSET_PATH = source.ASSET_PATH
        self.restart_list = source.restart_list
        self.hero_map = source.hero_map

        self.pic_inGame = source.pic_inGame
        self.all_pic_dead = source.all_pic_dead
        self.pic_one_star = source.pic_one_star
        self.pic_two_star = source.pic_two_star

        self.pic_wuqi = source.pic_wuqi
        self.btn_wuqi = source.btn_wuqi

        self.btn_start = source.btn_start
        self.btn_accept = source.btn_accept
        self.btn_ok = source.btn_ok
        self.btn_x = source.btn_x
        self.btn_ff_1 = source.btn_ff_1
        self.btn_ff_2 = source.btn_ff_2
        self.btn_ff_3 = source.btn_ff_3

        self.weapons = source.weapons
        self.chesses = source.chesses

        self.flag = 1  # 判断脚本是否允许
        self.first = 1
        self.TIMES = 0  # 判断当前是第几回合
        self.restart_times = 0
        self.INGAME = 0  # 判断当前是否在游戏中
        self.all_time = 0  # 上次心跳的时间
        self.f_time = 0  # 上次F的时间
        self.d_time = 0  # 上次D的时间
        self.z_time = 0  # 上次上装备的时间
        self.g_time = 0  # 判断当前游戏进行了多场时间了
        self.buy_time = 0  # 上次买牌的时间
        self.buy_flag_yes = 0
        self.buy_flag_no = 0
        self.walk_time = 0  # 上次买牌的时间
        self.switch_time = 0
        self.wuqi_time = 0
        self._2_1 = 0  # 判断当前是否是2-1回合
        self.chess_idx = 0

        self.rest = rest

        self.group = group  # 判断是否固定阵容
        self.group_mode = 1
        if self.group == source.group_combox_list[0]:
            self.group_mode = 1
        if self.group == source.group_combox_list[1]:
            self.group_mode = 2
        if self.group == source.group_combox_list[2]:
            self.group_mode = 3
        if self.group == source.group_combox_list[3]:
            self.group_mode = 4
        if self.group == source.group_combox_list[4]:
            self.group_mode = 5
        if self.group == source.group_combox_list[5]:
            self.group = -2

        self.buy_bero_list_1 = []
        for i in range(8):
            file_path = self.ASSET_PATH + "group0/item" + str(i) + ".png"
            self.buy_bero_list_1.append(file_path)
        self.buy_bero_list_2 = []
        for i in range(8):
            file_path = self.ASSET_PATH + "group1/item" + str(i) + ".png"
            self.buy_bero_list_2.append(file_path)
        self.buy_bero_list_3 = []
        for i in range(8):
            file_path = self.ASSET_PATH + "group2/item" + str(i) + ".png"
            self.buy_bero_list_3.append(file_path)
        self.buy_bero_list_4 = []
        for i in range(8):
            file_path = self.ASSET_PATH + "group3/item" + str(i) + ".png"
            self.buy_bero_list_4.append(file_path)
        self.buy_bero_list_5 = []
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero1])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero2])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero3])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero4])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero5])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero6])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero7])
        self.buy_bero_list_5.append(self.ASSET_PATH + self.hero_map[hero8])

        self.buy_hero_list = {
            1: self.buy_bero_list_1,
            2: self.buy_bero_list_2,
            3: self.buy_bero_list_3,
            4: self.buy_bero_list_4,
            5: self.buy_bero_list_5,
        }

        self.ffturn = ffturn  # 判断投降回合
        self.FF_mode = 0  # 0 永不投降 1 前n投降 2 时间投降
        self.FF_1 = 0
        self.FF_2 = 0
        if self.ffturn == "永不投降":
            self.FF_mode = 0
        if self.ffturn == "前二投降":
            self.FF_mode = 1
            self.FF_1 = 2
        if self.ffturn == "前四投降":
            self.FF_mode = 1
            self.FF_1 = 4
        if self.ffturn == "前六投降":
            self.FF_mode = 1
            self.FF_1 = 6
        if self.ffturn == "10分钟投降":
            self.FF_mode = 2
            self.FF_2 = 10
        if self.ffturn == "11分钟投降":
            self.FF_mode = 2
            self.FF_2 = 11
        if self.ffturn == "12分钟投降":
            self.FF_mode = 2
            self.FF_2 = 12
        if self.ffturn == "13分钟投降":
            self.FF_mode = 2
            self.FF_2 = 13
        if self.ffturn == "14分钟投降":
            self.FF_mode = 2
            self.FF_2 = 14
        if self.ffturn == "15分钟投降":
            self.FF_mode = 2
            self.FF_2 = 15

    def go_text(self, x):
        """
        将文本输出到对话框中
        :param x:
        :return:
        """
        if x is not None:
            self.strsin.emit('{} {}'.format(str(time.strftime("[%H:%M:%S]", time.localtime())), x))
            time.sleep(0.1)
            QtWidgets.QApplication.processEvents()

    def click_2(self, x, y, button, shake=True):
        """
        模拟鼠标操作 双击
        :param shake: 判断鼠标位置是否抖动
        :param x: 鼠标X坐标
        :param y: 鼠标Y坐标
        :param button: 鼠标点击键 ’left‘ or ’right‘
        :return:
        """
        if shake is True:
            x = x + random.randint(-10, 10)
            y = y + random.randint(-10, 10)

        auto.mouseDown(x=x, y=y, button=button)
        auto.mouseUp(x=x, y=y, button=button, duration=1)
        self.sleep(1)
        auto.mouseDown(x=x, y=y, button=button)
        auto.mouseUp(x=x, y=y, button=button, duration=1)
        self.sleep(1)


    def click_1(self, x, y, button):
        """
        模拟鼠标操作 单机
        :param x: 鼠标X坐标
        :param y: 鼠标Y坐标
        :param button: 鼠标点击键 ’left‘ or ’right‘
        :return:
        """
        x = x + random.randint(-10, 10)
        y = y + random.randint(-10, 10)

        auto.mouseDown(x=x, y=y, button=button)
        # time.sleep(1)
        auto.mouseUp(x=x, y=y, button=button, duration=1)
        # time.sleep(1)

    @staticmethod
    def check_pic(needleImage, region=None):
        """
        在当前屏幕region区域是否存在needleImage
        :param needleImage: 要求识别的图片
        :param region: （x1, y1, x2, y2）左上角的坐标和右下角的坐标
        :return: 点击的中心坐标
        """

        if region is None:
            region = (0, 0, 1920, 1080)
        haystackImage = auto.screenshot(
            region=(region[0], region[1], region[2] - region[0], region[3] - region[1]))
        # haystackImage.save(self.BASE_PATH+"sys/test"+needleImage[7]+".png")
        pic = auto.locate(needleImage, haystackImage, confidence=0.8)
        if pic is not None:
            pic = auto.center(pic)
            return [pic[0] + region[0], pic[1] + region[1]]

        return None

    @staticmethod
    def check_all_pic(needleImage, region=None, space=(0, 0)):
        """
        在当前屏幕region区域是否存在needleImage
        :param needleImage: 要求识别的图片
        :param region: （x1, y1, x2, y2）左上角的坐标和右下角的坐标
        :return: list 包含所有的pic的位置
        """

        if region is None:
            region = (0, 0, 1920, 1080)
        pics = list(auto.locateAllOnScreen(needleImage,
                                           region=(region[0], region[1], region[2] - region[0], region[3] - region[1]),
                                           confidence=0.8))
        pic_list = []
        for pic in pics:
            pic = auto.center(pic)
            if not pic_list:
                pic_list.append((pic[0], pic[1]))
            elif pic[0] - pic_list[-1][0] >= space[0] and pic[1] - pic_list[-1][1] >= space[1]:
                pic_list.append((pic[0], pic[1]))

            # if pic_list and pic[0] - pic_list[-1][0] >= space[0] and pic[1] - pic_list[-1][1] >= space[1]:
            #     pic_list.append((pic[0], pic[1]))
            # else:
            #     pic_list.append((pic[0], pic[1]))
        return pic_list

    def Exit(self):
        if self.flag == 0:
            return

    def sleep(self, x):
        for i in range(x):
            time.sleep(1)
            if self.flag == 0:
                return

    # 开局三连
    def room(self):
        if self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is None:
            if self.INGAME == 1:
                # 从一局游戏中退出来
                self.INGAME = 0
                # 如果需要休息
                if self.rest:
                    sleep_time_min = random.randint(4, 7)
                    sleep_time_sec = random.randint(0, 59)
                    self.go_text("> {}分{}秒后准备开始一局新的游戏".format(str(sleep_time_min), str(sleep_time_sec)))
                    self.sleep(sleep_time_min*60+sleep_time_sec)
                    if self.flag == 0:
                        return

            self.click_2(self.btn_start[0], self.btn_start[1], "left")
            self.click_2(self.btn_accept[0], self.btn_accept[1], "left")
            self.click_2(self.btn_ok[0], self.btn_ok[1], "left")
            self.sleep(5)
            return

        return

    # 点击投降
    def ff_stage(self):
        """
        noFF = 1， 前四投降
        noFF = 0， 根据ffturn进行投降
        :return:
        """
        try:
            if self.INGAME == 0:
                return

            ff_times = 0
            if self.FF_mode == 1:
                pic = self.check_all_pic(self.all_pic_dead[0], region=self.all_pic_dead[1], space=self.all_pic_dead[2])
                if len(pic) > 8 - self.FF_1 - 1:
                    while self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is not None and ff_times < 5:
                        ff_times += 1
                        self.click_2(self.btn_ff_1[0], self.btn_ff_1[1], "left", shake=False)
                        self.click_2(self.btn_ff_2[0], self.btn_ff_2[1], "left")
                        self.click_2(self.btn_ff_3[0], self.btn_ff_3[1], "left")
                        self.go_text("> 准备认输")
                        self.sleep(10)
                        if self.flag == 0:
                            return

            if self.FF_mode == 2 and time.time() - self.g_time > self.FF_2 * 60:
                while self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is not None and ff_times < 5:
                    ff_times += 1
                    self.click_2(self.btn_ff_1[0], self.btn_ff_1[1], "left", shake=False)
                    self.click_2(self.btn_ff_2[0], self.btn_ff_2[1], "left")
                    self.click_2(self.btn_ff_3[0], self.btn_ff_3[1], "left")
                    self.go_text("> 准备认输")
                    self.sleep(10)
                    if self.flag == 0:
                        return

            if ff_times == 5:
                self.restart(fource=True)
        except:
            print('{} {}'.format(str(time.strftime("[%H:%M:%S]", time.localtime())), 'ff stage'))

    @staticmethod
    def sale(x, y):
        auto.moveTo(x, y, duration=0.25)
        auto.dragTo(970, 910, duration=0.5)
        auto.moveTo(random.randint(700, 1300), random.randint(200, 700), duration=0.25)

    def sale_1_2(self):
        region = (590, 190, 1324, 337)
        x = random.randint(region[0], region[2])
        y = random.randint(region[1], region[3])
        self.click_2(x, y, "right")
        self.sale(460, 740)
        self.sale(560, 740)

    def maintain(self, step=1):
        x = [460, 560, 670, 790, 900, 1000, 1110, 1220, 1330]
        y = 740

        if step > 2:
            step = 2

        for i in range(2, len(x), step):
            x0 = x[0] + random.randint(-10, 10)
            xi = x[i] + random.randint(-10, 10)
            yy = y + random.randint(-10, 10)
            auto.moveTo(x0, yy, duration=0.25)
            auto.dragTo(xi, yy, duration=(0.4+i*0.1))

            if self.flag == 0:
                return

        if step > 1:
            for i in range(3, len(x), step):
                x0 = x[1] + random.randint(-10, 10)
                xi = x[i] + random.randint(-10, 10)
                yy = y + random.randint(-10, 10)
                auto.moveTo(x0, yy, duration=0.25)
                auto.dragTo(xi, yy, duration=(0.4+i*0.1*step))

                if self.flag == 0:
                    return

        self.sale_1_2()

    def game_walk(self, region=None):
        if region is None:
            region = (0, 0, 1920, 1080)

        x = random.randint(region[0], region[2])
        y = random.randint(region[1], region[3])
        self.click_2(x, y, "right")
        self.click_2(x, y, "left")
        self.sleep(2)
        self.sale_1_2()

    def game_buy_hero(self):
        try:
            num = 0
            pics_list = []

            for hero in self.buy_hero_list[self.group_mode]:
                pics = self.check_all_pic(hero, region=(450, 800, 1500, 1080), space=(100, 0))
                pics_list.extend(pics)

                if self.flag == 0:
                    return

            self.sale_1_2()
            for pic in pics_list[:5]:
                x = pic[0]
                y = pic[1]
                self.click_2(x, y, "left")
                num += 1

                if self.flag == 0:
                    return
            current_time = time.time()
            if num > 0:
                self.maintain(num)
                self.buy_flag_yes = current_time
            elif num == 0:
                self.buy_flag_no = current_time

            return num
        except:
            print('{} {}'.format(str(time.strftime("[%H:%M:%S]", time.localtime())), 'buy hero'))

    def in_game_init(self):
        if self.INGAME == 0:
            self.g_time = time.time()
            self.d_time = self.g_time
            self.f_time = self.g_time
            self.z_time = self.g_time
            self.buy_time = self.g_time
            self.buy_flag_no = self.g_time
            self.buy_flag_yes = self.g_time
            self.walk_time = self.g_time
            self.switch_time = self.g_time
            self.wuqi_time = self.g_time
            if self.group == -2:
                self.group_mode = random.randint(1, 4)
            self._2_1 = 0
            self.chess_idx = 0
            self.INGAME = 1
            self.TIMES = self.TIMES + 1
            self.go_text('> 第{}局开始'.format(str(self.TIMES)))

    def in_game_walk(self):
        current_time = time.time()
        if current_time - self.walk_time > 10:
            self.game_walk(region=(700, 200, 1300, 700))
            self.click_2(830, 560, "left", shake=False)  # 退出游戏按钮
            self.walk_time = current_time

    def in_game_2_1(self):
        current_time = time.time()
        if self._2_1 == 0 and current_time - self.g_time > 150:
            if self.DEBUG:
                tempImage = auto.screenshot()
                tempImage.save('{}{}{}.png'.format(self.BASE_PATH + 'test/', '2-1',
                                                   str(time.strftime("[%Y-%m-%d %H-%M-%S]", time.localtime()))))
            self._2_1 = 1
            self.sale(960, 620)
            # self.game_walk(region=(700, 200, 1300, 700))

    def in_game_buy(self):
        current_time = time.time()
        num = 0
        if current_time - self.buy_time > 20:
            num = self.game_buy_hero()
            self.buy_time = current_time
        return num

    def in_game_D(self):
        current_time = time.time()
        temp = 70
        run_time = current_time - self.g_time
        if run_time > 8 * 60:
            temp = 60
        if run_time > 13 * 60:
            temp = 50
        if run_time > 18 * 60:
            temp = 30

        if current_time - self.d_time > temp and current_time - self.g_time > 3 * 60:
            if self.DEBUG:
                self.go_text('> D, {}, {}, {}'.format(temp, current_time - self.d_time, current_time - self.g_time))
            self.click_1(400, 1000, "left")
            self.d_time = current_time

            num = self.game_buy_hero()
            self.buy_time = current_time

    def in_game_F(self):
        current_time = time.time()
        temp = 70
        run_time = current_time - self.g_time
        if run_time > 5 * 60:
            temp = 60
        if run_time > 10 * 60:
            temp = 50
        if run_time > 25 * 60:
            temp = 100000000

        if current_time - self.f_time > temp and current_time - self.g_time > 3 * 60:
            if self.DEBUG:
                self.go_text('> F, {}, {}, {}'.format(temp, current_time - self.f_time, current_time - self.g_time))
            self.click_1(400, 930, "left")
            self.f_time = current_time

    # 放装备
    def in_game_Z(self):
        current_time = time.time()
        if current_time - self.z_time < 90 or current_time - self.g_time < 4 * 60:
            return

        chesss = self.chesses[self.chess_idx]
        self.chess_idx = (self.chess_idx + 1) % 6

        for weapon in self.weapons[:5]:
            auto.moveTo(weapon[0], weapon[1], duration=0.25)
            auto.dragTo(chesss[0], chesss[1], duration=0.5)
            if self.flag == 0:
                return
        # self.game_walk(region=(700, 200, 1300, 700))

        self.z_time = current_time

        if self.DEBUG:
            self.go_text('> 放装备{}'.format(self.chess_idx))

    # 场下2星换场上1星
    def in_game_switch(self):
        current_time = time.time()
        if current_time - self.g_time < 5 * 60 or current_time - self.switch_time < 60:
            return

        down_x = [460, 560, 670, 790, 900, 1000, 1110, 1220, 1330]
        down_y = 740

        pic_two = self.check_pic(self.pic_two_star[0], region=self.pic_two_star[1])
        pic_one = self.check_pic(self.pic_one_star[0], region=self.pic_one_star[1])
        if pic_two is None or pic_one is None:
            return

        two_star_x, two_star_y = pic_two
        one_star_x, one_star_y = pic_one

        for i in down_x:
            if two_star_x < i:
                two_star_x = i
                two_star_y = down_y
                break

        one_star_x += 30
        one_star_y += 50

        auto.moveTo(two_star_x, two_star_y, duration=0.25)
        auto.dragTo(one_star_x, one_star_y, duration=0.5)

        self.switch_time = current_time

        if self.DEBUG:
            self.go_text('> switch')
            # print('一星位置 x={}, y={}'.format(one_star_x, one_star_y))
            # print('二星位置 x={}, y={}'.format(two_star_x, two_star_y))

    # s5 光明武器库 启用
    def in_game_wuqi(self):
        current_time = time.time()
        if current_time - self.wuqi_time < 60:
            return

        if self.check_pic(self.pic_wuqi[0], region=self.pic_wuqi[1]) is not None:
            self.click_2(self.btn_wuqi[0], self.btn_wuqi[1], "left")
            self.sale_1_2()

        self.wuqi_time = current_time

    def in_game_stage(self):
        """
        模拟抓牌买牌等操作
        :return:
        """
        if self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is None:
            return None

        self.in_game_init()
        self.in_game_walk()
        self.in_game_2_1()
        num = self.in_game_buy()
        self.in_game_F()
        self.in_game_Z()
        self.in_game_switch()
        self.in_game_D()
        # self.in_game_wuqi()

    def restart(self, fource=False):
        try:
            flag_x = False
            current_time = time.time()
            if fource:
                flag_x = True
            elif current_time - min(self.buy_flag_yes, self.buy_flag_no) > 10 * 60 and self.INGAME == 1:
                self.go_text('> 准备重启{}'.format(int(current_time - min(self.buy_flag_yes, self.buy_flag_no))))
                self.restart_times += 1
                flag_x = True

            if flag_x:
                self.click_2(self.btn_x[0], self.btn_x[1], 'left', shake=False)
                self.sleep(10)
                while self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is not None:
                    self.click_2(self.btn_x[0], self.btn_x[1], 'left', shake=False)
                    self.sleep(10)

            if self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is None:
                FLAG = True
                while FLAG:
                    FLAG = False
                    for i in self.restart_list:
                        pic_path = i[0]
                        click_pos = i[1]
                        region = i[2]
                        # print("> restart: ", pic_path)
                        if self.check_pic(pic_path, region) is not None:
                            if pic_path == "C:/Program Files/noBB/asset/sys/reStart4.png":
                                click_pos = self.check_pic(pic_path, region)
                            self.click_2(click_pos[0], click_pos[1], 'left', shake=False)
                            FLAG = True
                            self.sleep(10)

                        if self.flag == 0:
                            return
        except:
            print('{} {}'.format(str(time.strftime("[%H:%M:%S]", time.localtime())), 'restart'))

    # def heart_beat(self):
    #     try:
    #         current_time = time.time()
    #         run_time = current_time - self.all_time
    #         if run_time > 3 * 60 * 60:
    #             res = self.login_check.heart_beat()
    #             if res == -1:
    #                 self.go_text("$ 请检查网络连接")
    #                 self.stop()
    #                 return
    #
    #             self.all_time = current_time
    #     except:
    #         print('{} {}'.format(str(time.strftime("[%H:%M:%S]", time.localtime())), 'heart beat'))

    def debug_func(self):
        if not self.DEBUG:
            return
        current_time = time.time()
        if current_time - self.debug_time > 30:
            tempImage = auto.screenshot()
            tempImage.save('{}{}{}.png'.format(self.BASE_PATH + 'test/', 'debug_func',
                                               str(time.strftime("[%Y-%m-%d %H-%M-%S]", time.localtime()))))
            self.debug_time = current_time

    def game(self):
        try:

            if self.check_pic(self.pic_inGame[0], region=self.pic_inGame[1]) is None:
                self.go_text("> 准备开始一局新的游戏")
            self.g_time = time.time()
            self.all_time = time.time()
            self.debug_time = time.time()

            while True:

                if self.flag == 1:
                    self.restart()
                if self.flag == 0:
                    return

                if self.flag == 1:
                    self.room()
                if self.flag == 0:
                    return

                if self.flag == 1:
                    self.in_game_stage()
                if self.flag == 0:
                    return

                if self.flag == 1:
                    self.ff_stage()
                if self.flag == 0:
                    return

                if self.flag == 1:
                    self.debug_func()
                if self.flag == 0:
                    return

        except Exception as e:
            print(e)

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

    def check_vip(self, TIME):
        """
        检查脚本是否过期
        :param TIME: string类型 格式 'YYYY-MM-DD hh:mm:ss'
        :return: -1表示过期， 1表示没过期
        """
        beijinTime = self.get_beijin_time()
        if beijinTime == -1:
            self.go_text("$ 请连接网络")
            return -1
        vip = TIME
        timeArray = time.strptime(vip, "%Y-%m-%d %H:%M:%S")

        timeStamp = int(time.mktime(timeArray))
        if (beijinTime > timeStamp):
            self.go_text("$ 该脚本已过期，请加QQ群905167917获取最新脚本")
            self.go_text("$ 或者从百度网盘链接:https://pan.baidu.com/s/1JeIKOCtov_RShm8eZpBirA  提取码:78oc 下载最新版本")
            return -1
        self.go_text("> 该版本可使用至{}，马上开始脚本".format(TIME))
        return 1

    def check_device_caps(self):
        # 检查电脑分辨率是否正确
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(0)
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        hdpi = gdi32.GetDeviceCaps(dc, 88)

        if width != 1920 or height != 1080 or hdpi != 96:
            return False

        return True

    def run(self):
        if not self.check_device_caps():
            self.go_text("$ 请检查电脑分辨率为1920*1080, 缩放为100% ！！！")
            self.stop()
            return

        self.go_text("> 电脑分辨率检查 OK")

        ###############################################################################################################

        vipTime = '2022-10-15 10:00:00'
        # 检查脚本是否过期

        isVIP = self.check_vip(vipTime)
        if isVIP == -1:
            self.stop()
            return

        self.go_text("> 脚本开始启动")
        self.game()
        self.stop()
        # self.test()

    def stop(self):
        self.flag = 0
        self.strsin.emit("$ 脚本停止！！")
        self.strsin.emit("$ 可以点击开始挂机重新开始！")
        self.strsin.emit("$ ------------------------")
        self.strsin.emit("$ 共完成{}局游戏，重启{}次".format(self.TIMES - self.restart_times, self.restart_times))
        self.isEnable.emit()


class Ui_MainWindow(QObject):
    sin = pyqtSignal()  # 结束挂机信号
    sig_keyhot = pyqtSignal(str)  # 热键信号

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        # 初始化设置
        self.config = QtCore.QSettings(source.CONFIG_FILE, QtCore.QSettings.IniFormat)
        self.GROUP = self.config.value("SETUP/GROUP_VALUE")
        self.FFTURN = self.config.value("SETUP/FFTURN_VALUE")
        self.HERO1 = self.config.value("SETUP/HERO1_VALUE")
        self.HERO2 = self.config.value("SETUP/HERO2_VALUE")
        self.HERO3 = self.config.value("SETUP/HERO3_VALUE")
        self.HERO4 = self.config.value("SETUP/HERO4_VALUE")
        self.HERO5 = self.config.value("SETUP/HERO5_VALUE")
        self.HERO6 = self.config.value("SETUP/HERO6_VALUE")
        self.HERO7 = self.config.value("SETUP/HERO7_VALUE")
        self.HERO8 = self.config.value("SETUP/HERO8_VALUE")
        self.TEMPLINKCODE = self.config.value("SETUP/TEMPLINKCODE_VALUE")
        self.REST = self.config.value("SETUP/REST_VALUE")

        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(276, 641)
        MainWindow.resize(310, 360)
        MainWindow.move(10, 10)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/source/tuBiao.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(0.85)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.central_VerticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_VerticalLayout.setObjectName("central_VerticalLayout")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # -tab 主界面

        self.Main_Tab = QtWidgets.QWidget()
        self.Main_Tab.setObjectName("Main_Tab")

        ## -box

        self.Main_Box = QtWidgets.QGroupBox(self.Main_Tab)
        self.Main_Box.setObjectName("Main_Box")

        ### -V

        self.Main_VerticalLayout = QtWidgets.QVBoxLayout(self.Main_Box)
        self.Main_VerticalLayout.setObjectName("Main_VerticalLayout")

        #### -H 开始按钮
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.qt_btn_start = QtWidgets.QPushButton(self.Main_Box)
        self.qt_btn_start.setObjectName("qt_btn_start")
        self.horizontalLayout_2.addWidget(self.qt_btn_start)

        #### -H 关闭按钮
        self.qt_btn_stop = QtWidgets.QPushButton(self.Main_Box)
        self.qt_btn_stop.setObjectName("qt_btn_stop")
        self.horizontalLayout_2.addWidget(self.qt_btn_stop)
        self.Main_VerticalLayout.addLayout(self.horizontalLayout_2)

        ### -V 运行日志输出

        self.qt_text_print = QtWidgets.QTextBrowser(self.Main_Box)
        self.qt_text_print.setObjectName("qt_text_print")
        self.Main_VerticalLayout.addWidget(self.qt_text_print)

        # self.central_VerticalLayout.addWidget(self.Main_Box)

        self.tabWidget.addTab(self.Main_Tab, "")

        # -tab 设置界面

        self.Setting_Tab = QtWidgets.QWidget()
        self.Setting_Tab.setObjectName("setting_Tab")

        # -box V

        self.Setting_Tab_VerticalLayout = QtWidgets.QVBoxLayout(self.Setting_Tab)
        self.Setting_Tab_VerticalLayout.setObjectName("Setting_Tab_VerticalLayout")

        ##  -box Setting_Box

        self.Setting_Box = QtWidgets.QGroupBox(self.Setting_Tab)
        self.Setting_Box.setObjectName("Setting_Box")

        ### -V

        self.Setting_VerticalLayout = QtWidgets.QVBoxLayout(self.Setting_Box)
        self.Setting_VerticalLayout.setObjectName("Setting_VerticalLayout")

        #### -H
        self.Groupsetting_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.Groupsetting_HorizontalLayout.setObjectName("Groupsetting_HorizontalLayout")

        ##### combox 阵容选择
        self.Group_combox = QtWidgets.QComboBox(self.Setting_Box)
        self.Group_combox.setObjectName("Group_combox")
        for i in range(6):
            self.Group_combox.addItem("")
        self.Group_combox.setCurrentIndex(int(self.GROUP))
        self.Groupsetting_HorizontalLayout.addWidget(self.Group_combox)

        ##### label
        self.Group_label = QtWidgets.QLabel(self.Setting_Box)
        self.Group_label.setObjectName("Group_label")
        self.Groupsetting_HorizontalLayout.addWidget(self.Group_label)

        self.Setting_VerticalLayout.addLayout(self.Groupsetting_HorizontalLayout)

        #### -H

        self.FFsetting_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.FFsetting_HorizontalLayout.setObjectName("FFsetting_HorizontalLayout")

        ##### combox 投降模式
        self.FFturn_combox = QtWidgets.QComboBox(self.Setting_Box)
        self.FFturn_combox.setObjectName("FFturn_combox")
        for i in range(10):
            self.FFturn_combox.addItem("")
        self.FFturn_combox.setCurrentIndex(int(self.FFTURN))
        self.FFsetting_HorizontalLayout.addWidget(self.FFturn_combox)

        ##### label
        self.label_2 = QtWidgets.QLabel(self.Setting_Box)
        self.label_2.setObjectName("label_2")
        self.FFsetting_HorizontalLayout.addWidget(self.label_2)

        self.Setting_VerticalLayout.addLayout(self.FFsetting_HorizontalLayout)

        ####  -H
        self.rest_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.rest_HorizontalLayout.setObjectName("rest_HorizontalLayout")

        ##### checkbox 每局休息4-8分钟
        self.rest_check_box = QtWidgets.QCheckBox("每局结束后休息4-8分钟")
        self.rest_check_box.setObjectName("rest_check_box")
        if self.REST == "false":
            self.rest_check_box.setChecked(False)
        else:
            self.rest_check_box.setChecked(True)
        self.rest_HorizontalLayout.addWidget(self.rest_check_box)
        self.Setting_VerticalLayout.addLayout(self.rest_HorizontalLayout)

        # -----------------------

        self.Customize_Box = QtWidgets.QGroupBox(self.Setting_Tab)
        self.Customize_Box.setObjectName("Customize_Box")

        self.Customize_Box_VerticalLayout = QtWidgets.QVBoxLayout(self.Customize_Box)
        self.Customize_Box_VerticalLayout.setObjectName("Customize_Box_VerticalLayout")

        # ----------------------------------------------------------------------------------

        self.hero12_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.hero12_HorizontalLayout.setObjectName("hero1_HorizontalLayout")

        self.hero1_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero1_combox.setObjectName("hero1_combox")
        for i in source.hero_chi_name:
            self.hero1_combox.addItem(i)
        self.hero1_combox.setCurrentIndex(int(self.HERO1))
        self.hero1_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero1_label.setObjectName("hero1_label")

        self.hero2_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero2_combox.setObjectName("hero2_combox")
        for i in source.hero_chi_name:
            self.hero2_combox.addItem(i)
        self.hero2_combox.setCurrentIndex(int(self.HERO2))
        self.hero2_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero2_label.setObjectName("hero2_label")

        self.hero12_HorizontalLayout.addWidget(self.hero1_combox)
        self.hero12_HorizontalLayout.addWidget(self.hero1_label)
        self.hero12_HorizontalLayout.addWidget(self.hero2_combox)
        self.hero12_HorizontalLayout.addWidget(self.hero2_label)

        self.Customize_Box_VerticalLayout.addLayout(self.hero12_HorizontalLayout)

        # ----------------------------------------------------------------------------------

        self.hero34_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.hero34_HorizontalLayout.setObjectName("hero34_HorizontalLayout")

        self.hero3_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero3_combox.setObjectName("hero3_combox")
        for i in source.hero_chi_name:
            self.hero3_combox.addItem(i)
        self.hero3_combox.setCurrentIndex(int(self.HERO3))
        self.hero3_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero3_label.setObjectName("hero3_label")

        self.hero4_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero4_combox.setObjectName("hero4_combox")
        for i in source.hero_chi_name:
            self.hero4_combox.addItem(i)
        self.hero4_combox.setCurrentIndex(int(self.HERO4))
        self.hero4_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero4_label.setObjectName("hero4_label")

        self.hero34_HorizontalLayout.addWidget(self.hero3_combox)
        self.hero34_HorizontalLayout.addWidget(self.hero3_label)
        self.hero34_HorizontalLayout.addWidget(self.hero4_combox)
        self.hero34_HorizontalLayout.addWidget(self.hero4_label)

        self.Customize_Box_VerticalLayout.addLayout(self.hero34_HorizontalLayout)

        # ----------------------------------------------------------------------------------

        self.hero56_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.hero56_HorizontalLayout.setObjectName("hero56_HorizontalLayout")

        self.hero5_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero5_combox.setObjectName("hero5_combox")
        for i in source.hero_chi_name:
            self.hero5_combox.addItem(i)
        self.hero5_combox.setCurrentIndex(int(self.HERO5))
        self.hero5_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero5_label.setObjectName("hero5_label")

        self.hero6_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero6_combox.setObjectName("hero6_combox")
        for i in source.hero_chi_name:
            self.hero6_combox.addItem(i)
        self.hero6_combox.setCurrentIndex(int(self.HERO6))
        self.hero6_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero6_label.setObjectName("hero6_label")

        self.hero56_HorizontalLayout.addWidget(self.hero5_combox)
        self.hero56_HorizontalLayout.addWidget(self.hero5_label)
        self.hero56_HorizontalLayout.addWidget(self.hero6_combox)
        self.hero56_HorizontalLayout.addWidget(self.hero6_label)

        self.Customize_Box_VerticalLayout.addLayout(self.hero56_HorizontalLayout)

        # ----------------------------------------------------------------------------------

        self.hero78_HorizontalLayout = QtWidgets.QHBoxLayout()
        self.hero78_HorizontalLayout.setObjectName("hero78_HorizontalLayout")

        self.hero7_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero7_combox.setObjectName("hero7_combox")
        for i in source.hero_chi_name:
            self.hero7_combox.addItem(i)
        self.hero7_combox.setCurrentIndex(int(self.HERO7))
        self.hero7_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero7_label.setObjectName("hero7_label")

        self.hero8_combox = QtWidgets.QComboBox(self.Customize_Box)
        self.hero8_combox.setObjectName("hero8_combox")
        for i in source.hero_chi_name:
            self.hero8_combox.addItem(i)
        self.hero8_combox.setCurrentIndex(int(self.HERO8))
        self.hero8_label = QtWidgets.QLabel(self.Customize_Box)
        self.hero8_label.setObjectName("hero8_label")

        self.hero78_HorizontalLayout.addWidget(self.hero7_combox)
        self.hero78_HorizontalLayout.addWidget(self.hero7_label)
        self.hero78_HorizontalLayout.addWidget(self.hero8_combox)
        self.hero78_HorizontalLayout.addWidget(self.hero8_label)

        self.Customize_Box_VerticalLayout.addLayout(self.hero78_HorizontalLayout)

        # ----------------------------------------------------------------------------------
        self.Setting_Tab_VerticalLayout.addWidget(self.Setting_Box)
        self.Setting_Tab_VerticalLayout.addWidget(self.Customize_Box)
        self.tabWidget.addTab(self.Setting_Tab, "")

        ###########################################################################################################

        self.Intro_Tab = QtWidgets.QWidget()
        self.Intro_Tab.setObjectName("Intro_Tab")

        self.Intro_Box = QtWidgets.QGroupBox(self.Intro_Tab)
        self.Intro_Box.setObjectName("Intro_Box")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Intro_Box)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label = QtWidgets.QLabel(self.Intro_Box)
        self.label.setMinimumSize(QtCore.QSize(256, 256))
        self.label.setAcceptDrops(False)
        self.label.setStyleSheet("image: url(:/pic/source/publicQRcode.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.verticalLayout_2.addWidget(self.label)
        self.tabWidget.addTab(self.Intro_Tab, "")

        ###########################################################################################################

        self.Sponsor_Tab = QtWidgets.QWidget()
        self.Sponsor_Tab.setObjectName("Sponsor_Tab")

        self.Sponsor_Box = QtWidgets.QGroupBox(self.Sponsor_Tab)
        self.Sponsor_Box.setObjectName("Sponsor_Box")

        self.SponsorVerticalLayout = QtWidgets.QVBoxLayout(self.Sponsor_Box)
        self.SponsorVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.SponsorVerticalLayout.setSpacing(0)
        self.SponsorVerticalLayout.setObjectName("SponsorVerticalLayout")

        self.SponsorLabel = QtWidgets.QLabel(self.Sponsor_Box)
        self.SponsorLabel.setMinimumSize(QtCore.QSize(256, 256))
        self.SponsorLabel.setAcceptDrops(False)
        self.SponsorLabel.setStyleSheet("image: url(:/pic/source/sponsorship.jpg);")
        self.SponsorLabel.setText("")
        self.SponsorLabel.setObjectName("SponsorLabel")

        self.SponsorVerticalLayout.addWidget(self.SponsorLabel)
        self.tabWidget.addTab(self.Sponsor_Tab, "")

        ###########################################################################################################

        self.central_VerticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 设置样式
        # MainWindow.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))
        # with open(os.path.join('qdark.qss'), 'r') as f:
        #     qss = f.read()
        # MainWindow.setStyleSheet(qss)
        MainWindow.setStyleSheet(style.qss)

        self.qt_btn_stop.clicked.connect(
            lambda: self.startOrStop(self.qt_btn_stop.objectName(),
                                     self.Group_combox.currentText(), self.FFturn_combox.currentText(),
                                     self.hero1_combox.currentText(), self.hero2_combox.currentText(),
                                     self.hero3_combox.currentText(), self.hero4_combox.currentText(),
                                     self.hero5_combox.currentText(), self.hero6_combox.currentText(),
                                     self.hero7_combox.currentText(), self.hero8_combox.currentText(),
                                     self.TEMPLINKCODE, self.rest_check_box.isChecked()
                                     )
        )
        self.qt_btn_start.clicked.connect(
            lambda: self.startOrStop(self.qt_btn_start.objectName(),
                                     self.Group_combox.currentText(), self.FFturn_combox.currentText(),
                                     self.hero1_combox.currentText(), self.hero2_combox.currentText(),
                                     self.hero3_combox.currentText(), self.hero4_combox.currentText(),
                                     self.hero5_combox.currentText(), self.hero6_combox.currentText(),
                                     self.hero7_combox.currentText(), self.hero8_combox.currentText(),
                                     self.TEMPLINKCODE, self.rest_check_box.isChecked()
                                     )
        )

        self.sig_keyhot.connect(self.MKey_pressEvent)
        # 3. 初始化两个热键
        self.hk_start, self.hk_stop = SystemHotkey(), SystemHotkey()
        # 4. 绑定快捷键和对应的信号发送函数
        # self.hk_start.register(("control", "9"), callback=lambda x: self.send_key_event("start"))
        self.hk_stop.register(("control", "0"), callback=lambda x: self.send_key_event("stop"))

        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def MKey_pressEvent(self, i_str):
        # print("按下的按键是%s" % (i_str,))
        # self.sin.emit()
        self.qt_btn_stop.click()

    # 热键信号发送函数(将外部信号，转化成qt信号)
    def send_key_event(self, i_str):
        self.sig_keyhot.emit(i_str)

    def save_config(self):
        self.config.setValue("SETUP/GROUP_VALUE", self.Group_combox.currentIndex())
        self.config.setValue("SETUP/FFTURN_VALUE", self.FFturn_combox.currentIndex())
        self.config.setValue("SETUP/HERO1_VALUE", self.hero1_combox.currentIndex())
        self.config.setValue("SETUP/HERO2_VALUE", self.hero2_combox.currentIndex())
        self.config.setValue("SETUP/HERO3_VALUE", self.hero3_combox.currentIndex())
        self.config.setValue("SETUP/HERO4_VALUE", self.hero4_combox.currentIndex())
        self.config.setValue("SETUP/HERO5_VALUE", self.hero5_combox.currentIndex())
        self.config.setValue("SETUP/HERO6_VALUE", self.hero6_combox.currentIndex())
        self.config.setValue("SETUP/HERO7_VALUE", self.hero7_combox.currentIndex())
        self.config.setValue("SETUP/HERO8_VALUE", self.hero8_combox.currentIndex())
        self.config.setValue("SETUP/REST_VALUE", self.rest_check_box.isChecked())

    def startOrStop(self, text, group, ffturn, hero1, hero2, hero3, hero4, hero5, hero6, hero7, hero8, temp_link_code, rest):
        try:
            print(text)

            if text == "qt_btn_start":
                self.save_config()
                self.qt_text_print.clear()
                self.ts1 = TS(group, ffturn, hero1, hero2, hero3, hero4, hero5, hero6, hero7, hero8, temp_link_code, rest)
                self.ts1.strsin.connect(self.updateText)
                # self.sin.connect(self.ts1.stop)
                self.ts1.isEnable.connect(self.reStart)
                self.ts1.flag = 1
                self.qt_btn_start.setEnabled(False)
                self.ts1.start()
            elif text == "qt_btn_stop":
                if self.ts1.flag == 0:
                    self.updateText("$ 脚本已经停止。")
                else:
                    self.updateText("$ 脚本正在停止......")
                self.ts1.flag = 0
                self.ts1.exit()
                # self.sin.emit()
        except Exception as e:
            print(e)

    def updateText(self, text):
        self.qt_text_print.append(text)

    def reStart(self):
        self.qt_btn_start.setEnabled(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", noBB_version))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Main_Tab), _translate("MainWindow", "主页面"))
        self.Main_Box.setTitle(_translate("MainWindow", "使用前请看说明书1000000遍!!"))
        self.qt_btn_start.setText(_translate("MainWindow", "开始挂机"))
        self.qt_btn_stop.setText(_translate("MainWindow", "停止挂机(Alt+Tab,Ctrl+0)"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Setting_Tab), _translate("MainWindow", "设置"))
        self.Setting_Box.setTitle(_translate("MainWindow", "使用前请看说明书1000000遍!!"))
        for i in range(len(source.group_combox_list)):
            self.Group_combox.setItemText(i, _translate("MainWindow", source.group_combox_list[i]))

        self.Group_label.setText(_translate("MainWindow", "阵容选择"))
        self.FFturn_combox.setItemText(0, _translate("MainWindow", "10分钟投降"))
        self.FFturn_combox.setItemText(1, _translate("MainWindow", "11分钟投降"))
        self.FFturn_combox.setItemText(2, _translate("MainWindow", "12分钟投降"))
        self.FFturn_combox.setItemText(3, _translate("MainWindow", "13分钟投降"))
        self.FFturn_combox.setItemText(4, _translate("MainWindow", "14分钟投降"))
        self.FFturn_combox.setItemText(5, _translate("MainWindow", "15分钟投降"))
        self.FFturn_combox.setItemText(6, _translate("MainWindow", "前二投降"))
        self.FFturn_combox.setItemText(7, _translate("MainWindow", "前四投降"))
        self.FFturn_combox.setItemText(8, _translate("MainWindow", "前六投降"))
        self.FFturn_combox.setItemText(9, _translate("MainWindow", "永不投降"))
        self.label_2.setText(_translate("MainWindow", "投降模式"))

        self.Customize_Box.setTitle(_translate("MainWindow", "自定义阵容英雄选择"))
        self.hero1_label.setText(_translate("MainWindow", "英雄1"))
        self.hero2_label.setText(_translate("MainWindow", "英雄2"))
        self.hero3_label.setText(_translate("MainWindow", "英雄3"))
        self.hero4_label.setText(_translate("MainWindow", "英雄4"))
        self.hero5_label.setText(_translate("MainWindow", "英雄5"))
        self.hero6_label.setText(_translate("MainWindow", "英雄6"))
        self.hero7_label.setText(_translate("MainWindow", "英雄7"))
        self.hero8_label.setText(_translate("MainWindow", "英雄8"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Intro_Tab), _translate("MainWindow", "微信公众号"))
        self.Intro_Box.setTitle(_translate("MainWindow", "最新版本下载，最新群号，使用说明书等"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Sponsor_Tab), _translate("MainWindow", "一元赞助"))
        self.Sponsor_Box.setTitle(_translate("MainWindow", "一元赞助 升群人口 谢谢老板"))


import apprcc_rc