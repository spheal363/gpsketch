from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests
import logging
import time
from dotenv import load_dotenv
import os
from services.route_service import generate_running_route

from config import Config
from models import db, Route, Run, TrackPoint

app = Flask(__name__)
CORS(app)

# 設定をアプリケーションに適用
app.config.from_object(Config)

# データベース初期化
db.init_app(app)

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
        if shape not in SHAPES:
            points = SHAPES["hiyoko"] #用意されていないイラストの場合はhiyokoとする
        else:
            points = SHAPES[shape]
        
        # フロントエンドに返す経路一覧を格納するリスト
        features = []

        # ルート作成処理を呼び出す
        route_data = generate_running_route(current_lat, current_lon, points, target_distance, ORS_API_KEY)
        # ルート作成処理を呼び出す
        route_data = generate_running_route(current_lat, current_lon, points, target_distance, ORS_API_KEY)

        # 結果が期待通りでない場合、エラーログを追加
        if not route_data:
            return jsonify({"error": "Failed to generate route"}), 500
        # 結果が期待通りでない場合、エラーログを追加
        if not route_data:
            return jsonify({"error": "Failed to generate route"}), 500

        # 成功した場合はフロントエンドに返す
        features.append(route_data["route"]["features"][0])
        print(features)
        
        # routesに保存
        route = Route(
            id=str(uuid.uuid4()),
            animal_name=shape,
            distance_km=target_distance,
            route_geojson=features[0],
            stat_end_latitude=current_lat,
            stat_end_longitude=current_lon
        )

        return jsonify({
            "type": "FeatureCollection",
            "features": features,
            "waypoints":route_data["waypoints"],
            "total_distance":route_data["total_distance"]
        })

    except Exception as e:
        # 例外発生時のエラーログ
        return jsonify({"error": e}), 500

@app.route('/api/run/start', methods=['POST'])
def start_run():
    try:
        data = request.json
        route_id = data['route_id']

        new_run = Run(
            id=str(uuid.uuid4()),
            route_id=route_id,
            start_time=datetime.utcnow()
        )
        db.session.add(new_run)
        db.session.commit()

        return jsonify({"run_id": new_run.id}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to start run: {e}")
        return jsonify({"error": "Failed to start run"}), 500

@app.route('/api/run/track', methods=['POST'])
def track_run():
    try:
        data = request.json
        run_id = data['run_id']
        latitude = data['latitude']
        longitude = data['longitude']
        timestamp = data.get('timestamp', datetime.utcnow())

        new_track_point = TrackPoint(
            id=str(uuid.uuid4()),
            run_id=run_id,
            timestamp=timestamp,
            latitude=latitude,
            longitude=longitude
        )

        db.session.add(new_track_point)
        db.session.commit()

        return jsonify({"status": "ok"}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to track point: {e}")
        return jsonify({"error": "Failed to track point"}), 500

def haversine(lat1, lon1, lat2, lon2):
    # 2点間の距離を計算する（ハーヴァサイン公式）
    R = 6371  # 地球半径 (km)
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

@app.route('/api/run/finish', methods=['POST'])
def finish_run():
    try:
        data = request.json
        run_id = data['run_id']

        run = Run.query.get(run_id)
        if not run:
            return jsonify({"error": "Run not found"}), 404

        # TrackPoint取得
        track_points = TrackPoint.query.filter_by(run_id=run_id).order_by(TrackPoint.timestamp).all()

        if len(track_points) < 2:
            return jsonify({"error": "Not enough track points"}), 400

        # 総移動距離を計算
        total_distance_km = 0.0
        for i in range(1, len(track_points)):
            prev = track_points[i-1]
            curr = track_points[i]
            distance = haversine(prev.latitude, prev.longitude, curr.latitude, curr.longitude)
            total_distance_km += distance

        # 開始/終了時刻
        start_time = track_points[0].timestamp
        end_time = track_points[-1].timestamp

        # 総時間（分）
        total_minutes = (end_time - start_time).total_seconds() / 60.0

        # ペース（分/km）
        pace_min_per_km = total_minutes / total_distance_km if total_distance_km > 0 else None

        # 簡易カロリー計算（仮：体重60kgとして 1kmあたり60kcal）
        calories = int(total_distance_km * 60)

        # Run更新
        run.end_time = end_time
        run.actual_distance_km = total_distance_km
        run.pace_min_per_km = pace_min_per_km
        run.calories = calories

        db.session.commit()

        return jsonify({
            "status": "finished",
            "total_distance_km": total_distance_km,
            "pace_min_per_km": pace_min_per_km,
            "calories": calories
        }), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to finish run: {e}")
        return jsonify({"error": "Failed to finish run"}), 500

@app.route("/api/runs", methods=["GET"])
def get_runs():
    try:
        # `runs` テーブルの全データを取得
        runs = Run.query.all()
        
        # データをシリアライズしてJSON形式で返す
        runs_data = []
        for run in runs:
            # route_idを使ってRouteテーブルからanimal_nameを取得
            route = Route.query.get(run.route_id)
            animal_name = route.animal_name if route else None
            
            # データを構築
            runs_data.append({
                "id": run.id,
                "route_id": run.route_id,
                "start_time": run.start_time,
                "end_time": run.end_time,
                "actual_distance_km": run.actual_distance_km,
                "pace_min_per_km": run.pace_min_per_km,
                "calories": run.calories,
                "track_geojson": run.track_geojson,
                "animal_name": animal_name
            })
            
        return jsonify(runs_data), 200
    except Exception as e:
        logging.error(f"Error fetching runs: {e}")
        return jsonify({"error": "Failed to fetch runs"}), 500

@app.route("/api/route/753ca900-227d-11f0-8765-0242ac1a0003", methods=["GET"])
def get_route(route_id):
    try:
        # 指定されたroute_idに対応するRouteを取得
        route = Route.query.get(route_id)
        if not route:
            return jsonify({"error": "Route not found"}), 404

        # RouteデータをJSON形式で返す
        route_data = {
            "id": route.id,
            "animal_name": route.animal_name,
            "distance_km": route.distance_km,
            "actual_route_distance_km": route.actual_route_distance_km,
            "route_geojson": route.route_geojson,
            "stat_end_latitude": route.stat_end_latitude,
            "stat_end_longitude": route.stat_end_longitude,
            "image_url": route.image_url,
            "image_bounds": route.image_bounds
        }
        return jsonify(route_data), 200
    except Exception as e:
        logging.error(f"Error fetching route {route_id}: {e}")
        return jsonify({"error": "Failed to fetch route"}), 500

# ログの設定
if __name__ == "__main__":
    # ログレベル設定（DEBUGにして詳細なログを取得）
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

