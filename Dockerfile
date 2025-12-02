# MUDANÇA IMPORTANTE: De 3.9 para 3.10
FROM python:3.10-slim

# 2. Pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o resto do código
COPY . .

# 5. Comando para iniciar o servidor
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]