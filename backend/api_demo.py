import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🚀 TodoEveryday API 功能展示")
    print("=" * 50)
    
    # 1. 健康检查
    print("\n1. 健康检查:")
    response = requests.get(f"{base_url}/health")
    print(f"   状态: {response.json()}")
    
    # 2. 获取所有待办事项
    print("\n2. 当前所有待办事项:")
    response = requests.get(f"{base_url}/api/v1/todos")
    if response.status_code == 200:
        data = response.json()
        todos = data['data']
        print(f"   总数: {data['total']}")
        for todo in todos:
            status = "✅" if todo['is_completed'] else "❌"
            print(f"   {status} {todo['title']} (优先级: {todo['priority']})")
    
    # 3. 创建新的待办事项
    print("\n3. 创建新的待办事项:")
    new_todo = {
        "title": "完成前端React开发",
        "description": "创建现代化的React前端界面",
        "priority": 5
    }
    response = requests.post(f"{base_url}/api/v1/todos", json=new_todo)
    if response.status_code == 201:
        todo = response.json()['data']
        print(f"   ✅ 创建成功: {todo['title']} (ID: {todo['id']})")
    
    # 4. 获取统计信息
    print("\n4. 统计信息:")
    response = requests.get(f"{base_url}/api/v1/todos/stats/")
    if response.status_code == 200:
        stats = response.json()['data']
        print(f"   📊 总任务: {stats['total']}")
        print(f"   ✅ 已完成: {stats['completed']}")
        print(f"   ❌ 待完成: {stats['pending']}")
        print(f"   ⏰ 过期: {stats['overdue']}")
    
    # 5. 测试过滤功能
    print("\n5. 过滤功能测试:")
    for status in ['pending', 'completed']:
        response = requests.get(f"{base_url}/api/v1/todos?status={status}")
        if response.status_code == 200:
            count = response.json()['total']
            print(f"   {status.capitalize()}: {count} 个任务")
    
    print("\n🎉 API展示完成!")
    print(f"📖 API文档: {base_url}/docs")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 错误: {e}")
