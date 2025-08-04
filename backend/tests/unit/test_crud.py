"""
Unit tests for CRUD operations
Tests all database operations, business logic, and edge cases
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app import crud, models, schemas


class TestGetTodo:
    """Test suite for get_todo function"""

    def test_get_existing_todo_success(self, db_session):
        """Test retrieving existing todo by valid ID"""
        # Create a test todo
        todo = models.Todo(title="Test Todo", priority=2)
        db_session.add(todo)
        db_session.commit()
        
        # Retrieve the todo
        result = crud.get_todo(db_session, todo.id)
        
        assert result is not None
        assert result.id == todo.id
        assert result.title == "Test Todo"
        assert result.priority == 2

    def test_get_nonexistent_todo_returns_none(self, db_session):
        """Test retrieving todo with non-existent ID returns None"""
        result = crud.get_todo(db_session, 99999)
        assert result is None

    def test_get_todo_with_zero_id(self, db_session):
        """Test retrieving todo with ID zero"""
        result = crud.get_todo(db_session, 0)
        assert result is None

    def test_get_todo_with_negative_id(self, db_session):
        """Test retrieving todo with negative ID"""
        result = crud.get_todo(db_session, -1)
        assert result is None

    def test_get_todo_database_session_handling(self, db_session):
        """Test function handles database session correctly"""
        # Create todo
        todo = models.Todo(title="Session Test")
        db_session.add(todo)
        db_session.commit()
        
        # Test that function uses provided session
        result = crud.get_todo(db_session, todo.id)
        assert result is not None
        
        # Test that session is not closed by function
        assert db_session.is_active

    def test_get_todo_query_efficiency(self, db_session):
        """Test that function performs efficient database query"""
        # Create multiple todos
        for i in range(5):
            todo = models.Todo(title=f"Todo {i}")
            db_session.add(todo)
        db_session.commit()
        
        # Mock the query to count calls
        with patch.object(db_session, 'query') as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None
            
            crud.get_todo(db_session, 1)
            
            # Should only call query once
            assert mock_query.call_count == 1


class TestGetTodos:
    """Test suite for get_todos function"""

    def test_get_all_todos_default_params(self, db_session, multiple_todos):
        """Test retrieving all todos with default parameters"""
        todos, total = crud.get_todos(db_session)
        
        assert isinstance(todos, list)
        assert len(todos) == len(multiple_todos)
        assert total == len(multiple_todos)

    def test_get_todos_filter_completed(self, db_session, mixed_status_todos):
        """Test filtering by completed status"""
        todos, total = crud.get_todos(db_session, status="completed")
        
        assert all(todo.is_completed for todo in todos)
        completed_count = len([t for t in mixed_status_todos if t.is_completed])
        assert total == completed_count

    def test_get_todos_filter_pending(self, db_session, mixed_status_todos):
        """Test filtering by pending status"""
        todos, total = crud.get_todos(db_session, status="pending")
        
        assert all(not todo.is_completed for todo in todos)
        pending_count = len([t for t in mixed_status_todos if not t.is_completed])
        assert total == pending_count

    def test_get_todos_filter_all(self, db_session, mixed_status_todos):
        """Test filtering with 'all' status"""
        todos, total = crud.get_todos(db_session, status="all")
        
        assert total == len(mixed_status_todos)

    def test_get_todos_pagination_skip(self, db_session, many_todos):
        """Test pagination with skip parameter"""
        todos, total = crud.get_todos(db_session, skip=2, limit=3)
        
        assert len(todos) <= 3
        assert total == len(many_todos)  # Total should be full count
        
        # Test that we get different todos when skipping
        all_todos, _ = crud.get_todos(db_session, skip=0, limit=3)
        assert todos[0].id != all_todos[0].id

    def test_get_todos_pagination_limit(self, db_session, many_todos):
        """Test pagination with limit parameter"""
        todos, total = crud.get_todos(db_session, limit=3)
        
        assert len(todos) <= 3
        assert total == len(many_todos)

    def test_get_todos_pagination_beyond_available(self, db_session, multiple_todos):
        """Test pagination when skip exceeds available todos"""
        todos, total = crud.get_todos(db_session, skip=100, limit=10)
        
        assert len(todos) == 0
        assert total == len(multiple_todos)

    def test_get_todos_sorting_order(self, db_session):
        """Test that todos are sorted by created_at desc"""
        # Create todos with slight time differences
        first_todo = models.Todo(title="First Todo")
        db_session.add(first_todo)
        db_session.commit()
        
        # Small delay to ensure different timestamps
        import time
        time.sleep(0.01)
        
        second_todo = models.Todo(title="Second Todo")
        db_session.add(second_todo)
        db_session.commit()
        
        todos, _ = crud.get_todos(db_session)
        
        # Second todo should come first (newest first)
        assert todos[0].id == second_todo.id
        assert todos[1].id == first_todo.id

    def test_get_todos_empty_database(self, db_session):
        """Test behavior with empty database"""
        todos, total = crud.get_todos(db_session)
        
        assert todos == []
        assert total == 0

    def test_get_todos_invalid_status(self, db_session, multiple_todos):
        """Test with invalid status filter"""
        # Should default to showing all todos
        todos, total = crud.get_todos(db_session, status="invalid")
        
        assert total == len(multiple_todos)

    def test_get_todos_zero_limit(self, db_session, multiple_todos):
        """Test with zero limit"""
        todos, total = crud.get_todos(db_session, limit=0)
        
        assert len(todos) == 0
        assert total == len(multiple_todos)

    def test_get_todos_negative_skip(self, db_session, multiple_todos):
        """Test with negative skip value"""
        todos, total = crud.get_todos(db_session, skip=-1)
        
        # Should handle gracefully, likely treat as 0
        assert len(todos) > 0
        assert total == len(multiple_todos)


class TestCreateTodo:
    """Test suite for create_todo function"""

    def test_create_todo_valid_data(self, db_session):
        """Test creating todo with valid data"""
        todo_data = schemas.TodoCreate(
            title="New Todo",
            description="Test description",
            priority=3
        )
        
        result = crud.create_todo(db_session, todo_data)
        
        assert result.id is not None
        assert result.title == "New Todo"
        assert result.description == "Test description"
        assert result.priority == 3
        assert result.is_completed is False
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_todo_minimal_data(self, db_session):
        """Test creating todo with minimal required data"""
        todo_data = schemas.TodoCreate(title="Minimal Todo")
        
        result = crud.create_todo(db_session, todo_data)
        
        assert result.title == "Minimal Todo"
        assert result.description is None
        assert result.priority == 1  # Default value
        assert result.due_date is None

    def test_create_todo_with_due_date(self, db_session):
        """Test creating todo with due date"""
        future_date = datetime.now() + timedelta(days=7)
        todo_data = schemas.TodoCreate(
            title="Due Date Todo",
            due_date=future_date
        )
        
        result = crud.create_todo(db_session, todo_data)
        
        assert result.due_date == future_date

    def test_create_todo_database_persistence(self, db_session):
        """Test that created todo is persisted to database"""
        todo_data = schemas.TodoCreate(title="Persistence Test")
        
        result = crud.create_todo(db_session, todo_data)
        todo_id = result.id
        
        # Verify todo exists in database
        db_todo = db_session.query(models.Todo).filter(models.Todo.id == todo_id).first()
        assert db_todo is not None
        assert db_todo.title == "Persistence Test"

    def test_create_todo_return_value_type(self, db_session):
        """Test that function returns correct type"""
        todo_data = schemas.TodoCreate(title="Type Test")
        
        result = crud.create_todo(db_session, todo_data)
        
        assert isinstance(result, models.Todo)

    def test_create_todo_default_values_applied(self, db_session):
        """Test that model default values are applied"""
        todo_data = schemas.TodoCreate(title="Defaults Test")
        
        result = crud.create_todo(db_session, todo_data)
        
        assert result.is_completed is False
        assert result.priority == 1
        assert result.completed_at is None

    def test_create_todo_timestamps_set(self, db_session):
        """Test that timestamps are set on creation"""
        before_creation = datetime.now()
        todo_data = schemas.TodoCreate(title="Timestamp Test")
        
        result = crud.create_todo(db_session, todo_data)
        after_creation = datetime.now()
        
        assert before_creation <= result.created_at <= after_creation
        assert before_creation <= result.updated_at <= after_creation

    def test_create_todo_session_commit_called(self, db_session):
        """Test that database session is committed"""
        todo_data = schemas.TodoCreate(title="Commit Test")
        
        with patch.object(db_session, 'commit') as mock_commit:
            crud.create_todo(db_session, todo_data)
            mock_commit.assert_called_once()

    def test_create_todo_session_refresh_called(self, db_session):
        """Test that database session refresh is called"""
        todo_data = schemas.TodoCreate(title="Refresh Test")
        
        with patch.object(db_session, 'refresh') as mock_refresh:
            result = crud.create_todo(db_session, todo_data)
            mock_refresh.assert_called_once_with(result)


class TestUpdateTodo:
    """Test suite for update_todo function"""

    def test_update_existing_todo_all_fields(self, db_session, sample_todo):
        """Test updating existing todo with all fields"""
        update_data = schemas.TodoUpdate(
            title="Updated Title",
            description="Updated description",
            is_completed=True,
            priority=5,
            due_date=datetime.now() + timedelta(days=1)
        )
        
        result = crud.update_todo(db_session, sample_todo.id, update_data)
        
        assert result is not None
        assert result.title == "Updated Title"
        assert result.description == "Updated description"
        assert result.is_completed is True
        assert result.priority == 5
        assert result.due_date is not None

    def test_update_todo_partial_fields(self, db_session, sample_todo):
        """Test updating todo with only some fields"""
        original_title = sample_todo.title
        update_data = schemas.TodoUpdate(priority=4)
        
        result = crud.update_todo(db_session, sample_todo.id, update_data)
        
        assert result.title == original_title  # Unchanged
        assert result.priority == 4  # Changed

    def test_update_nonexistent_todo(self, db_session):
        """Test updating non-existent todo returns None"""
        update_data = schemas.TodoUpdate(title="Does not exist")
        
        result = crud.update_todo(db_session, 99999, update_data)
        
        assert result is None

    def test_update_todo_completion_timestamp_logic(self, db_session, pending_todo):
        """Test completion timestamp is set when marking as completed"""
        update_data = schemas.TodoUpdate(is_completed=True)
        
        result = crud.update_todo(db_session, pending_todo.id, update_data)
        
        assert result.is_completed is True
        assert result.completed_at is not None
        assert isinstance(result.completed_at, datetime)

    def test_update_todo_completion_timestamp_cleared(self, db_session, completed_todo):
        """Test completion timestamp is cleared when marking as pending"""
        update_data = schemas.TodoUpdate(is_completed=False)
        
        result = crud.update_todo(db_session, completed_todo.id, update_data)
        
        assert result.is_completed is False
        assert result.completed_at is None

    def test_update_todo_unchanged_fields_preserved(self, db_session, sample_todo):
        """Test that unchanged fields remain intact"""
        original_created_at = sample_todo.created_at
        original_description = sample_todo.description
        
        update_data = schemas.TodoUpdate(title="New Title")
        
        result = crud.update_todo(db_session, sample_todo.id, update_data)
        
        assert result.created_at == original_created_at
        assert result.description == original_description

    def test_update_todo_updated_at_timestamp(self, db_session, sample_todo):
        """Test that updated_at timestamp is modified"""
        original_updated_at = sample_todo.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        update_data = schemas.TodoUpdate(title="Updated")
        
        result = crud.update_todo(db_session, sample_todo.id, update_data)
        
        assert result.updated_at > original_updated_at

    def test_update_todo_empty_update_data(self, db_session, sample_todo):
        """Test updating with empty update data"""
        update_data = schemas.TodoUpdate()
        
        result = crud.update_todo(db_session, sample_todo.id, update_data)
        
        # Should still return the todo, even if nothing changed
        assert result is not None
        assert result.id == sample_todo.id

    def test_update_todo_exclude_unset_behavior(self, db_session, sample_todo):
        """Test that only provided fields are updated"""
        original_priority = sample_todo.priority
        
        # Only update title, priority should remain unchanged
        update_data = schemas.TodoUpdate(title="Only Title Updated")
        
        result = crud.update_todo(db_session, sample_todo.id, update_data)
        
        assert result.title == "Only Title Updated"
        assert result.priority == original_priority

    def test_update_todo_database_persistence(self, db_session, sample_todo):
        """Test that updates are persisted to database"""
        update_data = schemas.TodoUpdate(title="Persisted Update")
        
        crud.update_todo(db_session, sample_todo.id, update_data)
        
        # Verify change is persisted
        db_todo = db_session.query(models.Todo).filter(models.Todo.id == sample_todo.id).first()
        assert db_todo.title == "Persisted Update"


class TestToggleTodo:
    """Test suite for toggle_todo function"""

    def test_toggle_pending_to_completed(self, db_session, pending_todo):
        """Test toggling pending todo to completed"""
        result = crud.toggle_todo(db_session, pending_todo.id)
        
        assert result is not None
        assert result.is_completed is True
        assert result.completed_at is not None
        assert isinstance(result.completed_at, datetime)

    def test_toggle_completed_to_pending(self, db_session, completed_todo):
        """Test toggling completed todo back to pending"""
        result = crud.toggle_todo(db_session, completed_todo.id)
        
        assert result is not None
        assert result.is_completed is False
        assert result.completed_at is None

    def test_toggle_nonexistent_todo(self, db_session):
        """Test toggling non-existent todo returns None"""
        result = crud.toggle_todo(db_session, 99999)
        assert result is None

    def test_toggle_todo_timestamp_accuracy(self, db_session, pending_todo):
        """Test that completion timestamp is accurate"""
        before_toggle = datetime.now()
        
        result = crud.toggle_todo(db_session, pending_todo.id)
        
        after_toggle = datetime.now()
        
        assert before_toggle <= result.completed_at <= after_toggle

    def test_toggle_todo_state_consistency(self, db_session, sample_todo):
        """Test that state remains consistent after multiple toggles"""
        original_state = sample_todo.is_completed
        
        # Toggle twice should return to original state
        crud.toggle_todo(db_session, sample_todo.id)
        result = crud.toggle_todo(db_session, sample_todo.id)
        
        assert result.is_completed == original_state

    def test_toggle_todo_preserves_other_fields(self, db_session, sample_todo):
        """Test that toggle preserves all other fields"""
        original_title = sample_todo.title
        original_description = sample_todo.description
        original_priority = sample_todo.priority
        original_created_at = sample_todo.created_at
        
        result = crud.toggle_todo(db_session, sample_todo.id)
        
        assert result.title == original_title
        assert result.description == original_description
        assert result.priority == original_priority
        assert result.created_at == original_created_at

    def test_toggle_todo_updates_timestamp(self, db_session, sample_todo):
        """Test that toggle updates the updated_at timestamp"""
        original_updated_at = sample_todo.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        result = crud.toggle_todo(db_session, sample_todo.id)
        
        assert result.updated_at > original_updated_at


class TestDeleteTodo:
    """Test suite for delete_todo function"""

    def test_delete_existing_todo_success(self, db_session, sample_todo):
        """Test successful deletion of existing todo"""
        todo_id = sample_todo.id
        
        result = crud.delete_todo(db_session, todo_id)
        
        assert result is True
        
        # Verify todo is deleted from database
        deleted_todo = db_session.query(models.Todo).filter(models.Todo.id == todo_id).first()
        assert deleted_todo is None

    def test_delete_nonexistent_todo(self, db_session):
        """Test deletion of non-existent todo returns False"""
        result = crud.delete_todo(db_session, 99999)
        assert result is False

    def test_delete_todo_database_consistency(self, db_session, multiple_todos):
        """Test that only the specified todo is deleted"""
        todo_to_delete = multiple_todos[0]
        remaining_todos = multiple_todos[1:]
        
        result = crud.delete_todo(db_session, todo_to_delete.id)
        
        assert result is True
        
        # Verify other todos still exist
        for todo in remaining_todos:
            existing_todo = db_session.query(models.Todo).filter(models.Todo.id == todo.id).first()
            assert existing_todo is not None

    def test_delete_todo_transaction_commit(self, db_session, sample_todo):
        """Test that database transaction is committed"""
        with patch.object(db_session, 'commit') as mock_commit:
            crud.delete_todo(db_session, sample_todo.id)
            mock_commit.assert_called_once()

    def test_delete_todo_return_value_types(self, db_session, sample_todo):
        """Test return value is boolean"""
        result = crud.delete_todo(db_session, sample_todo.id)
        assert isinstance(result, bool)
        
        result_false = crud.delete_todo(db_session, 99999)
        assert isinstance(result_false, bool)

    def test_delete_todo_zero_id(self, db_session):
        """Test deletion with zero ID"""
        result = crud.delete_todo(db_session, 0)
        assert result is False

    def test_delete_todo_negative_id(self, db_session):
        """Test deletion with negative ID"""
        result = crud.delete_todo(db_session, -1)
        assert result is False


class TestBatchDeleteCompleted:
    """Test suite for batch_delete_completed function"""

    def test_batch_delete_only_completed_todos(self, db_session, mixed_status_todos):
        """Test that only completed todos are deleted"""
        completed_count = len([t for t in mixed_status_todos if t.is_completed])
        pending_count = len([t for t in mixed_status_todos if not t.is_completed])
        
        result = crud.batch_delete_completed(db_session)
        
        assert result == completed_count
        
        # Verify only pending todos remain
        remaining_todos = db_session.query(models.Todo).all()
        assert len(remaining_todos) == pending_count
        assert all(not todo.is_completed for todo in remaining_todos)

    def test_batch_delete_count_accuracy(self, db_session, mixed_status_todos):
        """Test that returned count matches actual deletions"""
        expected_count = len([t for t in mixed_status_todos if t.is_completed])
        
        result = crud.batch_delete_completed(db_session)
        
        assert result == expected_count

    def test_batch_delete_no_completed_todos(self, db_session, pending_todos):
        """Test behavior when no completed todos exist"""
        result = crud.batch_delete_completed(db_session)
        
        assert result == 0
        
        # Verify all todos still exist
        remaining_todos = db_session.query(models.Todo).all()
        assert len(remaining_todos) == len(pending_todos)

    def test_batch_delete_empty_database(self, db_session):
        """Test behavior with empty database"""
        result = crud.batch_delete_completed(db_session)
        
        assert result == 0

    def test_batch_delete_all_completed_todos(self, db_session, completed_todos):
        """Test deleting when all todos are completed"""
        expected_count = len(completed_todos)
        
        result = crud.batch_delete_completed(db_session)
        
        assert result == expected_count
        
        # Verify database is empty
        remaining_todos = db_session.query(models.Todo).all()
        assert len(remaining_todos) == 0

    def test_batch_delete_transaction_handling(self, db_session, mixed_status_todos):
        """Test that database transaction is handled correctly"""
        with patch.object(db_session, 'commit') as mock_commit:
            crud.batch_delete_completed(db_session)
            mock_commit.assert_called_once()

    def test_batch_delete_performance_many_todos(self, db_session, many_completed_todos):
        """Test performance with large number of completed todos"""
        import time
        
        start_time = time.time()
        result = crud.batch_delete_completed(db_session)
        end_time = time.time()
        
        # Should complete reasonably quickly (adjust threshold as needed)
        assert end_time - start_time < 1.0  # Less than 1 second
        assert result == len(many_completed_todos)

    def test_batch_delete_return_type(self, db_session):
        """Test that function returns integer"""
        result = crud.batch_delete_completed(db_session)
        assert isinstance(result, int)
