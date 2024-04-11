"""
# Venturenix Lab: Advanced Generative AI: End to end development with LLMs
### Lession 2: Introduction to Python (2)

Goal: Rewrite the data models of thisthisrice using SQLModel and store the data on sqlite
"""
# 匯入模組
import re
from typing import Annotated, List
from annotated_types import Interval
from pydantic import computed_field, ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import func
from pathlib import Path
from fastapi import FastAPI, HTTPException
from random import randint

# 定義環境及"constant"
CSV_FILE = 'thisthisrice.csv'
DB_PATH = 'rice.db'
SQLDB_PATH = 'sqlite:///' + DB_PATH
# 餐廳規矩
FISH_SET_KEYWORD: str = '蒸倉魚'
MAX_NO_OF_DISHES: int = 4
MIN_NO_OF_DISHES: int = 2
MAX_NO_OF_FISH_DISHES: int = 3
BASE_PRICE: int  = 35
PERDISH_PRICE: int = 8
FISH_BASE_PRICE: int = 58

# class Dish(BaseModel):
class Dish(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    wday: Annotated[int, Interval(ge=0, lt=6)] 
    
    @computed_field
    def is_meat(self) -> bool:
        _meat_keywords: List[str] = ['牛', '豬', '雞', '魚', '羊', '叉燒', '肉', '班腩', '鴨', '鵝']
        for m in _meat_keywords:
            if m in self.name:
                return(True)
        return(False)

class Bento(SQLModel, table=False):
    dishes: List[str]
    menu: List[str]
    wday: int

    def __init__(self, weekday: Annotated[int, Interval(ge=1, le=5)] = randint(1,5), dishes : List[str] = list()) -> None:
        # 讀取所選當日餸菜
        self.menu = []
        self.dishes = []
        self.wday = weekday
        statement = select(Dish).where(Dish.wday == self.wday)
        with Session(engine) as session:
            selected_dishes = session.exec(statement)
            for d in selected_dishes:
                self.menu.append(d.name)
        for d in dishes:
            if d in self.menu:
                self.dishes.append(d.name)

    def change_wday(self, weekday: Annotated[int, Interval(ge=1, le=5)]) -> None:
        self.wday = weekday
        self.menu = []
        statement = select(Dish).where(Dish.wday == self.wday)
        with Session(engine) as session:
            selected_dishes = session.exec(statement)
            for d in selected_dishes:
                self.menu.append(d.name)

    def add_dish(self, dish: str) -> None:
        print(dish)
        if dish in self.menu:
            self.dishes.append(dish)
        else:
            raise Exception("餸菜今日並未供應")

    def has_fish(self) -> bool:
        for dish in self.dishes:
            if FISH_SET_KEYWORD in dish:
                return True
        return False

    @computed_field
    def num_of_dishes(self) -> int:
        return len(self.dishes)

    def sellable(self) -> bool: # 檢查飯盒內容是否可售
        """
        合格飯盒的條件
        1. 如無蒸魚，最少兩餸，最多4餸
        2. 如有蒸魚，最少兩餸，最多3餸
        3. 所有餸都在今天餐單上
        """
        if self.num_of_dishes > MAX_NO_OF_DISHES or self.num_of_dishes < MIN_NO_OF_DISHES:
            return False
        if self.has_fish() and self.num_of_dishes > MAX_NO_OF_FISH_DISHES:
            return False
        for d in self.dishes:
            if d not in self.menu:
                return False
        return True

    @computed_field
    def price(self) -> int:
        price: int = 0
        if not self.sellable():
            raise Exception('非法飯盒')
        if self.has_fish():
            return FISH_BASE_PRICE + (self.num_of_dishes-2)*PERDISH_PRICE
        #elif not self.has_fish():
        else:
            return BASE_PRICE + (self.num_of_dishes-2)*PERDISH_PRICE
                

# Importing data
if Path(DB_PATH).exists():
    engine = create_engine(SQLDB_PATH)
    print("DB已建立，跳過CSV")
else:
    engine = create_engine(SQLDB_PATH)
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

    # 把Dish儲存到SQLite
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(len(dish_by_wday)):
            for x in dish_by_wday[i]:
                session.add(Dish(name=pattern.sub('', x), wday=i))
            session.commit()

b = Bento()

app = FastAPI()

@app.get("/")
def get_root():
    return {"Greeting": "歡迎幫襯兩餸飯"}

@app.get("/today")
def get_today():
    return b.wday

@app.get("/menu")
def get_menu() -> List[str]:
    return b.menu

@app.get("/price")
def get_bento_price() -> int:
    try: 
        return b.price
    except Exception as e:
        return(str(e))

@app.post("/today/{today}")
def post_today(today: Annotated[int, Interval(ge=1, le=5)]) -> str:
    try:
        b.change_wday(today)
    except Exception as e:
        return(str(e))
    
@app.get("/dishes")
def get_dishes() -> List[str]:
    return b.dishes

@app.post("/dishes/add/{dish}")
def post_dishes_add(dish: str) -> str:
    try:
        b.add_dish(dish)
        return 'OK'
    except Exception as e:
        return (str(e))