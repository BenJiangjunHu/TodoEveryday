"""
Unit tests for Pydantic schemas
Tests validation, serialization, and edge cases
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.schemas import (
    TodoBase, TodoCreate, TodoUpdate, TodoResponse,
    FilterStatus, BatchAction, BatchRequest,
    BaseResponse, TodoListResponse, SingleTodoResponse,
    StatsResponse, StatsResponseWrapper, ErrorResponse, ErrorDetail
)


class TestTodoBaseSchema:
    """Test suite for TodoBase schema validation"""

    def test_valid_todo_base_creation(self):
        """Test creating valid TodoBase with all fields"""
        due_date = datetime.now() + timedelta(days=7)
        todo_data = {
            "title": "Test Todo",
            "description": "Test description",
            "priority": 3,
            "due_date": due_date
        }
        
        todo = TodoBase(**todo_data)
        
        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.priority == 3
        assert todo.due_date == due_date

    def test_valid_todo_base_minimal_fields(self):
        """Test creating TodoBase with only required fields"""
        todo = TodoBase(title="Minimal Todo")
        
        assert todo.title == "Minimal Todo"
        assert todo.description is None
        assert todo.priority == 1  # Default value
        assert todo.due_date is None

    def test_title_validation_empty_string(self):
        """Test title validation rejects empty string"""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="")
        
        assert "at least 1 character" in str(exc_info.value)

    def test_title_validation_whitespace_only(self):
        """Test title validation handles whitespace-only strings"""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="   ")
        
        # Should fail validation due to min_length after stripping
        assert "at least 1 character" in str(exc_info.value)

    def test_title_validation_max_length(self):
        """Test title validation enforces maximum length"""
        long_title = "x" * 256  # Exceeds 255 character limit
        
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title=long_title)
        
        assert "at most 255 characters" in str(exc_info.value)

    def test_title_validation_max_length_boundary(self):
        """Test title validation at exact maximum length"""
        max_title = "x" * 255  # Exactly 255 characters
        
        todo = TodoBase(title=max_title)
        assert todo.title == max_title

    def test_title_validation_unicode_characters(self):
        """Test title validation with unicode characters"""
        unicode_title = "测试任务 🚀 émoji"
        
        todo = TodoBase(title=unicode_title)
        assert todo.title == unicode_title

    def test_priority_validation_valid_range(self):
        """Test priority validation within valid range (1-5)"""
        for priority in [1, 2, 3, 4, 5]:
            todo = TodoBase(title="Priority Test", priority=priority)
            assert todo.priority == priority

    def test_priority_validation_below_minimum(self):
        """Test priority validation rejects values below 1"""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="Low Priority", priority=0)
        
        assert "greater than or equal to 1" in str(exc_info.value)

    def test_priority_validation_above_maximum(self):
        """Test priority validation rejects values above 5"""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="High Priority", priority=6)
        
        assert "less than or equal to 5" in str(exc_info.value)

    def test_priority_validation_negative_values(self):
        """Test priority validation rejects negative values"""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="Negative Priority", priority=-1)
        
        assert "greater than or equal to 1" in str(exc_info.value)

    def test_priority_default_value(self):
        """Test priority defaults to 1 when not provided"""
        todo = TodoBase(title="Default Priority")
        assert todo.priority == 1

    def test_description_optional_field(self):
        """Test description field is optional"""
        todo = TodoBase(title="No Description")
        assert todo.description is None

    def test_description_accepts_long_text(self):
        """Test description accepts long text content"""
        long_description = "x" * 1000
        todo = TodoBase(title="Long Description", description=long_description)
        assert todo.description == long_description

    def test_description_accepts_empty_string(self):
        """Test description accepts empty string"""
        todo = TodoBase(title="Empty Description", description="")
        assert todo.description == ""

    def test_due_date_optional_field(self):
        """Test due_date field is optional"""
        todo = TodoBase(title="No Due Date")
        assert todo.due_date is None

    def test_due_date_valid_datetime(self):
        """Test due_date accepts valid datetime objects"""
        future_date = datetime.now() + timedelta(days=30)
        todo = TodoBase(title="Future Due Date", due_date=future_date)
        assert todo.due_date == future_date

    def test_due_date_past_datetime_allowed(self):
        """Test due_date accepts past datetime (overdue todos)"""
        past_date = datetime.now() - timedelta(days=1)
        todo = TodoBase(title="Overdue Todo", due_date=past_date)
        assert todo.due_date == past_date

    def test_due_date_string_parsing(self):
        """Test due_date parses ISO format strings"""
        date_string = "2025-12-31T23:59:59"
        todo = TodoBase(title="String Date", due_date=date_string)
        
        assert isinstance(todo.due_date, datetime)
        assert todo.due_date.year == 2025
        assert todo.due_date.month == 12
        assert todo.due_date.day == 31

    def test_due_date_invalid_format(self):
        """Test due_date validation with invalid date format"""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="Invalid Date", due_date="invalid-date")
        
        assert "datetime" in str(exc_info.value).lower()


class TestTodoCreateSchema:
    """Test suite for TodoCreate schema"""

    def test_valid_todo_create(self):
        """Test creating valid TodoCreate instance"""
        todo_data = {
            "title": "New Todo",
            "description": "Create todo test",
            "priority": 2
        }
        
        todo = TodoCreate(**todo_data)
        
        assert todo.title == "New Todo"
        assert todo.description == "Create todo test"
        assert todo.priority == 2

    def test_todo_create_inheritance(self):
        """Test TodoCreate inherits from TodoBase correctly"""
        assert issubclass(TodoCreate, TodoBase)

    def test_todo_create_required_fields(self):
        """Test TodoCreate with only required fields"""
        todo = TodoCreate(title="Required Only")
        assert todo.title == "Required Only"

    def test_todo_create_all_base_validations(self):
        """Test TodoCreate inherits all TodoBase validations"""
        # Should inherit title length validation
        with pytest.raises(ValidationError):
            TodoCreate(title="")
        
        # Should inherit priority range validation
        with pytest.raises(ValidationError):
            TodoCreate(title="Test", priority=10)


class TestTodoUpdateSchema:
    """Test suite for TodoUpdate schema"""

    def test_valid_todo_update_all_fields(self):
        """Test TodoUpdate with all fields provided"""
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "is_completed": True,
            "priority": 4,
            "due_date": datetime.now() + timedelta(days=1)
        }
        
        todo_update = TodoUpdate(**update_data)
        
        assert todo_update.title == "Updated Title"
        assert todo_update.description == "Updated description"
        assert todo_update.is_completed is True
        assert todo_update.priority == 4
        assert todo_update.due_date is not None

    def test_todo_update_partial_fields(self):
        """Test TodoUpdate with only some fields provided"""
        todo_update = TodoUpdate(title="Partial Update")
        
        assert todo_update.title == "Partial Update"
        assert todo_update.description is None
        assert todo_update.is_completed is None
        assert todo_update.priority is None
        assert todo_update.due_date is None

    def test_todo_update_empty_update(self):
        """Test TodoUpdate with no fields provided"""
        todo_update = TodoUpdate()
        
        assert todo_update.title is None
        assert todo_update.description is None
        assert todo_update.is_completed is None
        assert todo_update.priority is None
        assert todo_update.due_date is None

    def test_todo_update_title_validation(self):
        """Test TodoUpdate title field validation"""
        # Should validate title length when provided
        with pytest.raises(ValidationError):
            TodoUpdate(title="")
        
        # Should accept valid title
        todo_update = TodoUpdate(title="Valid Title")
        assert todo_update.title == "Valid Title"

    def test_todo_update_priority_validation(self):
        """Test TodoUpdate priority field validation"""
        # Should validate priority range when provided
        with pytest.raises(ValidationError):
            TodoUpdate(priority=0)
        
        with pytest.raises(ValidationError):
            TodoUpdate(priority=6)
        
        # Should accept valid priority
        todo_update = TodoUpdate(priority=3)
        assert todo_update.priority == 3

    def test_todo_update_completion_status(self):
        """Test TodoUpdate is_completed field"""
        # Test setting to True
        todo_update = TodoUpdate(is_completed=True)
        assert todo_update.is_completed is True
        
        # Test setting to False
        todo_update = TodoUpdate(is_completed=False)
        assert todo_update.is_completed is False

    def test_todo_update_null_values(self):
        """Test TodoUpdate with explicit null values"""
        todo_update = TodoUpdate(
            description=None,
            due_date=None
        )
        
        assert todo_update.description is None
        assert todo_update.due_date is None


class TestTodoResponseSchema:
    """Test suite for TodoResponse schema"""

    def test_todo_response_creation(self):
        """Test creating TodoResponse with all fields"""
        now = datetime.now()
        response_data = {
            "id": 1,
            "title": "Response Todo",
            "description": "Response test",
            "is_completed": False,
            "priority": 2,
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
            "due_date": now + timedelta(days=7)
        }
        
        response = TodoResponse(**response_data)
        
        assert response.id == 1
        assert response.title == "Response Todo"
        assert response.description == "Response test"
        assert response.is_completed is False
        assert response.priority == 2
        assert response.created_at == now
        assert response.updated_at == now
        assert response.completed_at is None
        assert response.due_date is not None

    def test_todo_response_inheritance(self):
        """Test TodoResponse inherits from TodoBase"""
        assert issubclass(TodoResponse, TodoBase)

    def test_todo_response_required_fields(self):
        """Test TodoResponse requires additional fields beyond TodoBase"""
        now = datetime.now()
        
        # Should require id, is_completed, created_at, updated_at
        response = TodoResponse(
            id=1,
            title="Required Fields",
            is_completed=False,
            created_at=now,
            updated_at=now
        )
        
        assert response.id == 1
        assert response.is_completed is False

    def test_todo_response_completed_todo(self):
        """Test TodoResponse for completed todo"""
        now = datetime.now()
        completed_at = now - timedelta(hours=1)
        
        response = TodoResponse(
            id=2,
            title="Completed Todo",
            is_completed=True,
            created_at=now - timedelta(days=1),
            updated_at=now,
            completed_at=completed_at
        )
        
        assert response.is_completed is True
        assert response.completed_at == completed_at


class TestEnumClasses:
    """Test suite for enum classes"""

    def test_filter_status_enum_values(self):
        """Test FilterStatus enum has correct values"""
        assert FilterStatus.all == "all"
        assert FilterStatus.completed == "completed"
        assert FilterStatus.pending == "pending"

    def test_filter_status_enum_membership(self):
        """Test FilterStatus enum membership"""
        assert "all" in FilterStatus
        assert "completed" in FilterStatus
        assert "pending" in FilterStatus
        assert "invalid" not in FilterStatus

    def test_batch_action_enum_values(self):
        """Test BatchAction enum has correct values"""
        assert BatchAction.delete_completed == "delete_completed"
        assert BatchAction.delete_all == "delete_all"
        assert BatchAction.complete_all == "complete_all"

    def test_batch_action_enum_membership(self):
        """Test BatchAction enum membership"""
        assert "delete_completed" in BatchAction
        assert "delete_all" in BatchAction
        assert "complete_all" in BatchAction
        assert "invalid_action" not in BatchAction

    def test_enum_string_conversion(self):
        """Test enum string representation"""
        assert str(FilterStatus.all) == "all"
        assert str(BatchAction.delete_completed) == "delete_completed"

    def test_enum_iteration(self):
        """Test enum iteration"""
        filter_values = [status.value for status in FilterStatus]
        assert "all" in filter_values
        assert "completed" in filter_values
        assert "pending" in filter_values
        assert len(filter_values) == 3

        batch_values = [action.value for action in BatchAction]
        assert "delete_completed" in batch_values
        assert "delete_all" in batch_values
        assert "complete_all" in batch_values
        assert len(batch_values) == 3


class TestBatchRequestSchema:
    """Test suite for BatchRequest schema"""

    def test_valid_batch_request(self):
        """Test creating valid BatchRequest"""
        batch_request = BatchRequest(
            action=BatchAction.delete_completed,
            todo_ids=[1, 2, 3]
        )
        
        assert batch_request.action == BatchAction.delete_completed
        assert batch_request.todo_ids == [1, 2, 3]

    def test_batch_request_without_todo_ids(self):
        """Test BatchRequest without todo_ids (for operations like delete_all)"""
        batch_request = BatchRequest(action=BatchAction.delete_all)
        
        assert batch_request.action == BatchAction.delete_all
        assert batch_request.todo_ids is None

    def test_batch_request_with_empty_todo_ids(self):
        """Test BatchRequest with empty todo_ids list"""
        batch_request = BatchRequest(
            action=BatchAction.delete_completed,
            todo_ids=[]
        )
        
        assert batch_request.action == BatchAction.delete_completed
        assert batch_request.todo_ids == []


class TestResponseSchemas:
    """Test suite for response wrapper schemas"""

    def test_base_response_success(self):
        """Test BaseResponse for successful operation"""
        response = BaseResponse(success=True, message="Operation successful")
        
        assert response.success is True
        assert response.message == "Operation successful"

    def test_base_response_minimal(self):
        """Test BaseResponse with minimal data"""
        response = BaseResponse(success=True)
        
        assert response.success is True
        assert response.message is None

    def test_todo_list_response(self):
        """Test TodoListResponse structure"""
        now = datetime.now()
        todo_data = TodoResponse(
            id=1,
            title="List Todo",
            is_completed=False,
            created_at=now,
            updated_at=now
        )
        
        list_response = TodoListResponse(
            success=True,
            data=[todo_data],
            total=1,
            page=1,
            limit=10
        )
        
        assert list_response.success is True
        assert len(list_response.data) == 1
        assert list_response.total == 1
        assert list_response.page == 1
        assert list_response.limit == 10

    def test_single_todo_response(self):
        """Test SingleTodoResponse structure"""
        now = datetime.now()
        todo_data = TodoResponse(
            id=1,
            title="Single Todo",
            is_completed=False,
            created_at=now,
            updated_at=now
        )
        
        single_response = SingleTodoResponse(
            success=True,
            data=todo_data
        )
        
        assert single_response.success is True
        assert single_response.data.id == 1
        assert single_response.data.title == "Single Todo"

    def test_stats_response(self):
        """Test StatsResponse structure"""
        stats = StatsResponse(
            total=10,
            completed=3,
            pending=7,
            overdue=2
        )
        
        assert stats.total == 10
        assert stats.completed == 3
        assert stats.pending == 7
        assert stats.overdue == 2

    def test_stats_response_wrapper(self):
        """Test StatsResponseWrapper structure"""
        stats = StatsResponse(total=5, completed=2, pending=3, overdue=1)
        stats_wrapper = StatsResponseWrapper(
            success=True,
            data=stats
        )
        
        assert stats_wrapper.success is True
        assert stats_wrapper.data.total == 5

    def test_error_response(self):
        """Test ErrorResponse structure"""
        error_detail = ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid input data",
            details={"field": "title", "issue": "too short"}
        )
        
        error_response = ErrorResponse(
            success=False,
            error=error_detail
        )
        
        assert error_response.success is False
        assert error_response.error.code == "VALIDATION_ERROR"
        assert error_response.error.message == "Invalid input data"
        assert error_response.error.details is not None

    def test_error_detail_minimal(self):
        """Test ErrorDetail with minimal data"""
        error_detail = ErrorDetail(
            code="GENERIC_ERROR",
            message="Something went wrong"
        )
        
        assert error_detail.code == "GENERIC_ERROR"
        assert error_detail.message == "Something went wrong"
        assert error_detail.details is None


class TestSchemaEdgeCases:
    """Test suite for schema edge cases and error conditions"""

    def test_invalid_data_types(self):
        """Test schemas with invalid data types"""
        # Test invalid priority type
        with pytest.raises(ValidationError):
            TodoBase(title="Test", priority="high")  # String instead of int
        
        # Test invalid boolean type
        with pytest.raises(ValidationError):
            TodoUpdate(is_completed="yes")  # String instead of bool

    def test_missing_required_fields(self):
        """Test schemas missing required fields"""
        # TodoResponse missing required fields
        with pytest.raises(ValidationError):
            TodoResponse(title="Missing Fields")  # Missing id, is_completed, etc.

    def test_extra_fields_ignored(self):
        """Test that extra fields are ignored (if model config allows)"""
        try:
            todo = TodoBase(
                title="Extra Fields",
                extra_field="should be ignored"
            )
            # Should not raise error, extra field should be ignored
            assert todo.title == "Extra Fields"
        except ValidationError:
            # This is expected if the model doesn't allow extra fields
            pass

    def test_none_for_required_fields(self):
        """Test None values for required fields"""
        with pytest.raises(ValidationError):
            TodoBase(title=None)

    def test_boundary_value_testing(self):
        """Test boundary values for all validated fields"""
        # Test exact boundary for title length
        boundary_title = "x" * 255
        todo = TodoBase(title=boundary_title)
        assert len(todo.title) == 255
        
        # Test exact boundary for priority
        todo_min = TodoBase(title="Min Priority", priority=1)
        todo_max = TodoBase(title="Max Priority", priority=5)
        assert todo_min.priority == 1
        assert todo_max.priority == 5
