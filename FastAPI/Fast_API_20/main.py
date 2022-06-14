# CH.20 Security, authentication 인증 시스템
import uvicorn as uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

# 토큰 = 아이디, 패스워드는 보안상으로 위험성이 있음(해킹) ex)식권(여러 사이트에 접속이 가능하도록 해줌)
# 보안상 유효기간이 존재

# OAuth2PasswordBearer = Bearer 토큰 을 사용하여 비밀번호 흐름 과 함께 OAuth2 를 사용
# Bearer 토큰은 일반적으로 인증 서버에 의해 생성 된 일종의 불투명 한 값입니다.
# 액세스 토큰은 수명이 짧습니다 (1 시간 정도). Bearer 토큰을 사용하여 새 액세스 토큰을 얻습니다.

# 1. FastAPI's OAuth2PasswordBearer

# app = FastAPI()
#
# # OAuth2란 인증 및 권한 부여를 처리하는 여러 방법을 정의하는 사양입
# # OAuth2PasswordBearer 객체를 생성할때 tokenUrl이라는 파라미터를 넘겨준다.
# # 이 파라미터는 프론트엔드에서 유저가 token값(유저가 입력한 아이디 비번) 을 얻어 올 때 사용된다.
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# # # API는 username과 password를 확인한뒤 reponse로 token을 넘겨준다
# # # token이란 단순한 string이며 유저를 확인하기 위해 사용
# # # 프론트엔드에서는 이 token을 어디다가 저장한다
# # # 로그인 하는거 테스트하는 툴이다.
# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}
# http://192.168.19.125:4300/docs

# 2. OAuth2 password flow and Bearer 예제
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# 인증 정보를 받고 로그인을 위해 경로 함수
from pydantic import BaseModel

# 유저 정보를 담은 db생성
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

# 패스워드 해싱을 사용
# 도난당한 데이터베이스에 실제 패스워드가 있다면 해커가 그걸보고 유저 계정을 로그인하여 해킹할수 있겠지만
# 만약 해싱된 패스워드를 본다면 해킹이 불가능!! 우리가 패스워드 앞에 fakehashed이걸 써놨기 때문에
# hashed_password의 앞부문은 일치 뒷부분만 다름
def fake_hash_password(password: str):
    return "fakehashed" + password

# oauth2_scheme 에 토큰값 유저 아이디 비번 정보를 담아오기
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# db안에 유저 네임이 있으면 UserInDB에서 그에 해당하는 hashed_password를 리턴해줌
# 입력은 username 이지만 위에 5개의 정보를 다 가져온다. (get_user유저이름가져온다.)
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# get_user 안에 유저 정보를 가져옴
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

# 디팬던시로 토큰값을 지니고 있는 oauth2_scheme를 가져옴
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user") # alice 엘레스 에러 발생
    return current_user

# OAuth2PasswordRequestForm 클래스를 인스턴스로
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    # fake database에서 username이 있는지 확인하자. 만약 error가 날 시 HTTPException을 일으킨다.
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

# 유저가 acitve인 상태에서만 current_user를 리턴하고 아니면 에러
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user



if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )


# 이 매개변수에는 클라이언트(사용자의 브라우저에서 실행되는 프런트엔드)가 토큰을 받기 위해 아이디 비번 전송에 사용할 URL이 포함