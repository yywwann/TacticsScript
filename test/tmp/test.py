# -*- coding: utf-8 -*-
#! /usr/bin/env python
import time
import pyautogui as auto
import random
import os
import sys
sys.path.append("..")
import source
import loginAPI


class TEST(object):

    def __init__(self, group, ffturn, hero1, hero2, hero3, hero4, hero5, hero6, hero7, hero8, temp_link_code):
        self.DEBUG = source.DEBUG
        self.debug_time = 0
        self.BASE_PATH = source.BASE_PATH
        self.ASSET_PATH = source.ASSET_PATH
        self.restart_list = source.restart_list
        self.hero_map = source.hero_map_s4_5

        self.pic_inGame = source.pic_inGame
        self.all_pic_dead = source.all_pic_dead
        self.pic_one_star = source.pic_one_star
        self.pic_two_star = source.pic_two_star

        self.btn_start = source.btn_start
        self.btn_accept = source.btn_accept
        self.btn_ok = source.btn_ok
        self.btn_x = source.btn_x
        self.btn_ff_1 = source.btn_ff_1
        self.btn_ff_2 = source.btn_ff_2
        self.btn_ff_3 = source.btn_ff_3

        self.weapons = source.weapons
        self.chesses = source.chesses

        self.url = source.URL
        self.CDKEY = source.CDKEY
        self.temp_link_code = temp_link_code
        self.login_check = loginAPI.noBBLogin(self.url, self.CDKEY, self.temp_link_code)

        self.flag = 1  # 判断脚本是否允许
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
        self._2_1 = 0  # 判断当前是否是2-1回合
        self.chess_idx = 0

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

    def check_pic(self, needleImage, region=None):
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
        # haystackImage.save("assert/test"+needleImage[7]+".png")
        pic = auto.locate(needleImage, haystackImage, confidence=0.9)
        if pic is not None:
            pic = auto.center(pic)
            return [pic[0] + region[0], pic[1] + region[1]]

        return None

    def check_all_pic(self, needleImage, region=None):
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
                                          confidence=0.99))
        pic_list = []
        for pic in pics:
            pic = auto.center(pic)
            pic_list.append((pic[0] + region[0], pic[1] + region[1]))
        return pic_list

    def in_game_switch(self):
        down_x = [460, 560, 670, 790, 900, 1000, 1110, 1220, 1330]
        down_y = 740
        # current_time = time.time()
        # if current_time - self.g_time < 5 * 60 or current_time - self.switch_time < 120:
        #     return

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



        print('一星位置 x={}, y={}'.format(one_star_x, one_star_y))
        print('二星位置 x={}, y={}'.format(two_star_x, two_star_y))


if __name__ == "__main__":
    ts = TEST(0, 0, '1豹女', '1豹女', '1豹女', '1豹女', '1豹女', '1豹女', '1豹女', '1豹女', '0')
    time.sleep(5)
    ts.in_game_switch()