import pytest
from datetime import datetime, timedelta

def test_root_endpoint(test_client):
    """测试根路径"""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "TodoEveryday API"
    assert data["version"] == "1.0.0"

def test_health_check(test_client):
    """测试健康检查"""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_todo(test_client, clean_db):
    """测试创建待办事项"""
    todo_data = {
        "title": "测试任务",
        "description": "这是一个测试任务",
        "priority": 2
    }
    response = test_client.post("/api/v1/todos/", json=todo_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["success"] == True
    assert data["data"]["title"] == "测试任务"
    assert data["data"]["description"] == "这是一个测试任务"
    assert data["data"]["priority"] == 2
    assert data["data"]["is_completed"] == False

def test_get_todos_empty(test_client, clean_db):
    """测试获取空的待办事项列表"""
    response = test_client.get("/api/v1/todos/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["data"] == []
    assert data["total"] == 0

def test_get_todos_with_data(test_client, clean_db):
    """测试获取有数据的待办事项列表"""
    # 先创建一些测试数据
    test_client.post("/api/v1/todos/", json={"title": "任务1"})
    test_client.post("/api/v1/todos/", json={"title": "任务2"})
    
    response = test_client.get("/api/v1/todos/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert len(data["data"]) == 2
    assert data["total"] == 2

def test_get_single_todo(test_client, clean_db):
    """测试获取单个待办事项"""
    # 先创建一个待办事项
    create_response = test_client.post("/api/v1/todos/", json={"title": "测试任务"})
    todo_id = create_response.json()["data"]["id"]
    
    # 获取这个待办事项
    response = test_client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["data"]["id"] == todo_id
    assert data["data"]["title"] == "测试任务"

def test_get_nonexistent_todo(test_client, clean_db):
    """测试获取不存在的待办事项"""
    response = test_client.get("/api/v1/todos/999")
    assert response.status_code == 404

def test_update_todo(test_client, clean_db):
    """测试更新待办事项"""
    # 先创建一个待办事项
    create_response = test_client.post("/api/v1/todos/", json={"title": "原始任务"})
    todo_id = create_response.json()["data"]["id"]
    
    # 更新这个待办事项
    update_data = {
        "title": "更新后的任务",
        "description": "新的描述",
        "priority": 3
    }
    response = test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["data"]["title"] == "更新后的任务"
    assert data["data"]["description"] == "新的描述"
    assert data["data"]["priority"] == 3

def test_toggle_todo(test_client, clean_db):
    """测试切换待办事项状态"""
    # 先创建一个待办事项
    create_response = test_client.post("/api/v1/todos/", json={"title": "测试任务"})
    todo_id = create_response.json()["data"]["id"]
    
    # 切换状态为完成
    response = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["data"]["is_completed"] == True
    assert data["data"]["completed_at"] is not None
    
    # 再次切换状态为未完成
    response = test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["data"]["is_completed"] == False
    assert data["data"]["completed_at"] is None

def test_delete_todo(test_client, clean_db):
    """测试删除待办事项"""
    # 先创建一个待办事项
    create_response = test_client.post("/api/v1/todos/", json={"title": "待删除任务"})
    todo_id = create_response.json()["data"]["id"]
    
    # 删除这个待办事项
    response = test_client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["message"] == "Todo deleted successfully"
    
    # 确认已删除
    get_response = test_client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404

def test_filter_todos_by_status(test_client, clean_db):
    """测试按状态过滤待办事项"""
    # 创建一些测试数据
    test_client.post("/api/v1/todos/", json={"title": "未完成任务1"})
    test_client.post("/api/v1/todos/", json={"title": "未完成任务2"})
    
    # 创建并完成一个任务
    create_response = test_client.post("/api/v1/todos/", json={"title": "已完成任务"})
    todo_id = create_response.json()["data"]["id"]
    test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
    
    # 测试获取所有任务
    response = test_client.get("/api/v1/todos/?status=all")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 3
    
    # 测试获取未完成任务
    response = test_client.get("/api/v1/todos/?status=pending")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
    
    # 测试获取已完成任务
    response = test_client.get("/api/v1/todos/?status=completed")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1

def test_batch_operations(test_client, clean_db):
    """测试批量操作"""
    # 创建一些测试数据
    test_client.post("/api/v1/todos/", json={"title": "任务1"})
    test_client.post("/api/v1/todos/", json={"title": "任务2"})
    
    # 完成一个任务
    create_response = test_client.post("/api/v1/todos/", json={"title": "任务3"})
    todo_id = create_response.json()["data"]["id"]
    test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
    
    # 测试批量完成所有任务
    response = test_client.post("/api/v1/todos/batch", json={"action": "complete_all"})
    assert response.status_code == 200
    assert "Completed 2 todos" in response.json()["message"]
    
    # 测试批量删除已完成任务
    response = test_client.post("/api/v1/todos/batch", json={"action": "delete_completed"})
    assert response.status_code == 200
    assert "Deleted 3 completed todos" in response.json()["message"]

def test_get_stats(test_client, clean_db):
    """测试获取统计信息"""
    # 创建一些测试数据
    test_client.post("/api/v1/todos/", json={"title": "未完成任务1"})
    test_client.post("/api/v1/todos/", json={"title": "未完成任务2"})
    
    # 创建并完成一个任务
    create_response = test_client.post("/api/v1/todos/", json={"title": "已完成任务"})
    todo_id = create_response.json()["data"]["id"]
    test_client.patch(f"/api/v1/todos/{todo_id}/toggle")
    
    # 获取统计信息
    response = test_client.get("/api/v1/todos/stats/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert data["data"]["total"] == 3
    assert data["data"]["completed"] == 1
    assert data["data"]["pending"] == 2
    assert data["data"]["overdue"] == 0

def test_pagination(test_client, clean_db):
    """测试分页功能"""
    # 创建10个待办事项
    for i in range(10):
        test_client.post("/api/v1/todos/", json={"title": f"任务{i+1}"})
    
    # 测试第一页，每页5个
    response = test_client.get("/api/v1/todos/?page=1&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] == True
    assert len(data["data"]) == 5
    assert data["total"] == 10
    assert data["page"] == 1
    assert data["limit"] == 5
    
    # 测试第二页
    response = test_client.get("/api/v1/todos/?page=2&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["data"]) == 5
    assert data["page"] == 2

def test_validation_errors(test_client, clean_db):
    """测试数据验证错误"""
    # 测试空标题
    response = test_client.post("/api/v1/todos/", json={"title": ""})
    assert response.status_code == 422
    
    # 测试无效优先级
    response = test_client.post("/api/v1/todos/", json={"title": "测试", "priority": 10})
    assert response.status_code == 422
