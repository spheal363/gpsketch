from flask import Flask, jsonify
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

# 取得した緯度経度を元に、円の周上となる点の緯度経度を生成する関数
# radius_km: 半径（km）
# num_points: 円周上の点の数
def generate_circle_points(center_lat, center_lng, radius_km=10, num_points=4):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        dx = radius_km * math.cos(angle)
        dy = radius_km * math.sin(angle)
        # 緯度経度に変換
        # 緯度1度 ≈ 111km、経度1度 ≈ 111km * cos(緯度)
        lat = center_lat + (dy / 111)
        lng = center_lng + (dx / (111 * math.cos(math.radians(center_lat))))
        points.append([lng, lat])
    return points

def get_ors_route(start, end):
    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [start, end]
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"ORS Error: {response.status_code} - {response.text}")
        return None

# @app.route("/api/route")
# def route():
#     # TODO: フロントエンドから送られた緯度経度を取得
    
#     # フロントエンドから送られた緯度経度を設定（ひとまず東京駅の緯度経度にしてます）
#     center_lat = 35.681236
#     center_lng = 139.767125
    
#     # 通過点となる地点の緯度経度を取得（ひとまず円形にしてます）
#     points = generate_circle_points(center_lat, center_lng)

#     # TODO: フロントエンドから送られた地点がスタート/ゴールになるように調整
    
#     # フロントエンドに返す経路一覧を格納するリスト
#     features = []

#     for i in range(len(points)):
#         start = points[i]
#         end = points[(i + 1) % len(points)]  # 隣り合う次の点（最後は始点に戻る）

#         # OpenRouteService APIを呼び出して2点間の経路を取得
#         route = get_ors_route(start, end)
        
#         if route:
#             features.append(route["features"][0])
#             time.sleep(2)  # APIの呼び出し制限に引っかからないように2秒程度待つ

#     # 取得した経路をフロントエンドに返す
#     return jsonify({
#         "type": "FeatureCollection",
#         "features": features
#     })

@app.route("/api/route")
def route():
    try:
        # デバッグ: ルート作成関数のテスト開始ログ
        app.logger.debug("Start generating route")

        # フロントエンドから送られた緯度経度を設定（ひとまず東京駅の緯度経度にしてます）
        current_lat = 35.681236
        current_lon = 139.767125

        # 動物（例：ひよこ）の形を表す座標点
        points = [
            (2, 624),  # x1, y1 は現在地に対応
            (889, 27),
            (1559, 193),
            (2751, 911),
            (1684, 2728),
            (806, 2506)
        ]

        target_distance = 10.0  # 目標距離 10km

        # フロントエンドに返す経路一覧を格納するリスト
        features = []

        # ルート作成処理を呼び出す
        app.logger.debug("Calling generate_running_route function")
        route_data = generate_running_route(current_lat, current_lon, points, target_distance, ORS_API_KEY)

        # デバッグ: ルート作成結果を確認
        app.logger.debug("Route generated: %s", route_data)

        # 結果が期待通りでない場合、エラーログを追加
        if not route_data:
            app.logger.error("Failed to generate route. No route data returned.")
            return jsonify({"error": "Failed to generate route"}), 500

        # 成功した場合はフロントエンドに返す
        features.append(route_data["route"]["features"][0])

        # デバッグ: 返すデータを確認
        app.logger.debug("Returning route data to frontend: %s", features)

        return jsonify({
            "type": "FeatureCollection",
            "features": features
        })

    except Exception as e:
        # 例外発生時のエラーログ
        app.logger.error("Error in generating route: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

# ログの設定
if __name__ == "__main__":
    # ログレベル設定（DEBUGにして詳細なログを取得）
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)