CREATE DATABASE IF NOT EXISTS touka_db;

USE touka_db;

-- routes テーブル
CREATE TABLE routes (
  id CHAR(36) PRIMARY KEY,
  animal_name TEXT NOT NULL,
  distance_km FLOAT NOT NULL,
  actual_route_distance_km FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  route_geojson JSON,
  stat_end_latitude FLOAT,
  stat_end_longitude FLOAT,
  image_url TEXT,
  image_bounds JSON
);

-- runs テーブル
CREATE TABLE runs (
  id CHAR(36) PRIMARY KEY,
  route_id CHAR(36) NOT NULL,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  actual_distance_km FLOAT,
  pace_min_per_km FLOAT,
  calories INT,
  track_geojson JSON,
  FOREIGN KEY (route_id) REFERENCES routes(id)
);

-- track_points テーブル
CREATE TABLE track_points (
  id CHAR(36) PRIMARY KEY,
  run_id CHAR(36) NOT NULL,
  timestamp TIMESTAMP,
  latitude FLOAT,
  longitude FLOAT,
  distance_from_start FLOAT,
  route_index INT,
  FOREIGN KEY (run_id) REFERENCES runs(id)
);
