# AI智能体开发教学项目（本地大模型工具助手）

## 项目简介
这是一个基于Python的AI智能体开发教学项目，专注于大语言模型（LLM）的本地部署与应用开发，同时实现了功能丰富的本地大模型工具助手，核心内容包括：
- 本地大模型部署与调用
- 流式输出与性能优化
- 环境配置与依赖管理
- 代码规范与最佳实践
- 本地大模型工具调用（文件操作、网页访问等）
- 聊天记录智能管理（压缩、关键信息提取、历史查找）
- 工具调用后台执行优化

## 环境要求
- Python 3.6+
- pip
- LM Studio（或其他OpenAI兼容的本地大模型服务器）

## 快速开始

### 1. 创建虚拟环境
```bash
python -m venv venv
```

### 2. 激活虚拟环境
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
复制环境变量模板并配置：
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

编辑 `.env` 文件，配置你的本地大模型参数：
```env
BASE_URL=http://localhost:1234  # 大模型API地址
MODEL=google/gemma-3-4b        # 模型名称
API_KEY=your_api_key_here      # API密钥（如果需要）
TEMPERATURE=0.7                # 可选配置
MAX_TOKENS=1000                # 可选配置
TIMEOUT=30                     # 可选配置
```

### 5. 运行示例
```bash
# 基础LLM流式调用示例
python practice01/llm_test.py

# 运行基础版本工具助手（含聊天记录压缩）
python practice02/tool_chat_client.py

# 运行增强版本工具助手（含关键信息提取、历史查找）
python practice02/tool_chat_client_v2.py

# 运行完整版本工具助手
python practice03/tool_chat_client.py

# 运行集成AnythingLLM的工具助手
python practice04/tool_chat_client.py
```

## 项目结构
```
studioAIceshi/
├── practice01/         # 实践练习模块
│   └── llm_test.py    # LLM流式调用示例
├── practice02/         # 工具调用功能模块
│   ├── tool_chat_client.py   # 基础版本工具助手（含聊天记录压缩）
│   └── tool_chat_client_v2.py # 增强版本工具助手（含关键信息提取、历史查找）
├── practice03/         # 完整工具调用聊天客户端
│   ├── tool_chat_client.py   # 完整版本工具助手
│   └── tool_chat_client_v2.py # 增强版本工具助手
├── practice04/         # 集成AnythingLLM的工具调用聊天客户端
│   ├── tool_chat_client.py   # 集成AnythingLLM的工具助手
├── venv/              # 虚拟环境
├── requirements.txt   # 项目依赖
├── env.example        # 环境变量配置模板（可重命名为.env）
├── .gitignore         # Git忽略文件
└── README.md          # 项目说明
```

## 核心功能

### 1. LLM流式调用
`practice01/llm_test.py` 实现了完整的流式调用功能：
- **环境变量管理**：从 `.env` 文件加载配置
- **流式输出**：实时显示AI回复内容
- **性能统计**：计算tokens数量、响应时间和生成速度
- **错误处理**：完善的异常捕获和错误提示
- **技术特性**：
  - 使用标准HTTP库实现OpenAI兼容协议
  - 支持流式输出（stream=True）
  - 自动解析SSE（Server-Sent Events）格式
  - 实时性能监控

### 2. 工具调用功能
`practice02/tool_chat_client.py` / `tool_chat_client_v2.py` 实现了完整的工具调用能力：

#### 基础工具能力
- **文件操作工具**：
  - `list_files(directory)`：列出目录下的文件及其属性
  - `rename_file(directory, old_name, new_name)`：修改文件名字
  - `delete_file(directory, file_name)`：删除文件
  - `create_file(directory, file_name, content)`：新建文件并写入内容
  - `read_file(directory, file_name)`：读取文件内容
- **网络访问工具**：
  - `curl_request(url)`：通过 curl 访问网页并返回内容（修复Unicode解码错误）
- **自动HTTP/HTTPS连接切换**：适配不同网络请求场景

#### 工具调用流程
1. 用户输入请求
2. LLM 分析请求并生成工具调用指令
3. 系统执行工具调用
4. LLM 根据工具执行结果生成最终回复

### 3. 新增功能（工具助手增强能力）
#### 功能1：聊天记录压缩
- 当聊天轮数超过5轮或聊天上下文长度超过3000时，自动触发LLM执行聊天记录总结
- 对前70%左右的内容进行压缩，保留最后30%左右的内容原文
- 压缩后的摘要与保留的原文组合成新的消息历史

#### 功能2：关键信息提取
- 每5轮聊天自动触发LLM提取关键信息
- 按照5W规则（Who、What、When、Where、Why）提取信息
- 将提取的信息保存到D:\chat-log\log.txt文件中
- 实现增量更新，每次提取都会追加到文件末尾
- 自动创建目录和文件（如果不存在）

#### 功能3：聊天历史查找
- 添加了新的function call `search_chat_history`
- 当用户发送的信息以"/search"开头或表达了"查找聊天历史"的意思时，大语言模型会调用此工具
- 工具会读取log.txt文件内容，并与用户的请求结合，完成完整的LLM请求

#### 功能4：工具调用后台执行
- 工具调用在后台执行，不显示工具调用信息
- 只显示与用户问题相关的AI回复，提供更专注的对话体验

### 4. AnythingLLM集成
`practice04/tool_chat_client.py` 实现了与AnythingLLM的集成：

#### 功能特性
- **AnythingLLM查询工具**：`anythingllm_query(message)` 通过curl命令访问AnythingLLM的聊天API接口
- **智能触发机制**：当用户提到"文档仓库"、"文件仓库"、"仓库"时，自动触发AnythingLLM查询
- **API认证**：使用API密钥进行身份验证
- **错误处理**：完善的异常捕获和错误提示

#### 配置方法
1. 开启AnythingLLM本地服务
2. 在AnythingLLM中创建API KEY
3. 在practice04目录的.env文件中填写ANYTHINGLLM_API_KEY
4. 确保.env文件中包含以下配置：
   ```env
   # AnythingLLM配置
   ANYTHINGLLM_API_KEY=your-anythingllm-api-key
   ```

## 依赖说明
- **numpy/pandas**：数据处理基础库
- **openai**：OpenAI API客户端
- **langchain**：LLM应用开发框架
- **python-dotenv**：环境变量管理
- **requests**：HTTP请求库
- **jupyter/ipykernel**：交互式开发环境
- **black/flake8/mypy**：代码质量工具

## 开发指南

### 代码规范
- 遵循PEP 8代码规范
- 使用black进行代码格式化：`black .`
- 使用flake8进行代码检查：`flake8 .`
- 使用mypy进行类型检查：`mypy .`

### 推荐开发流程
1. 使用Jupyter Notebook进行实验性开发
2. 将成熟代码迁移到Python脚本
3. 运行代码检查工具确保质量
4. 添加必要的注释和文档

## 注意事项
- 确保LM Studio或其他本地大模型服务器已启动
- 检查 `.env` 文件中的配置参数是否正确（尤其是BASE_URL和MODEL）
- 流式输出需要较长的超时时间（默认120秒）
- 首次运行可能需要下载模型文件
- 关键信息提取功能会自动创建D:\chat-log\目录，需确保有写入权限
- 工具调用功能执行文件/网络操作时，需注意权限和网络安全

## 常见问题

### 连接失败
- 检查LM Studio是否正在运行
- 确认 `BASE_URL` 端口是否正确
- 验证防火墙设置

### 环境变量未加载
- 确保 `.env` 文件存在于项目根目录
- 检查文件格式是否正确（KEY=VALUE格式，无多余空格）

### 工具调用无响应
- 检查模型是否支持function call功能
- 确认超时时间配置（TIMEOUT）是否足够
- 验证文件/网络操作的权限是否充足

### 聊天历史查找失败
- 检查D:\chat-log\log.txt文件是否存在
- 确认文件是否有读取权限
- 验证/search指令格式是否正确