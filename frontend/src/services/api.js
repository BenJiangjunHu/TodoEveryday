import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// 待办事项API接口
export const todoAPI = {
  // 获取所有待办事项
  async getTodos(status = 'all', page = 1, limit = 100) {
    try {
      const response = await api.get('/todos/', {
        params: { status, page, limit }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 创建新的待办事项
  async createTodo(todoData) {
    try {
      const response = await api.post('/todos/', todoData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新待办事项
  async updateTodo(id, updates) {
    try {
      const response = await api.put(`/todos/${id}/`, updates);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 切换完成状态
  async toggleTodo(id) {
    try {
      const response = await api.patch(`/todos/${id}/toggle/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 删除待办事项
  async deleteTodo(id) {
    try {
      const response = await api.delete(`/todos/${id}/`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 批量操作
  async batchOperation(action, todoIds = []) {
    try {
      const response = await api.post('/todos/batch/', {
        action,
        todo_ids: todoIds
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取统计信息
  async getStats() {
    try {
      const response = await api.get('/todos/stats/');
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default api;
