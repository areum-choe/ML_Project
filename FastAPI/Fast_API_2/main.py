############################################################################################################
#todo Query 파라미터
############################################################################################################
import uvicorn as uvicorn
from fastapi import FastAPI
from typing import Optional
app = FastAPI()
# 1
#
# # 딕셔너리 형태의 리스트를 만들어 줌
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# 함수 안에 들어간 skip, limit은 쿼리 파라미터
# skip: int = 0, limit: int = 10 값을 지정해 준 이유는 Default value로 /item까지만 작성해도 결과값이 자동으로 나온다.
# 만약 limit의 Default value가 1이면 위 item name은 Foo만 나오게 될것이다.

# http://127.0.0.1:4300/items/               -------return 값은 위 리스트 안 딕셔너리 값 다 나옴
# http://127.0.0.1:4300/items/?skip=0&limit=1 -------return 값은 위 리스트 안 딕셔너리 [0:1]까지 나옴
#
# ############################################################################################################
# #todo Optional 파라미터
# ############################################################################################################
# # typing 모듈의 Optional은 None이 허용되는 함수의 매개 변수에 대한 타입을 명시할 때 유용합니다.
# # 기본값이 정해지지 않은 파라미터에 사용하는 것이 적합함.
# # q값이 str일수도 None값일 수 도 있다는 의미.

# 2
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}
#
# # http://127.0.0.1:4300/items/dfs          -------return 값은 item_id
# # http://127.0.0.1:4300/items/dfs?q=dfds      -------return 값은 item_id, q
#
# ############################################################################################################
# #todo Query Parameter Type Conversion (타입 변환)
# ############################################################################################################
#
# 3
@app.get("/items/{item_id}")
# 불(bool) 자료형이란 참(True)과 거짓(False)을 나타내는 자료형. 불 자료형은 다음 2가지 값만을 가질 수 있다.

async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item
#
# # http://127.0.0.1:4300/items/dfs?short=true           ------리턴 값 > item_id
# # http://127.0.0.1:4300/items/dfs?q=dfds&short=True   ------리턴 값 > item_id, q
# # http://127.0.0.1:4300/items/dfs?q=dfds&short=False   ------리턴 값 > item_id, q, description
#
# ############################################################################################################
# #todo Multiple Path and Multiple Query Parameter
# ############################################################################################################
#
# 4
# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "This is an amazing item that has a long description"})
#     return item
#
# # http://127.0.0.1:4300/users/1234/items/tert?short=True       ------return 값 > item_id, owner_id
# # http://127.0.0.1:4300/users/1234/items/tert                  ------return 값 > item_id, owner_id, description
# # http://127.0.0.1:4300/users/1234/items/tert?q=ds&short=True  ------return 값 > item_id, owner_id,  q
# # http://127.0.0.1:4300/users/1234/items/tert?q=ds&short=False ------return 값 > item_id, owner_id,  q, description
#
# # uvicorn main:app --reload

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',   # 지정된 로컬호스트 ip
                    port=4300,
                    )

# if __name__ == '__main__':
#         uvicorn.run('main:app',
#                     host='192.168.19.125',
#                     port=4300,
#                     )