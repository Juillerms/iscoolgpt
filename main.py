import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Carrega variáveis
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

app = FastAPI(
    title="IsCoolGPT API",
    description="Backend Conexão Direta REST",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str
    topic: str = "Cloud Computing"

# --- FRONTEND (MANTIDO IGUAL) ---
html_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IsCoolGPT | Terminal</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0f0c29; }
        ::-webkit-scrollbar-thumb { background: #302b63; border-radius: 4px; }
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        .container {
            width: 90%;
            max-width: 900px;
            height: 85vh;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }
        .header {
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 1.2rem;
            margin: 0;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }
        .status-badge {
            font-size: 0.7rem;
            color: #00ff80;
            border: 1px solid rgba(0, 255, 128, 0.3);
            padding: 4px 10px;
            border-radius: 12px;
            background: rgba(0, 255, 128, 0.1);
        }
        #chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            max-width: 80%;
            padding: 15px;
            border-radius: 12px;
            line-height: 1.6;
            font-size: 0.9rem;
        }
        .user-message {
            align-self: flex-end;
            background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
            color: white;
            box-shadow: 0 5px 15px rgba(0, 114, 255, 0.3);
            border-bottom-right-radius: 2px;
        }
        .ai-message {
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #e2e8f0;
            border-bottom-left-radius: 2px;
        }
        .typing {
            font-size: 0.75rem;
            color: #00c6ff;
            margin-left: 20px;
            display: none;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
        .input-area {
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .input-wrapper { display: flex; gap: 15px; flex-direction: column; }
        textarea {
            width: 100%; height: 60px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px; padding: 15px;
            color: #fff; font-family: 'JetBrains Mono', monospace;
            resize: none; outline: none; transition: border 0.3s;
        }
        textarea:focus { border-color: #00c6ff; }
        .btn-send {
            align-self: flex-end; background: transparent;
            border: 1px solid #00c6ff; color: #00c6ff;
            font-family: 'JetBrains Mono', monospace; font-weight: bold;
            padding: 10px 30px; border-radius: 8px; cursor: pointer;
            transition: all 0.3s; text-transform: uppercase;
        }
        .btn-send:hover { background: #00c6ff; color: #000; }
        .btn-send:disabled { border-color: #444; color: #444; cursor: not-allowed; }
        .links { margin-top: 10px; text-align: center; }
        .links a { color: rgba(255, 255, 255, 0.3); text-decoration: none; font-size: 0.7rem; margin: 0 10px; }
        .links a:hover { color: #00c6ff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>IsCoolGPT_v1.0</h1>
            <div class="status-badge">● SYSTEM ONLINE</div>
        </div>
        <div id="chat-box">
            <div class="message ai-message">
                > System initialized.<br>
                > Olá! Sou o teu assistente de Cloud Computing. Pergunta-me algo.
            </div>
        </div>
        <div id="typing-indicator" class="typing">> Processando resposta...</div>
        <div class="input-area">    
            <div class="input-wrapper">
                <textarea id="user-input" placeholder="Insira o comando ou pergunta..."></textarea>
                <button class="btn-send" onclick="sendMessage()" id="send-btn">EXECUTAR</button>
            </div>
            <div class="links">
                <a href="/docs" target="_blank">[ DOCUMENTATION ]</a>
                <a href="/health" target="_blank">[ STATUS CHECK ]</a>
            </div>
        </div>
    </div>
    <script>
        document.getElementById("user-input").addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); sendMessage(); }
        });
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const typingIndicator = document.getElementById('typing-indicator');
            const question = input.value.trim();
            if (!question) return;
            appendMessage(question, 'user-message');
            input.value = '';
            sendBtn.disabled = true; sendBtn.innerText = "AGUARDE...";
            typingIndicator.style.display = 'block';
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                appendMessage(data.answer || "Erro no processamento.", 'ai-message');
            } catch (error) {
                appendMessage("Falha de conexão com o servidor.", 'ai-message');
            } finally {
                sendBtn.disabled = false; sendBtn.innerText = "EXECUTAR";
                typingIndicator.style.display = 'none'; input.focus();
            }
        }
        function appendMessage(text, className) {
            const chatBox = document.getElementById('chat-box');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message ' + className;
            msgDiv.innerHTML = text.replace(/\\n/g, '<br>');
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return html_content

@app.get("/health")
def health_check():
    return {"status": "active", "system": "IsCoolGPT", "env": "Production"}

@app.post("/ask")
def ask_assistant(request: QuestionRequest):
    try:
        if not api_key:
            return {"answer": "ERRO: Configure a GEMINI_API_KEY no arquivo .env"}

        # --- CONEXÃO DIRETA (REST API) ---
        # Aqui conectamos direto na URL do Google, ignorando a biblioteca com defeito
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Aja como especialista em Cloud. Responda de forma curta: {request.question}"}]
            }]
        }
        
        # Faz a chamada HTTP direta
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            try:
                # O Google devolve um JSON complexo, aqui pegamos só o texto
                answer = data['candidates'][0]['content']['parts'][0]['text']
                return {"answer": answer}
            except:
                return {"answer": "Recebi resposta do Google, mas não consegui ler o texto."}
        else:
            # Se der erro, mostra exatamente o que o Google respondeu
            return {"answer": f"Erro do Google ({response.status_code}): {response.text}"}

    except Exception as e:
        return {"answer": f"Erro interno: {str(e)}"}