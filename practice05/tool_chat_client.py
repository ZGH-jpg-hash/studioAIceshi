import os
import time
import json
import http.client
from urllib.parse import urlparse
import subprocess
import re

# 读取 .env 文件
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        print(f"❌ 错误: .env 文件不存在，请放在当前脚本同一文件夹下")
        return None
    
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    # 增加关键配置检查
    required_vars = ['BASE_URL', 'MODEL', 'API_KEY']
    missing = [var for var in required_vars if var not in env_vars]
    if missing:
        print(f"❌ 错误: .env 文件缺少以下必填配置：{', '.join(missing)}")
        return None
    
    return env_vars

# ====================== 工具函数 ======================
def list_files(directory):
    try:
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                file_info = {
                    "name": item,
                    "size": os.path.getsize(item_path),
                    "last_modified": os.path.getmtime(item_path),
                    "is_file": True
                }
            else:
                file_info = {"name": item, "is_file": False}
            files.append(file_info)
        return json.dumps({"success": True, "files": files}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def rename_file(directory, old_name, new_name):
    try:
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            return json.dumps({"success": True, "message": f"文件已重命名为 {new_name}"}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "文件不存在"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def delete_file(directory, file_name):
    try:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return json.dumps({"success": True, "message": "文件已删除"}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "文件不存在"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def create_file(directory, file_name, content=""):
    try:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({"success": True, "message": f"文件 {file_name} 已创建成功"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def read_file(directory, file_name):
    try:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return json.dumps({"success": True, "content": content}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "文件不存在"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def curl_request(url):
    try:
        result = subprocess.run(['curl', '-s', url], capture_output=True, timeout=30)
        if result.returncode == 0:
            try:
                content = result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                content = result.stdout.decode('gbk', errors='replace')
            return json.dumps({"success": True, "content": content}, ensure_ascii=False)
        else:
            try:
                error = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                error = result.stderr.decode('gbk', errors='replace')
            return json.dumps({"success": False, "error": error}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

# ====================== Skills 相关函数 ======================
def list_available_skills():
    """
    读取本项目目录下的 .agents/skills 目录中的所有技能
    返回包含 name 和 description 的 JSON 格式数据
    """
    try:
        skills_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.agents', 'skills')
        
        if not os.path.exists(skills_dir):
            return json.dumps({"success": True, "skills": []}, ensure_ascii=False)
        
        skills = []
        
        for item in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, item)
            if os.path.isdir(skill_path):
                skill_file = os.path.join(skill_path, 'SKILL.md')
                if os.path.exists(skill_file):
                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取 YAML front matter
                        front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                        if front_matter_match:
                            front_matter = front_matter_match.group(1)
                            
                            # 解析 name 和 description
                            name_match = re.search(r'name:\s*(.+)', front_matter)
                            desc_match = re.search(r'description:\s*(.+)', front_matter)
                            
                            if name_match:
                                skill_name = name_match.group(1).strip().strip('"\'')
                                skill_desc = desc_match.group(1).strip().strip('"\'') if desc_match else ""
                                
                                skills.append({
                                    "name": skill_name,
                                    "description": skill_desc
                                })
                    except Exception as e:
                        print(f"⚠️  读取技能 {item} 失败: {str(e)}")
                        continue
        
        return json.dumps({"success": True, "skills": skills}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def load_skill_content(skill_name):
    """
    加载指定技能的 SKILL.md 文件正文内容（YAML front matter 之后的部分）
    """
    try:
        skills_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.agents', 'skills')
        
        if not os.path.exists(skills_dir):
            return json.dumps({"success": False, "error": "skills 目录不存在"}, ensure_ascii=False)
        
        for item in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, item)
            if os.path.isdir(skill_path):
                skill_file = os.path.join(skill_path, 'SKILL.md')
                if os.path.exists(skill_file):
                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取 YAML front matter
                        front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                        if front_matter_match:
                            front_matter = front_matter_match.group(1)
                            
                            # 检查 name 是否匹配
                            name_match = re.search(r'name:\s*(.+)', front_matter)
                            if name_match:
                                extracted_name = name_match.group(1).strip().strip('"\'')
                                if extracted_name == skill_name:
                                    # 返回正文内容（YAML front matter 之后的部分）
                                    body_content = content[front_matter_match.end():]
                                    return json.dumps({"success": True, "content": body_content}, ensure_ascii=False)
                    except Exception as e:
                        continue
        
        return json.dumps({"success": False, "error": f"未找到名为 {skill_name} 的技能"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

# ====================== 工具定义 ======================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "列出本地电脑指定目录下的所有文件和文件夹，仅当用户明确提到本地文件、电脑文件夹、磁盘路径时使用",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "要列出的本地目录路径，例如 D:\\\\test"
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "在本地电脑指定目录下创建一个新文件并写入内容，仅用于本地文件操作",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "本地文件所在的目录路径"
                    },
                    "file_name": {
                        "type": "string",
                        "description": "要创建的本地文件名，例如 test.txt"
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入文件的内容，默认为空字符串",
                        "default": ""
                    }
                },
                "required": ["directory", "file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "删除本地电脑指定目录下的指定文件，仅用于本地文件操作",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "本地文件所在的目录路径"
                    },
                    "file_name": {
                        "type": "string",
                        "description": "要删除的本地文件名"
                    }
                },
                "required": ["directory", "file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rename_file",
            "description": "重命名本地电脑指定目录下的文件，仅用于本地文件操作",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "本地文件所在的目录路径"
                    },
                    "old_name": {
                        "type": "string",
                        "description": "原本地文件名"
                    },
                    "new_name": {
                        "type": "string",
                        "description": "新本地文件名"
                    }
                },
                "required": ["directory", "old_name", "new_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取本地电脑指定目录下文件的内容，仅用于本地文件操作",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "本地文件所在的目录路径"
                    },
                    "file_name": {
                        "type": "string",
                        "description": "要读取的本地文件名"
                    }
                },
                "required": ["directory", "file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "curl_request",
            "description": "访问指定的网页URL并返回内容，用于网络请求",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "要访问的网页URL，例如 https://www.baidu.com"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "load_skill_content",
            "description": "加载指定技能的详细内容。当用户请求需要使用某个技能时，调用此函数获取该技能的完整说明",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "要加载的技能名称，例如 notice"
                    }
                },
                "required": ["skill_name"]
            }
        }
    }
]

# ====================== 系统提示词（LMStudio兼容版） ======================
def build_system_prompt(user_info, skills_json=None):
    skills_info = ""
    if skills_json:
        skills_info = f"\n\n【可用技能列表】\n{skills_json}\n\n【技能使用规则】\n- 当用户的请求与某个技能的描述匹配时，必须先调用 load_skill_content 函数加载该技能的完整内容\n- 加载技能内容后，严格按照技能的规则和要求执行任务\n- 不要猜测技能的规则，必须通过 load_skill_content 获取准确信息"
    
    return f"""【最高优先级规则】
1.  绝对禁止提及"通义千问"、"阿里巴巴"、"我是AI助手"
2.  用户叫{user_info}
3.  回答必须完全贴合用户问题，不能答非所问
4.  不能在回复中提及任何工具相关内容、接口、代码、日志底层信息
5.  用户问"我是谁"时，必须回答"你是{user_info}"
6.  用户问"你是谁"时，回答要友好自然
{skills_info}

【🔴 工具调用规则】
- 只有当用户明确提到"本地文件"、"电脑文件夹"、"D盘"、"C盘"时，才能使用本地文件工具
- 工具返回结果后，你**必须**直接把result字段的内容整理成通顺的中文回复用户
- 若工具返回失败，直接把result字段的错误信息告诉用户

【⚠️ 重要：LMStudio兼容说明】
- 当你看到工具返回的结果时，**必须立即生成回答**，不要再次调用工具
- 不要忽略工具返回的内容，必须基于工具结果进行回复
"""

# ====================== 流式调用（修复LMStudio兼容问题） ======================
def call_llm_stream(env_vars, messages, user_info, is_tool_result=False):
    start_time = time.time()
    url = urlparse(env_vars['BASE_URL'])
    host = url.netloc
    path = "/v1/chat/completions"

    # 获取技能列表
    skills_result = list_available_skills()
    skills_data = json.loads(skills_result)
    skills_json = None
    if skills_data.get("success"):
        skills_list = skills_data.get("skills", [])
        if skills_list:
            skills_json = json.dumps({"skills": skills_list}, ensure_ascii=False, indent=2)

    # LMStudio兼容：使用system角色发送系统提示
    system_msg = {"role": "system", "content": build_system_prompt(user_info, skills_json)}
    final_messages = [system_msg] + messages

    data = {
        "model": env_vars["MODEL"],
        "messages": final_messages,
        "tools": TOOLS if not is_tool_result else None,
        "tool_choice": "auto" if not is_tool_result else "none",
        "temperature": 0.1,
        "max_tokens": int(env_vars.get("MAX_TOKENS", 2048)),
        "stream": True
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {env_vars.get('API_KEY', '')}"
    }

    timeout = int(env_vars.get('TIMEOUT', '180'))
    if url.scheme == 'https':
        conn = http.client.HTTPSConnection(host, timeout=timeout)
    else:
        conn = http.client.HTTPConnection(host, timeout=timeout)

    full_content = ""
    tool_calls = []

    try:
        conn.request("POST", path, json.dumps(data), headers)
        response = conn.getresponse()

        if not is_tool_result:
            print("AI 正在思考...", end="", flush=True)
        else:
            print("AI 正在整理回答...", end="", flush=True)

        for line in response.fp:
            line = line.decode("utf-8").strip()
            if not line: continue
            if line.startswith("data: "):
                data_part = line[6:]
                if data_part == "[DONE]": break
                try:
                    jd = json.loads(data_part)
                    delta = jd["choices"][0]["delta"]
                    
                    if "content" in delta and delta["content"]:
                        token = delta["content"]
                        full_content += token
                        if not tool_calls:
                            if not full_content or len(full_content) == len(token):
                                print("\r" + " " * 20 + "\r", end="", flush=True)
                                print("AI 回复：", end="", flush=True)
                            print(token, end="", flush=True)
                    
                    if not is_tool_result and "tool_calls" in delta and delta["tool_calls"]:
                        for tc in delta["tool_calls"]:
                            index = tc["index"]
                            if index >= len(tool_calls):
                                tool_calls.append({
                                    "id": tc.get("id", ""),
                                    "type": "function",
                                    "function": {
                                        "name": "",
                                        "arguments": ""
                                    }
                                })
                            if "function" in tc:
                                if "name" in tc["function"]:
                                    tool_calls[index]["function"]["name"] += tc["function"]["name"]
                                if "arguments" in tc["function"]:
                                    tool_calls[index]["function"]["arguments"] += tc["function"]["arguments"]
                except:
                    continue

        print("\n")
    except Exception as e:
        print(f"\n❌ 连接失败：{str(e)}")
        return None, None, 0, 0, 0
    finally:
        conn.close()

    duration = time.time() - start_time
    total_tokens = len(full_content) // 3
    speed = total_tokens / duration if duration > 0 else 0

    return full_content, tool_calls, total_tokens, duration, speed

# ====================== 非流式调用（专门用于压缩聊天记录） ======================
def call_llm_non_stream(env_vars, messages):
    start_time = time.time()
    url = urlparse(env_vars['BASE_URL'])
    host = url.netloc
    path = "/v1/chat/completions"

    data = {
        "model": env_vars["MODEL"],
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 500,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {env_vars.get('API_KEY', '')}"
    }

    timeout = int(env_vars.get('TIMEOUT', '180'))
    if url.scheme == 'https':
        conn = http.client.HTTPSConnection(host, timeout=timeout)
    else:
        conn = http.client.HTTPConnection(host, timeout=timeout)

    full_content = ""
    try:
        conn.request("POST", path, json.dumps(data), headers)
        response = conn.getresponse()
        response_data = json.loads(response.read().decode('utf-8'))
        if "choices" in response_data and len(response_data["choices"]) > 0:
            full_content = response_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ 压缩失败：{str(e)}")
        return ""
    finally:
        conn.close()

    return full_content

# ====================== 计算聊天上下文长度 ======================
def calculate_context_length(messages):
    total_chars = 0
    for msg in messages:
        total_chars += len(msg.get("content", ""))
    return total_chars

# ====================== 压缩聊天记录 ======================
def compress_chat_history(env_vars, messages):
    if len(messages) < 6:
        return messages
    
    context_length = calculate_context_length(messages)
    if context_length < 3000:
        return messages
    
    print("\n📊 聊天记录较长，正在智能压缩...")
    
    split_point = int(len(messages) * 0.7)
    messages_to_compress = messages[:split_point]
    messages_to_keep = messages[split_point:]
    
    compression_prompt = [{"role": "system", "content": "请将以下对话历史压缩成一段简洁的摘要，保留关键信息和上下文。"}] + messages_to_compress
    
    summary = call_llm_non_stream(env_vars, compression_prompt)
    
    if summary:
        compressed_messages = [{"role": "system", "content": f"【历史对话摘要】{summary}"}] + messages_to_keep
        print(f"✅ 压缩完成：{len(messages)} 条消息 → {len(compressed_messages)} 条消息")
        return compressed_messages
    else:
        print("⚠️  压缩失败，保留原始记录")
        return messages

# ====================== 执行工具调用 ======================
def execute_tool_call(tool_call):
    function_name = tool_call["function"]["name"]
    function_args = json.loads(tool_call["function"]["arguments"])
    
    function_map = {
        "list_files": list_files,
        "create_file": create_file,
        "delete_file": delete_file,
        "rename_file": rename_file,
        "read_file": read_file,
        "curl_request": curl_request,
        "load_skill_content": load_skill_content
    }
    
    if function_name in function_map:
        return function_map[function_name](**function_args)
    else:
        return json.dumps({"success": False, "error": f"未知工具: {function_name}"}, ensure_ascii=False)

# ====================== 主循环 ======================
def main():
    print("=== 本地大模型工具助手（支持Skills） ===")
    print("输入 'quit' 或 'exit' 退出\n")
    
    env_vars = load_env()
    if not env_vars:
        return
    
    user_info = input("请输入你的名字：").strip()
    if not user_info:
        user_info = "用户"
    
    messages = []
    
    while True:
        try:
            user_input = input("\n你：").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            
            if not user_input:
                continue
            
            messages.append({"role": "user", "content": user_input})
            
            messages = compress_chat_history(env_vars, messages)
            
            full_content, tool_calls, total_tokens, duration, speed = call_llm_stream(env_vars, messages, user_info)
            
            if tool_calls:
                tool_results = []
                for tool_call in tool_calls:
                    result = execute_tool_call(tool_call)
                    tool_results.append({
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "content": result
                    })
                
                messages.append({"role": "assistant", "content": full_content if full_content else ""})
                messages.extend(tool_results)
                
                full_content, _, total_tokens, duration, speed = call_llm_stream(env_vars, messages, user_info, is_tool_result=True)
            
            if full_content:
                messages.append({"role": "assistant", "content": full_content})
                
                print(f"\n📊 统计信息：{total_tokens} tokens | {duration:.2f}秒 | {speed:.1f} tokens/秒")
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误：{str(e)}")
            continue

if __name__ == "__main__":
    main()
