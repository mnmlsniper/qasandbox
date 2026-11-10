# Локальный стенд. Railway собирает приложение через Nixpacks (railway.json) и этот файл не использует.
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
EXPOSE 8080
# сид тестовых данных (идемпотентный), затем сервер
CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port $PORT"]
