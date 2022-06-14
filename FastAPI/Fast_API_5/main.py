from fastapi import FastAPI, Path, Query
import uvicorn as uvicorn
app = FastAPI()

# 숫자 제한하기
@app.get("/items/{item_id}")
async def read_items(
        *, item_id: int = Path(..., title="The ID of the item to get", ge=1), q: str):  # 앞에 *이 있으면
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# # 숫자 제한하기
# @app.get("/items/{item_id}")
# async def read_items(*,item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),q: str,):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get("/items/{item_id}")
# async def read_items(*,item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),q: str,
#                      size: float = Query(..., gt=0, lt=10.5)):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',
                    port=4300,
                    )