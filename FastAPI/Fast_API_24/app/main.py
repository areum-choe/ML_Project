# 라우터를 main fastapi에 합치는 방법은 include_rounter를 이용

from fastapi import Depends, FastAPI
from app.dependencies import  get_token_header
import uvicorn as uvicorn
from app.routers import items, users


app = FastAPI(dependencies=[Depends(get_token_header)])

app.include_router(users.router)
app.include_router(items.router)
# app.include_router(
#     items.router, prefix="/items-1")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )