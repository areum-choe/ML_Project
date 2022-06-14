# todo 데이터베이스와 소통하는 함수를 만들
from sqlalchemy.orm import Session #이 Session을 통해 db라는 파라미터를 만들고 데이터베이스와 소통할 수 있다.
from sql_app import models, schemas

# TODO Read data
# ID와 email로 한명의 유저 정보를 읽는 함수
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 여러 유저 정보를 읽는 함수
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 여러 아이템을 읽는 함수
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# TODO Read data
# 데이터베이스에 데이터를 만드는 함수를 만들기

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password) # SQLAlchemy model 객체를 만든다
    db.add(db_user) # 만든 객체를 add 함수를 이용하여 데이터베이스에 추가한다.
    db.commit() # commit 함수를 이용해 데이터베이스에 반영한다.
    db.refresh(db_user) # refresh 함수를 이용해 데이터베이스의 데이터를 최신으로 갱신한다.
    return db_user

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item