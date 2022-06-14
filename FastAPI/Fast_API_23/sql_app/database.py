#todo 설정 클래스를 작성하는 공간
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlalchemy는?
# python에서 사용가능한 ORM(Object-relational maping)이다.
# ORM은 말그대로 객체(Object)와 관계(Relation)를 연결해주는것이다.
# 데이터베이스의 데이터를 <—매핑—> Object필드
# orm => 객체: 파이썬의 클래스 / 관계: 테이블

# sqlite 데이터베이스에다가 connecting. url 구조를 보면 현재 폴더에 있는 sql_app.db 파일을 여는거와 같다는걸 알 수 있다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# todo 2.  데이터베이스와의 연결
# create_engine 함수를 이용하여 데이터베이스와 연결을 맺는 '엔진' 을 만듭니다.
# connect_args={"check_same_thread": False} => 여기서 주목할점은 하기 세팅은 SQLite에서만 필요하고 다른 데이터베이스는 필요하지 않다
# SQLite라서 매우 간단하지만, 다른 DB라면 별도의 접속정보를 명기해야한다.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# sessionmaker는 sqlalchemy에서 제공하는 class로 session을 만들어 주는 factory
# ORM은 Entity(객체)를 DB Table에 맵핑하게 되는데 맵핑된 객체들을 지속적으로 관리해주는 역할을 하는 것이 Session
# autoflush  – 새로 생성된 Session객체에 사용할 autoflush 설정. (False=>버퍼가 가득 차면 예외발생 후 작업을 중지시키고 에러페이지 출력)
# autocommit  – 새로 생성된 Session객체에 사용할 자동 커밋 설정.
# => 클라이언트와 서버 연결
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# todo 3.  Mapping 매핑
# declarative_base() 함수를 이용하여 클래스 하나를 리턴받자.
# declarative_base( ) : 상속클래스들을 자동으로 인지하고 알아서 매핑해줌.
Base = declarative_base()