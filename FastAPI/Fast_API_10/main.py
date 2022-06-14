#todo Cookie 파라미터, Header 파라미터
import uvicorn as uvicorn
from typing import Optional
from fastapi import Cookie, FastAPI, Header
app = FastAPI()

#Cookie? Header?

# 1. Cookie 파라미터
# 쿠키는 클라이언트 단에 저장되는 작은 정보의 단위이다.
# 클라이언트에서 생성하고 저장된다. 서버에서 전송한 쿠키가 클라이언트에 저장될 수 있다.
# 서버에서 쿠키 객체를 생성한 후, 응답과 함께 클라이언트의 브라우저로 전송되어, 사용자의 컴퓨터에 서버별로 저장된다.
# 저장된 쿠키는 다시 해당하는 웹 페이지에 접속할 때(서버한테 다시 요청 보낼 때) 브라우저에서 서버로 전송된다.
# 쿠키는 이름(name)과 값(value) 쌍으로 정보를 저장한다. (단순한 문자열로 된 데이터다.)
# (이름-값 쌍 외에도 도메인, 경로, 유효기간, 보안, HttpOnly 속성을 저장할 수 있다.)
# 쿠키의 이름은 알파벳과 숫자로만 구성이 된다.
# 쿠키 값을 한글로 저장하고 싶다면 인코딩, 디코딩 과정이 필요하다.

@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

# http://192.168.19:4300/items/    ---"ads_id": null

# 2. Header 파라미터
# Cookie의 "자매"클래스입니다.
# Header에서 특별한 점은 대문자를 자동으로 소문자화 하고, 하이픈(-)을 자동으로 언더바(_)로 변환한다
# Request Header에는 headers-test 처럼 헤더명이 -으로 이어져있다. 하지만 이는 파이썬에서는 허용되지 않은 변수 이름이며,
# Fast API는 이를 _로 snake case로 자동으로 변환을 해준다.


# @app.get("/headers/")
# def headers(headers_test: Optional[str] = Header(None)):
#     return {"headers_test": headers_test}
# http://192.168.19.125:4300/items/

# 3.Automatic Conversion
# 하지만 자동 변환을 비활성화 하려면 convert_underscorres를 false로 지정해주면 됩니다.

# @app.get("/items/")
# async def read_items(
#     strange_header: Optional[str] = Header(None, convert_underscores=False)):
#     return {"strange_header": strange_header}


if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )