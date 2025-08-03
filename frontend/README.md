# TodoEveryday Frontend

基于 React + Vite 构建的现代化待办事项管理前端应用。

## 🚀 功能特性

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
- 🔄 **实时更新**: 与后端API实时同步

## 🛠️ 技术栈

- **框架**: React 18.2
- **构建工具**: Vite 5.0
- **HTTP客户端**: Axios 1.6
- **样式**: 原生CSS3 + CSS变量
- **代码规范**: ESLint + React插件

## 📁 项目结构

```
frontend/
├── public/
│   └── index.html              # HTML模板
├── src/
│   ├── components/             # React组件
│   │   ├── TodoForm.jsx        # 任务输入表单
│   │   ├── TodoList.jsx        # 任务列表
│   │   ├── TodoItem.jsx        # 单个任务项
│   │   ├── TodoFilter.jsx      # 过滤器组件
│   │   └── TodoActions.jsx     # 批量操作组件
│   ├── services/
│   │   └── api.js              # API服务封装
│   ├── styles/
│   │   └── App.css             # 全局样式
│   ├── App.jsx                 # 主应用组件
│   └── main.jsx                # 应用入口
├── package.json                # 依赖配置
├── vite.config.js              # Vite配置
├── .eslintrc.json              # ESLint配置
└── README.md                   # 说明文档
```

## 🚦 快速开始

### 环境要求
- Node.js 16.0 或更高版本
- npm 或 yarn 包管理器
- 后端API服务运行在 http://localhost:8000

### 安装依赖
```bash
cd frontend
npm install
```

### 启动开发服务器
```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本
```bash
npm run build
```

### 预览生产版本
```bash
npm run preview
```

### 代码检查
```bash
npm run lint
```

## 🔧 配置说明

### API配置
API服务地址在 `src/services/api.js` 中配置：

```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

如需修改后端地址，请更新 `baseURL` 配置。

### 开发代理配置
Vite开发服务器已配置API代理，在 `vite.config.js` 中：

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

## 📱 组件说明

### TodoForm
任务输入表单组件，支持：
- 任务标题输入（必填）
- 任务描述输入（可选）
- 优先级选择（1-5级）
- 截止日期设置
- 实时验证和错误提示

### TodoList & TodoItem
任务列表和单项组件，功能包括：
- 任务信息展示（标题、描述、优先级、日期）
- 完成状态切换
- 就地编辑功能
- 删除确认
- 过期任务标记

### TodoFilter
过滤和统计组件，提供：
- 按状态过滤（全部、未完成、已完成）
- 实时统计信息展示
- 完成进度条
- 响应式计数器

### TodoActions
批量操作组件，支持：
- 清除所有已完成任务
- 清除全部任务
- 操作确认对话框
- 加载状态指示

## 🎨 样式系统

### CSS变量
使用CSS变量实现主题一致性：

```css
:root {
  --primary-color: #007bff;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --border-radius: 8px;
  --box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}
```

### 响应式设计
- 桌面端：> 768px，多列布局
- 移动端：≤ 768px，单列布局
- 小屏幕：≤ 480px，优化按钮和字体

### 动画效果
- 淡入动画：新增/更新任务
- 悬停效果：按钮和列表项
- 状态转换：完成/未完成切换
- 加载指示器：操作进行中

## 🔌 API集成

### 支持的API端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/v1/todos/` | 获取任务列表 |
| POST | `/api/v1/todos/` | 创建新任务 |
| PUT | `/api/v1/todos/{id}/` | 更新任务 |
| PATCH | `/api/v1/todos/{id}/toggle/` | 切换完成状态 |
| DELETE | `/api/v1/todos/{id}/` | 删除任务 |
| POST | `/api/v1/todos/batch/` | 批量操作 |
| GET | `/api/v1/todos/stats/` | 获取统计信息 |

### 错误处理
- 网络错误自动重试
- 用户友好的错误提示
- 控制台详细错误日志
- 操作失败回滚机制

## 🚀 性能优化

### 代码优化
- React.useCallback 减少不必要的重渲染
- 组件懒加载（可扩展）
- 事件处理防抖（可扩展）

### 网络优化
- Axios请求/响应拦截器
- API错误统一处理
- 加载状态管理

### 用户体验
- 实时UI反馈
- 操作确认对话框
- 加载动画和状态指示
- 键盘快捷键支持

## 🔧 开发指南

### 添加新组件
1. 在 `src/components/` 创建组件文件
2. 按照现有组件模式编写
3. 在 `App.jsx` 中导入使用
4. 添加相应样式到 `App.css`

### 修改样式
1. 优先使用CSS变量
2. 遵循响应式设计原则
3. 保持命名一致性
4. 添加适当的动画效果

### API扩展
1. 在 `services/api.js` 添加新的API方法
2. 更新相关组件调用
3. 处理错误和加载状态
4. 添加适当的用户反馈

## 🐛 故障排除

### 常见问题

**1. API连接失败**
- 检查后端服务是否运行在 http://localhost:8000
- 确认CORS设置是否正确
- 检查网络防火墙设置

**2. 样式显示异常**
- 清除浏览器缓存
- 检查CSS文件是否正确加载
- 确认浏览器兼容性

**3. 功能异常**
- 打开浏览器开发者工具查看错误
- 检查API响应状态
- 确认数据格式是否正确

### 调试技巧
- 使用React Developer Tools
- 查看Network面板的API请求
- 检查Console面板的错误信息
- 使用断点调试功能

## 📊 项目统计

- **组件数量**: 6个主要组件
- **API接口**: 7个RESTful端点
- **CSS样式**: 300+ 行响应式样式
- **功能特性**: 15+ 个核心功能

## 🤝 贡献指南

1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见LICENSE文件

---

**TodoEveryday Frontend** - 让每一天都更有条理 🚀
