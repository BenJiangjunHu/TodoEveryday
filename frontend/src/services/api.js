import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
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
  async getTodos(completed = null, page = 0, size = 10) {
    try {
      const params = { page, size };
      if (completed !== null) {
        params.completed = completed;
      }
      const response = await api.get('/todos', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 创建新的待办事项
  async createTodo(todoData) {
    try {
      const response = await api.post('/todos', todoData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 获取单个待办事项
  async getTodo(id) {
    try {
      const response = await api.get(`/todos/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 更新待办事项
  async updateTodo(id, updates) {
    try {
      const response = await api.put(`/todos/${id}`, updates);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 切换完成状态 (通过更新实现)
  async toggleTodo(id, currentStatus) {
    try {
      const response = await api.put(`/todos/${id}`, {
        isCompleted: !currentStatus
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 删除待办事项
  async deleteTodo(id) {
    try {
      const response = await api.delete(`/todos/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 批量删除
  async batchDelete(todoIds = []) {
    try {
      const response = await api.delete('/todos/batch', {
        data: { ids: todoIds }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // 批量更新状态
  async batchUpdateStatus(todoIds = [], completed) {
    try {
      const response = await api.patch('/todos/batch/status', {
        ids: todoIds,
        completed: completed
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default api;
