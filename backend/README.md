# TodoEveryday Backend

TodoEveryday 后端 API 服务，基于 FastAPI 构建的现代化待办事项管理系统。

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: SQLite
- **ORM**: SQLAlchemy 2.0.23
- **数据验证**: Pydantic 2.5.0
- **ASGI服务器**: Uvicorn
- **测试**: Pytest

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI应用入口
│   ├── database.py       # 数据库配置
│   ├── models.py         # SQLAlchemy模型
│   ├── schemas.py        # Pydantic模式
│   ├── crud.py           # 数据库操作
│   └── routes/
│       ├── __init__.py
│       └── todos.py      # 待办事项路由
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # 测试配置
│   └── test_todos.py     # API测试
├── requirements.txt      # 依赖包列表
├── run.py               # 启动脚本
├── init_db.py           # 数据库初始化脚本
└── README.md            # 本文档
```

## 快速开始

### 1. 环境准备

确保已安装 Python 3.9 或更高版本：

```bash
python --version
```

### 2. 安装依赖

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
# 初始化数据库
python init_db.py

# 如需重置数据库
python init_db.py reset
```

### 4. 启动服务

```bash
# 方式1：使用启动脚本（推荐）
python run.py

# 方式2：直接使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问服务

- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## API 接口

### 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **Content-Type**: `application/json`
- **响应格式**: JSON

### 接口列表

#### 1. 获取待办事项列表

```http
GET /api/v1/todos
```

**查询参数:**
- `status`: 过滤状态 (`all` | `completed` | `pending`)
- `page`: 页码，默认1
- `limit`: 每页数量，默认10

**示例请求:**
```bash
curl "http://localhost:8000/api/v1/todos?status=all&page=1&limit=10"
```

**响应示例:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "title": "学习FastAPI",
            "description": "完成FastAPI基础教程",
            "is_completed": false,
            "priority": 2,
            "created_at": "2025-08-02T10:00:00Z",
            "updated_at": "2025-08-02T10:00:00Z",
            "completed_at": null,
            "due_date": "2025-08-15T23:59:59Z"
        }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
}
```

#### 2. 创建待办事项

```http
POST /api/v1/todos
```

**请求体:**
```json
{
    "title": "新任务",
    "description": "任务描述",
    "priority": 2,
    "due_date": "2025-08-20T23:59:59Z"
}
```

**示例请求:**
```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "学习React",
    "description": "完成React基础项目",
    "priority": 3
  }'
```

#### 3. 更新待办事项

```http
PUT /api/v1/todos/{todo_id}
```

**示例请求:**
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新后的任务标题",
    "is_completed": true
  }'
```

#### 4. 切换完成状态

```http
PATCH /api/v1/todos/{todo_id}/toggle
```

**示例请求:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/todos/1/toggle"
```

#### 5. 删除待办事项

```http
DELETE /api/v1/todos/{todo_id}
```

**示例请求:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1"
```

#### 6. 批量操作

```http
POST /api/v1/todos/batch
```

**请求体:**
```json
{
    "action": "delete_completed"
}
```

**支持的操作:**
- `delete_completed`: 删除所有已完成的待办事项
- `delete_all`: 删除所有待办事项
- `complete_all`: 完成所有未完成的待办事项

**示例请求:**
```bash
curl -X POST "http://localhost:8000/api/v1/todos/batch" \
  -H "Content-Type: application/json" \
  -d '{"action": "delete_completed"}'
```

#### 7. 获取统计信息

```http
GET /api/v1/todos/stats/
```

**示例请求:**
```bash
curl "http://localhost:8000/api/v1/todos/stats/"
```

**响应示例:**
```json
{
    "success": true,
    "data": {
        "total": 10,
        "completed": 4,
        "pending": 6,
        "overdue": 2
    }
}
```

## 测试

### 运行所有测试

```bash
# 在backend目录下运行
pytest

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=app
```

### 运行特定测试

```bash
# 运行特定测试文件
pytest tests/test_todos.py

# 运行特定测试函数
pytest tests/test_todos.py::test_create_todo

# 运行包含特定关键词的测试
pytest -k "test_create"
```

### 测试覆盖的功能

- ✅ 创建待办事项
- ✅ 获取待办事项列表
- ✅ 获取单个待办事项
- ✅ 更新待办事项
- ✅ 切换完成状态
- ✅ 删除待办事项
- ✅ 状态过滤
- ✅ 分页功能
- ✅ 批量操作
- ✅ 统计信息
- ✅ 数据验证
- ✅ 错误处理

## 数据库模型

### Todo 模型

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INTEGER | 主键ID | PRIMARY KEY, AUTOINCREMENT |
| title | VARCHAR(255) | 任务标题 | NOT NULL |
| description | TEXT | 任务描述 | 可选 |
| is_completed | BOOLEAN | 是否完成 | NOT NULL, DEFAULT FALSE |
| priority | INTEGER | 优先级(1-5) | DEFAULT 1 |
| created_at | DATETIME | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | 更新时间 | DEFAULT CURRENT_TIMESTAMP |
| completed_at | DATETIME | 完成时间 | NULL |
| due_date | DATETIME | 截止日期 | NULL |

## 配置

### 环境变量

可以通过环境变量配置以下选项：

- `DATABASE_URL`: 数据库连接URL（默认: `sqlite:///./todos.db`）
- `DEBUG`: 调试模式（默认: `False`）
- `LOG_LEVEL`: 日志级别（默认: `INFO`）

### CORS 配置

默认允许的前端地址：
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 部署

### 开发环境

```bash
# 使用默认配置启动
python run.py

# 或使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境

```bash
# 使用Gunicorn（需要安装gunicorn）
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用uvicorn（生产模式）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
# 构建镜像
docker build -t todoeveryday-backend .

# 运行容器
docker run -p 8000:8000 todoeveryday-backend
```

## 开发指南

### 代码风格

- 使用 Black 格式化代码
- 使用 isort 排序导入
- 遵循 PEP 8 规范

```bash
# 格式化代码
black app/ tests/

# 排序导入
isort app/ tests/

# 检查代码质量
flake8 app/ tests/
```

### 添加新功能

1. 在 `models.py` 中定义数据模型
2. 在 `schemas.py` 中定义 Pydantic 模式
3. 在 `crud.py` 中实现数据库操作
4. 在 `routes/` 中添加 API 路由
5. 在 `tests/` 中添加测试用例

### 数据库迁移

如果需要修改数据库结构，建议使用 Alembic：

```bash
# 安装Alembic
pip install alembic

# 初始化迁移
alembic init alembic

# 创建迁移文件
alembic revision --autogenerate -m "添加新字段"

# 应用迁移
alembic upgrade head
```

## 故障排除

### 常见问题

1. **端口占用错误**
   ```bash
   # 查找占用端口的进程
   netstat -ano | findstr :8000
   # 或在Linux/macOS上
   lsof -i :8000
   ```

2. **数据库锁定错误**
   ```bash
   # 删除数据库文件重新初始化
   rm todos.db
   python init_db.py
   ```

3. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   # 清理缓存
   pip cache purge
   ```

### 日志查看

应用日志会输出到控制台，包含以下信息：
- API 请求和响应
- 数据库操作
- 错误信息和堆栈跟踪

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请创建 Issue 或联系维护者。

---

**更新日期**: 2025-08-02  
**版本**: 1.0.0
