
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_token_header

router = APIRouter(
    prefix="/items", # 라우터의 모든 path operation은 /items 로 시작
    tags=["items"], # 태그는 items안으로
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

# 위애서 tags와 response를 지정해줘도 또한번 추가로 tags와 reponse를 추가 가능
@router.put("/{item_id}",
    tags=["custom"], # put의 태그는 ["items", "custom"]
    responses={403: {"description": "Operation forbidden"}}, # eponse도 404와 403을 가지게 됨
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus")
    return {"item_id": item_id, "name": "The great Plumbus"}
