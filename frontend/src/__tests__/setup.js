import '@testing-library/jest-dom'
import { expect, afterEach, beforeAll, afterAll, vi } from 'vitest'
import { cleanup } from '@testing-library/react'

// Setup MSW
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

// Mock handlers for API endpoints
export const handlers = [
  // GET /api/v1/todos
  http.get('http://localhost:8000/api/v1/todos', () => {
    return HttpResponse.json({
      success: true,
      data: [
        {
          id: 1,
          title: 'Test Todo 1',
          description: 'Test description 1',
          is_completed: false,
          priority: 1,
          due_date: null,
          created_at: '2024-01-01T10:00:00Z',
          updated_at: '2024-01-01T10:00:00Z',
          completed_at: null
        },
        {
          id: 2,
          title: 'Test Todo 2',
          description: 'Test description 2',
          is_completed: true,
          priority: 3,
          due_date: '2024-12-31T23:59:59Z',
          created_at: '2024-01-01T11:00:00Z',
          updated_at: '2024-01-01T12:00:00Z',
          completed_at: '2024-01-01T12:00:00Z'
        }
      ],
      total: 2,
      page: 1,
      limit: 10
    })
  }),

  // POST /api/v1/todos
  http.post('http://localhost:8000/api/v1/todos', async ({ request }) => {
    const body = await request.json()
    return HttpResponse.json({
      success: true,
      data: {
        id: 3,
        title: body.title,
        description: body.description || null,
        is_completed: false,
        priority: body.priority || 1,
        due_date: body.due_date || null,
        created_at: '2024-01-01T13:00:00Z',
        updated_at: '2024-01-01T13:00:00Z',
        completed_at: null
      }
    }, { status: 201 })
  }),

  // PUT /api/v1/todos/:id
  http.put('http://localhost:8000/api/v1/todos/:id', async ({ params, request }) => {
    const body = await request.json()
    return HttpResponse.json({
      success: true,
      data: {
        id: parseInt(params.id),
        title: body.title || 'Updated Todo',
        description: body.description || null,
        is_completed: body.is_completed !== undefined ? body.is_completed : false,
        priority: body.priority || 1,
        due_date: body.due_date || null,
        created_at: '2024-01-01T10:00:00Z',
        updated_at: '2024-01-01T14:00:00Z',
        completed_at: body.is_completed ? '2024-01-01T14:00:00Z' : null
      }
    })
  }),

  // PATCH /api/v1/todos/:id/toggle
  http.patch('http://localhost:8000/api/v1/todos/:id/toggle', ({ params }) => {
    return HttpResponse.json({
      success: true,
      data: {
        id: parseInt(params.id),
        title: 'Toggled Todo',
        description: null,
        is_completed: true,
        priority: 1,
        due_date: null,
        created_at: '2024-01-01T10:00:00Z',
        updated_at: '2024-01-01T15:00:00Z',
        completed_at: '2024-01-01T15:00:00Z'
      }
    })
  }),

  // DELETE /api/v1/todos/:id
  http.delete('http://localhost:8000/api/v1/todos/:id', () => {
    return HttpResponse.json({
      success: true,
      message: 'Todo deleted successfully'
    })
  })
]

export const server = setupServer(...handlers)

// Setup and teardown
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterAll(() => server.close())
afterEach(() => {
  server.resetHandlers()
  cleanup()
})

// Mock console methods to reduce test noise
global.console = {
  ...console,
  // Uncomment to ignore specific console methods
  // log: vi.fn(),
  // warn: vi.fn(),
  // error: vi.fn(),
}

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))

// Mock localStorage
Object.defineProperty(window, 'localStorage', {
  value: {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
    length: 0,
    key: vi.fn(),
  },
  writable: true,
})

// Mock sessionStorage
Object.defineProperty(window, 'sessionStorage', {
  value: {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
    length: 0,
    key: vi.fn(),
  },
  writable: true,
})
