# todo [Fast API] Fast API 배우기 14부 - Form Data
#pip install python-multipart

from fastapi import FastAPI, Form #함수
import uvicorn as uvicorn

app = FastAPI()

# 폼필드란 양식 데이터 라고 한다.
# 양식을 채울때 입력한 세부 정보와 같이 양식 내분에 래핑하는 데이터를 보내는데 사용
# KEY-VALUE쌍으로 작성하여 전송
# 키/값 쌍의 폼 데이터를 보내는 것을 편리하게 제공하는게 form 기능
# json이 아닌 폼 필드로 전달되어 진다.
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )

