from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])

@router.get("/", response_model=schemas.TodoListResponse)
def get_todos(
    status: schemas.FilterStatus = Query(default="all", description="过滤状态"),
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取所有待办事项"""
    skip = (page - 1) * limit
    todos, total = crud.get_todos(db, status=status.value, skip=skip, limit=limit)
    
    return schemas.TodoListResponse(
        success=True,
        data=[schemas.TodoResponse.model_validate(todo) for todo in todos],
        total=total,
        page=page,
        limit=limit
    )

@router.post("/", response_model=schemas.SingleTodoResponse, status_code=201)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db)
):
    """创建新的待办事项"""
    db_todo = crud.create_todo(db=db, todo=todo)
    return schemas.SingleTodoResponse(
        success=True,
        data=schemas.TodoResponse.model_validate(db_todo)
    )

@router.get("/{todo_id}", response_model=schemas.SingleTodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """获取单个待办事项"""
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return schemas.SingleTodoResponse(
        success=True,
        data=schemas.TodoResponse.model_validate(db_todo)
    )

@router.put("/{todo_id}", response_model=schemas.SingleTodoResponse)
def update_todo(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """更新待办事项"""
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo_update)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return schemas.SingleTodoResponse(
        success=True,
        data=schemas.TodoResponse.model_validate(db_todo)
    )

@router.patch("/{todo_id}/toggle", response_model=schemas.SingleTodoResponse)
def toggle_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """切换待办事项完成状态"""
    db_todo = crud.toggle_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return schemas.SingleTodoResponse(
        success=True,
        data=schemas.TodoResponse.model_validate(db_todo)
    )

@router.delete("/{todo_id}", response_model=schemas.BaseResponse)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """删除待办事项"""
    success = crud.delete_todo(db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return schemas.BaseResponse(
        success=True,
        message="Todo deleted successfully"
    )

@router.post("/batch", response_model=schemas.BaseResponse)
def batch_operation(
    request: schemas.BatchRequest,
    db: Session = Depends(get_db)
):
    """批量操作"""
    if request.action == schemas.BatchAction.delete_completed:
        count = crud.batch_delete_completed(db)
        message = f"Deleted {count} completed todos"
    elif request.action == schemas.BatchAction.delete_all:
        count = crud.batch_delete_all(db)
        message = f"Deleted {count} todos"
    elif request.action == schemas.BatchAction.complete_all:
        count = crud.batch_complete_all(db)
        message = f"Completed {count} todos"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    return schemas.BaseResponse(
        success=True,
        message=message
    )

@router.get("/stats/", response_model=schemas.StatsResponseWrapper)
def get_stats(db: Session = Depends(get_db)):
    """获取统计信息"""
    stats = crud.get_todos_stats(db)
    return schemas.StatsResponseWrapper(
        success=True,
        data=schemas.StatsResponse(**stats)
    )
