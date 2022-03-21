import source
import os

hero_eng_name = ['group4/1BoBi.png', 'group4/1ELuoYi.png', 'group4/1EZ.png', 'group4/1GaiLun.png', 'group4/1KaMiEr.png',
                 'group4/1KaPai.png', 'group4/1KaSaDing.png', 'group4/1LaoShu.png', 'group4/1LianJin.png',
                 'group4/1NanQiang.png', 'group4/1NuoShou.png', 'group4/1NvJing.png', 'group4/1ZhaDanRen.png',
                 'group4/2DaZui.png', 'group4/2JieLa.png', 'group4/2JiLan.png', 'group4/2JiQiRen.png',
                 'group4/2JuMo.png', 'group4/2KaTe.png', 'group4/2KuiYin.png', 'group4/2LangRen.png',
                 'group4/2TaiLong.png', 'group4/2Wei.png', 'group4/2WuYa.png', 'group4/2XiaoPao.png',
                 'group4/3AiKe.png', 'group4/3BaoShi.png', 'group4/3ChuangZhang.png', 'group4/3DaChongZi.png',
                 'group4/3DaTou.png', 'group4/3LeiOuNa.png', 'group4/3LiSangZhuo.png', 'group4/3LuLu.png',
                 'group4/3MaErZhaHa.png', 'group4/3NvQiang.png', 'group4/3ShaMiLa.png', 'group4/3WeiGuSi.png',
                 'group4/3XiaoChou.png', 'group4/3ZhaKe.png', 'group4/4BuLong.png', 'group4/4EJiaTe.png',
                 'group4/4FaTiao.png', 'group4/4FengNv.png', 'group4/4JianJi.png', 'group4/4Jing.png',
                 'group4/4LaKeSi.png', 'group4/4MengDuo.png', 'group4/4SaiEn.png', 'group4/4SaLeFenNi.png',
                 'group4/4YongEn.png', 'group4/5AKaLi.png', 'group4/5JiaLiAo.png', 'group4/5JinKeSi.png',
                 'group4/5KaSha.png', 'group4/5WeiKeTuo.png']

hero_chi_name = [
    '1波比', '1俄洛伊', '1EZ', '1盖伦', '1卡尔玛', '1卡牌', '1卡萨丁', '1老鼠', '1炼金', '1男枪', '1诺手', '1女警', '1炸弹人',

    '2大嘴', '2婕拉', '2基兰', '2机器人', '2巨魔', '2卡特', '2奎因', '2狼人', '2泰隆', '2蔚', '2乌鸦', '2小炮',

    '3艾克', '3宝石', '3船长', '3大虫子', '3大头', '3蕾欧娜', '3丽桑卓', '3露露', '3马尔扎哈', '3女枪', '3莎弥拉', '3薇古丝', '3小丑', '3扎克',

    '4布隆', '4厄加特', '4发条', '4风女', '4剑姬', '4烬', '4拉克丝', '4蒙多', '4塞恩', '4萨勒芬妮', '4永恩',

    '5阿卡丽', '5加里奥', '5金克斯', '5卡莎', '5维克托'
]


def getGroup4():
    file_list = os.listdir('C:/Projects/PythonProjects/noBB/asset/group4')
    list = []
    for file in file_list:
        file = 'group4/' + file
        list.append(file)
    print(list)


def get_hero_map():
    fo = open('source_hero_map.py', 'w', encoding='utf8')
    fo.write('hero_map = {\n')
    for i, j in zip(hero_chi_name, hero_eng_name):
        fo.write("\t\"{}\": \"{}\",\n".format(i, j))
    fo.write("}\n")


getGroup4()
get_hero_map()
