############################################################################################################
#todo Pydantic의 BaseModel import 하기
############################################################################################################
# Request Body : 클라이언트가 API로 데이터를 보낼때 사용되는 데이터
# Response Body : API가 request의 응답으로 클라이언트에게 보내는 데이터
# fast api에서는 request body를 만들기 위해선 Pydantic models 를 사용
# pydantic은 타입 애너테이션을 사용해서 데이터를 검증하고 설정들을 관리하는 라이브러리( 런타임 환경에서 타입을 강제하고 타입이 유효하지 않을 때 에러를 발생)

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn as uvicorn

# postman에서 post방식의 body를 raw의 json형태로
# http://127.0.0.1:4300/items
# requests body
# {
#     "name": "areum",
#     "description": "hi",
#     "price": "12.96",
#     "tax": 45
# }
class Item(BaseModel):
    name: str        #required값
    description: Optional[str] = None       # description은 str을 의미하고 반드시 필요한 것은 아니며, 기본값은 None값이라는 의미
    price: float
    tax: Optional[float] = None

app = FastAPI()

# 1
# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# 2
# @app.post("/items/")                    # post는 값을 넣어주는것
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:                          # 0이 아닌 다른 값이 있을때 True, 0이거나 값이 존재하지 않을 때 False !!
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# http://127.0.0.1:4300/docs

############################################################################################################
#todo Request body + path + query parameters
############################################################################################################
# items/{}?item_id=1&q=8000
# 3
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}   # ** 이거 의미 알아오기 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 딕셔너리 형태로 return 할 때
    if q:
        result.update({"q": q})
    return result
# http://127.0.0.1:4300/items/5432?q=8000
# Parameter가 Path에 정의되어 있으면 path로 해석한다
# path를 제외하고 sigular typ(int, float, bool str, etc)이면 query parameter로 해석한다
# Parameter가 Pydantic Model로 정의되어 있으면 Request Body로 해석한다


if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',
                    port=4300,
                    )