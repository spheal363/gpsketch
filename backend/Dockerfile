FROM python:3.13-alpine

# 作業ディレクトリを設定
WORKDIR /backend

# 必要な依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Flaskアプリを起動
CMD ["flask", "run"]