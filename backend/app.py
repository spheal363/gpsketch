from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests
import logging
import time
from dotenv import load_dotenv
import os
from services.route_service import generate_running_route

app = Flask(__name__)
CORS(app)

# 一つ上のディレクトリにある .env を読み込む
load_dotenv()

# 環境変数からOpenRouteServiceのAPIキーを取得
ORS_API_KEY = os.getenv("ORS_API_KEY")
print(f"ORS_API_KEY: {ORS_API_KEY}")

# イラストと座標点データの紐づけ（のちのちデータベースに移行）
SHAPES = {
    "hiyoko":  [
            (2, 624),  # x1, y1 は現在地に対応
            (889, 27),
            (1559, 193),
            (2751, 911),
            (1684, 2728),
            (806, 2506)
        ],
    "kuma":  [
            (136, 177),  # x1, y1 は現在地に対応
            (2585, 129),
            (2770, 565),
            (2532, 2219),
            (320, 2300),
            (70, 1804)
        ],
    "uma":  [
            (306, 0),  # x1, y1 は現在地に対応
            (997, 0),
            (1205, 285),
            (1004, 2601),
            (758, 2767),
            (325, 2621)
        ],
    "yunicorn":  [
            (1668, 119),  # x1, y1 は現在地に対応
            (1838, 174),
            (2759, 51),
            (2438, 1907),
            (1179, 2210),
            (0, 1697)
        ]
}

#イラストと距離を受け取り、ルートを生成する
@app.route("/api/route/generate", methods=["POST"])
def generate_route():
    try:
        # フロントエンドからのデータを取得
        data = request.json
        
        # データのバリデーション
        if not data:
            return jsonify({"error": "データが送信されていません"}), 400
        
        # 必要なパラメータを取得
        shape = data.get("shape", "hiyoko")  # イラストname
        target_distance = data.get("length", 10.0)      # 距離（km）
        current_lat = data.get("latitude", 35.681236)       # 緯度
        current_lon = data.get("longitude", 139.767125)     # 経度
        
        # 緯度経度のバリデーション
        if current_lat is None or current_lon is None:
            return jsonify({"error": "緯度・経度が指定されていません"}), 400
        
        # 座標点データを生成
        if shape ==  shape not in SHAPES:
            points = SHAPES["hiyoko"] #用意されていないイラストの場合はhiyokoとする
        else:
            points = SHAPES[shape]
        
        # フロントエンドに返す経路一覧を格納するリスト
            features = []

            # ルート作成処理を呼び出す
            route_data = generate_running_route(current_lat, current_lon, points, target_distance, ORS_API_KEY)

            # 結果が期待通りでない場合、エラーログを追加
            if not route_data:
                return jsonify({"error": "Failed to generate route"}), 500

            # 成功した場合はフロントエンドに返す
            features.append(route_data["route"]["features"][0])

            return jsonify({
                "type": "FeatureCollection",
                "features": features
            })

    except Exception as e:
        # 例外発生時のエラーログ
        return jsonify({"error": "Internal Server Error"}), 500


# ログの設定
if __name__ == "__main__":
    # ログレベル設定（DEBUGにして詳細なログを取得）
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

