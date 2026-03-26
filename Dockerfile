# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクト全ファイルをコピー
COPY . .

# FastAPI起動 (host 0.0.0.0 でコンテナ外からの接続を許可)
CMD ["uvicorn", "app.back.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]