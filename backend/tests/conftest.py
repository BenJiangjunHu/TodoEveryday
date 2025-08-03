import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建测试数据库表
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# 覆盖依赖
app.dependency_overrides[get_db] = override_get_db

# 创建测试客户端
client = TestClient(app)

@pytest.fixture
def test_client():
    return client

@pytest.fixture
def clean_db():
    """每个测试前清理数据库"""
    # 清理所有表
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # 测试后清理
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
