# 초기 Pydantic 모델 / 스키마 생성하기
# Item와 UserBase를 만들고 이를 상속받아 ItemCreate와 UserCreate를 만든다.
from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass # class아래 한줄이라도 없으면 실행이 안됌. 임시로 형태만 만든것. (나중에 변형된 값이 들어갈 수 있으니깐 위에는 기본적인 base값만)

class Item(ItemBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

######################################################################################################

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True