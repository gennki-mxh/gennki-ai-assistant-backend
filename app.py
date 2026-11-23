from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "YOUR_API_KEY_HERE")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_prompt = data.get('prompt', '')
    
    if not user_prompt:
        return jsonify({"status": "error", "msg": "Prompt 不能为空"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_prompt}]
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        result = response.json()
        ai_reply = result['choices'][0]['message']['content']
        return jsonify({"status": "success", "data": {"reply": ai_reply}})
    except Exception as e:
        return jsonify({"status": "error", "msg": f"调用失败: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)