# todo auery 클래스

from typing import List, Optional
from fastapi import FastAPI, Query
import uvicorn as uvicorn

app = FastAPI()

# 1 q가 쿼리 파라미터이고 Optional인 상황이다 q의 기본값은 None값이므로 파라미터값을 지정해주지 않으면 else값으로 감
@app.get("/items/")
async def read_items(q: Optional[str] ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# http://127.0.0.1:4300/items/  ---return > results
# http://127.0.0.1:4300/items/?q=frr    ---return > results , q

# 2 Query 클래스 - max_length
#
# @app.get("/items/")
# # q의 default value로 Query 객체 / q는 기본적으로 None값을 가지므로 Optional / string의 최대 길이를 50으로 제한 / Query는 q에 대한 제약 조건을 거는
# async def read_items(q: Optional[str] = Query(None, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# 50 개 이상쓰면 에러 발생
# http://127.0.0.1:4300/items/?q=asd

# 3 Query 클래스 - min_length & max_length

# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# http://127.0.0.1:4300/items/?q=a ---limit_value 에러

# 4 Query 파미터를 정규식으로 제한하기
# regex 정규식 표현 Regular expressions
# ^ : 뒤에나오는 문자로 시작한다. 즉 q값은 무조건 fixedquery로 시작함
# $ : 정규식의 끝마침. 이 뒤로 문자가 올 수 없다

# @app.get("/items/")
# async def read_items(
#     q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# http://127.0.0.1:4300/items/?q=fixedquery

# 5 Default Value 값 지정하기

# @app.get("/items/")
# async def read_items(q: str = Query("fixedquery", min_length=3)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# http://127.0.0.1:4300/items/?q=fsd    -----------"q": "fsd"
# http://127.0.0.1:4300/items/       -----------"q": "fixedquery"

# 6 Query Parameter required로 만드는법

# @app.get("/items/")
# async def read_items(q: str = Query(..., min_length=3)):       # ... 이 required로 필수적으로 들어가야 하는 값
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# http://127.0.0.1:4300/items/     -------오류
# http://127.0.0.1:4300/items/?q=fsfdds        ------q값이 나옴

# 7 List Value를 Query 파라미터로 사용하기

# @app.get("/items/")
# async def read_items(q: Optional[List[str]] = Query(None)):
#     query_items = {"q": q}
#     return query_items

# http://localhost:4300/items/?q=foo&q=bar       ----리스트 안에 foo, bar가 들어가 있음.
# http://localhost:4300/items/                   ----q=null

# 8 List Value를 Default Value로

# @app.get("/items/")
# async def read_items(q: List[str] = Query(["foo", "bar"])):                 #List[str] 와 List[]똑같음
#     query_items = {"q": q}
#     return query_items

# http://localhost:4300/items/    ---"foo", "bar" 나옴

# 9 Metadata 추가하기

# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(None, title="Query string",
#         description="Query string for the items to search in the database that have a good match",
#         min_length=3,)):
#
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

#http://localhost:4300/docs

# 10 Alias Parameter, 별명 파라미터 (에일리어스는 가명이란 뜻으로 변수=객체일때, 객체의 변수라는 가명)           ------- 더 공부하기

# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(None, alias="item-query")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bㅇar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# http://127.0.0.1:4300/items/?item-query=dfsfsd

# Deprecated 표시하기
# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(
#             None,
#             alias="item-query",         # - 기호는 못쓰게 되있는데 alias덕분에 쓸 수 있는 것이다.  그래서 alias를 사용함으로써 사용자가 더 유용하게 쓸 수 있도록 하는 것
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             min_length=3,
#             max_length=50,
#             regex="^fixedquery$",
#             deprecated=True,)):                  ############################################ deprecated
#
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',
                    port=4300,
                    )