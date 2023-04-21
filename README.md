# 原神祈愿模拟 GenshinWish
本Python库是用来模拟原神抽卡的，作者为Lawrence Guo，具体可以模拟角色活动祈愿、武器祈愿和常驻祈愿（暂不支持新手祈愿）
# `Wish()`类
用于设定卡池初始状态并预备好抽卡。可以直接什么都不填，用`Wish()`来进行实例化，也可以自定义卡池的信息和抽卡状态数据。

目前只能让一个对象进行实例化，在一个对象内不可以混合使用三种方法，因为水位是继承的。如果想在同意程序中抽别的池子需要对另外一个对象实例化。后续的更新中可能会将这个问题修复。

（可选）输入参数如下：
## 卡池信息
### 限定角色祈愿
- `up_candidate`为限定角色祈愿中UP的五星角色，类型为`str`，默认值为`"纳西妲"`
- `four_star_up`为限定角色祈愿中UP的四星角色，类型为长度为3的`list`，默认值为`["久岐忍", "多莉", "莱依拉"]`
### 限定武器祈愿
- `five_star_weapon_up`为限定武器祈愿中UP的五星武器，类型为长度为2的`list`，默认值为`["千夜浮梦", "圣显之钥"]`
- `four_star_weapon_up`为限定武器祈愿中UP的四星武器星武器，类型为长度为5的`list`，默认值为`["绝弦", "祭礼残章", "匣里灭辰", "西风大剑", "西福斯的月光"]`

## 抽卡状态
### 通用状态信息
- `draw_count`为抽卡水位统计，类型为`int`，默认值为`0`。
- `four_star_count`为四星物品水位统计，类型为`int`，默认值为`0`。
- `five_star_grt`为五星保底状态，类型为`bool`，默认值为`False`。当`five_star_grt=False`时，可能会歪，也可能不歪；当`five_star_grt=True`时，必定出本期UP五星物品。
- `four_star_grt`为四星保底状态，类型为`bool`，默认值为`False`。当`four_star_grt=False`时，可能会歪，也可能不歪；当`four_star_grt=True`时，必定出本期UP四星物品。
- `is_limited`判断是否为本期限定角色，类型为`bool`，默认值为`False`。
- `star`为物品星级，类型为范围在[3,5]的`int`，默认值为`3`
- `is_character`判断上一抽结果是否为角色，类型为`bool`，默认值为`False`
- `history`存储抽卡记录，类型为`list`
### 武器池专用状态信息
- `chart_course`为定轨状态，类型应为`str`，默认值为`None`。
- `fate_points`为命定值，类型为范围在[0,2]的`int`，默认值为`0`.
- `is_chart_course`最近一次出五星时，判断结果是否为定轨武器，类型为`bool`，默认值为`False`。

## 使用示例


```python
from genshinwish import Wish

wish = Wish(up_candidate="纳西妲", four_star_up=["久岐忍", "多莉", "莱依拉"])
```

# 方法
## 1. 限定角色卡池 抽取结果生成 `char_event_wish()`
返回类型为`dict`

输出格式参考：
```
{'time': '2023-04-22 01:02:47',
 'five_star_grt': False,
 'four_star_grt': False,
 'draw_count': 1,
 'four_star_count': 1,
 'star': 3,
 'is_limited': False,
 'is_character': False,
 'result': '鸦羽弓'}
```


```python
wish = Wish(up_candidate="纳西妲", four_star_up=["久岐忍", "多莉", "莱依拉"])

wish.char_event_wish()
```

## 2. 限定武器卡池 抽取结果生成 `weapon_event_wish()`
返回类型为`dict`

输出格式参考：
```
{'time': '2023-04-22 01:05:47',
 'five_star_grt': False,
 'four_star_grt': True,
 'draw_count': 13,
 'four_star_count': 10,
 'star': 4,
 'is_character': False,
 'is_limited': True,
 'is_chart_course': False,
 'fate_points': 0,
 'result': '绝弦'}
```


```python
wish = Wish(five_star_weapon_up=["千夜浮梦", "圣显之钥"],
            four_star_weapon_up=["绝弦", "祭礼残章", "匣里灭辰", "西风大剑", "西福斯的月光"])

wish.weapon_event_wish()
```

## 3. 常驻卡池 抽取结果生成 `std_wish()`
返回类型为`dict`

输出格式参考：
```
{'time': '2023-04-22 01:12:43',
 'draw_count': 13,
 'four_star_count': 10,
 'star': 4,
 'is_limited': False,
 'is_character': False,
 'result': '匣里龙吟'}
```


```python
wish = Wish()

wish.std_wish()
```

# 使用例


```python
from genshinwish import Wish

wish = Wish(up_candidate="纳西妲", four_star_up=["久岐忍", "多莉", "莱依拉"], chart_course="千夜浮梦")
wish.history = []
collect = []
count = 0

# 使用例：模拟抽卡（直到第一次抽中限定五星）
while True:
    # 我的回合！抽卡！
    state = wish.char_event_wish()
    # print(state)

    if state["star"] == 5 and state["is_limited"]:  # 抽中本期UP就计数
        count += 1

    if count == 6:  # 抽满命！！！
        break
    # if state["star"] == 5:
    #     break

    # 提取分析抽出的五星
for i in range(len(wish.history)):
    if wish.history[i]["star"] == 5:
        print(wish.history[i])
```

输出示例：
```
{'time': '2023-04-22 01:25:31', 'five_star_grt': False, 'four_star_grt': False, 'draw_count': 79, 'four_star_count': 1, 'star': 5, 'is_limited': False, 'is_character': True, 'result': '莫娜'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': True, 'four_star_grt': True, 'draw_count': 78, 'four_star_count': 6, 'star': 5, 'is_limited': True, 'is_character': True, 'result': '纳西妲'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': False, 'four_star_grt': False, 'draw_count': 79, 'four_star_count': 8, 'star': 5, 'is_limited': True, 'is_character': True, 'result': '纳西妲'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': False, 'four_star_grt': False, 'draw_count': 77, 'four_star_count': 10, 'star': 5, 'is_limited': False, 'is_character': True, 'result': '刻晴'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': True, 'four_star_grt': True, 'draw_count': 75, 'four_star_count': 4, 'star': 5, 'is_limited': True, 'is_character': True, 'result': '纳西妲'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': False, 'four_star_grt': False, 'draw_count': 40, 'four_star_count': 6, 'star': 5, 'is_limited': True, 'is_character': True, 'result': '纳西妲'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': False, 'four_star_grt': False, 'draw_count': 18, 'four_star_count': 5, 'star': 5, 'is_limited': False, 'is_character': True, 'result': '提纳里'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': True, 'four_star_grt': True, 'draw_count': 67, 'four_star_count': 1, 'star': 5, 'is_limited': True, 'is_character': True, 'result': '纳西妲'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': False, 'four_star_grt': True, 'draw_count': 47, 'four_star_count': 1, 'star': 5, 'is_limited': False, 'is_character': True, 'result': '迪卢克'}
{'time': '2023-04-22 01:25:31', 'five_star_grt': True, 'four_star_grt': False, 'draw_count': 83, 'four_star_count': 6, 'star': 5, 'is_limited': True, 'is_character': True, 'result': '纳西妲'}
```
