# AI智能体开发教学项目

这是一个基于Python的AI智能体开发教学项目，专注于大语言模型（LLM）的本地部署与应用开发。

## 项目简介

本项目提供了从零开始学习AI智能体开发的完整实践教程，包括：
- 本地大模型部署与调用
- 流式输出与性能优化
- 环境配置与依赖管理
- 代码规范与最佳实践

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
copy env.example .env
```

编辑 `.env` 文件，配置你的本地大模型参数：

```env
BASE_URL=http://localhost:1234
MODEL=google/gemma-3-4b
API_KEY=your_api_key_here
TEMPERATURE=0.7
MAX_TOKENS=1000
TIMEOUT=30
```

### 5. 运行示例

```bash
python practice01/llm_test.py
```

## 项目结构

```
studioAIceshi/
├── practice01/         # 实践练习模块
│   └── llm_test.py    # LLM流式调用示例
├── practice02/         # 工具调用功能模块
│   └── tool_chat_client.py  # 工具调用客户端
├── venv/              # 虚拟环境
├── requirements.txt   # 项目依赖
├── env.example       # 环境变量配置模板
├── .gitignore        # Git忽略文件
└── README.md         # 项目说明
```

## 核心功能

### LLM流式调用

`practice01/llm_test.py` 实现了完整的流式调用功能：

- **环境变量管理**：从 `.env` 文件加载配置
- **流式输出**：实时显示AI回复内容
- **性能统计**：计算tokens数量、响应时间和生成速度
- **错误处理**：完善的异常捕获和错误提示

### 工具调用功能

`practice02/tool_chat_client.py` 实现了工具调用功能：

- **文件操作工具**：
  - `list_files(directory)`：列出目录下的文件及其属性
  - `rename_file(directory, old_name, new_name)`：修改文件名字
  - `delete_file(directory, file_name)`：删除文件
  - `create_file(directory, file_name, content)`：新建文件并写入内容
  - `read_file(directory, file_name)`：读取文件内容

- **网络访问工具**：
  - `curl_request(url)`：通过 curl 访问网页并返回内容

- **工具调用流程**：
  1. 用户输入请求
  2. LLM 分析请求并生成工具调用指令
  3. 系统执行工具调用
  4. LLM 根据工具执行结果生成最终回复

### 技术特性

- 使用标准HTTP库实现OpenAI兼容协议
- 支持流式输出（stream=True）
- 自动解析SSE（Server-Sent Events）格式
- 实时性能监控

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
- 检查 `.env` 文件中的配置参数是否正确
- 流式输出需要较长的超时时间（默认120秒）
- 首次运行可能需要下载模型文件

## 常见问题

### 连接失败

- 检查LM Studio是否正在运行
- 确认 `BASE_URL` 端口是否正确
- 验证防火墙设置

### 环境变量未加载

- 确保 `.env` 文件存在于项目根目录
- 检查文件格式是否正确（KEY=VALUE格式）
