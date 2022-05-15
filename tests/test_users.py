from fastapi.testclient import TestClient
from app.main import app
from app import schemas

from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_qa'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



# def test_root():
#     res = client.get("/")
#     t= res.json().get('message')
#     assert t == 'Hello World'
#     assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"email": "user@gmail.com", "password": "password123"})
    #print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "user@gmail.com"
    assert res.status_code == 201
