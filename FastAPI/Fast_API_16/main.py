#todo [Fast API] Fast API 배우기 16부 - Handling Errors

from fastapi import FastAPI, HTTPException , Request
from fastapi.responses import JSONResponse
import uvicorn as uvicorn


app = FastAPI()

# 1. HTTP Exception
# items = {"foo": "The Foo Wrestlers"}
#
# # raise- 일부러 에러를 발생시켜야 하는 경우
# # 사용하는 클라이언트에 오류가 있는 HTTP 응답을 반환하려면 HTTPException.
# # “status_code”에는 HTTP status를 넣는대 200, 204, 404, 500 등이 이용된다.
# # “detail”에는 관련된 응답 메시지를 넣는다.
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": items[item_id]}  #item[foo] > The Foo Wrestlers

# http://192.168.19.125:4300/items/foo
# #http://192.168.19.125:4300/items/bar


# 2. 커스텀 Exception 만들기
# # 맨아래 있는 app.get방식이 main > 여기서 class를 호출해서 > exception_handler를 발생시켜서 리턴값을 content로 줌
#
# # 사용자 예외 클래스 객체를 만든다.
# class UnicornException(Exception):
#     def __init__(self, name: str):  # 초기화 매서드
#         self.name = name
#
# # 예외 핸들러를 만들고 우리 클래스 객체에 전달한다. handler를 등록
# #  @ExceptionHandler라는 어노테이션을 이용하여 Exception Handling을 할 수 있다.
# @app.exception_handler(UnicornException)  # UnicornException예외가 발생하면 아래 함수가 실행되도록 실행해라.
# async def unicorn_exception_handler(request: Request, exception: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exception.name} did something. There goes a rainbow..."},
#     )
#
# @app.get("/unicorns/{name}")
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)   # name이 yolo이면 발생.
#     return {"unicorn_name": name}

# http://192.168.19.125:4300/unicorns/yolo --정상실행

# 3. Default Exception handler 오버라이드 하기
# from fastapi import FastAPI, HTTPException
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
#
# # 이 핸들러는 예외를 오버라이드(위로 덮어쓰기)하고 JSON 대신에 평문을 돌려준다.
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}

# 4. RequestValidationError Body
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# RequestValidationError는 body 속성을 가지고 있다. body는 에러가 난 데이터를 가지고 있다.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),)

class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item

# 5. FastAPI의 exception handler 재활용 하기

from fastapi import FastAPI, HTTPException

from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")               #3일때

    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")    #str일때

    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )
