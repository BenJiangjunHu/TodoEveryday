# TodoEveryday 技术架构文档

## 项目概述

TodoEveryday 是一个现代化的待办事项管理应用，采用前后端分离架构，提供完整的任务管理功能。

## 技术栈

### 前端技术栈
- **框架**: React 18+
- **状态管理**: React Hooks (useState, useEffect)
- **HTTP客户端**: Axios
- **样式**: CSS3 + CSS Modules
- **构建工具**: Vite
- **包管理**: npm

### 后端技术栈
- **框架**: FastAPI
- **数据库**: SQLite
- **ORM**: SQLAlchemy
- **数据验证**: Pydantic
- **CORS**: FastAPI CORS中间件
- **文档**: OpenAPI (Swagger)

### 开发工具
- **代码格式化**: Prettier (前端), Black (后端)
- **代码检查**: ESLint (前端), Flake8 (后端)
- **版本控制**: Git

## 项目结构

```
TodoEveryday/
├── backend/                    # 后端目录
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI应用入口
│   │   ├── database.py        # 数据库配置
│   │   ├── models.py          # SQLAlchemy模型
│   │   ├── schemas.py         # Pydantic模式
│   │   ├── crud.py            # 数据库操作
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── todos.py       # 待办事项路由
│   ├── requirements.txt       # Python依赖
│   └── alembic/               # 数据库迁移
├── frontend/                  # 前端目录
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── TodoApp.jsx    # 主应用组件
│   │   │   ├── TodoForm.jsx   # 任务输入表单
│   │   │   ├── TodoList.jsx   # 任务列表
│   │   │   ├── TodoItem.jsx   # 单个任务项
│   │   │   └── TodoFilter.jsx # 过滤器组件
│   │   ├── services/
│   │   │   └── api.js         # API服务
│   │   ├── styles/
│   │   │   └── App.css        # 全局样式
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── README.md
└── ARCHITECTURE.md
```

## 数据库设计

### 表结构

```sql
-- 创建待办事项表
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME NULL,
    due_date DATETIME NULL
);

-- 创建索引以提高查询性能
CREATE INDEX idx_todos_is_completed ON todos(is_completed);
CREATE INDEX idx_todos_created_at ON todos(created_at);
CREATE INDEX idx_todos_due_date ON todos(due_date);

-- 创建触发器，自动更新 updated_at 字段
CREATE TRIGGER update_todos_updated_at 
    AFTER UPDATE ON todos
    FOR EACH ROW
    BEGIN
        UPDATE todos SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
```

### 字段说明

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

## API接口设计

### 基础配置
- **Base URL**: `http://localhost:8000/api/v1`
- **Content-Type**: `application/json`
- **响应格式**: JSON

### 接口列表

#### 1. 获取所有待办事项
```http
GET /api/v1/todos
```

**查询参数:**
- `status` (可选): `all` | `completed` | `pending` - 过滤状态
- `page` (可选): 页码，默认1
- `limit` (可选): 每页数量，默认10

**响应示例:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "title": "学习React",
            "description": "完成React基础教程",
            "is_completed": false,
            "priority": 2,
            "created_at": "2025-08-01T10:00:00Z",
            "updated_at": "2025-08-01T10:00:00Z",
            "completed_at": null,
            "due_date": "2025-08-15T23:59:59Z"
        }
    ],
    "total": 1,
    "page": 1,
    "limit": 10
}
```

#### 2. 创建新待办事项
```http
POST /api/v1/todos
```

**请求体:**
```json
{
    "title": "学习FastAPI",
    "description": "完成FastAPI项目开发",
    "priority": 3,
    "due_date": "2025-08-20T23:59:59Z"
}
```

**响应示例:**
```json
{
    "success": true,
    "data": {
        "id": 2,
        "title": "学习FastAPI",
        "description": "完成FastAPI项目开发",
        "is_completed": false,
        "priority": 3,
        "created_at": "2025-08-02T14:30:00Z",
        "updated_at": "2025-08-02T14:30:00Z",
        "completed_at": null,
        "due_date": "2025-08-20T23:59:59Z"
    }
}
```

#### 3. 更新待办事项
```http
PUT /api/v1/todos/{todo_id}
```

**请求体:**
```json
{
    "title": "学习FastAPI（已更新）",
    "description": "完成FastAPI项目开发和部署",
    "is_completed": true,
    "priority": 3
}
```

#### 4. 标记完成/取消完成
```http
PATCH /api/v1/todos/{todo_id}/toggle
```

**响应示例:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "is_completed": true,
        "completed_at": "2025-08-02T15:00:00Z"
    }
}
```

#### 5. 删除待办事项
```http
DELETE /api/v1/todos/{todo_id}
```

**响应示例:**
```json
{
    "success": true,
    "message": "Todo deleted successfully"
}
```

#### 6. 批量操作
```http
POST /api/v1/todos/batch
```

**请求体:**
```json
{
    "action": "delete_completed", // "delete_completed" | "delete_all" | "complete_all"
    "todo_ids": [1, 2, 3] // 可选，指定特定ID
}
```

#### 7. 获取统计信息
```http
GET /api/v1/todos/stats
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

### 错误响应格式

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Validation failed",
        "details": {
            "title": ["This field is required"]
        }
    }
}
```

### HTTP状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 500 | 服务器内部错误 |

## 前端组件设计

### 组件层次结构

```
TodoApp (主应用)
├── TodoForm (输入表单)
├── TodoFilter (过滤器)
├── TodoList (任务列表)
│   └── TodoItem (单个任务)
└── TodoStats (统计信息)
```

### 状态管理

```javascript
// 主要状态
const [todos, setTodos] = useState([]);
const [filter, setFilter] = useState('all'); // 'all', 'completed', 'pending'
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
```

### 核心功能函数

```javascript
// API调用函数
const fetchTodos = async (filter = 'all') => { /* ... */ };
const createTodo = async (todoData) => { /* ... */ };
const updateTodo = async (id, updates) => { /* ... */ };
const deleteTodo = async (id) => { /* ... */ };
const toggleTodo = async (id) => { /* ... */ };
const clearCompleted = async () => { /* ... */ };
const clearAll = async () => { /* ... */ };
```

## 样式设计规范

### CSS变量
```css
:root {
    --primary-color: #007bff;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --light-gray: #f8f9fa;
    --dark-gray: #6c757d;
    --border-radius: 8px;
    --box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}
```

### 响应式设计
- 移动端：< 768px
- 平板端：768px - 1024px
- 桌面端：> 1024px

## 部署方案

### 开发环境
1. 后端：`uvicorn app.main:app --reload --port 8000`
2. 前端：`npm run dev` (Vite开发服务器)

### 生产环境
1. 后端：Docker容器 + Nginx反向代理
2. 前端：静态文件部署到CDN
3. 数据库：SQLite文件挂载到持久化存储

### Docker配置

**后端Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**前端Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

## 安全考虑

1. **CORS配置**: 限制允许的源
2. **输入验证**: 前后端双重验证
3. **SQL注入防护**: 使用ORM参数化查询
4. **XSS防护**: React自动转义，后端验证
5. **API限流**: 防止恶意请求

## 性能优化

1. **前端优化**:
   - React.memo 减少不必要渲染
   - 虚拟滚动处理大量数据
   - 懒加载和代码分割

2. **后端优化**:
   - 数据库索引优化
   - API响应缓存
   - 分页查询

3. **网络优化**:
   - 静态资源CDN
   - HTTP/2支持
   - 资源压缩

## 测试策略

### 前端测试
- **单元测试**: Jest + React Testing Library
- **集成测试**: API接口测试
- **E2E测试**: Cypress

### 后端测试
- **单元测试**: pytest
- **API测试**: FastAPI TestClient
- **数据库测试**: SQLite内存数据库

## 监控和日志

1. **前端监控**: 错误追踪、性能监控
2. **后端监控**: API响应时间、错误率
3. **日志系统**: 结构化日志记录

## 扩展计划

1. **用户系统**: 用户注册、登录、个人空间
2. **分类标签**: 任务分类和标签功能
3. **团队协作**: 共享待办事项
4. **移动应用**: React Native版本
5. **离线支持**: PWA和离线缓存

---

*本文档将随项目发展持续更新*
