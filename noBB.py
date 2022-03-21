#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui  # , QtCore, QtWidgets
# import noBBui5 as noBBui
import noBBui
import source
import os
import random
import base64


BASE_PATH = source.BASE_PATH
ASSET_PATH = source.ASSET_PATH
ASSET_DIR = source.ASSET_DIR
ASSET_FILE_LIST = source.ASSET_FILE_LIST

VERSION_FILE = source.VERSION_FILE
VERSION = source.VERSION

CONFIG_FILE = source.CONFIG_FILE
CONFIG = source.CONFIG


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def del_asset_files():
    file_list = []
    for root, dirs, files in os.walk(ASSET_PATH):
        for f in files:
            file_list.append(os.path.join(root, f))
    for i in file_list:
        os.remove(i)


def load_asset_files():

    for folder in ASSET_DIR:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for file in ASSET_FILE_LIST:
        save_path = file[0]
        img_str = file[1]
        if not os.path.exists(save_path):
            # print(save_path, img_str)
            img_data = base64.b64decode(img_str)
            with open(save_path, 'wb') as f:
                f.write(img_data)


def get_temp_code_link():
    # 读最后一行的code
    with open(CONFIG_FILE, 'r') as f:
        lines = f.readlines()

    return lines[-1][19:]


def load_files():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    # 本机第一次启动脚本
    if not os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'w', encoding='utf8') as f:
            f.write(VERSION)
        with open(CONFIG_FILE, 'w', encoding='utf8') as f:
            f.write(CONFIG)
            f.write("TEMPLINKCODE_VALUE=" + generate_random_str(16))
        load_asset_files()
    else:
        with open(VERSION_FILE, 'r') as f:
            current_version = f.read()
        if current_version == VERSION:
            return

        # version改了
        with open(VERSION_FILE, 'w', encoding='utf8') as f:
            f.write(VERSION)
        current_config_temp_link_code = get_temp_code_link()
        with open(CONFIG_FILE, 'w', encoding='utf8') as f:
            f.write(CONFIG)
            f.write("TEMPLINKCODE_VALUE=" + current_config_temp_link_code)
        del_asset_files()
        load_asset_files()


if __name__ == '__main__':
    load_files()

    app = QApplication(sys.argv)  # 所有的PyQt5应用必须创建一个应用（Application）对象。
    app.setWindowIcon(QtGui.QIcon('./bitbug_favicon.ico'))
    # sys.argv参数是一个来自命令行的参数列表。
    myMainWindow = QMainWindow()  # Qwidget组件是PyQt5中所有用户界面类的基础类。我们给QWidget提供了默认的构造方法。 不过这里用的是mainwindow
    # 默认构造方法没有父类。没有父类的widget组件将被作为窗口使用。

    myUi = noBBui.Ui_MainWindow()
    myUi.setupUi(myMainWindow)

    myMainWindow.show()  # show()方法在屏幕上显示出widget。一个widget对象在这里第一次被在内存中创建，并且之后在屏幕上显示。
    sys.exit(app.exec_())
    # 应用进入主循环。在这个地方，事件处理开始执行。主循环用于接收来自窗口触发的事件，
    # 并且转发他们到widget应用上处理。如果我们调用exit()方法或主widget组件被销毁，主循环将退出。
    # sys.exit()方法确保一个不留垃圾的退出。系统环境将会被通知应用是怎样被结束的。
