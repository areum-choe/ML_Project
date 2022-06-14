# CH.18 jsonable_encoder, PUT, PATCH
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder # 데이터 자료형을 json 호환가능한 데이터로 바꿔주는 함수
from pydantic import BaseModel
import uvicorn as uvicorn

# 1. jsonable_encoder
# 데이터 자료형을 json compatiable한 데이터로 바꿔주는 함수이다.
# 다른 파이썬 라이브러리를 사용할때 json 호환 데이터를 요구할 경우가 있다면 이 함수를 이용
# 가령 예를들면 데이터베이스는 Pydantic model을 받지 않고 dict만 받는 경우가 있다.
# 또는 datetime을 데이터베이스로 넘겨줄때 str로 바꿔주어야 한다.
# 이럴때 jsonable_encoder를 사용한다.

# fake_db = {}
#
# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     timestamp: Optional[str] = None
#
# app = FastAPI()
#
# @app.put("/items/{id}")
# def update_item(id: str, item: Item):
#     print(item)
#     json_compatible_item_data = jsonable_encoder(item)
#     print(json_compatible_item_data)
#     fake_db[id] = json_compatible_item_data
#     print(fake_db)

# 2. PUT operation
from typing import List, Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    print(item)
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    items[item_id] = update_item_encoded
    print(items)
    return update_item_encoded

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )