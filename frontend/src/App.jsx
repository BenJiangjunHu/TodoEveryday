import React, { useState, useEffect, useCallback } from 'react';
import TodoForm from './components/TodoForm';
import TodoFilter from './components/TodoFilter';
import TodoList from './components/TodoList';
import TodoActions from './components/TodoActions';
import { todoAPI } from './services/api';
import './styles/App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [filteredTodos, setFilteredTodos] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    pending: 0,
    overdue: 0
  });

  // 获取所有待办事项
  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await todoAPI.getTodos('all');
      
      if (response.success) {
        setTodos(response.data);
      } else {
        throw new Error(response.error?.message || '获取数据失败');
      }
    } catch (err) {
      console.error('获取待办事项失败:', err);
      setError(err.response?.data?.error?.message || err.message || '网络连接失败');
    } finally {
      setLoading(false);
    }
  }, []);

  // 获取统计信息
  const fetchStats = useCallback(async () => {
    try {
      const response = await todoAPI.getStats();
      if (response.success) {
        setStats(response.data);
      }
    } catch (err) {
      console.error('获取统计信息失败:', err);
    }
  }, []);

  // 过滤待办事项
  const filterTodos = useCallback((todosToFilter, currentFilter) => {
    let filtered = [...todosToFilter];
    
    switch (currentFilter) {
      case 'completed':
        filtered = todosToFilter.filter(todo => todo.isCompleted);
        break;
      case 'pending':
        filtered = todosToFilter.filter(todo => !todo.isCompleted);
        break;
      case 'all':
      default:
        // 显示全部，不需要过滤
        break;
    }
    
    // 按创建时间倒序排列，未完成的在前
    filtered.sort((a, b) => {
      if (a.isCompleted !== b.isCompleted) {
        return a.isCompleted ? 1 : -1;
      }
      return new Date(b.createdAt) - new Date(a.createdAt);
    });
    
    return filtered;
  }, []);

  // 初始化数据
  useEffect(() => {
    fetchTodos();
    fetchStats();
  }, [fetchTodos, fetchStats]);

  // 当todos或filter变化时更新过滤后的列表
  useEffect(() => {
    const filtered = filterTodos(todos, filter);
    setFilteredTodos(filtered);
  }, [todos, filter, filterTodos]);

  // 添加待办事项
  const handleAddTodo = async (todoData) => {
    try {
      setLoading(true);
      const response = await todoAPI.createTodo(todoData);
      
      if (response.success) {
        setTodos(prev => [response.data, ...prev]);
        await fetchStats();
      } else {
        throw new Error(response.error?.message || '添加失败');
      }
    } catch (err) {
      console.error('添加待办事项失败:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 切换完成状态
  const handleToggleTodo = async (id) => {
    try {
      const response = await todoAPI.toggleTodo(id);
      
      if (response.success) {
        setTodos(prev => prev.map(todo => 
          todo.id === id 
            ? { ...todo, ...response.data }
            : todo
        ));
        await fetchStats();
      } else {
        throw new Error(response.error?.message || '操作失败');
      }
    } catch (err) {
      console.error('切换状态失败:', err);
      alert('操作失败，请重试');
    }
  };

  // 更新待办事项
  const handleUpdateTodo = async (id, updates) => {
    try {
      const response = await todoAPI.updateTodo(id, updates);
      
      if (response.success) {
        setTodos(prev => prev.map(todo => 
          todo.id === id 
            ? { ...todo, ...response.data }
            : todo
        ));
        await fetchStats();
      } else {
        throw new Error(response.error?.message || '更新失败');
      }
    } catch (err) {
      console.error('更新待办事项失败:', err);
      throw err;
    }
  };

  // 删除待办事项
  const handleDeleteTodo = async (id) => {
    try {
      const response = await todoAPI.deleteTodo(id);
      
      if (response.success) {
        setTodos(prev => prev.filter(todo => todo.id !== id));
        await fetchStats();
      } else {
        throw new Error(response.error?.message || '删除失败');
      }
    } catch (err) {
      console.error('删除待办事项失败:', err);
      alert('删除失败，请重试');
    }
  };

  // 清除已完成
  const handleClearCompleted = async () => {
    try {
      setLoading(true);
      const response = await todoAPI.batchOperation('delete_completed');
      
      if (response.success) {
        setTodos(prev => prev.filter(todo => !todo.isCompleted));
        await fetchStats();
      } else {
        throw new Error(response.error?.message || '清除失败');
      }
    } catch (err) {
      console.error('清除已完成失败:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 清除全部
  const handleClearAll = async () => {
    try {
      setLoading(true);
      const response = await todoAPI.batchOperation('delete_all');
      
      if (response.success) {
        setTodos([]);
        await fetchStats();
      } else {
        throw new Error(response.error?.message || '清除失败');
      }
    } catch (err) {
      console.error('清除全部失败:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 刷新数据
  const handleRefresh = () => {
    fetchTodos();
    fetchStats();
  };

  return (
    <div className="container">
      <header className="text-center mb-4">
        <h1 style={{ 
          color: 'var(--primary-color)', 
          marginBottom: '8px',
          fontSize: '2.5rem',
          fontWeight: '700'
        }}>
          📝 TodoEveryday
        </h1>
        <p className="text-muted">
          每日待办事项管理 - 让生活更有条理
        </p>
        <button
          className="btn btn-outline btn-sm mt-2"
          onClick={handleRefresh}
          disabled={loading}
        >
          🔄 刷新
        </button>
      </header>

      <main>
        {/* 添加表单 */}
        <TodoForm 
          onAddTodo={handleAddTodo} 
          loading={loading}
        />

        {/* 过滤器和统计 */}
        <TodoFilter
          currentFilter={filter}
          onFilterChange={setFilter}
          stats={stats}
        />

        {/* 任务列表 */}
        <TodoList
          todos={filteredTodos}
          loading={loading}
          error={error}
          onToggle={handleToggleTodo}
          onDelete={handleDeleteTodo}
          onUpdate={handleUpdateTodo}
        />

        {/* 批量操作 */}
        <TodoActions
          onClearCompleted={handleClearCompleted}
          onClearAll={handleClearAll}
          stats={stats}
          loading={loading}
        />
      </main>

      <footer className="text-center mt-4">
        <p className="text-muted">
          © 2025 TodoEveryday - 基于 React + FastAPI 构建
        </p>
      </footer>
    </div>
  );
}

export default App;
