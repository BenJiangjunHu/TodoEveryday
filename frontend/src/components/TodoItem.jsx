import React, { useState } from 'react';

const TodoItem = ({ todo, onToggle, onDelete, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [editPriority, setEditPriority] = useState(todo.priority);

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getPriorityText = (priority) => {
    const priorityMap = {
      1: '低',
      2: '普通', 
      3: '中等',
      4: '高',
      5: '紧急'
    };
    return priorityMap[priority] || '普通';
  };

  const getPriorityColor = (priority) => {
    const colorMap = {
      1: '#28a745',
      2: '#17a2b8',
      3: '#ffc107',
      4: '#fd7e14',
      5: '#dc3545'
    };
    return colorMap[priority] || '#17a2b8';
  };

  const isOverdue = () => {
    if (!todo.due_date || todo.is_completed) return false;
    return new Date(todo.due_date) < new Date();
  };

  const handleSave = async () => {
    if (!editTitle.trim()) {
      alert('任务标题不能为空');
      return;
    }

    try {
      await onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim(),
        priority: parseInt(editPriority)
      });
      setIsEditing(false);
    } catch (error) {
      console.error('更新任务失败:', error);
      alert('更新任务失败，请重试');
    }
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditPriority(todo.priority);
    setIsEditing(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  if (isEditing) {
    return (
      <li className="todo-item editing fade-in">
        <div className="todo-content">
          <input
            type="text"
            className="form-control mb-2"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onKeyPress={handleKeyPress}
            autoFocus
          />
          <textarea
            className="form-control mb-2"
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            placeholder="任务描述（可选）..."
            rows="2"
            style={{ resize: 'vertical' }}
          />
          <select
            className="form-control mb-2"
            value={editPriority}
            onChange={(e) => setEditPriority(e.target.value)}
          >
            <option value={1}>低</option>
            <option value={2}>普通</option>
            <option value={3}>中等</option>
            <option value={4}>高</option>
            <option value={5}>紧急</option>
          </select>
        </div>
        <div className="todo-actions">
          <button className="btn btn-success btn-sm" onClick={handleSave}>
            ✓ 保存
          </button>
          <button className="btn btn-outline btn-sm" onClick={handleCancel}>
            ✕ 取消
          </button>
        </div>
      </li>
    );
  }

  return (
    <li className={`todo-item ${todo.is_completed ? 'completed' : ''} ${isOverdue() ? 'overdue' : ''} fade-in`}>
      <div className="todo-content">
        <div className="todo-header">
          <h4 className={`todo-title ${todo.is_completed ? 'completed-text' : ''}`}>
            {todo.title}
          </h4>
          <div className="todo-meta">
            <span 
              className="priority-badge" 
              style={{ backgroundColor: getPriorityColor(todo.priority) }}
            >
              {getPriorityText(todo.priority)}
            </span>
            {isOverdue() && (
              <span className="overdue-badge">已过期</span>
            )}
          </div>
        </div>
        
        {todo.description && (
          <p className={`todo-description ${todo.is_completed ? 'completed-text' : ''}`}>
            {todo.description}
          </p>
        )}
        
        <div className="todo-dates">
          <small className="text-muted">
            创建于: {formatDate(todo.created_at)}
          </small>
          {todo.due_date && (
            <small className="text-muted">
              截止: {formatDate(todo.due_date)}
            </small>
          )}
          {todo.completed_at && (
            <small className="text-muted">
              完成于: {formatDate(todo.completed_at)}
            </small>
          )}
        </div>
      </div>
      
      <div className="todo-actions">
        <button
          className={`btn btn-sm ${todo.is_completed ? 'btn-outline' : 'btn-success'}`}
          onClick={() => onToggle(todo.id)}
          title={todo.is_completed ? '标记为未完成' : '标记为完成'}
        >
          {todo.is_completed ? '↩️ 撤销' : '✅ 完成'}
        </button>
        
        <button
          className="btn btn-outline btn-sm"
          onClick={() => setIsEditing(true)}
          title="编辑任务"
        >
          ✏️ 编辑
        </button>
        
        <button
          className="btn btn-danger btn-sm"
          onClick={() => {
            if (window.confirm('确定要删除这个任务吗？')) {
              onDelete(todo.id);
            }
          }}
          title="删除任务"
        >
          🗑️ 删除
        </button>
      </div>
    </li>
  );
};

export default TodoItem;
