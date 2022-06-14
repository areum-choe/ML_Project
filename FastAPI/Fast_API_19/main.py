# CH.19 Dependency Injection
import uvicorn as uvicorn
from typing import Optional
from fastapi import Depends, FastAPI

# 1. Dependency Injection
# Dependency Injection이란 코드의 재활용을 위해 제공해주는 fastapi의 기능이다.
# 재활용될 dependency 코드를 작성한다.

# 의존성 주입 => 유지보수를 편하게 하기 위해
# app = FastAPI()
# async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}
#
# # common_parameters함수를 디팬던시로 불러왔으니 그 함수 내에 있는 파라미터 값이 넘어와 사용할 수 있는 것.
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons
#
# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons

# http://192.168.19.125:4300/users/
# http://192.168.19.125:4300/docs
# http://192.168.19.125:4300/users/?q=fdg

# 2. Class Dependency
# 함수처럼 사용이 가능하니 클래스도 가능
# app = FastAPI()
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
# class CommonQueryParams:
#     def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit
#
# @app.get("/items/")
# # : CommonQueryParams 없는것과 동일(.뒤에 자동완성 가능)
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):   # commons: CommonQueryParams = Depends() 이렇게 작성해도 됌
#     response = {}
#     if commons.q:          #q가 존재하면
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response

# 앞선 예제에서는 함수가 dict만 리턴해 주었다.
# 이를 사용할 때 q, skip, limit 같은 key값들은 ide에서 자동완성이 안되니 내가 수기로 입력해줘야 하는 불편함이 있다. (commons. 다음으로 자동완성 되는 것들)
# 허나 클래스로 디펜던시를 사용하면 key값을 내가 찾지 않아도 자동완성 된다.

# 3. Sub Dependency
# 디펜던시의 디펜던시를 만든다.
# from typing import Optional
# from fastapi import Cookie, Depends, FastAPI
#
# app = FastAPI()
#
# def query_extractor(q: Optional[str] = None):
#     return q
#
# def query_or_cookie_extractor(
#         q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
# ):
#     if not q:
#         return last_query
#     return q
#
# @app.get("/items/")
# async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
#     return {"q_or_cookie": query_or_default}

# http://192.168.19.125:4300/items?q=fd
# http://192.168.19.125:4300/items/

# 4. Path Operation Decorator's Dependency

# 만약에 디펜던시가 리턴하는 값이 필요하지 않고 실행은 꼭 해야한다면
# path operation decorator에 디펜던시를 달 수 있다.
# 사용방법은 데코레이터에 dependencies 파라미터에 Depends를 list형태로 넘겨준다.

# from fastapi import Depends, FastAPI, Header, HTTPException
#
# app = FastAPI()
#
# async def verify_token(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")
#
# async def verify_key(x_key: str = Header(...)):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key
#
# @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)]) # 여러 디팬던시를 사용해서 이렇게 작성한것!
# async def read_items():
#     return [{"item": "Foo"}, {"item": "Bar"}]

# 5. Global Dependency
from fastapi import Depends, FastAPI, Header, HTTPException

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# 전체에 dependency를 걸어주고 싶다면 global dependency를 이용하면 된다
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

@app.get("/items/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]

@app.get("/users/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

# 퍼포먼스(속도), 유지보수성 중요


if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )