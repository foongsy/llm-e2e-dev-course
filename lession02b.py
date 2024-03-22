"""
# Venturenix Lab: Advanced Generative AI: End to end development with LLMs
### Lession 2: Introduction to Python (2)

Goal: Rewrite the data models of thisthisrice using OO approach
"""
# 匯入模組
import re
from random import sample

# 定義環境及"constant"
CSV_FILE = 'thisthisrice.csv'

class Dish:
    MEAT_KEYWORDS: list[str] = ['牛', '豬', '雞', '魚', '羊', '叉燒', '肉', '班腩', '鴨', '鵝']

    def __init__(self, name: str, wday: str) -> None:
        self.name: str = name
        self.is_meat: bool = False
        # 檢查wday是否周一至周五
        if 0 <= int(wday) <= 5:
            self.wday: int = wday
        else:
            raise ValueError('Invalid weekday for dish')
        # 檢查是否肉類
        for m in self.MEAT_KEYWORDS:
            if m in self.name:
                self.is_meat = True

    def __repr__(self):
        return(self.name)

    def __str__(self):
        return(self.name)

class Ricebox:
    FISH_SET_KEYWORD: str = '蒸倉魚'
    MAX_NO_OF_DISHES: int = 4
    MAX_NO_OF_FISH_DISHES: int = 3
    BASE_PRICE: int  = 35
    PERDISH_PRICE: int = 8
    FISH_BASE_PRICE: int = 58

    def __init__(self) -> None:
        self.price: int = 0
        self.dish_count: int = 0

    def add(dish: Dish):
        pass

# Importing data
with open(CSV_FILE, 'r', encoding='utf-8') as file_descriptor:
    csv_content: list[str] = file_descriptor.readlines()

# 移除最後一行
csv_content.pop()

pattern = re.compile(r"[0-9\. \n\*]+")

fields_list: list[str] = []
for line in csv_content:
    fields_list.append(line.split(","))

# 問題1：*在這裡的用處；zip的功能
dish_by_wday = list(zip(*fields_list))
# 問題2：range的用途
for i in range(len(dish_by_wday)):
    # 問題3：這行到底是做什麼？
    dish_by_wday[i] = [ Dish(pattern.sub('', x), i) for x in dish_by_wday[i] ]

print(repr(dish_by_wday))


# 用基本input取得用戶輸入
print("問：今天是星期幾？[1-5]")
weekday = input()
if(weekday not in ['1','2','3','4','5']):
    raise Exception("錯誤用戶輸入")
print(f"星期{weekday}的菜色")

weekday = int(weekday) - 1
print(repr(dish_by_wday[weekday]))

print("問：要選多少個餸？[2-4]")
num_of_dish = int(input())
if num_of_dish > 4 or num_of_dish < 2:
    raise Exception("必須挑選合適數目的餸")
dish_num = sample(range(12), num_of_dish)
print("隨機選中的菜色:")

selected = list()
for i in dish_num:
    print(f"\t{dish_by_wday[weekday][i]}")
    selected.append(dish_by_wday[weekday][i])
print(repr(selected))
# print(f"價錢：{how_much(selected)}")