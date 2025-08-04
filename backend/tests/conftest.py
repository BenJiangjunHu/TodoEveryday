import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app.database import Base, get_db
from app.main import app
from app.models import Todo

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

@pytest.fixture
def db_session():
    """Provide clean database session for each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_todo(db_session):
    """Provide a sample todo for testing"""
    todo = Todo(
        title="Sample Todo",
        description="Sample description",
        priority=2,
        due_date=datetime.now() + timedelta(days=7)
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

@pytest.fixture
def pending_todo(db_session):
    """Provide a pending (not completed) todo"""
    todo = Todo(
        title="Pending Todo",
        is_completed=False
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

@pytest.fixture
def completed_todo(db_session):
    """Provide a completed todo"""
    todo = Todo(
        title="Completed Todo",
        is_completed=True,
        completed_at=datetime.now()
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

@pytest.fixture
def multiple_todos(db_session):
    """Provide multiple todos for testing"""
    todos = []
    for i in range(5):
        todo = Todo(title=f"Todo {i}", priority=i % 3 + 1)
        todos.append(todo)
        db_session.add(todo)
    
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

@pytest.fixture
def mixed_status_todos(db_session):
    """Provide todos with mixed completion status"""
    todos = []
    
    # Create 3 completed todos
    for i in range(3):
        todo = Todo(
            title=f"Completed Todo {i}",
            is_completed=True,
            completed_at=datetime.now()
        )
        todos.append(todo)
        db_session.add(todo)
    
    # Create 3 pending todos
    for i in range(3):
        todo = Todo(
            title=f"Pending Todo {i}",
            is_completed=False
        )
        todos.append(todo)
        db_session.add(todo)
    
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

@pytest.fixture
def pending_todos(db_session):
    """Provide only pending todos"""
    todos = []
    for i in range(5):
        todo = Todo(
            title=f"Pending Todo {i}",
            is_completed=False
        )
        todos.append(todo)
        db_session.add(todo)
    
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

@pytest.fixture
def completed_todos(db_session):
    """Provide only completed todos"""
    todos = []
    for i in range(5):
        todo = Todo(
            title=f"Completed Todo {i}",
            is_completed=True,
            completed_at=datetime.now()
        )
        todos.append(todo)
        db_session.add(todo)
    
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

@pytest.fixture
def many_todos(db_session):
    """Provide many todos for pagination testing"""
    todos = []
    for i in range(20):
        todo = Todo(
            title=f"Todo {i}",
            priority=(i % 5) + 1,
            is_completed=i % 3 == 0  # Every 3rd todo is completed
        )
        todos.append(todo)
        db_session.add(todo)
    
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

@pytest.fixture
def many_completed_todos(db_session):
    """Provide many completed todos for performance testing"""
    todos = []
    for i in range(100):
        todo = Todo(
            title=f"Completed Todo {i}",
            is_completed=True,
            completed_at=datetime.now()
        )
        todos.append(todo)
        db_session.add(todo)
    
    db_session.commit()
    for todo in todos:
        db_session.refresh(todo)
    return todos

@pytest.fixture
def valid_todo_data():
    """Provide valid todo creation data"""
    return {
        "title": "Valid Todo",
        "description": "Valid description",
        "priority": 3,
        "due_date": datetime.now() + timedelta(days=7)
    }

@pytest.fixture
def minimal_todo_data():
    """Provide minimal todo creation data"""
    return {
        "title": "Minimal Todo"
    }

@pytest.fixture
def sample_todo_orm(db_session):
    """Provide sample todo ORM object for schema testing"""
    todo = Todo(
        title="ORM Todo",
        description="ORM description",
        priority=2,
        is_completed=False,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo
