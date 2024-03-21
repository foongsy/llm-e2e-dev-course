"""
# Venturenix Lab: Advanced Generative AI: End to end development with LLMs
### Lession 2: Introduction to Python (2)
"""
# 匯入模組
import re
from random import sample

# 定義環境及"constant"
CSV_FILE = 'thisthisrice.csv'
MEAT_KEYWORDS = ['牛', '豬', '雞', '魚', '羊', '叉燒', '肉', '班腩', '鴨', '鵝']
FISH_SET_KEYWORD = '蒸倉魚'
BASE_PRICE = 35
PERDISH_PRICE = 8
FISH_BASE_PRICE = 58
MAX_NO_OF_DISHES = 4
MAX_NO_OF_FISH_DISHES = 3

# 判斷是否有肉
def is_meat(dish):
    for m in MEAT_KEYWORDS:
        if m in dish:
            return True
    return False

# 計算飯盒價錢
def how_much(dishes):
    is_fish = False
    # 檢查是否超過配菜上限
    if len(dishes) > MAX_NO_OF_DISHES:
        raise Exception('Too many dishes')
    for dish in dishes:
        # 檢查是否蒸魚餐
        if FISH_SET_KEYWORD in dish:
            is_fish = True
            break
    # 檢查是否超過蒸魚餐上限
    if is_fish and len(dishes) > MAX_NO_OF_FISH_DISHES:
        raise Exception('蒸魚餐最多只能3個餸')
    # 計算價錢
    if is_fish:
        price = FISH_BASE_PRICE + (len(dishes) - 2) * PERDISH_PRICE
    else:
        price = BASE_PRICE + (len(dishes) - 2) * PERDISH_PRICE
    return(price)

with open(CSV_FILE, 'r', encoding='utf-8') as file_descriptor:
    csv_content = file_descriptor.readlines()

# 移除最後一行
csv_content.pop()

pattern = re.compile(r"[0-9\. \n\*]+")

fields_list = []
for line in csv_content:
    fields_list.append(line.split(","))

# 問題1：*在這裡的用處；zip的功能
dish_by_wday = list(zip(*fields_list))
# 問題2：range的用途
for i in range(len(dish_by_wday)):
    # 問題3：這行到底是做什麼？
    dish_by_wday[i] = [ pattern.sub('', x) for x in dish_by_wday[i] ]


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
print(f"價錢：{how_much(selected)}")