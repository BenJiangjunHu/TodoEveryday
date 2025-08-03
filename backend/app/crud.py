from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import Optional, List
from . import models, schemas

def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    """获取单个待办事项"""
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def get_todos(
    db: Session, 
    status: str = "all", 
    skip: int = 0, 
    limit: int = 10
) -> tuple[List[models.Todo], int]:
    """获取待办事项列表"""
    query = db.query(models.Todo)
    
    # 根据状态过滤
    if status == "completed":
        query = query.filter(models.Todo.is_completed == True)
    elif status == "pending":
        query = query.filter(models.Todo.is_completed == False)
    
    # 获取总数
    total = query.count()
    
    # 分页和排序
    todos = query.order_by(models.Todo.created_at.desc()).offset(skip).limit(limit).all()
    
    return todos, total

def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    """创建新的待办事项"""
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        due_date=todo.due_date
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate) -> Optional[models.Todo]:
    """更新待办事项"""
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    
    # 如果状态改为完成，设置完成时间
    if "is_completed" in update_data:
        if update_data["is_completed"]:
            update_data["completed_at"] = datetime.now()
        else:
            update_data["completed_at"] = None
    
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

def toggle_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    """切换待办事项完成状态"""
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    db_todo.is_completed = not db_todo.is_completed
    if db_todo.is_completed:
        db_todo.completed_at = datetime.now()
    else:
        db_todo.completed_at = None
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int) -> bool:
    """删除待办事项"""
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    
    db.delete(db_todo)
    db.commit()
    return True

def batch_delete_completed(db: Session) -> int:
    """批量删除已完成的待办事项"""
    deleted_count = db.query(models.Todo).filter(models.Todo.is_completed == True).count()
    db.query(models.Todo).filter(models.Todo.is_completed == True).delete()
    db.commit()
    return deleted_count

def batch_delete_all(db: Session) -> int:
    """批量删除所有待办事项"""
    deleted_count = db.query(models.Todo).count()
    db.query(models.Todo).delete()
    db.commit()
    return deleted_count

def batch_complete_all(db: Session) -> int:
    """批量完成所有未完成的待办事项"""
    updated_count = db.query(models.Todo).filter(models.Todo.is_completed == False).count()
    db.query(models.Todo).filter(models.Todo.is_completed == False).update({
        models.Todo.is_completed: True,
        models.Todo.completed_at: datetime.now()
    })
    db.commit()
    return updated_count

def get_todos_stats(db: Session) -> dict:
    """获取待办事项统计信息"""
    total = db.query(models.Todo).count()
    completed = db.query(models.Todo).filter(models.Todo.is_completed == True).count()
    pending = total - completed
    
    # 计算过期任务数量
    now = datetime.now()
    overdue = db.query(models.Todo).filter(
        and_(
            models.Todo.is_completed == False,
            models.Todo.due_date < now
        )
    ).count()
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue
    }
