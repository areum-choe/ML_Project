# todo ch.8 Example Data 넣기
from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel , Field
import uvicorn as uvicorn
app = FastAPI()

#{
#    "name": "areum",
#    "description": "choi a reum",
#    "price": 35.4,
#    "tax": 3.2}

# 1 Example Data 넣기 (중첩클래스)
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#             }
#         }
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# http://127.0.0.1:4300/docs


# 2 example, examples in OpenAPI
# Field는 Model의 Field에 대한 추가적인 정보에 대해서 제공하는 것에 목적을 두고 있습니다.
# 추가적으로 한 가지 주의할 점은 Field는 class가 아니라 method 입니다. 그렇기 때문에 variable(변수)에 할당이 가능 합니다.

# example 없어도 되긴하지만 개발자나 사용자들이 볼때 어떠한것인지 알기 위해 작성 된것

# class Item(BaseModel):
#     name: str = Field(..., example="Foo")  # ...은 필수적으로 값이 들어가야한다는 의미
#     description: Optional[str] = Field(None, example="A very nice Item")
#     price: float = Field(..., example=35.4)
#     tax: Optional[float] = Field(None, example=3.2)
#
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# http://127.0.0.1:4300/items/342  -------postman
# http://127.0.0.1:4300/docs


# 3 examples 사용하기
# example을 여러개 사용하고 싶다면 examples를 사용 (dict형으로 작성)
# summary: example에 대한 간단한 설명이다
# description: example에 대한 긴 설명. 구두점 . 을 포함 할 수 있다.
# value: 실제 example 값을 담는곳


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",  #**글씨 진하게
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

# http://127.0.0.1:4300/docs

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',
                    port=4300,
                    )