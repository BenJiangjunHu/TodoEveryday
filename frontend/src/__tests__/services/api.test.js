/**
 * Unit tests for API service
 * Tests HTTP client, error handling, and data transformation
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { http, HttpResponse } from 'msw'
import { server } from '../setup.js'
import { todoAPI } from '../../services/api.js'

describe('API Service', () => {
  describe('todoAPI.getTodos', () => {
    it('should fetch todos with default parameters', async () => {
      const result = await todoAPI.getTodos()
      
      expect(result).toEqual({
        success: true,
        data: expect.any(Array),
        total: 2,
        page: 1,
        limit: 10
      })
      expect(result.data).toHaveLength(2)
      expect(result.data[0]).toHaveProperty('id')
      expect(result.data[0]).toHaveProperty('title')
      expect(result.data[0]).toHaveProperty('is_completed')
    })

    it('should fetch todos with custom parameters', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos', ({ request }) => {
          const url = new URL(request.url)
          const status = url.searchParams.get('status')
          const page = url.searchParams.get('page')
          const limit = url.searchParams.get('limit')
          
          expect(status).toBe('completed')
          expect(page).toBe('2')
          expect(limit).toBe('5')
          
          return HttpResponse.json({
            success: true,
            data: [],
            total: 0,
            page: 2,
            limit: 5
          })
        })
      )

      const result = await todoAPI.getTodos('completed', 2, 5)
      expect(result.page).toBe(2)
      expect(result.limit).toBe(5)
    })

    it('should handle API errors properly', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos', () => {
          return HttpResponse.json(
            { success: false, message: 'Server error' },
            { status: 500 }
          )
        })
      )

      await expect(todoAPI.getTodos()).rejects.toThrow()
    })

    it('should handle network errors', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos', () => {
          return HttpResponse.error()
        })
      )

      await expect(todoAPI.getTodos()).rejects.toThrow()
    })
  })

  describe('todoAPI.createTodo', () => {
    it('should create a new todo successfully', async () => {
      const todoData = {
        title: 'New Todo',
        description: 'New description',
        priority: 3
      }

      const result = await todoAPI.createTodo(todoData)
      
      expect(result).toEqual({
        success: true,
        data: expect.objectContaining({
          id: expect.any(Number),
          title: 'New Todo',
          description: 'New description',
          priority: 3,
          is_completed: false
        })
      })
    })

    it('should create todo with minimal data', async () => {
      const todoData = { title: 'Minimal Todo' }

      const result = await todoAPI.createTodo(todoData)
      
      expect(result.data.title).toBe('Minimal Todo')
      expect(result.data.description).toBeNull()
      expect(result.data.priority).toBe(1)
    })

    it('should handle validation errors', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/todos', () => {
          return HttpResponse.json(
            { 
              success: false, 
              detail: [{ loc: ['title'], msg: 'field required', type: 'value_error.missing' }]
            },
            { status: 422 }
          )
        })
      )

      await expect(todoAPI.createTodo({})).rejects.toThrow()
    })

    it('should send correct request format', async () => {
      let requestBody = null
      
      server.use(
        http.post('http://localhost:8000/api/v1/todos', async ({ request }) => {
          requestBody = await request.json()
          return HttpResponse.json({
            success: true,
            data: { id: 1, ...requestBody, is_completed: false }
          }, { status: 201 })
        })
      )

      const todoData = {
        title: 'Test Todo',
        description: 'Test description',
        priority: 2,
        due_date: '2024-12-31T23:59:59Z'
      }

      await todoAPI.createTodo(todoData)
      expect(requestBody).toEqual(todoData)
    })
  })

  describe('todoAPI.updateTodo', () => {
    it('should update todo successfully', async () => {
      const updates = {
        title: 'Updated Title',
        description: 'Updated description',
        priority: 4
      }

      const result = await todoAPI.updateTodo(1, updates)
      
      expect(result).toEqual({
        success: true,
        data: expect.objectContaining({
          id: 1,
          title: 'Updated Title',
          description: 'Updated description',
          priority: 4
        })
      })
    })

    it('should update only specified fields', async () => {
      const updates = { title: 'Only Title Updated' }

      const result = await todoAPI.updateTodo(1, updates)
      
      expect(result.data.title).toBe('Only Title Updated')
    })

    it('should handle non-existent todo', async () => {
      server.use(
        http.put('http://localhost:8000/api/v1/todos/999', () => {
          return HttpResponse.json(
            { success: false, message: 'Todo not found' },
            { status: 404 }
          )
        })
      )

      await expect(todoAPI.updateTodo(999, { title: 'Test' })).rejects.toThrow()
    })

    it('should send PUT request to correct endpoint', async () => {
      let requestUrl = null
      
      server.use(
        http.put('http://localhost:8000/api/v1/todos/:id', ({ request, params }) => {
          requestUrl = request.url
          expect(params.id).toBe('42')
          return HttpResponse.json({
            success: true,
            data: { id: 42, title: 'Updated' }
          })
        })
      )

      await todoAPI.updateTodo(42, { title: 'Updated' })
      expect(requestUrl).toContain('/todos/42/')
    })
  })

  describe('todoAPI.toggleTodo', () => {
    it('should toggle todo completion status', async () => {
      const result = await todoAPI.toggleTodo(1)
      
      expect(result).toEqual({
        success: true,
        data: expect.objectContaining({
          id: 1,
          is_completed: true,
          completed_at: expect.any(String)
        })
      })
    })

    it('should handle toggle for non-existent todo', async () => {
      server.use(
        http.patch('http://localhost:8000/api/v1/todos/999/toggle', () => {
          return HttpResponse.json(
            { success: false, message: 'Todo not found' },
            { status: 404 }
          )
        })
      )

      await expect(todoAPI.toggleTodo(999)).rejects.toThrow()
    })

    it('should send PATCH request to correct endpoint', async () => {
      let requestUrl = null
      
      server.use(
        http.patch('http://localhost:8000/api/v1/todos/:id/toggle', ({ request, params }) => {
          requestUrl = request.url
          expect(params.id).toBe('123')
          return HttpResponse.json({
            success: true,
            data: { id: 123, is_completed: true }
          })
        })
      )

      await todoAPI.toggleTodo(123)
      expect(requestUrl).toContain('/todos/123/toggle')
    })
  })

  describe('todoAPI.deleteTodo', () => {
    it('should delete todo successfully', async () => {
      const result = await todoAPI.deleteTodo(1)
      
      expect(result).toEqual({
        success: true,
        message: 'Todo deleted successfully'
      })
    })

    it('should handle deletion of non-existent todo', async () => {
      server.use(
        http.delete('http://localhost:8000/api/v1/todos/999', () => {
          return HttpResponse.json(
            { success: false, message: 'Todo not found' },
            { status: 404 }
          )
        })
      )

      await expect(todoAPI.deleteTodo(999)).rejects.toThrow()
    })

    it('should send DELETE request to correct endpoint', async () => {
      let requestUrl = null
      
      server.use(
        http.delete('http://localhost:8000/api/v1/todos/:id', ({ request, params }) => {
          requestUrl = request.url
          expect(params.id).toBe('456')
          return HttpResponse.json({
            success: true,
            message: 'Todo deleted successfully'
          })
        })
      )

      await todoAPI.deleteTodo(456)
      expect(requestUrl).toContain('/todos/456/')
    })
  })

  describe('todoAPI.batchOperation', () => {
    it('should perform batch operations successfully', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/todos/batch', async ({ request }) => {
          const body = await request.json()
          expect(body).toEqual({
            action: 'delete',
            todo_ids: [1, 2, 3]
          })
          
          return HttpResponse.json({
            success: true,
            message: 'Batch operation completed',
            processed: 3
          })
        })
      )

      const result = await todoAPI.batchOperation('delete', [1, 2, 3])
      
      expect(result).toEqual({
        success: true,
        message: 'Batch operation completed',
        processed: 3
      })
    })

    it('should handle batch operation with empty todo list', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/todos/batch', async ({ request }) => {
          const body = await request.json()
          expect(body.todo_ids).toEqual([])
          
          return HttpResponse.json({
            success: true,
            message: 'No todos to process',
            processed: 0
          })
        })
      )

      const result = await todoAPI.batchOperation('complete', [])
      expect(result.processed).toBe(0)
    })

    it('should handle invalid batch action', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/todos/batch', () => {
          return HttpResponse.json(
            { success: false, message: 'Invalid action' },
            { status: 400 }
          )
        })
      )

      await expect(todoAPI.batchOperation('invalid_action', [1])).rejects.toThrow()
    })
  })

  describe('todoAPI.getStats', () => {
    it('should fetch todo statistics', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos/stats', () => {
          return HttpResponse.json({
            success: true,
            data: {
              total: 10,
              completed: 6,
              pending: 4,
              overdue: 1,
              today: 2
            }
          })
        })
      )

      const result = await todoAPI.getStats()
      
      expect(result).toEqual({
        success: true,
        data: expect.objectContaining({
          total: 10,
          completed: 6,
          pending: 4,
          overdue: 1,
          today: 2
        })
      })
    })

    it('should handle stats API errors', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos/stats', () => {
          return HttpResponse.json(
            { success: false, message: 'Stats unavailable' },
            { status: 503 }
          )
        })
      )

      await expect(todoAPI.getStats()).rejects.toThrow()
    })
  })

  describe('Error Handling', () => {
    it('should handle timeout errors', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos', () => {
          // Simulate timeout - in real tests this would require network configuration
          return HttpResponse.json(
            { success: false, message: 'Request timeout' },
            { status: 408 }
          )
        })
      )

      await expect(todoAPI.getTodos()).rejects.toThrow()
    })

    it('should handle malformed JSON responses', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos', () => {
          return new Response('Invalid JSON{', {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          })
        })
      )

      await expect(todoAPI.getTodos()).rejects.toThrow()
    })

    it('should handle CORS errors', async () => {
      server.use(
        http.get('http://localhost:8000/api/v1/todos', () => {
          return HttpResponse.json(
            { success: false, message: 'CORS error' },
            { status: 0 }
          )
        })
      )

      await expect(todoAPI.getTodos()).rejects.toThrow()
    })
  })

  describe('Request/Response Interceptors', () => {
    it('should log requests and responses', async () => {
      const consoleSpy = vi.spyOn(console, 'log')
      
      await todoAPI.getTodos()
      
      expect(consoleSpy).toHaveBeenCalledWith(
        'API Request:',
        'GET',
        '/todos/'
      )
      expect(consoleSpy).toHaveBeenCalledWith(
        'API Response:',
        200,
        expect.any(Object)
      )
      
      consoleSpy.mockRestore()
    })

    it('should log API errors', async () => {
      const consoleErrorSpy = vi.spyOn(console, 'error')
      
      server.use(
        http.get('http://localhost:8000/api/v1/todos', () => {
          return HttpResponse.json(
            { success: false, message: 'Test error' },
            { status: 400 }
          )
        })
      )

      try {
        await todoAPI.getTodos()
      } catch (error) {
        // Expected error
      }
      
      expect(consoleErrorSpy).toHaveBeenCalledWith(
        'API Error:',
        expect.objectContaining({
          success: false,
          message: 'Test error'
        })
      )
      
      consoleErrorSpy.mockRestore()
    })
  })

  describe('Data Validation', () => {
    it('should validate required fields in createTodo', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/todos', async ({ request }) => {
          const body = await request.json()
          
          if (!body.title) {
            return HttpResponse.json(
              { 
                success: false, 
                detail: [{ loc: ['title'], msg: 'field required' }]
              },
              { status: 422 }
            )
          }
          
          return HttpResponse.json({
            success: true,
            data: { id: 1, ...body }
          }, { status: 201 })
        })
      )

      await expect(todoAPI.createTodo({})).rejects.toThrow()
      
      // Should succeed with title
      const result = await todoAPI.createTodo({ title: 'Valid Todo' })
      expect(result.success).toBe(true)
    })

    it('should handle invalid data types', async () => {
      server.use(
        http.post('http://localhost:8000/api/v1/todos', async ({ request }) => {
          const body = await request.json()
          
          if (typeof body.priority !== 'number') {
            return HttpResponse.json(
              { 
                success: false, 
                detail: [{ loc: ['priority'], msg: 'value is not a valid integer' }]
              },
              { status: 422 }
            )
          }
          
          return HttpResponse.json({
            success: true,
            data: { id: 1, ...body }
          }, { status: 201 })
        })
      )

      await expect(todoAPI.createTodo({ 
        title: 'Test', 
        priority: 'invalid' 
      })).rejects.toThrow()
    })
  })
})
