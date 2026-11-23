from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # 本地前后端分离调试用；同源部署时可去掉

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
TIMEOUT = 30
MAX_PROMPT_LEN = 2000
SYSTEM_PROMPT = "你是一个简洁的助手，回答控制在 300 字以内。"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    user_prompt = (data.get('prompt') or '').strip()

    if not user_prompt:
        return jsonify({"status": "error", "msg": "Prompt 不能为空"}), 400
    if len(user_prompt) > MAX_PROMPT_LEN:
        return jsonify({"status": "error", "msg": "Prompt 过长"}), 400
    if not DEEPSEEK_API_KEY:
        return jsonify({"status": "error", "msg": "服务端未配置 DEEPSEEK_API_KEY"}), 500

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL, headers=headers, json=payload, timeout=TIMEOUT
        )
    except requests.Timeout:
        return jsonify({"status": "error", "msg": "上游模型响应超时"}), 504
    except requests.RequestException as e:
        return jsonify({"status": "error", "msg": f"上游连接失败: {e}"}), 502

    if response.status_code != 200:
        return jsonify({"status": "error",
                        "msg": f"上游返回 {response.status_code}"}), 502

    result = response.json()
    try:
        ai_reply = result['choices'][0]['message']['content']
    except (KeyError, IndexError):
        return jsonify({"status": "error", "msg": "上游返回格式异常"}), 502

    return jsonify({
        "status": "success",
        "data": {"reply": ai_reply, "usage": result.get("usage", {})},
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
