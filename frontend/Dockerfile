FROM node:lts-alpine

# コンテナ内での作業ディレクトリを/frontendに設定
WORKDIR /frontend

# gitをインストール
RUN apk add git --no-cache git

# 必要な依存関係をインストール
COPY package.json package-lock.json ./
RUN npm install

# frontend/ディレクトリのプロジェクトをコンテナにコピー
COPY . ./

# コンテナ起動時にこのコマンドを実行
CMD ["npm", "run", "dev", "--", "--host"]