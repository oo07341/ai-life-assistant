#!/usr/bin/env python3
"""
测试智能搜索API功能
"""

import requests
import json

def test_search_api():
    """测试搜索API"""
    url = "http://localhost:3001/api/search"
    headers = {"Content-Type": "application/json"}
    
    test_cases = [
        {"query": "我想吃披萨"},
        {"query": "帮我制定考研计划"},
        {"query": "明天下午3点开会提醒"},
        {"query": "附近有什么好吃的"},
    ]
    
    print("=== 测试智能搜索API ===")
    print(f"后端地址: {url}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case['query']}")
        try:
            response = requests.post(url, headers=headers, json=test_case, timeout=10)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  响应格式: {type(data)}")
                
                # 检查响应结构
                if isinstance(data, dict):
                    if "intent" in data:
                        intent = data["intent"]
                        print(f"  意图分析: {intent.get('intent', '未知')}")
                        
                        if intent.get("intent") == "shopping":
                            print(f"  商品关键词: {intent.get('product_keywords', [])}")
                            print(f"  位置偏好: {intent.get('location_hint', '不限')}")
                        elif intent.get("intent") == "schedule":
                            schedule_info = intent.get("schedule_info", {})
                            print(f"  目标: {schedule_info.get('goal', '未知')}")
                    
                    if "deals" in data:
                        deals = data["deals"]
                        print(f"  比价结果数量: {len(deals)}")
                        if deals:
                            print(f"  第一个商品: {deals[0].get('name', '未知')}")
                            print(f"  价格: ¥{deals[0].get('price', 0)}")
                    
                    if "hot_keywords" in data:
                        print(f"  热门关键词: {data['hot_keywords'][:3]}...")
                
                print(f"  响应大小: {len(response.content)} bytes")
            else:
                print(f"  错误响应: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print("  错误: 无法连接到后端服务")
        except requests.exceptions.Timeout:
            print("  错误: 请求超时")
        except Exception as e:
            print(f"  错误: {type(e).__name__}: {str(e)}")
        
        print()

def test_backend_health():
    """测试后端健康状态"""
    print("=== 测试后端健康状态 ===")
    
    try:
        response = requests.get("http://localhost:3001/", timeout=5)
        print(f"后端根端点状态: {response.status_code}")
        if response.status_code == 200:
            print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"后端健康检查失败: {e}")

def test_frontend_connection():
    """测试前端连接"""
    print("\n=== 测试前端连接 ===")
    
    try:
        response = requests.get("http://localhost:5175/", timeout=5)
        print(f"前端状态: {response.status_code}")
        print(f"前端标题: {'喂来日程' if '喂来日程' in response.text else '未找到标题'}")
    except Exception as e:
        print(f"前端连接失败: {e}")

if __name__ == "__main__":
    print("AI生活助手系统测试")
    print("=" * 50)
    
    test_backend_health()
    test_search_api()
    test_frontend_connection()
    
    print("\n" + "=" * 50)
    print("测试完成")