import requests
import json

def test_full_stack_integration():
    """测试前后端集成功能"""
    
    print("🚀 TodoEveryday 全栈集成测试")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. 测试后端健康检查
        print("\n1. 测试后端连接...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("   ✅ 后端API服务正常运行")
        else:
            print("   ❌ 后端API服务异常")
            return False
        
        # 2. 测试创建任务
        print("\n2. 测试创建任务...")
        task_data = {
            "title": "前后端集成测试任务",
            "description": "验证前后端API连接正常",
            "priority": 3
        }
        create_response = requests.post(f"{base_url}/api/v1/todos/", json=task_data, timeout=5)
        if create_response.status_code == 201:
            task = create_response.json()['data']
            task_id = task['id']
            print(f"   ✅ 任务创建成功 (ID: {task_id})")
        else:
            print("   ❌ 任务创建失败")
            return False
        
        # 3. 测试获取任务
        print("\n3. 测试获取任务列表...")
        get_response = requests.get(f"{base_url}/api/v1/todos/", timeout=5)
        if get_response.status_code == 200:
            todos = get_response.json()['data']
            print(f"   ✅ 获取任务列表成功 (共{len(todos)}个任务)")
        else:
            print("   ❌ 获取任务列表失败")
            return False
        
        # 4. 测试切换状态
        print("\n4. 测试切换任务状态...")
        toggle_response = requests.patch(f"{base_url}/api/v1/todos/{task_id}/toggle/", timeout=5)
        if toggle_response.status_code == 200:
            print("   ✅ 任务状态切换成功")
        else:
            print("   ❌ 任务状态切换失败")
            return False
        
        # 5. 测试统计信息
        print("\n5. 测试获取统计信息...")
        stats_response = requests.get(f"{base_url}/api/v1/todos/stats/", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()['data']
            print(f"   ✅ 统计信息获取成功")
            print(f"      总任务: {stats['total']}")
            print(f"      已完成: {stats['completed']}")
            print(f"      待完成: {stats['pending']}")
        else:
            print("   ❌ 统计信息获取失败")
            return False
        
        # 6. 清理测试数据
        print("\n6. 清理测试数据...")
        delete_response = requests.delete(f"{base_url}/api/v1/todos/{task_id}/", timeout=5)
        if delete_response.status_code == 200:
            print("   ✅ 测试数据清理成功")
        else:
            print("   ⚠️ 测试数据清理失败，请手动删除")
        
        print("\n🎉 全栈集成测试完成!")
        print("=" * 50)
        print("✅ 所有测试通过")
        print()
        print("📋 访问地址:")
        print(f"   前端应用: http://localhost:5174")
        print(f"   API文档:  http://localhost:8000/docs")
        print(f"   API健康:  http://localhost:8000/health")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ 无法连接到后端服务")
        print("   💡 请确保后端服务运行在 http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ 请求超时")
        return False
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    test_full_stack_integration()
