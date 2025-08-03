# TodoEveryday - 全栈待办事项管理应用

一个现代化的全栈待办事项管理应用，采用 React + FastAPI + SQLite 技术栈构建。

## 🎯 项目概述

TodoEveryday 是一个功能完整的待办事项管理系统，提供直观的用户界面和强大的后端API支持。应用采用前后端分离架构，支持任务的创建、编辑、删除、完成状态切换、优先级设置、截止日期管理等核心功能。

## ✨ 主要特性

### 核心功能
- ✅ **任务管理**: 创建、编辑、删除、完成待办事项
- 🔍 **智能过滤**: 按状态筛选（全部、未完成、已完成）
- 📊 **实时统计**: 任务总数、完成度、进度展示
- 🗑️ **批量操作**: 清除已完成任务、清除全部任务
- 📱 **响应式设计**: 完美适配桌面端和移动端

### 高级功能
- 🎯 **优先级管理**: 5级优先级设置（低、普通、中等、高、紧急）
- ⏰ **截止日期**: 设置任务截止时间，过期任务自动标记
- 📝 **任务描述**: 支持详细的任务说明
- 🎨 **现代UI**: 优雅的设计和流畅的动画效果
- 🔄 **实时同步**: 前后端数据实时同步

## 🛠️ 技术栈

### 前端技术
- **框架**: React 18.2
- **构建工具**: Vite 7.0
- **HTTP客户端**: Axios 1.6
- **样式**: 原生CSS3 + CSS变量
- **代码规范**: ESLint

### 后端技术
- **框架**: FastAPI 0.115.4
- **数据库**: SQLite
- **ORM**: SQLAlchemy 2.0.36
- **数据验证**: Pydantic 2.9.2
- **API文档**: OpenAPI/Swagger

### 开发工具
- **版本控制**: Git
- **测试框架**: Pytest
- **API测试**: HTTPx
- **环境管理**: Python venv

## 📁 项目结构

```
TodoEveryday/
├── frontend/                   # React前端应用
│   ├── src/
│   │   ├── components/         # React组件
│   │   ├── services/           # API服务
│   │   ├── styles/             # 样式文件
│   │   ├── App.jsx             # 主应用组件
│   │   └── main.jsx            # 应用入口
│   ├── public/                 # 静态资源
│   ├── package.json            # 依赖配置
│   ├── vite.config.js          # Vite配置
│   └── README.md               # 前端文档
├── backend/                    # FastAPI后端API
│   ├── app/
│   │   ├── main.py             # FastAPI应用
│   │   ├── database.py         # 数据库配置
│   │   ├── models.py           # 数据模型
│   │   ├── schemas.py          # 数据验证
│   │   ├── crud.py             # 数据库操作
│   │   └── routes/             # API路由
│   ├── tests/                  # 测试用例
│   ├── requirements.txt        # Python依赖
│   └── README.md               # 后端文档
├── ARCHITECTURE.md             # 技术架构文档
└── README.md                   # 项目总文档
```

## 🚀 快速开始

### 环境要求
- **Node.js**: 16.0 或更高版本
- **Python**: 3.9 或更高版本
- **npm**: 或 yarn 包管理器

### 1. 克隆项目
```bash
git clone <repository-url>
cd TodoEveryday
```

### 2. 启动后端服务

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（可选）
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务器
python start_server.py
```

后端服务将在 http://localhost:8000 启动

### 3. 启动前端应用

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npx vite dev
```

前端应用将在 http://localhost:5174 启动

### 4. 访问应用

- **前端应用**: http://localhost:5174
- **API文档**: http://localhost:8000/docs
- **API健康检查**: http://localhost:8000/health

## 📖 使用指南

### 基本操作

1. **添加任务**
   - 在输入框中输入任务标题
   - 可选填写任务描述
   - 设置优先级（1-5级）
   - 可选设置截止日期
   - 点击"添加任务"按钮

2. **管理任务**
   - 点击"✅ 完成"按钮标记任务完成
   - 点击"✏️ 编辑"按钮修改任务信息
   - 点击"🗑️ 删除"按钮删除任务

3. **过滤任务**
   - 使用"全部"、"未完成"、"已完成"按钮过滤
   - 查看实时统计信息和完成进度

4. **批量操作**
   - 使用"清除已完成"清理完成的任务
   - 使用"清除全部"删除所有任务

### 高级功能

- **优先级颜色编码**: 不同优先级显示不同颜色标签
- **过期提醒**: 过期任务自动标记为红色
- **就地编辑**: 双击任务或点击编辑按钮进行修改
- **键盘快捷键**: Enter键快速提交，Escape键取消编辑

## 🔧 开发指南

### 前端开发

```bash
cd frontend

# 启动开发服务器
npx vite dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 代码检查
npm run lint
```

### 后端开发

```bash
cd backend

# 运行测试
pytest tests/ -v

# 启动开发服务器
python start_server.py

# API功能测试
python test_api.py

# 查看API文档
# 访问 http://localhost:8000/docs
```

## 📊 API文档

### 主要端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/todos/` | 获取任务列表 |
| POST | `/api/v1/todos/` | 创建新任务 |
| PUT | `/api/v1/todos/{id}/` | 更新任务 |
| PATCH | `/api/v1/todos/{id}/toggle/` | 切换完成状态 |
| DELETE | `/api/v1/todos/{id}/` | 删除任务 |
| POST | `/api/v1/todos/batch/` | 批量操作 |
| GET | `/api/v1/todos/stats/` | 获取统计信息 |
| GET | `/health` | 健康检查 |

详细API文档请访问：http://localhost:8000/docs

## 🎉 项目状态

**当前版本**: 1.0.0  
**开发状态**: ✅ 完成  
**部署状态**: 🟡 开发环境  

**TodoEveryday** - 让每一天都更有条理！ 🚀

- HTML5
- CSS3
- JavaScript (ES6+)
- Local Storage API for data persistence
