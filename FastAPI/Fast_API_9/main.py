# todo ch.9 [Fast API] Fast API 배우기 9부 - Extra Data Types
from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID
from fastapi import Body, FastAPI
import uvicorn as uvicorn


app = FastAPI()
# UUID(Universally Unique IDentifier)는 네트워크 상에서 고유성이 보장되는 id를 만들기 위한 표준 규약이다.
# UUID는 32개의 16진수로 구성되며, 5개의 그룹으로 표시되고 각 그룹은 하이픈으로 구분된다.

# UUID는 기본적으로 어떤 개체(데이터)를 고유하게 식별하는 데 사용되는 16바이트(128비트) 길이의 숫자
#ex) 022db29c-d0e2-11e5-bb4c-60f81dca7676

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
# http://127.0.0.1:4300/items/6a186ec9-695b-49b0-9359-d5c0f499a41a
if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='127.0.0.1',
                    port=4300,
                    )