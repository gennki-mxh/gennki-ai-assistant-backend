# 🤖 GennKi's AI Assistant (Flask + DeepSeek API)

这是一个基于 Python Flask 框架与大语言模型（DeepSeek）API 打造的最小闭环（MVP）演示项目。旨在验证后端服务与大模型 API 的交互逻辑，并提供一个极简的前端页面进行实时对话测试。

## 🛠️ 技术栈

**后端**：Python 3 / Flask / Flask-CORS

**网络请求**：Requests

**大模型**：DeepSeek API (`deepseek-chat`)

**前端**：HTML5 / 原生 Fetch API / Pico.css / Marked.js (用于渲染 Markdown)

## ✨ 核心工程亮点

**1. 安全与规范**：API Key 通过系统环境变量注入 (`os.environ`)，避免密钥硬编码导致的泄露风险。

**2. 防御性编程**：在后端接口层对前端传入的 `prompt` 进行非空校验，拦截无效请求并返回 `400` 状态码。

**3. 容错与异常处理**：使用 `try-except` 捕获网络请求异常，并通过 `raise_for_status()` 处理 HTTP 错误，确保服务稳定性。

**4. 成本控制意识**：在接口返回值中保留了大模型的 Token 消耗量（`usage` 字段），为后续评估调用成本提供数据支撑。

**5. 跨域联调**：配置了 `Flask-CORS`，解决前后端分离本地调试时的跨域限制。

## 🚀 本地运行指南

**1. 克隆项目**

```bash
git clone https://github.com/gennki-mxh/gennki-ai-assistant-backend
cd gennki-ai-assistant-backend
```

**2. 创建并激活虚拟环境**

*Windows:*

```powershell
python -m venv venv
.\venv\Scripts\activate
```

*macOS/Linux:*

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. 安装依赖**

```bash
pip install flask flask-cors requests
```

**4. 配置环境变量**

你需要一个 DeepSeek 的 API Key。

*Windows:*

```powershell
$env:DEEPSEEK_API_KEY="sk-你的真实API密钥"
```

macOS/Linux:

```bash
export DEEPSEEK_API_KEY="sk-你的真实API密钥"
```

**5. 启动服务**

```bash
python app.py
```

打开浏览器访问 `http://127.0.0.1:5000` 即可体验。

## 📡 接口说明

**POST** `/api/chat`

- 请求体：

```json
{
  "prompt": "你好，请自我介绍一下"
}
```

- 成功响应：

```json
{
  "status": "success",
  "data": {
    "reply": "你好呀！很高兴认识你...",
    "usage": { "prompt_tokens": 15, "completion_tokens": 60, "total_tokens": 75 }
  }
}
```

## 🚀 推送到 GitHub 的终端命令

既然要推，咱们就按正规流程走，在终端的项目文件夹下（确保带 `(venv)` 的环境里），依次输入以下命令：

```powershell
# 1. 初始化 Git 仓库
git init

# 2. 把所有文件添加到暂存区
git add .

# 3. 提交
git commit -m "feat: 初始化项目并完成 Flask + DeepSeek 最小闭环 Demo"

# 4. 将默认分支重命名为 main
git branch -M main

# 5. 关联你的远程仓库（先在 GitHub 上新建一个名为 flask-deepseek-demo 的空仓库，然后复制仓库地址）
git remote add origin https://github.com/gennki-mxh/gennki-ai-assistant-backend

# 6. 推送
git push -u origin main
```

Created by [GennKi](https://gennki-mxh.github.io/)
