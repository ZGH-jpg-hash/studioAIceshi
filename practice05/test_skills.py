import os
import sys
import json

# 添加 practice05 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tool_chat_client import list_available_skills, load_skill_content

def test_list_skills():
    print("=== 测试 1: 列出可用技能 ===")
    result = list_available_skills()
    data = json.loads(result)
    
    if data.get("success"):
        skills = data.get("skills", [])
        print(f"[OK] 成功读取到 {len(skills)} 个技能：")
        for skill in skills:
            print(f"  - {skill['name']}: {skill['description']}")
    else:
        print(f"[ERROR] 读取技能列表失败: {data.get('error')}")
    
    print()
    return data.get("success", False)

def test_load_notice_skill():
    print("=== 测试 2: 加载 notice 技能内容 ===")
    result = load_skill_content("notice")
    data = json.loads(result)
    
    if data.get("success"):
        content = data.get("content", "")
        print(f"[OK] 成功加载 notice 技能内容（共 {len(content)} 字符）")
        print("\n技能内容预览（前 200 字符）：")
        print(content[:200] + "...")
    else:
        print(f"[ERROR] 加载 notice 技能失败: {data.get('error')}")
    
    print()
    return data.get("success", False)

def main():
    print("=== Skills 功能测试 ===\n")
    
    test1_passed = test_list_skills()
    test2_passed = test_load_notice_skill()
    
    print("=== 测试总结 ===")
    if test1_passed and test2_passed:
        print("[OK] 所有测试通过！Skills 功能正常工作。")
        print("\n接下来可以运行主程序进行交互测试：")
        print("  python tool_chat_client.py")
        print("\n测试建议：")
        print("  1. 输入: '帮我写一个五一节放假的通知'")
        print("     预期: 输出以 'XX部通知' 开头")
        print("  2. 输入: '我是销售部的，帮我写一个五一节放假的通知'")
        print("     预期: 输出以 '销售部通知' 开头")
    else:
        print("[ERROR] 部分测试失败，请检查配置和文件。")

if __name__ == "__main__":
    main()
