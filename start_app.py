#!/usr/bin/env python3
"""
TodoEveryday 全栈应用启动脚本
自动启动前端和后端服务，并进行健康检查
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def check_port(port, service_name):
    """检查端口是否被占用"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return True
    except:
        return False

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端API服务...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ 未找到backend目录")
        return None
    
    os.chdir(backend_dir)
    
    # 设置Python路径
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd().absolute())
    
    # 启动后端服务
    try:
        process = subprocess.Popen([
            sys.executable, "start_server.py"
        ], env=env)
        
        # 等待服务启动
        print("   等待后端服务启动...")
        for i in range(30):  # 最多等待30秒
            if check_port(8000, "后端"):
                print("   ✅ 后端API服务启动成功 (http://localhost:8000)")
                os.chdir("..")
                return process
            time.sleep(1)
        
        print("   ❌ 后端服务启动超时")
        process.terminate()
        os.chdir("..")
        return None
        
    except Exception as e:
        print(f"   ❌ 启动后端服务失败: {e}")
        os.chdir("..")
        return None

def start_frontend():
    """启动前端服务"""
    print("🎨 启动前端开发服务...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ 未找到frontend目录")
        return None
    
    os.chdir(frontend_dir)
    
    # 检查node_modules是否存在
    if not Path("node_modules").exists():
        print("   📦 安装前端依赖...")
        result = subprocess.run(["npm", "install"], capture_output=True, text=True)
        if result.returncode != 0:
            print("   ❌ 前端依赖安装失败")
            os.chdir("..")
            return None
        print("   ✅ 前端依赖安装完成")
    
    # 启动前端服务
    try:
        process = subprocess.Popen([
            "npx", "vite", "dev", "--host", "localhost", "--port", "5174"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务启动
        print("   等待前端服务启动...")
        for i in range(20):  # 最多等待20秒
            if check_port(5174, "前端"):
                print("   ✅ 前端开发服务启动成功 (http://localhost:5174)")
                os.chdir("..")
                return process
            time.sleep(1)
        
        print("   ❌ 前端服务启动超时")
        process.terminate()
        os.chdir("..")
        return None
        
    except Exception as e:
        print(f"   ❌ 启动前端服务失败: {e}")
        os.chdir("..")
        return None

def run_health_check():
    """运行健康检查"""
    print("🔍 执行健康检查...")
    
    try:
        # 检查后端API
        backend_response = requests.get("http://localhost:8000/health", timeout=5)
        if backend_response.status_code == 200:
            print("   ✅ 后端API健康检查通过")
        else:
            print("   ❌ 后端API健康检查失败")
            return False
        
        # 检查前端应用
        frontend_response = requests.get("http://localhost:5174", timeout=5)
        if frontend_response.status_code == 200:
            print("   ✅ 前端应用健康检查通过")
        else:
            print("   ❌ 前端应用健康检查失败")
            return False
        
        # 测试API连接
        api_response = requests.get("http://localhost:8000/api/v1/todos/stats/", timeout=5)
        if api_response.status_code == 200:
            stats = api_response.json()['data']
            print(f"   ✅ API连接测试通过 (总任务: {stats['total']})")
        else:
            print("   ❌ API连接测试失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ 健康检查异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 TodoEveryday 全栈应用启动器")
    print("=" * 60)
    
    # 检查当前目录
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ 请在TodoEveryday项目根目录下运行此脚本")
        sys.exit(1)
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        print("❌ 后端服务启动失败，退出")
        sys.exit(1)
    
    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ 前端服务启动失败，正在关闭后端...")
        backend_process.terminate()
        sys.exit(1)
    
    # 健康检查
    time.sleep(2)  # 等待服务完全启动
    if not run_health_check():
        print("❌ 健康检查失败，正在关闭服务...")
        frontend_process.terminate()
        backend_process.terminate()
        sys.exit(1)
    
    # 显示访问信息
    print("\n" + "=" * 60)
    print("🎉 TodoEveryday 应用启动完成!")
    print("=" * 60)
    print("📋 访问地址:")
    print("   🌐 前端应用:  http://localhost:5174")
    print("   📚 API文档:   http://localhost:8000/docs")
    print("   💚 健康检查:  http://localhost:8000/health")
    print("   🔄 API状态:   http://localhost:8000/api/v1/todos/stats/")
    print("\n📖 使用指南:")
    print("   - 在前端应用中创建、管理您的待办事项")
    print("   - 使用API文档测试后端功能")
    print("   - 按 Ctrl+C 停止所有服务")
    print("=" * 60)
    
    try:
        # 保持脚本运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 正在停止服务...")
        frontend_process.terminate()
        backend_process.terminate()
        print("✅ 所有服务已停止")
        print("👋 感谢使用 TodoEveryday!")

if __name__ == "__main__":
    main()
