# 1. Imagem base: Python leve oficial
FROM python:3.9-slim

# 2. Pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o resto do código
COPY . .

# 5. Comando para iniciar o servidor
# O --host 0.0.0.0 é OBRIGATÓRIO para o Docker funcionar
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]