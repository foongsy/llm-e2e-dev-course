"""
# Venturenix Lab: Advanced Generative AI: End to end development with LLMs
### Lession 2: Introduction to Python (2)

Goal: Rewrite the data models of thisthisrice using SQLModel and store the data on sqlite
"""
# 匯入模組
import re
from typing import Annotated, List, Optional
from annotated_types import Interval
from pydantic import computed_field, ValidationError
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import func
from pathlib import Path
from fastapi import FastAPI, HTTPException

# 定義環境及"constant"
CSV_FILE = 'thisthisrice.csv'
DB_PATH = 'rice.db'
SQLDB_PATH = 'sqlite:///' + DB_PATH

# class Dish(BaseModel):
class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    wday: Annotated[int, Interval(ge=0, lt=6)] 
    
    @computed_field
    def is_meat(self) -> bool:
        _meat_keywords: List[str] = ['牛', '豬', '雞', '魚', '羊', '叉燒', '肉', '班腩', '鴨', '鵝']
        for m in _meat_keywords:
            if m in self.name:
                return(True)
        return(False)

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


app = FastAPI()

@app.get("/")
def read_root():
    return {"Greeting": "歡迎幫襯兩餸飯"}

@app.get("/menu/{wday}")
def read_item(wday: Annotated[int, Interval(ge=1, le=5)]) -> List[Dish]:
    weekday = int(wday) - 1
    statement = select(Dish).where(Dish.wday == weekday)
    with Session(engine) as session:
        dishes = session.exec(statement).all()
    return(dishes)