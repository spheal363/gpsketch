import math
import requests
import json
import os


def haversine_distance(lat1, lon1, lat2, lon2):
    """緯度経度で表される2点間の直線距離をキロメートルで計算"""
    R = 6371.0  # 地球の半径（km）
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def calculate_geo_coordinates(current_lat, current_lon, points, target_distance):
    """
    座標点リストから対応する緯度経度を計算する
    
    Args:
        current_lat: 現在地の緯度
        current_lon: 現在地の経度
        points: [(x1,y1), (x2,y2), ..., (xn,yn)] 形式の座標リスト
        target_distance: 目標となる総距離（km）
        
    Returns:
        計算された緯度経度のリスト [(a1,b1), (a2,b2), ..., (an,bn)]
    """
    n = len(points)
    if n < 2:
        return [(current_lat, current_lon)]
    
    # ステップ1: 各ベクトルの方向と大きさを計算
    directions = []  # 方向角（ラジアン）
    distances = []   # ベクトルの大きさ
    
    for i in range(n - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # ベクトル (x2-x1, y2-y1) の方向を計算
        # (0,-1) を基準として時計回りの角度
        dx = x2 - x1
        dy = y2 - y1
        
        # arctan2は(-π, π]の範囲で角度を返す
        # (0,-1)を基準にするので、π/2を加えて調整
        angle = math.atan2(dx, -dy)
        
        # 角度が負の場合は2πを加えて[0, 2π)の範囲に変換
        if angle < 0:
            angle += 2 * math.pi
        
        # ベクトルの大きさを計算
        magnitude = math.sqrt(dx**2 + dy**2)
        
        directions.append(angle)
        distances.append(magnitude)
    
    # 最後の点から最初の点へのベクトル
    x_last, y_last = points[n - 1]
    x_first, y_first = points[0]
    
    dx = x_first - x_last
    dy = y_first - y_last
    
    # 最後のベクトルの方向
    angle = math.atan2(dx, -dy)
    if angle < 0:
        angle += 2 * math.pi
    
    # 最後のベクトルの大きさ
    magnitude = math.sqrt(dx**2 + dy**2)
    
    directions.append(angle)
    distances.append(magnitude)
    
    # ステップ2: スケーリング係数hを計算
    total_distance_raw = sum(distances)

    detour_factor=1.4 #デトア係数：直線距離に一定の係数を掛けることです。この係数は「迂回係数」または「デトア係数」と呼ばれます。

    h = target_distance /detour_factor / total_distance_raw
    
    # ステップ3: 緯度経度を計算
    geo_coords = [(current_lat, current_lon)]  # 初期位置
    
    lat, lon = current_lat, current_lon
    for i in range(n):
        if i < n - 1:  # 通常のポイント
            direction = directions[i]
            distance = distances[i] * h
        else:  # 最後の点は省略（最初に戻る）
            break
        
        # 地球上の緯度経度を計算
        next_lat, next_lon = calculate_destination_point(lat, lon, math.degrees(direction), distance)
        geo_coords.append((next_lat, next_lon))
        
        # 次のポイントの起点を更新
        lat, lon = next_lat, next_lon
    
    return geo_coords

def calculate_destination_point(lat, lon, bearing_deg, distance_km):
    """
    ある地点から指定した角度と距離にある目的地の緯度経度を計算
    
    Args:
        lat: 出発地点の緯度（度）
        lon: 出発地点の経度（度）
        bearing_deg: 方位角（度、北が0度、東が90度）
        distance_km: 距離（キロメートル）
        
    Returns:
        目的地の緯度経度のタプル(dest_lat, dest_lon)
    """
    # 地球の半径（km）
    R = 6371.0
    
    # 度をラジアンに変換
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing_deg)
    
    # 角距離（距離/地球半径）
    angular_distance = distance_km / R
    
    # 目的地の緯度を計算
    dest_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) +
        math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing_rad)
    )
    
    # 目的地の経度を計算
    dest_lon_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat_rad),
        math.cos(angular_distance) - math.sin(lat_rad) * math.sin(dest_lat_rad)
    )
    
    # ラジアンから度に変換
    dest_lat = math.degrees(dest_lat_rad)
    dest_lon = math.degrees(dest_lon_rad)
    
    # 経度を-180〜180の範囲に正規化
    dest_lon = (dest_lon + 540) % 360 - 180
    
    return dest_lat, dest_lon

def find_named_places_osm(lat, lon, radius=100):
    """
    OpenStreetMapのOverpass APIを使って指定された緯度経度の周辺で名称のある場所を検索
    
    Args:
        lat: 緯度
        lon: 経度
        radius: 検索半径（メートル）
        
    Returns:
        名称のある場所の情報（名前、緯度、経度）
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # 名前を持つノード、ウェイ、リレーションを検索するクエリ
    overpass_query = f"""
    [out:json];
    (
      node(around:{radius},{lat},{lon})["name"];
      way(around:{radius},{lat},{lon})["name"];
      relation(around:{radius},{lat},{lon})["name"];
    );
    out center;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        data = response.json()
        
        if data['elements']:
            # ランニングに適した場所のタイプのリスト
            running_friendly_types = [
                'park', 'playground', 'garden', 'sports_centre', 'stadium',
                'school', 'university', 'college', 'public_building',
                'station', 'bus_stop', 'subway_entrance', 'cafe', 'restaurant',
                'convenience', 'supermarket', 'mall', 'landmark', 'attraction',
                'memorial', 'monument', 'viewpoint', 'tourism'
            ]
            
            # 場所を評価してソート
            scored_places = []
            
            for element in data['elements']:
                # 座標を取得（ウェイやリレーションの場合はcenterプロパティを使用）
                if element['type'] == 'node':
                    lat = element['lat']
                    lon = element['lon']
                else:
                    if 'center' in element:
                        lat = element['center']['lat']
                        lon = element['center']['lon']
                    else:
                        continue
                
                # タグから情報を取得
                tags = element.get('tags', {})
                name = tags.get('name', f"Point at {lat:.6f}, {lon:.6f}")
                
                # スコアリング（ランニングに適した場所を優先）
                score = 0
                
                # 名前があれば基本スコア
                if 'name' in tags:
                    score += 10
                
                # ランニングに適したタイプの場所にボーナス
                for key, value in tags.items():
                    if key in running_friendly_types or value in running_friendly_types:
                        score += 5
                    
                    # 特に重要な場所タイプにボーナス
                    if (key == 'leisure' and value == 'park') or \
                       (key == 'amenity' and value in ['school', 'university']):
                        score += 3
                
                # ノードは通常ウェイやリレーションより小さい場所なので調整
                if element['type'] == 'node':
                    score -= 2
                
                scored_places.append({
                    'name': name,
                    'lat': lat,
                    'lng': lon,
                    'score': score,
                    'type': element['type'],
                    'tags': tags
                })
            
            # スコアでソート
            scored_places.sort(key=lambda x: x['score'], reverse=True)
            
            # 最も適した場所を返す
            if scored_places:
                return {
                    'name': scored_places[0]['name'],
                    'lat': scored_places[0]['lat'],
                    'lng': scored_places[0]['lng']
                }
    
    # 名称のある場所が見つからない場合は元の座標を返す
    return {
        'name': f"Waypoint at {lat:.6f}, {lon:.6f}",
        'lat': lat,
        'lng': lon
    }

def get_route_distance(waypoints, ors_api_key):
    """
    OpenRouteServiceを使って実際のルート距離を計算
    
    Args:
        waypoints: 経由地点のリスト [{'lat': a1, 'lng': b1}, ...]
        ors_api_key: OpenRouteService API Key
        
    Returns:
        実際のルート総距離（km）とGeoJSON形式のルート情報
    """
    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
    
    # 座標リストを作成
    coordinates = []
    for point in waypoints:
        coordinates.append([point['lng'], point['lat']])
    
    headers = {
        "Authorization": ors_api_key,
        "Content-Type": "application/json"
    }
    
    body = {
        "coordinates": coordinates
    }
    
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        route_data = response.json()
        # 総距離を取得（メートルからキロメートルに変換）
        total_distance = route_data['features'][0]['properties']['summary']['distance'] / 1000
        return total_distance, route_data
    else:
        print(f"OpenRouteService API Error: {response.status_code} - {response.text}")
        return None, None
    
def generate_running_route(current_lat, current_lon, points, target_distance, ors_api_key):
    """
    ランニングルートを生成する
    
    Args:
        current_lat: 現在地の緯度
        current_lon: 現在地の経度
        points: [(x1,y1), (x2,y2), ..., (xn,yn)] 形式の座標リスト
        target_distance: 目標となる総距離（km）
        ors_api_key: OpenRouteService API Key
        
    Returns:
        ルート情報（経由地点と総距離）のJSON
    """
    # 座標から緯度経度を計算
    geo_coords = calculate_geo_coordinates(current_lat, current_lon, points, target_distance)
    
    # 各地点周辺の名称のある場所を検索
    waypoints = []
    for lat, lon in geo_coords:
        waypoint = find_named_places_osm(lat, lon, radius=300)
        waypoints.append(waypoint)
    
    # 最初の地点を最後にも追加して循環ルートにする
    if waypoints and len(waypoints) > 0:
        # 注: 既に最初と最後が同じ場合は追加しない
        first_point = waypoints[0]
        if waypoints[-1]['lat'] != first_point['lat'] or waypoints[-1]['lng'] != first_point['lng']:
            waypoints.append(first_point)

    
    # 実際のルート距離を計算
    actual_distance, route_data = get_route_distance(waypoints, ors_api_key)
    
    waypoints.pop()#出発地と到着地は同じなので、到着地を除外
    # 結果を整形
    result = {
        "waypoints": waypoints,
        "total_distance": actual_distance,
        "route": route_data
    }
    return result
    # return json.dumps(result, indent=2, ensure_ascii=False) #テスト用


# # テスト用のメイン実行部分（このファイルが直接実行された場合のみ実行）
# if __name__ == "__main__":
#     # 例：現在地と(x,y)座標、目標距離
#     current_lat = 35.681236  # 東京駅の緯度
#     current_lon = 139.767125  # 東京駅の経度

#     # 動物（例：ひよこ）の形を表す座標点
#     points = [
#         (2,624),  # x1, y1 は現在地に対応
#         (889,27),  # 
#         (1559,193),  # 
#         (2751,911),  # 
#         (1684,2728),
#         (806,2506)   #
#     ]

#     target_distance = 10.0  # 目標距離 5km

#     # APIキー
#     ors_api_key = os.getenv("ORS_API_KEY")

#     # ルート生成
#     route_json = generate_running_route(
#         current_lat, current_lon, points, target_distance, ors_api_key
#     )

#     print(route_json)