# CH.17 Path Operation Configuration

from typing import Optional, Set
from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn as uvicorn

app = FastAPI()

# 1. status_code
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
# # response_model 은  docs에서 example예시를 보여준다.
# # docs에서 status_code없으면 에러 코드가 200이다.
#
# @app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED) # docs에서 status_code없으면 에러 코드가 200이다.
# async def create_item(item: Item):
#     return item

# 2. tags
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
# #  tags 를 통해 docs에서 분류되는 것을 알 수 있음.
# @app.post("/items/", response_model=Item, tags=["items"])
# async def create_item(item: Item):
#     return item
#
# @app.get("/items/", tags=["itemss"])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]
#
#
# @app.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "johndoe"}]
#
# # http://192.168.19.125:4300/docs

# 3. summary & description

# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
# @app.post(
#     "/items/",
#     response_model=Item,
#     summary="Create an item",
#     description="Create an item with all the information, name, description, price, tax and a set of unique tags",
# )
# async def create_item(item: Item):
#     return item

# 4. Docs에 description 추가하기

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []

# 주석을 길게 하고 싶으면 """ 을 달아주면 된다.
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )