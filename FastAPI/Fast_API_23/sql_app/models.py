#todo 테이블 생성
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# 위 database의 Base를 가져와 상속
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # index 변수는 쿼리의 퍼포먼스를 올려주는데 사용 (서칭이 빠름)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner") # relationship 함수를 이용하여 데이터베이션 간 relation으로 연결이 가능

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id")) # 참조관계
    owner = relationship("User", back_populates="items") # back_populates => relation에서 연결된 부분에서 접근할시의 이름