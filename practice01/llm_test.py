import os
import time
import json
import http.client
from urllib.parse import urlparse

# 读取.env文件
def load_env():
    """从项目根目录的.env文件加载环境变量"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_path):
        print(f"错误: .env文件不存在，请从env.example复制并填写正确参数")
        return None
    
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars

# 调用LLM API
def call_llm(env_vars, prompt):
    """使用标准HTTP库调用LLM API"""
    start_time = time.time()
    
    # 解析URL
    url = urlparse(env_vars['BASE_URL'])
    host = url.netloc
    path = f"{url.path.rstrip('/')}/api/v1/chat"
    
    # 准备请求数据
    data = {
        "model": env_vars['MODEL'],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": float(env_vars.get('TEMPERATURE', '0.7')),
        "max_tokens": int(env_vars.get('MAX_TOKENS', '1000')),
        "stream": False
    }
    
    # 准备请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {env_vars['API_KEY']}"
    }
    
    # 发送请求
    conn = http.client.HTTPSConnection(host, timeout=int(env_vars.get('TIMEOUT', '30')))
    try:
        conn.request('POST', path, json.dumps(data), headers)
        response = conn.getresponse()
        response_data = response.read().decode('utf-8')
        response_json = json.loads(response_data)
    finally:
        conn.close()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # 解析响应
    if 'error' in response_json:
        print(f"API错误: {response_json['error']['message']}")
        return None, 0, 0, 0
    
    # 提取token使用情况（LM Studio格式）
    usage = response_json.get('usage', {})
    if not usage:
        # LM Studio可能使用不同的字段名
        usage = response_json.get('stats', {})
    prompt_tokens = usage.get('prompt_tokens', 0)
    completion_tokens = usage.get('completion_tokens', 0)
    total_tokens = usage.get('total_tokens', prompt_tokens + completion_tokens)
    
    # 计算token速度
    token_speed = total_tokens / duration if duration > 0 else 0
    
    # 提取回复内容（LM Studio格式）
    content = response_json.get('choices', [{}])[0].get('message', {}).get('content', '')
    
    return content, total_tokens, duration, token_speed

def main():
    """主函数"""
    # 加载环境变量
    env_vars = load_env()
    if not env_vars:
        return
    
    # 测试提示词
    prompt = "请解释什么是人工智能，并给出一个简单的例子"
    
    print("正在调用LLM API...")
    print(f"使用模型: {env_vars['MODEL']}")
    print(f"API地址: {env_vars['BASE_URL']}")
    print("=" * 60)
    
    # 调用LLM
    content, total_tokens, duration, token_speed = call_llm(env_vars, prompt)
    
    if content:
        print("回复内容:")
        print(content)
        print("=" * 60)
        print(f"统计信息:")
        print(f"总消耗tokens: {total_tokens}")
        print(f"响应时间: {duration:.2f} 秒")
        print(f"Token速度: {token_speed:.2f} tokens/秒")

if __name__ == "__main__":
    main()
