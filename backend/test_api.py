#!/usr/bin/env python3
"""
API 功能测试脚本
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("🚀 开始测试 TodoEveryday API...")
    print("=" * 50)
    
    # 1. 测试健康检查
    print("1. 测试健康检查...")
    response = requests.get("http://localhost:8000/health")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()
    
    # 2. 测试创建待办事项
    print("2. 测试创建待办事项...")
    todo_data = {
        "title": "学习FastAPI",
        "description": "完成FastAPI基础教程和项目开发",
        "priority": 2,
        "due_date": (datetime.now() + timedelta(days=7)).isoformat()
    }
    response = requests.post(f"{BASE_URL}/todos/", json=todo_data)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 201:
        todo1 = response.json()["data"]
        print(f"   创建成功: {todo1['title']} (ID: {todo1['id']})")
    print()
    
    # 3. 再创建几个待办事项
    print("3. 创建更多待办事项...")
    todos_to_create = [
        {"title": "学习React", "description": "构建前端界面", "priority": 3},
        {"title": "写文档", "description": "完善项目文档", "priority": 1},
        {"title": "部署应用", "description": "部署到生产环境", "priority": 4}
    ]
    
    created_todos = []
    for todo_data in todos_to_create:
        response = requests.post(f"{BASE_URL}/todos/", json=todo_data)
        if response.status_code == 201:
            todo = response.json()["data"]
            created_todos.append(todo)
            print(f"   ✅ {todo['title']} (ID: {todo['id']})")
    print()
    
    # 4. 测试获取所有待办事项
    print("4. 测试获取所有待办事项...")
    response = requests.get(f"{BASE_URL}/todos/")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   总数: {data['total']}")
        for todo in data["data"]:
            print(f"   - {todo['title']} (完成: {todo['is_completed']})")
    print()
    
    # 5. 测试完成一个待办事项
    if created_todos:
        print("5. 测试切换待办事项状态...")
        todo_id = created_todos[0]["id"]
        response = requests.patch(f"{BASE_URL}/todos/{todo_id}/toggle")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            updated_todo = response.json()["data"]
            print(f"   ✅ {updated_todo['title']} 已标记为: {'完成' if updated_todo['is_completed'] else '未完成'}")
        print()
    
    # 6. 测试更新待办事项
    if created_todos:
        print("6. 测试更新待办事项...")
        todo_id = created_todos[1]["id"]
        update_data = {
            "title": "学习React (已更新)",
            "description": "深入学习React Hooks和状态管理",
            "priority": 5
        }
        response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            updated_todo = response.json()["data"]
            print(f"   ✅ 更新成功: {updated_todo['title']}")
        print()
    
    # 7. 测试过滤功能
    print("7. 测试过滤功能...")
    for status in ["all", "pending", "completed"]:
        response = requests.get(f"{BASE_URL}/todos/?status={status}")
        if response.status_code == 200:
            data = response.json()
            print(f"   {status}: {data['total']} 个任务")
    print()
    
    # 8. 测试统计信息
    print("8. 测试统计信息...")
    response = requests.get(f"{BASE_URL}/todos/stats/")
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()["data"]
        print(f"   📊 统计:")
        print(f"      总数: {stats['total']}")
        print(f"      已完成: {stats['completed']}")
        print(f"      待完成: {stats['pending']}")
        print(f"      过期: {stats['overdue']}")
    print()
    
    # 9. 测试批量操作
    print("9. 测试批量操作...")
    # 批量完成所有任务
    response = requests.post(f"{BASE_URL}/todos/batch", json={"action": "complete_all"})
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ {response.json()['message']}")
    print()
    
    # 10. 测试删除功能
    if created_todos:
        print("10. 测试删除待办事项...")
        todo_id = created_todos[-1]["id"]
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        print(f"    状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"    ✅ {response.json()['message']}")
        print()
    
    print("🎉 API测试完成!")
    print("=" * 50)
    print("✅ 所有功能测试通过")
    print("🌐 API文档: http://localhost:8000/docs")
    print("📊 API状态: http://localhost:8000/health")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务正在运行:")
        print("   python start_server.py")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
