from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import os
import json
import uuid
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

from services.route_service import generate_running_route
from config import Config
from models import db, Route, TrackPoint, Run

# アプリ設定
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

# 環境変数読み込み
load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")
print(f"ORS_API_KEY: {ORS_API_KEY}")

# イラストと座標点データ
SHAPES = {
    "hiyoko": [(2, 624), (889, 27), (1559, 193), (2751, 911), (1684, 2728), (806, 2506)],
    "kuma": [(136, 177), (2585, 129), (2770, 565), (2532, 2219), (320, 2300), (70, 1804)],
    "uma": [(306, 0), (997, 0), (1205, 285), (1004, 2601), (758, 2767), (325, 2621)],
    "yunicorn": [(1668, 119), (1838, 174), (2759, 51), (2438, 1907), (1179, 2210), (0, 1697)],
}

# ルート生成
@app.route("/api/route/generate", methods=["POST"])
def generate_route():
    try:
        data = request.json
        shape = data.get("shape", "hiyoko")
        target_distance = data.get("length", 10.0)
        current_lat = data.get("latitude", 35.681236)
        current_lon = data.get("longitude", 139.767125)

        if not data or current_lat is None or current_lon is None:
            return jsonify({"error": "Invalid input"}), 400

        points = SHAPES.get(shape, SHAPES["hiyoko"])

        route_data = generate_running_route(current_lat, current_lon, points, target_distance, ORS_API_KEY)
        if not route_data:
            return jsonify({"error": "Failed to generate route"}), 500

        features = [route_data["route"]["features"][0]]
        route_id = str(uuid.uuid4())
        route = Route(
            id=route_id,
            animal_name=shape,
            distance_km=target_distance,
            actual_route_distance_km=route_data["total_distance"],
            route_geojson=json.dumps({
                "type": "FeatureCollection",
                "features": features,
                "waypoints": route_data["waypoints"],
                "total_distance": route_data["total_distance"]
            }),
            stat_end_latitude=current_lat,
            stat_end_longitude=current_lon
        )
        db.session.add(route)
        db.session.commit()

        return jsonify({
            "routes_id": route_id,
            "type": "FeatureCollection",
            "features": features,
            "waypoints": route_data["waypoints"],
            "total_distance": route_data["total_distance"]
        })

    except Exception as e:
        logging.error(f"Error in generate_route: {e}")
        return jsonify({"error": str(e)}), 500

# ルート取得
@app.route("/api/route/<route_id>", methods=["GET"])
def get_route_by_id(route_id):
    try:
        route = Route.query.get(route_id)
        if not route:
            return jsonify({"error": "Route not found"}), 404

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
        return jsonify(route_data)

    except Exception as e:
        logging.error(f"Error fetching route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/route/complete", methods=["POST"])
def complete_route():
    try:
        data = request.get_json()

        route_id = data.get("route_id")
        start_time_str = data.get("start_time")
        geojson = data.get("geojson")

        if not route_id or not start_time_str or not geojson:
            return jsonify({"error": "必要なデータが足りません。"}), 400

        # start_timeをdatetime型に変換
        start_time = datetime.fromisoformat(start_time_str)

        # 現在時刻をend_timeに設定
        end_time = datetime.now()

        # 実際の距離（km）をgeojsonから取得する（total_distanceフィールド想定）
        actual_distance_km = geojson.get("total_distance", 0.0)

        # 仮にペース・カロリーを適当に設定する（あとでちゃんと計算してもOK）
        # 例：5分/km固定、カロリー=距離(㎞)×60kcalくらい
        pace_min_per_km = 5.0
        calories = int(actual_distance_km * 60)

        new_run = Run(
            route_id=route_id,
            start_time=start_time,
            end_time=end_time,
            actual_distance_km=actual_distance_km,
            pace_min_per_km=pace_min_per_km,
            calories=calories,
            track_geojson=geojson
        )

        db.session.add(new_run)
        db.session.commit()

        return jsonify({"message": "Runデータ登録成功！", "run_id": new_run.id}), 201

    except Exception as e:
        logging.error(f"Error in complete_route: {e}")
        return jsonify({"error": str(e)}), 500

# 起動
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
