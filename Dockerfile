# ベースイメージの指定
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 必要なPythonパッケージをインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . /app/

# Hugging Face用のディレクトリを設定
ENV HF_HOME=/app/.huggingface

ENV PYTHONPATH=/app

# FastAPIアプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
