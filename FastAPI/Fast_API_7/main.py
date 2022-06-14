# todo [Fast API] Fast API 배우기 7부 - Feild 클래스
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
import uvicorn as uvicorn

app = FastAPI()

# Field 클래스
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero") #  ...은 required
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results



if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',
                    port=4300,
                    )