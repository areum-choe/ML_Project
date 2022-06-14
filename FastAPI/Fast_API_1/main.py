# todo path parameter

from fastapi import FastAPI
from enum import Enum

# FastAPI 와 APIRouter는 같은 역할을 하지만 APIRouter는 response_model, tag, summary 제공 해준다.(같은 가방인데 모양만 다른 느낌)
# 부장님 코드에는 APIRouter이걸 불러와서 처리함.
app=FastAPI()
# http://127.0.0.1:8000
# 라우터 형태 async 비동기
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 열거형 자료형
# 모델 형태
# ModelName 이라는 클래스 안에 (str, Enum)가 있는 이유는?
# str, Enum도 클래스 개념으로 ModelName이 str, Enum 이 두가지의 클래스를 상속하고 있다는 개념이다.
class ModelName(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# 라우터 형태태
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
# 터미널에 uvicorn main:app --reload


# from fastapi import APIRouter
#
# router=APIRouter()
#
# @router.get("/",tags=['areum'])
# async def root():
#     return {"message":"hello"}