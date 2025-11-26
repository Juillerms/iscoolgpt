import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Carrega as variáveis
load_dotenv()

# 2. Configura a Chave do Google Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("AVISO: Chave GEMINI_API_KEY não encontrada no arquivo .env")
else:
    genai.configure(api_key=api_key)

app = FastAPI(
    title="IsCoolGPT API",
    description="Backend com Google Gemini",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str
    topic: str = "Cloud Computing"

@app.get("/")
def read_root():
    return {"status": "online", "provider": "Google Gemini"}

@app.post("/ask")
def ask_assistant(request: QuestionRequest):
    try:
        if not api_key:
            return {
                "answer": "Modo offline: " + request.question,
                "note": "Configure a GEMINI_API_KEY no .env"
            }

        # 3. Configuração do Modelo (Gemini 1.5 Flash é rápido e barato/gratuito)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt estruturado para garantir que ele age como professor
        prompt = (
            f"Aja como um professor especialista em {request.topic}. "
            f"Responda de forma curta e didática à seguinte pergunta: {request.question}"
        )

        # 4. Chamada à API
        response = model.generate_content(prompt)
        
        return {"answer": response.text}

    except Exception as e:
        # O Gemini às vezes bloqueia conteúdo se achar inseguro, ou erro de rede
        raise HTTPException(status_code=500, detail=f"Erro no Gemini: {str(e)}")