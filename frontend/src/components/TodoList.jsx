import React from 'react';
import TodoItem from './TodoItem';

const TodoList = ({ todos, loading, error, onToggle, onDelete, onUpdate }) => {
  if (loading) {
    return (
      <div className="card">
        <div className="loading">
          <div className="spinner"></div>
          <span className="ml-2">加载中...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">
          ❌ {error}
        </div>
      </div>
    );
  }

  if (!todos || todos.length === 0) {
    return (
      <div className="card">
        <div className="empty-state">
          <h3>📝 暂无任务</h3>
          <p>添加你的第一个待办事项吧！</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="mb-3">待办列表 ({todos.length})</h3>
      <ul className="todo-list">
        {todos.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggle={onToggle}
            onDelete={onDelete}
            onUpdate={onUpdate}
          />
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
