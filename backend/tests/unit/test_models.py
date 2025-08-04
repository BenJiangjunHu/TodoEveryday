"""
Unit tests for Todo model
Tests all model behaviors, constraints, and relationships
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.models import Todo
from app.database import Base


class TestTodoModel:
    """Test suite for Todo model functionality"""

    def test_todo_creation_with_required_fields(self, db_session):
        """Test basic todo model creation with only required fields"""
        todo = Todo(title="Test Todo")
        db_session.add(todo)
        db_session.commit()
        
        assert todo.id is not None
        assert todo.title == "Test Todo"
        assert todo.description is None
        assert todo.is_completed is False
        assert todo.priority == 1
        assert todo.created_at is not None
        assert todo.updated_at is not None
        assert todo.completed_at is None
        assert todo.due_date is None

    def test_todo_creation_with_all_fields(self, db_session):
        """Test todo creation with all fields populated"""
        due_date = datetime.now() + timedelta(days=7)
        todo = Todo(
            title="Complete Todo",
            description="Test description",
            priority=3,
            due_date=due_date
        )
        db_session.add(todo)
        db_session.commit()
        
        assert todo.title == "Complete Todo"
        assert todo.description == "Test description"
        assert todo.priority == 3
        assert todo.due_date == due_date
        assert todo.is_completed is False

    def test_todo_default_values(self, db_session):
        """Test default field values are set correctly"""
        todo = Todo(title="Default Values Test")
        
        # Test defaults before saving
        assert todo.is_completed is False
        assert todo.priority == 1
        
        db_session.add(todo)
        db_session.commit()
        
        # Test defaults after saving
        assert todo.is_completed is False
        assert todo.priority == 1
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_todo_timestamps_on_creation(self, db_session):
        """Test created_at and updated_at timestamps are set on creation"""
        before_creation = datetime.now()
        todo = Todo(title="Timestamp Test")
        db_session.add(todo)
        db_session.commit()
        after_creation = datetime.now()
        
        assert before_creation <= todo.created_at <= after_creation
        assert before_creation <= todo.updated_at <= after_creation
        assert todo.created_at == todo.updated_at

    def test_todo_updated_at_changes_on_update(self, db_session):
        """Test updated_at timestamp changes when todo is modified"""
        todo = Todo(title="Update Test")
        db_session.add(todo)
        db_session.commit()
        
        original_updated_at = todo.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        todo.title = "Updated Title"
        db_session.commit()
        
        assert todo.updated_at > original_updated_at

    def test_todo_title_not_null_constraint(self, db_session):
        """Test that title field cannot be null"""
        todo = Todo()  # No title provided
        db_session.add(todo)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_todo_title_empty_string_allowed(self, db_session):
        """Test that empty string title is allowed (though not recommended)"""
        todo = Todo(title="")
        db_session.add(todo)
        db_session.commit()
        
        assert todo.title == ""

    def test_todo_title_max_length(self, db_session):
        """Test title field handles maximum length"""
        long_title = "x" * 255  # Maximum allowed length
        todo = Todo(title=long_title)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.title == long_title

    def test_todo_description_optional(self, db_session):
        """Test description field is optional"""
        todo = Todo(title="No Description")
        db_session.add(todo)
        db_session.commit()
        
        assert todo.description is None

    def test_todo_description_text_field(self, db_session):
        """Test description can handle large text"""
        long_description = "x" * 1000  # Large text
        todo = Todo(title="Long Description", description=long_description)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.description == long_description

    def test_todo_priority_default_value(self, db_session):
        """Test priority defaults to 1"""
        todo = Todo(title="Priority Test")
        db_session.add(todo)
        db_session.commit()
        
        assert todo.priority == 1

    def test_todo_priority_custom_values(self, db_session):
        """Test priority accepts custom values"""
        for priority in [1, 2, 3, 4, 5]:
            todo = Todo(title=f"Priority {priority}", priority=priority)
            db_session.add(todo)
            db_session.commit()
            
            assert todo.priority == priority

    def test_todo_completion_status_toggle(self, db_session):
        """Test completion status can be toggled"""
        todo = Todo(title="Toggle Test")
        db_session.add(todo)
        db_session.commit()
        
        # Initially not completed
        assert todo.is_completed is False
        assert todo.completed_at is None
        
        # Mark as completed
        todo.is_completed = True
        todo.completed_at = datetime.now()
        db_session.commit()
        
        assert todo.is_completed is True
        assert todo.completed_at is not None

    def test_todo_due_date_optional(self, db_session):
        """Test due_date field is optional"""
        todo = Todo(title="No Due Date")
        db_session.add(todo)
        db_session.commit()
        
        assert todo.due_date is None

    def test_todo_due_date_datetime(self, db_session):
        """Test due_date accepts datetime objects"""
        future_date = datetime.now() + timedelta(days=30)
        todo = Todo(title="Future Due Date", due_date=future_date)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.due_date == future_date

    def test_todo_due_date_past_allowed(self, db_session):
        """Test due_date can be in the past (overdue todos)"""
        past_date = datetime.now() - timedelta(days=1)
        todo = Todo(title="Overdue Todo", due_date=past_date)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.due_date == past_date

    def test_todo_string_representation(self, db_session):
        """Test string representation of todo if implemented"""
        todo = Todo(title="String Repr Test")
        db_session.add(todo)
        db_session.commit()
        
        # Test that string representation doesn't crash
        str_repr = str(todo)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

    def test_todo_repr_representation(self, db_session):
        """Test repr representation of todo if implemented"""
        todo = Todo(title="Repr Test")
        db_session.add(todo)
        db_session.commit()
        
        # Test that repr doesn't crash
        repr_str = repr(todo)
        assert isinstance(repr_str, str)
        assert len(repr_str) > 0

    def test_todo_id_autoincrement(self, db_session):
        """Test ID field auto-increments correctly"""
        todo1 = Todo(title="First Todo")
        todo2 = Todo(title="Second Todo")
        
        db_session.add(todo1)
        db_session.add(todo2)
        db_session.commit()
        
        assert todo1.id != todo2.id
        assert todo1.id > 0
        assert todo2.id > 0

    def test_todo_unique_ids(self, db_session):
        """Test that each todo gets a unique ID"""
        todos = []
        for i in range(5):
            todo = Todo(title=f"Todo {i}")
            todos.append(todo)
            db_session.add(todo)
        
        db_session.commit()
        
        ids = [todo.id for todo in todos]
        assert len(set(ids)) == 5  # All IDs should be unique

    def test_todo_boolean_field_types(self, db_session):
        """Test boolean field accepts only boolean values"""
        todo = Todo(title="Boolean Test")
        
        # Test valid boolean values
        todo.is_completed = True
        assert todo.is_completed is True
        
        todo.is_completed = False
        assert todo.is_completed is False

    def test_todo_integer_field_types(self, db_session):
        """Test integer fields accept integer values"""
        todo = Todo(title="Integer Test")
        
        # Test priority as integer
        todo.priority = 5
        assert todo.priority == 5
        assert isinstance(todo.priority, int)

    def test_todo_datetime_field_types(self, db_session):
        """Test datetime fields accept datetime objects"""
        now = datetime.now()
        todo = Todo(title="Datetime Test", due_date=now)
        
        assert todo.due_date == now
        assert isinstance(todo.due_date, datetime)

    def test_todo_nullable_fields(self, db_session):
        """Test that nullable fields can be set to None"""
        todo = Todo(title="Nullable Test")
        
        # These fields should accept None
        todo.description = None
        todo.completed_at = None
        todo.due_date = None
        
        assert todo.description is None
        assert todo.completed_at is None
        assert todo.due_date is None

    def test_todo_field_updates(self, db_session):
        """Test that all fields can be updated after creation"""
        todo = Todo(title="Original Title")
        db_session.add(todo)
        db_session.commit()
        
        # Update all updatable fields
        new_due_date = datetime.now() + timedelta(days=1)
        new_completed_at = datetime.now()
        
        todo.title = "Updated Title"
        todo.description = "Updated Description"
        todo.is_completed = True
        todo.priority = 5
        todo.due_date = new_due_date
        todo.completed_at = new_completed_at
        
        db_session.commit()
        
        assert todo.title == "Updated Title"
        assert todo.description == "Updated Description"
        assert todo.is_completed is True
        assert todo.priority == 5
        assert todo.due_date == new_due_date
        assert todo.completed_at == new_completed_at

    def test_todo_edge_case_empty_values(self, db_session):
        """Test edge cases with empty/minimal values"""
        # Test with minimal required data
        todo = Todo(title="x")  # Single character title
        db_session.add(todo)
        db_session.commit()
        
        assert todo.title == "x"
        assert todo.id is not None

    def test_todo_edge_case_extreme_priority(self, db_session):
        """Test edge cases with extreme priority values"""
        # Test very high priority (should be allowed by model, validation in schema)
        todo = Todo(title="High Priority", priority=999)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.priority == 999

    def test_todo_edge_case_zero_priority(self, db_session):
        """Test edge case with zero priority"""
        todo = Todo(title="Zero Priority", priority=0)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.priority == 0

    def test_todo_edge_case_negative_priority(self, db_session):
        """Test edge case with negative priority"""
        todo = Todo(title="Negative Priority", priority=-1)
        db_session.add(todo)
        db_session.commit()
        
        assert todo.priority == -1
