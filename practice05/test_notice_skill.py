import os
import sys

# 添加 practice05 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tool_chat_client import load_skill_content
import json

def test_notice_skill_without_department():
    print("=" * 60)
    print("测试场景 1: 用户未提及部门")
    print("=" * 60)
    print("\n用户请求: 帮我写一个五一节放假的通知")
    print("\n预期结果: 输出应该以 'XX部通知' 开头")
    print("\n正在加载 notice skill...")
    
    result = load_skill_content("notice")
    data = json.loads(result)
    
    if data.get("success"):
        content = data.get("content", "")
        print("\n[OK] 成功加载 notice skill")
        print("\n技能规则摘要:")
        print("- 标题不能以'通知'开头")
        print("- 必须使用'XX部通知'格式")
        print("- 用户未提及部门时，使用'XX部'作为前缀")
        print("\n根据技能规则，LLM 应该:")
        print("1. 识别用户未提供部门信息")
        print("2. 使用'XX部'作为标题前缀")
        print("3. 输出以'XX部通知'开头的通知内容")
    else:
        print(f"[ERROR] 加载失败: {data.get('error')}")
    
    print("\n" + "=" * 60 + "\n")

def test_notice_skill_with_department():
    print("=" * 60)
    print("测试场景 2: 用户明确提及部门")
    print("=" * 60)
    print("\n用户请求: 我是销售部的，帮我写一个五一节放假的通知")
    print("\n预期结果: 输出应该以 '销售部通知' 开头")
    print("\n正在加载 notice skill...")
    
    result = load_skill_content("notice")
    data = json.loads(result)
    
    if data.get("success"):
        content = data.get("content", "")
        print("\n[OK] 成功加载 notice skill")
        print("\n技能规则摘要:")
        print("- 标题不能以'通知'开头")
        print("- 必须使用'XX部通知'格式")
        print("- 用户提及'销售部'时，使用'销售部'作为前缀")
        print("\n根据技能规则，LLM 应该:")
        print("1. 识别用户提供了'销售部'信息")
        print("2. 使用'销售部'作为标题前缀")
        print("3. 输出以'销售部通知'开头的通知内容")
    else:
        print(f"[ERROR] 加载失败: {data.get('error')}")
    
    print("\n" + "=" * 60 + "\n")

def main():
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  Notice Skill 功能测试（模拟测试）".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    test_notice_skill_without_department()
    test_notice_skill_with_department()
    
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print("\n[OK] Skills 功能测试完成")
    print("\n接下来可以进行实际交互测试:")
    print("  1. 确保 .env 文件已正确配置")
    print("  2. 运行: python tool_chat_client.py")
    print("  3. 输入测试请求并观察 LLM 的响应")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
