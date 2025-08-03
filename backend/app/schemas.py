from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class FilterStatus(str, Enum):
    all = "all"
    completed = "completed"
    pending = "pending"

class BatchAction(str, Enum):
    delete_completed = "delete_completed"
    delete_all = "delete_all"
    complete_all = "complete_all"

# 基础Todo模式
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    priority: int = Field(default=1, ge=1, le=5, description="优先级 1-5")
    due_date: Optional[datetime] = Field(None, description="截止日期")

# 创建Todo的请求模式
class TodoCreate(TodoBase):
    pass

# 更新Todo的请求模式
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None

# 响应模式
class TodoResponse(TodoBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# 批量操作请求模式
class BatchRequest(BaseModel):
    action: BatchAction
    todo_ids: Optional[list[int]] = None

# 统计信息响应模式
class StatsResponse(BaseModel):
    total: int
    completed: int
    pending: int
    overdue: int

# 通用响应模式
class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class TodoListResponse(BaseResponse):
    data: list[TodoResponse]
    total: int
    page: int
    limit: int

class SingleTodoResponse(BaseResponse):
    data: TodoResponse

class StatsResponseWrapper(BaseResponse):
    data: StatsResponse

# 错误响应模式
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
