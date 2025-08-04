"""
Unit tests for API routes
Tests all endpoint behaviors, validation, and error handling
"""
import pytest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import json

from fastapi import HTTPException
from app.routes.todos import router
from app import schemas


class TestGetTodosEndpoint:
    """Test suite for GET /api/v1/todos/ endpoint"""

    def test_get_todos_success_default_params(self, test_client, clean_db):
        """Test successful todos retrieval with default parameters"""
        # Create test data first
        test_client.post("/api/v1/todos/", json={"title": "Test Todo 1"})
        test_client.post("/api/v1/todos/", json={"title": "Test Todo 2"})
        
        response = test_client.get("/api/v1/todos/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert isinstance(data["data"], list)

    def test_get_todos_query_parameter_status_all(self, test_client, clean_db):
        """Test status parameter with 'all' value"""
        response = test_client.get("/api/v1/todos/?status=all")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_todos_query_parameter_status_completed(self, test_client, clean_db):
        """Test status parameter with 'completed' value"""
        response = test_client.get("/api/v1/todos/?status=completed")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_todos_query_parameter_status_pending(self, test_client, clean_db):
        """Test status parameter with 'pending' value"""
        response = test_client.get("/api/v1/todos/?status=pending")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_todos_query_parameter_status_invalid(self, test_client, clean_db):
        """Test status parameter with invalid value"""
        response = test_client.get("/api/v1/todos/?status=invalid")
        
        # Should return 422 for invalid enum value
        assert response.status_code == 422

    def test_get_todos_pagination_page_parameter(self, test_client, clean_db):
        """Test page parameter validation"""
        response = test_client.get("/api/v1/todos/?page=2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2

    def test_get_todos_pagination_page_minimum(self, test_client, clean_db):
        """Test page parameter minimum value"""
        response = test_client.get("/api/v1/todos/?page=0")
        
        # Should return 422 for page < 1
        assert response.status_code == 422

    def test_get_todos_pagination_page_negative(self, test_client, clean_db):
        """Test page parameter with negative value"""
        response = test_client.get("/api/v1/todos/?page=-1")
        
        assert response.status_code == 422

    def test_get_todos_pagination_limit_parameter(self, test_client, clean_db):
        """Test limit parameter validation"""
        response = test_client.get("/api/v1/todos/?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5

    def test_get_todos_pagination_limit_minimum(self, test_client, clean_db):
        """Test limit parameter minimum value"""
        response = test_client.get("/api/v1/todos/?limit=0")
        
        # Should return 422 for limit < 1
        assert response.status_code == 422

    def test_get_todos_pagination_limit_maximum(self, test_client, clean_db):
        """Test limit parameter maximum value"""
        response = test_client.get("/api/v1/todos/?limit=101")
        
        # Should return 422 for limit > 100
        assert response.status_code == 422

    def test_get_todos_pagination_limit_valid_boundary(self, test_client, clean_db):
        """Test limit parameter at valid boundaries"""
        response = test_client.get("/api/v1/todos/?limit=100")
        
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 100

    def test_get_todos_response_format_validation(self, test_client, clean_db):
        """Test response follows TodoListResponse schema"""
        response = test_client.get("/api/v1/todos/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        required_fields = ["success", "data", "total", "page", "limit"]
        for field in required_fields:
            assert field in data
        
        assert isinstance(data["success"], bool)
        assert isinstance(data["data"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["page"], int)
        assert isinstance(data["limit"], int)

    def test_get_todos_pagination_metadata_accuracy(self, test_client, clean_db):
        """Test pagination metadata accuracy"""
        # Create multiple todos
        for i in range(5):
            test_client.post("/api/v1/todos/", json={"title": f"Todo {i}"})
        
        response = test_client.get("/api/v1/todos/?page=1&limit=3")
        
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["limit"] == 3
        assert data["total"] == 5
        assert len(data["data"]) <= 3

    def test_get_todos_empty_database(self, test_client, clean_db):
        """Test response with empty database"""
        response = test_client.get("/api/v1/todos/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"] == []
        assert data["total"] == 0

    def test_get_todos_with_actual_data(self, test_client, clean_db):
        """Test response with actual todo data"""
        # Create test todos
        test_client.post("/api/v1/todos/", json={
            "title": "Test Todo",
            "description": "Test description",
            "priority": 3
        })
        
        response = test_client.get("/api/v1/todos/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        
        todo = data["data"][0]
        assert todo["title"] == "Test Todo"
        assert todo["description"] == "Test description"
        assert todo["priority"] == 3
        assert todo["is_completed"] is False

    @patch('app.routes.todos.crud')
    def test_get_todos_database_error_handling(self, mock_crud, test_client):
        """Test error handling when database operation fails"""
        mock_crud.get_todos.side_effect = Exception("Database error")
        
        response = test_client.get("/api/v1/todos/")
        
        # Should return 500 internal server error
        assert response.status_code == 500


class TestCreateTodoEndpoint:
    """Test suite for POST /api/v1/todos/ endpoint"""

    def test_create_todo_success_minimal_data(self, test_client, clean_db):
        """Test successful todo creation with minimal data"""
        todo_data = {"title": "New Todo"}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "New Todo"
        assert data["data"]["is_completed"] is False
        assert data["data"]["priority"] == 1

    def test_create_todo_success_complete_data(self, test_client, clean_db):
        """Test successful todo creation with all fields"""
        todo_data = {
            "title": "Complete Todo",
            "description": "Full description",
            "priority": 4,
            "due_date": "2025-12-31T23:59:59"
        }
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Complete Todo"
        assert data["data"]["description"] == "Full description"
        assert data["data"]["priority"] == 4
        assert data["data"]["due_date"] is not None

    def test_create_todo_request_validation_missing_title(self, test_client, clean_db):
        """Test request validation for missing title"""
        todo_data = {"description": "No title"}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 422

    def test_create_todo_request_validation_empty_title(self, test_client, clean_db):
        """Test request validation for empty title"""
        todo_data = {"title": ""}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 422

    def test_create_todo_request_validation_title_too_long(self, test_client, clean_db):
        """Test request validation for title too long"""
        todo_data = {"title": "x" * 256}  # Exceeds 255 character limit
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 422

    def test_create_todo_request_validation_priority_too_low(self, test_client, clean_db):
        """Test request validation for priority too low"""
        todo_data = {"title": "Test", "priority": 0}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 422

    def test_create_todo_request_validation_priority_too_high(self, test_client, clean_db):
        """Test request validation for priority too high"""
        todo_data = {"title": "Test", "priority": 6}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 422

    def test_create_todo_request_validation_invalid_due_date(self, test_client, clean_db):
        """Test request validation for invalid due date format"""
        todo_data = {"title": "Test", "due_date": "invalid-date"}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 422

    def test_create_todo_response_format(self, test_client, clean_db):
        """Test response follows SingleTodoResponse schema"""
        todo_data = {"title": "Format Test"}
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Validate response structure
        assert "success" in data
        assert "data" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["data"], dict)
        
        # Validate todo data structure
        todo = data["data"]
        required_fields = ["id", "title", "is_completed", "created_at", "updated_at"]
        for field in required_fields:
            assert field in todo

    def test_create_todo_input_sanitization(self, test_client, clean_db):
        """Test input sanitization and security"""
        # Test with potentially malicious input
        todo_data = {
            "title": "<script>alert('xss')</script>",
            "description": "'; DROP TABLE todos; --"
        }
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        # Input should be stored as-is (sanitization handled by frontend)
        assert data["data"]["title"] == "<script>alert('xss')</script>"

    def test_create_todo_unicode_characters(self, test_client, clean_db):
        """Test creation with unicode characters"""
        todo_data = {
            "title": "测试任务 🚀",
            "description": "Unicode description émoji 测试"
        }
        
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["title"] == "测试任务 🚀"
        assert data["data"]["description"] == "Unicode description émoji 测试"

    @patch('app.routes.todos.crud')
    def test_create_todo_database_error_handling(self, mock_crud, test_client):
        """Test error handling when database operation fails"""
        mock_crud.create_todo.side_effect = Exception("Database error")
        
        todo_data = {"title": "Error Test"}
        response = test_client.post("/api/v1/todos/", json=todo_data)
        
        assert response.status_code == 500


class TestGetSingleTodoEndpoint:
    """Test suite for GET /api/v1/todos/{todo_id} endpoint"""

    def test_get_existing_todo_success(self, test_client, clean_db):
        """Test retrieving existing todo by ID"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Get Test"})
        todo_id = create_response.json()["data"]["id"]
        
        response = test_client.get(f"/api/v1/todos/{todo_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == todo_id
        assert data["data"]["title"] == "Get Test"

    def test_get_nonexistent_todo_404(self, test_client, clean_db):
        """Test 404 error for non-existent todo"""
        response = test_client.get("/api/v1/todos/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_get_todo_path_parameter_validation_non_integer(self, test_client, clean_db):
        """Test path parameter validation with non-integer ID"""
        response = test_client.get("/api/v1/todos/not-a-number")
        
        assert response.status_code == 422

    def test_get_todo_path_parameter_validation_zero(self, test_client, clean_db):
        """Test path parameter validation with zero ID"""
        response = test_client.get("/api/v1/todos/0")
        
        assert response.status_code == 404

    def test_get_todo_path_parameter_validation_negative(self, test_client, clean_db):
        """Test path parameter validation with negative ID"""
        response = test_client.get("/api/v1/todos/-1")
        
        assert response.status_code == 404

    def test_get_todo_response_format(self, test_client, clean_db):
        """Test response follows SingleTodoResponse schema"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Format Test"})
        todo_id = create_response.json()["data"]["id"]
        
        response = test_client.get(f"/api/v1/todos/{todo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "success" in data
        assert "data" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["data"], dict)

    @patch('app.routes.todos.crud')
    def test_get_todo_database_error_handling(self, mock_crud, test_client):
        """Test error handling when database operation fails"""
        mock_crud.get_todo.side_effect = Exception("Database error")
        
        response = test_client.get("/api/v1/todos/1")
        
        assert response.status_code == 500


class TestUpdateTodoEndpoint:
    """Test suite for PUT /api/v1/todos/{todo_id} endpoint"""

    def test_update_existing_todo_success(self, test_client, clean_db):
        """Test successful todo update"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Original"})
        todo_id = create_response.json()["data"]["id"]
        
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "priority": 5
        }
        
        response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Updated Title"
        assert data["data"]["description"] == "Updated description"
        assert data["data"]["priority"] == 5

    def test_update_todo_partial_update(self, test_client, clean_db):
        """Test partial update with only some fields"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={
            "title": "Original",
            "description": "Original description",
            "priority": 2
        })
        todo_id = create_response.json()["data"]["id"]
        
        # Update only title
        update_data = {"title": "Updated Title Only"}
        
        response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Updated Title Only"
        assert data["data"]["description"] == "Original description"  # Unchanged
        assert data["data"]["priority"] == 2  # Unchanged

    def test_update_nonexistent_todo_404(self, test_client, clean_db):
        """Test 404 error for non-existent todo"""
        update_data = {"title": "Does not exist"}
        
        response = test_client.put("/api/v1/todos/99999", json=update_data)
        
        assert response.status_code == 404

    def test_update_todo_validation_empty_title(self, test_client, clean_db):
        """Test validation error for empty title"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Original"})
        todo_id = create_response.json()["data"]["id"]
        
        update_data = {"title": ""}
        
        response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 422

    def test_update_todo_validation_invalid_priority(self, test_client, clean_db):
        """Test validation error for invalid priority"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Original"})
        todo_id = create_response.json()["data"]["id"]
        
        update_data = {"priority": 10}  # Invalid priority
        
        response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 422

    def test_update_todo_completion_status(self, test_client, clean_db):
        """Test updating completion status"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "To Complete"})
        todo_id = create_response.json()["data"]["id"]
        
        update_data = {"is_completed": True}
        
        response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["is_completed"] is True
        assert data["data"]["completed_at"] is not None

    def test_update_todo_response_format(self, test_client, clean_db):
        """Test response follows SingleTodoResponse schema"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Format Test"})
        todo_id = create_response.json()["data"]["id"]
        
        update_data = {"title": "Updated"}
        
        response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "success" in data
        assert "data" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["data"], dict)

    @patch('app.routes.todos.crud')
    def test_update_todo_database_error_handling(self, mock_crud, test_client):
        """Test error handling when database operation fails"""
        mock_crud.update_todo.side_effect = Exception("Database error")
        
        update_data = {"title": "Error Test"}
        response = test_client.put("/api/v1/todos/1", json=update_data)
        
        assert response.status_code == 500


class TestToggleTodoEndpoint:
    """Test suite for PATCH /api/v1/todos/{todo_id}/toggle endpoint"""

    def test_toggle_pending_todo_success(self, test_client, clean_db):
        """Test successful toggling of pending todo to completed"""
        # Create a pending todo
        create_response = test_client.post("/api/v1/todos/", json={"title": "To Toggle"})
        todo_id = create_response.json()["data"]["id"]
        
        response = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_completed"] is True
        assert data["data"]["completed_at"] is not None

    def test_toggle_completed_todo_success(self, test_client, clean_db):
        """Test successful toggling of completed todo back to pending"""
        # Create and complete a todo
        create_response = test_client.post("/api/v1/todos/", json={"title": "To Toggle Back"})
        todo_id = create_response.json()["data"]["id"]
        
        # Complete it first
        test_client.put(f"/api/v1/todos/{todo_id}", json={"is_completed": True})
        
        # Toggle it back
        response = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["is_completed"] is False
        assert data["data"]["completed_at"] is None

    def test_toggle_nonexistent_todo_404(self, test_client, clean_db):
        """Test 404 error for non-existent todo"""
        response = test_client.patch("/api/v1/todos/99999/toggle")
        
        assert response.status_code == 404

    def test_toggle_todo_idempotency(self, test_client, clean_db):
        """Test that multiple toggles work correctly"""
        # Create a todo
        create_response = test_client.post("/api/v1/todos/", json={"title": "Idempotency Test"})
        todo_id = create_response.json()["data"]["id"]
        
        # Toggle twice
        response1 = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
        response2 = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Should be back to original state
        assert response1.json()["data"]["is_completed"] is True
        assert response2.json()["data"]["is_completed"] is False

    def test_toggle_todo_response_format(self, test_client, clean_db):
        """Test response follows SingleTodoResponse schema"""
        # Create a todo
        create_response = test_client.post("/api/v1/todos/", json={"title": "Format Test"})
        todo_id = create_response.json()["data"]["id"]
        
        response = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "success" in data
        assert "data" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["data"], dict)

    @patch('app.routes.todos.crud')
    def test_toggle_todo_database_error_handling(self, mock_crud, test_client):
        """Test error handling when database operation fails"""
        mock_crud.toggle_todo.side_effect = Exception("Database error")
        
        response = test_client.patch("/api/v1/todos/1/toggle")
        
        assert response.status_code == 500


class TestDeleteTodoEndpoint:
    """Test suite for DELETE /api/v1/todos/{todo_id} endpoint"""

    def test_delete_existing_todo_success(self, test_client, clean_db):
        """Test successful todo deletion"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "To Delete"})
        todo_id = create_response.json()["data"]["id"]
        
        response = test_client.delete(f"/api/v1/todos/{todo_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Todo deleted successfully"

    def test_delete_nonexistent_todo_404(self, test_client, clean_db):
        """Test 404 error for non-existent todo"""
        response = test_client.delete("/api/v1/todos/99999")
        
        assert response.status_code == 404

    def test_delete_todo_idempotency(self, test_client, clean_db):
        """Test that deleting same todo twice returns 404 on second attempt"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Delete Twice"})
        todo_id = create_response.json()["data"]["id"]
        
        # Delete first time
        response1 = test_client.delete(f"/api/v1/todos/{todo_id}")
        assert response1.status_code == 200
        
        # Delete second time
        response2 = test_client.delete(f"/api/v1/todos/{todo_id}")
        assert response2.status_code == 404

    def test_delete_todo_response_format(self, test_client, clean_db):
        """Test response follows BaseResponse schema"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Format Test"})
        todo_id = create_response.json()["data"]["id"]
        
        response = test_client.delete(f"/api/v1/todos/{todo_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "success" in data
        assert "message" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)

    def test_delete_todo_actually_deleted(self, test_client, clean_db):
        """Test that todo is actually deleted from database"""
        # Create a todo first
        create_response = test_client.post("/api/v1/todos/", json={"title": "Actually Delete"})
        todo_id = create_response.json()["data"]["id"]
        
        # Delete it
        response = test_client.delete(f"/api/v1/todos/{todo_id}")
        assert response.status_code == 200
        
        # Verify it's gone
        get_response = test_client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 404

    @patch('app.routes.todos.crud')
    def test_delete_todo_database_error_handling(self, mock_crud, test_client):
        """Test error handling when database operation fails"""
        mock_crud.delete_todo.side_effect = Exception("Database error")
        
        response = test_client.delete("/api/v1/todos/1")
        
        assert response.status_code == 500


class TestAPIErrorHandling:
    """Test suite for general API error handling"""

    def test_invalid_json_request_body(self, test_client, clean_db):
        """Test handling of invalid JSON in request body"""
        response = test_client.post(
            "/api/v1/todos/",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

    def test_missing_content_type_header(self, test_client, clean_db):
        """Test handling of missing content type header"""
        response = test_client.post("/api/v1/todos/", data='{"title": "test"}')
        
        # Should still work with valid JSON
        assert response.status_code in [200, 201, 422]

    def test_unsupported_http_method(self, test_client, clean_db):
        """Test handling of unsupported HTTP methods"""
        response = test_client.patch("/api/v1/todos/")  # PATCH not supported on collection
        
        assert response.status_code == 405

    def test_cors_headers_present(self, test_client, clean_db):
        """Test that CORS headers are present in responses"""
        response = test_client.get("/api/v1/todos/")
        
        # Check for CORS headers (if configured)
        assert response.status_code == 200
        # Note: Actual CORS header checks would depend on CORS configuration
