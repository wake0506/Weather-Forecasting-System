#!/usr/bin/env python3
print("=== 开始测试 ===")

# 测试基础导入
try:
    import requests
    print("✅ requests 导入成功")
except ImportError as e:
    print(f"❌ requests 导入失败: {e}")

try:
    import os
    from dotenv import load_dotenv
    print("✅ dotenv 导入成功")
except ImportError as e:
    print(f"❌ dotenv 导入失败: {e}")

print("=== 测试完成 ===")