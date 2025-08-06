import React, { useState } from 'react';

const TodoForm = ({ onAddTodo, loading }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState(1);
  const [dueDate, setDueDate] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim()) {
      alert('请输入任务标题');
      return;
    }

    const todoData = {
      title: title.trim(),
      description: description.trim(),
      priority: parseInt(priority),
      dueDate: dueDate || null
    };

    try {
      await onAddTodo(todoData);
      // 清空表单
      setTitle('');
      setDescription('');
      setPriority(1);
      setDueDate('');
    } catch (error) {
      console.error('添加任务失败:', error);
      alert('添加任务失败，请重试');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="card">
      <h2 className="mb-3">添加新任务</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            className="form-control"
            placeholder="输入任务标题..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
            autoFocus
          />
        </div>
        
        <div className="form-group">
          <textarea
            className="form-control"
            placeholder="任务描述（可选）..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={loading}
            rows="3"
            style={{ resize: 'vertical' }}
          />
        </div>

        <div className="d-flex gap-3 mb-3">
          <div className="form-group mb-0" style={{ flex: 1 }}>
            <label htmlFor="priority" style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: '500' }}>
              优先级
            </label>
            <select
              id="priority"
              className="form-control"
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              disabled={loading}
            >
              <option value={1}>低</option>
              <option value={2}>普通</option>
              <option value={3}>中等</option>
              <option value={4}>高</option>
              <option value={5}>紧急</option>
            </select>
          </div>
          
          <div className="form-group mb-0" style={{ flex: 1 }}>
            <label htmlFor="dueDate" style={{ display: 'block', marginBottom: '4px', fontSize: '14px', fontWeight: '500' }}>
              截止日期
            </label>
            <input
              id="dueDate"
              type="datetime-local"
              className="form-control"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              disabled={loading}
            />
          </div>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !title.trim()}
        >
          {loading ? (
            <>
              <span className="spinner" style={{ width: '16px', height: '16px', marginRight: '8px' }}></span>
              添加中...
            </>
          ) : (
            <>
              <span>➕</span>
              添加任务
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default TodoForm;
