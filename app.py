
from flask import Flask, render_template, request

app = Flask(__name__)

# 建立問答集 Store questions and answers in a simple list for demonstration purposes
questions_answers = {
    "蘋果": "apple",
    "apple": "蘋果",
    "香蕉": "banana",
    "banana": "香蕉",
    "貓": "cat",
    "cat": "貓",
    "狗": "dog",
    "dog": "狗",
    "書": "book",
    "book": "書",
    "桌子": "table",
    "table": "桌子",
    "椅子": "chair",
    "chair": "椅子"
    }

# 網站的首頁
@app.route('/')
def index():
    return render_template('index.html')

# 網頁_競賽經驗
@app.route('/competition')
def competition():
    return render_template('competition.html')

# 網頁_課外活動
@app.route('/activities')
def activities():
    return render_template('activities.html')

# 網頁_幹部經驗
@app.route('/leadership')
def leadership():
    return render_template('leadership.html')

# 網頁_社團經驗
@app.route('/club')
def club():
    return render_template('club.html')

# 網頁_多元選修課程
@app.route('/electives')
def electives():
    return render_template('electives.html')

# 網頁_AI應用
@app.route('/ai')
def ai():
    return render_template('ai.html')

# 網頁_字庫問答
@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        q = request.form['question'] # 從網頁讀取問題
        a = questions_answers[q] # 從題庫找對應問題的答案
        return render_template('ask.html', question=q, answer=a)
    return render_template('ask.html', question="", answer="")


# 輸入
import os, openai, requests

# Set up your OpenAI API key and endpoint
open_ai_api_key = os.getenv('OpenAI_API_KEY')
open_ai_endpoint = os.getenv('OpenAI_ENDPOINT')
deployment_name = os.getenv('OpenAI_DEPLOY_NAME')

openai.api_base = open_ai_endpoint

# Set the headers for the request
headers = {
    "Content-Type": "application/json",
    "api-key": open_ai_api_key,
}

# 函數_連接Chatgpt
def Chatgpt_response(prompt):
    # Define the payload for the request
    # You can modify the system message and the user prompt as needed
    payload = {
        "model": "o1-mini",  
        "messages": [
            #{"role": "system", "content": "You are a helpful assistant."},  # Context setting
            {"role": "user", "content": prompt}  # Replace with your actual prompt
        ],
       # "temperature": 0.7,  # Modify this value to adjust the creativity level of the model
        "max_completion_tokens": 1000,  # Control the length of the response
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    
    # Send the request to OpenAI's API
    # Note: This uses the Azure OpenAI endpoint format, ensure your endpoint is correct.
    response = requests.post(open_ai_endpoint, headers=headers, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse and print the response from GPT
        result = response.json()
        # This structure assumes a successful response from the Azure OpenAI API format.
        return result['choices'][0]['message']['content']
    else:
        # Print the error if the request was unsuccessful
        print(f"Error {response.status_code}: {response.text}")
        return f"ChatGPT failed: Error {response.status_code}"

# 網頁_連接Azure OpenAI
@app.route('/azure', methods=['GET', 'POST'])
def azure():
    if request.method == 'POST':
        q = request.form['question'] # 從網頁讀取問題
        a = Chatgpt_response(q) # 從Chatgpt取得對應問題的回應
        return render_template('azure.html', question=q, answer=a)
    return render_template('azure.html', question="", answer="")



# 主程式_app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
