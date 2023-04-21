import time
import random
import candidates


class Wish(object):
    """# 原神祈愿模拟

    在实例化时输入当期UP的五星:str和四星:list即可，也可以不输入，默认是纳西妲、久岐忍、多莉、莱依拉
    可以生成抽卡结果，也可以提取抽卡记录
    """
    # 存储抽卡记录
    history = []
    four_star_ctrl = []
    five_star_ctrl = []

    def __init__(self, up_candidate="纳西妲", four_star_up=["久岐忍", "多莉", "莱依拉"],
                 five_star_weapon_up=["千夜浮梦", "圣显之钥"],
                 four_star_weapon_up=["绝弦", "祭礼残章", "匣里灭辰", "西风大剑", "西福斯的月光"], chart_course=None,
                 draw_count=0,
                 four_star_count=0, five_star_grt=False, four_star_grt=False, is_limited=False, star=3,
                 is_character=False, fate_points=0, is_chart_course=False) -> None:
        # 设定UP五星和四星
        self.up_candidate = up_candidate
        self.four_star_up = four_star_up
        self.five_star_weapon_up = five_star_weapon_up
        self.four_star_weapon_up = four_star_weapon_up
        # 上一抽状态
        self.chart_course = chart_course  # 武器定轨
        self.fate_points = fate_points  # 命定值
        self.is_chart_course = is_chart_course
        self.draw_count = draw_count
        self.four_star_count = four_star_count
        self.five_star_grt = five_star_grt
        self.four_star_grt = four_star_grt
        self.is_limited = is_limited
        self.star = star
        self.is_character = is_character

    def __five_star(self):
        """# 生成五星抽取结果（限定池）
        根据保底情况生成抽取结果
        返回格式(抽卡结果:str,是否为当期限定:bool,是否为角色:bool)
        """
        if self.five_star_grt:  # 触发大保底
            return self.up_candidate, True, True  # 返回格式[抽卡结果,是否为当期限定,是否为角色]
        select_pos = random.random()  # 未触发大保底
        if select_pos <= 0.5:  # 没歪
            return self.up_candidate, True, True
        else:  # 歪了
            return random.choice(candidates.five_star_general_char), False, True

    def __five_star_weapon(self):
        """# 生成五星武器抽取结果
        根据保底情况生成抽取结果
        返回格式(抽卡结果:str,是否为当期限定:bool,是否为角色:bool，是否为定轨武器)
        """
        if self.five_star_grt:  # 触发大保底
            if self.fate_points < 2:
                five_star_pulled = random.choice(self.five_star_weapon_up)
                return five_star_pulled, True, False, five_star_pulled == self.chart_course
            else:  # 命定值已满
                return self.chart_course, True, False, True
        else:  # 没触发大保底
            five_star_rand = random.random()
            if five_star_rand <= 0.75:
                five_star_pulled = random.choice(self.five_star_weapon_up)
                return five_star_pulled, True, False, five_star_pulled == self.chart_course
            else:
                return random.choice(candidates.five_star_general_weapons), False, False, False

    def __five_star_std(self):
        """# 生成五星抽取结果（常驻池）
        根据保底情况生成抽取结果
        返回格式(抽卡结果:str,是否为当期限定:bool=False,是否为角色:bool)
        """

        def char_weapon_ctrl():
            if len(self.five_star_ctrl) < 3:
                return 0
            else:
                if self.five_star_ctrl[-3:] == [1, 1, 1]:  # 连续三次角色
                    return 2
                elif self.five_star_ctrl[-3:] == [0, 0, 0]:  # 连续三次武器
                    return 1
                else:
                    return 0

        five_sel_rand = random.random()  # 未触发大保底
        if (five_sel_rand <= 0.5 and char_weapon_ctrl() == 0) or char_weapon_ctrl() == 1:  # 角色
            self.five_star_ctrl.append(1)
            return random.choice(candidates.five_star_general_char), False, True
        elif (five_sel_rand > 0.5 and char_weapon_ctrl() == 0) or char_weapon_ctrl() == 2:  # 武器
            self.five_star_ctrl.append(0)
            return random.choice(candidates.five_star_general_weapons), False, False

    def __four_star(self):
        four_sel_rand = random.random()
        if self.four_star_grt:  # up四星角色保底
            return random.choice(self.four_star_up), True, True
        else:
            if four_sel_rand <= 0.5:  # 出四星角色,是UP
                return random.choice(self.four_star_up), True, True
            else:
                if 0.5 < four_sel_rand <= 0.75:  # 出非UP四星角色
                    while True:
                        four_star_pulled = random.choice(candidates.four_star_char)
                        if four_star_pulled not in self.four_star_up:  # 要保证抽出来的不是当期UP四星
                            return four_star_pulled, False, True
                else:  # 出四星武器
                    return random.choice(candidates.four_star_weapons), False, False

    def __four_star_weapon(self):
        four_sel_rand = random.random()
        if self.four_star_grt:  # 上次没出限定四星,这次触发四星UP保底
            return random.choice(self.four_star_weapon_up), True, False, False
        else:

            if four_sel_rand <= 0.75:  # 出限定四星武器，但不是当期UP
                return random.choice(self.four_star_weapon_up), True, False, False
            else:
                if 0.75 < four_sel_rand <= 0.75 + 0.25 / 2:  # 出角色
                    return random.choice(candidates.four_star_char), False, True, False
                else:  # 出武器
                    while True:
                        four_star_pulled = random.choice(candidates.four_star_weapons)
                        if four_star_pulled not in self.four_star_weapon_up:  # 要保证抽出来的不是当期UP四星
                            return four_star_pulled, False, False, False

    def __four_star_std(self):
        def char_weapon_ctrl():
            if len(self.four_star_ctrl) < 2:
                return 0
            else:
                if self.four_star_ctrl[-2:] == [1, 1]:  # 连续两次角色
                    return 2
                elif self.four_star_ctrl[-2:] == [0, 0]:  # 连续两次武器
                    return 1
                else:
                    return 0

        four_sel_rand = random.random()
        if (four_sel_rand <= 0.5 and char_weapon_ctrl() == 0) or char_weapon_ctrl() == 1:  # 出四星角色
            self.four_star_ctrl.append(1)
            return random.choice(candidates.four_star_char), False, True
        elif (four_sel_rand > 0.5 and char_weapon_ctrl() == 0) or char_weapon_ctrl() == 2:  # 出四星武器
            self.four_star_ctrl.append(0)
            return random.choice(candidates.four_star_weapons), False, False

    def __three_star(self):
        return random.choice(candidates.three_star_weapons), False, False, False

    def char_event_wish(self):
        """# 角色活动祈愿（Character Event Wish）
        输出格式参考

        {
            'time': '2023-04-19 09:26:01', # 抽卡时间
            'five_star_grt': True, # 五星保底状况，如果为True则当前抽中五星时必为当期UP五星
            'four_star_grt': True, # 四星保底状况，如果为True则当前抽中四星时必为当期UP四星
            'draw_count': 47, # 水位
            'four_star_count': 9, # 四星水位
            'star': 5, # 抽取结果星级
            'is_limited': True, # 是否为限定角色
            'is_character': True, # 是否为角色
            'result': '纳西妲', # 抽取结果名称
        }
        """
        # 输入上一次抽卡数据以生成当前抽卡数据

        # 将上一次抽卡数据转换成当前抽卡数据
        if self.star == 5:
            self.draw_count = 1  # 抽中五星之后复原水位
        else:
            self.draw_count = self.draw_count + 1  # 水位+1
        if self.star == 4:  # 上一次四星保底已触发（如果上次四星保底水位已经满了，但是出金了，那么四星保底水位顺移到当前抽卡）
            self.four_star_count = 1  # 复原四星保底水位
        elif self.four_star_count != 10:
            self.four_star_count = self.four_star_count + 1  # 四星保底水位+1

        # 没歪或者歪了之后转换五星和四星的保底状态
        if (self.star == 5 and self.is_limited == False) or (
                self.star == 5 and self.is_limited and self.five_star_grt):
            self.five_star_grt = not self.five_star_grt
        elif self.star == 4:
            self.four_star_grt = not self.four_star_grt

        # 当前抽卡状态(json输出格式预备)
        output = {
            "time": None,
            "five_star_grt": self.five_star_grt,
            "four_star_grt": self.four_star_grt,
            "draw_count": self.draw_count,
            "four_star_count": self.four_star_count,
            "star": self.star,
            "is_limited": self.is_limited,
            "is_character": self.is_character,
            "result": ""
        }

        # 概率初始值
        five_star_prob = 0.006
        four_star_prob = 0.051
        a = five_star_prob * 10
        b = four_star_prob * 10

        # 概率调整
        if 73 < self.draw_count <= 89:  # 概率逐次提升
            five_star_prob = min(1.0, five_star_prob + a * (self.draw_count - 73))
        elif self.draw_count == 90:  # 直接究极大保底，究极非酋
            five_star_prob = 1
        if 8 < self.four_star_count <= 9:
            four_star_prob = min(1.0 - five_star_prob, four_star_prob + b * (self.four_star_count - 8))
        elif self.four_star_count == 10:
            four_star_prob = 1.0 - five_star_prob

        pull = random.random()
        if pull <= five_star_prob:  # 五星出金
            draw_out = self.__five_star()
            self.star = 5
        elif five_star_prob < pull <= five_star_prob + four_star_prob:  # 出四星
            draw_out = self.__four_star()
            self.star = 4
        else:
            draw_out = self.__three_star()
            self.star = 3

        result = draw_out[0]
        self.is_limited = draw_out[1]
        self.is_character = draw_out[2]
        output["result"] = result
        output["star"] = self.star
        output["is_limited"] = self.is_limited
        output["is_character"] = self.is_character
        output["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.history.append(output)  # 存储结果
        return output

    def std_wish(self):
        """# 常驻角色祈愿（Standard Wish）
        输出格式参考

        {
            'time': '2023-04-19 09:26:01', # 抽卡时间
            'five_star_grt': True, # 五星保底状况，如果为True则当前抽中五星时必为当期UP五星
            'four_star_grt': True, # 四星保底状况，如果为True则当前抽中四星时必为当期UP四星
            'draw_count': 47, # 水位
            'four_star_count': 9, # 四星水位
            'star': 5, # 抽取结果星级
            'is_limited': True, # 是否为限定角色
            'is_character': True, # 是否为角色
            'result': '纳西妲', # 抽取结果名称
        }
        """
        # 输入上一次抽卡数据以生成当前抽卡数据

        # 将上一次抽卡数据转换成当前抽卡数据
        if self.star == 5:
            self.draw_count = 1  # 抽中五星之后复原水位
        else:
            self.draw_count = self.draw_count + 1  # 水位+1
        if self.star == 4:  # 上一次四星保底已触发（如果上次四星保底水位已经满了，但是出金了，那么四星保底水位顺移到当前抽卡）
            self.four_star_count = 1  # 复原四星保底水位
        elif self.four_star_count != 10:
            self.four_star_count = self.four_star_count + 1  # 四星保底水位+1

        # 没歪或者歪了之后转换五星和四星的保底状态
        if self.star == 5:
            self.five_star_grt = not self.five_star_grt
        elif self.star == 4:
            self.four_star_grt = not self.four_star_grt

        # 当前抽卡状态(json输出格式预备)
        output = {
            "time": None,
            "draw_count": self.draw_count,
            "four_star_count": self.four_star_count,
            "star": self.star,
            "is_limited": self.is_limited,
            "is_character": self.is_character,
            "result": ""
        }

        # 概率初始值
        five_star_prob = 0.006
        four_star_prob = 0.051
        a = five_star_prob * 10
        b = four_star_prob * 10

        # 概率调整
        if 73 < self.draw_count <= 89:  # 概率逐次提升
            five_star_prob = min(1.0, five_star_prob + a * (self.draw_count - 73))
        elif self.draw_count == 90:  # 直接究极大保底，究极非酋
            five_star_prob = 1
        if 8 < self.four_star_count <= 9:
            four_star_prob = min(1.0 - five_star_prob, four_star_prob + b * (self.four_star_count - 8))
        elif self.four_star_count == 10:
            four_star_prob = 1.0 - five_star_prob

        pull = random.random()
        if pull <= five_star_prob:  # 五星出金
            draw_out = self.__five_star_std()
            self.star = 5
        elif five_star_prob < pull <= five_star_prob + four_star_prob:  # 出四星
            draw_out = self.__four_star_std()
            self.star = 4
        else:
            draw_out = self.__three_star()
            self.star = 3

        result = draw_out[0]
        self.is_limited = draw_out[1]
        self.is_character = draw_out[2]
        output["result"] = result
        output["star"] = self.star
        output["is_limited"] = self.is_limited
        output["is_character"] = self.is_character
        output["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.history.append(output)  # 存储结果
        return output

    def weapon_event_wish(self):
        """# 武器活动祈愿（Weapon Event Wish）
        输出格式参考

        {
            'time': '2023-04-19 09:26:01', # 抽卡时间
            'five_star_grt': True, # 五星保底状况，如果为True则当前抽中五星时必为当期UP五星
            'four_star_grt': True, # 四星保底状况，如果为True则当前抽中四星时必为当期UP四星
            'draw_count': 47, # 水位
            'four_star_count': 9, # 四星水位
            'star': 5, # 抽取结果星级
            'is_limited': True, # 是否为限定角色
            'is_character': True, # 是否为角色
            'result': '纳西妲', # 抽取结果名称
        }
        """
        # 输入上一次抽卡数据以生成当前抽卡数据

        # 将上一次抽卡数据转换成当前抽卡数据
        if self.star == 5:
            self.draw_count = 1  # 抽中五星之后复原水位
        else:
            self.draw_count = self.draw_count + 1  # 水位+1
        if self.star == 4:  # 上一次四星保底已触发（如果上次四星保底水位已经满了，但是出金了，那么四星保底水位顺移到当前抽卡）
            self.four_star_count = 1  # 复原四星保底水位
        elif self.four_star_count != 10:
            self.four_star_count = self.four_star_count + 1  # 四星保底水位+1

        # 没歪或者歪了之后转换五星和四星的保底状态
        if self.fate_points < 2 and self.star == 5 and self.is_chart_course == False:
            self.fate_points += 1
        elif self.is_chart_course:
            self.fate_points = 0
        if (self.star == 5 and self.is_limited == False) or (
                self.star == 5 and self.five_star_grt and self.is_chart_course):
            self.five_star_grt = not self.five_star_grt
        if self.star == 4:
            self.four_star_grt = not self.four_star_grt

        # 当前抽卡状态(json输出格式预备)
        output = {
            "time": None,
            "five_star_grt": self.five_star_grt,
            "four_star_grt": self.four_star_grt,
            "draw_count": self.draw_count,
            "four_star_count": self.four_star_count,
            "star": self.star,
            "is_character": self.is_character,
            "is_limited": self.is_limited,
            "is_chart_course": self.is_chart_course,
            "fate_points": self.fate_points,
            "result": ""
        }

        # 概率初始值
        five_star_prob = 0.007
        four_star_prob = 0.06
        a = five_star_prob * 10
        rise = 63

        # 概率调整
        if rise < self.draw_count <= 79:  # 概率逐次提升
            five_star_prob = min(1.0, five_star_prob + a * (self.draw_count - rise))
        elif self.draw_count == 80:  # 直接究极大保底，究极非酋
            five_star_prob = 1

        pull = random.random()
        if pull <= five_star_prob:  # 五星出金
            draw_out = self.__five_star_weapon()
            self.star = 5
        elif (five_star_prob < pull <= five_star_prob + four_star_prob) or self.four_star_count == 10:  # 出四星
            draw_out = self.__four_star_weapon()
            self.star = 4
        else:
            draw_out = self.__three_star()
            self.star = 3

        result = draw_out[0]
        self.is_limited = draw_out[1]
        self.is_character = draw_out[2]
        self.is_chart_course = draw_out[3]
        output["result"] = result
        output["star"] = self.star
        output["is_limited"] = self.is_limited
        output["is_character"] = self.is_character
        output["is_chart_course"] = self.is_chart_course
        output["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.history.append(output)  # 存储结果
        return output
