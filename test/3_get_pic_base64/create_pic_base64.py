import os
import base64

'''
将项目里asset文件夹里的内容全部转成base64码
'''

BASE_PATH = 'C:/Projects/PythonProjects/noBB/'
ASSET_PATH = 'asset/'
ASSET_FOLDERS = ['', 'group0/', 'group1/', 'group2/', 'group3/', 'group4/', 'sys/']
file_list = []


def get_all_files(dir_path):
    file_list = []
    folder_list = []
    for root, dirs, files in os.walk(dir_path):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print(os.path.join(root, f))
            file_list.append(os.path.join(root, f).replace("\\", "/"))

        # 遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root, d))
        #     folder_list.append(os.path.join(root, d))

    return file_list



def writePic(file_list):
    dirs = 'C:/Program Files/noBB/asset/'
    fo = open('C:/Projects/PythonProjects/noBB/test/3_get_pic_base64/asset_file_list.py', 'w')
    fo.write("ASSET_FILE_LIST = [\n")
    for file_name in file_list:
        file_path = file_name[len(BASE_PATH)+len(ASSET_PATH):]
        save_path = dirs + file_path
        # print(file_path, save_path)
        with open(file_name, "rb") as f:
            # b64encode是编码，b64decode是解码
            base64_data = base64.b64encode(f.read())
        # print(base64_data)  # 输出生成的base64码
        fo.write("\t(\"{}\", {}),\n".format(save_path, base64_data))
    fo.write("]\n")
    fo.close()

file_list = get_all_files(BASE_PATH+ASSET_PATH)
# print(file_list)
writePic(file_list)
