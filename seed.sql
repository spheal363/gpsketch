USE touka_db;

-- routes テーブルに仮データを挿入
INSERT INTO routes (id, animal_name, distance_km, actual_route_distance_km, route_geojson, stat_point, image_url, image_bounds)
VALUES
  (UUID(), 'ねこ', 5.0, 5.2, '{"type": "LineString", "coordinates": [[139.6917, 35.6895], [139.7000, 35.6900]]}', ST_GeomFromText('POINT(139.6917 35.6895)'), 'https://example.com/cat.png', '{"northwest": [139.6900, 35.6900], "southeast": [139.7000, 35.6800]}'),
  (UUID(), 'いぬ', 3.0, 3.1, '{"type": "LineString", "coordinates": [[139.7000, 35.6800], [139.7100, 35.6850]]}', ST_GeomFromText('POINT(139.7000 35.6800)'), 'https://example.com/dog.png', '{"northwest": [139.6950, 35.6850], "southeast": [139.7100, 35.6750]}');

-- runs テーブルに仮データを挿入
INSERT INTO runs (id, route_id, start_time, end_time, actual_distance_km, pace_min_per_km, calories, track_geojson)
VALUES
  (UUID(), (SELECT id FROM routes WHERE animal_name = 'ねこ'), '2025-04-26 08:00:00', '2025-04-26 08:30:00', 5.2, 6.0, 300, '{"type": "LineString", "coordinates": [[139.6917, 35.6895], [139.7000, 35.6900]]}'),
  (UUID(), (SELECT id FROM routes WHERE animal_name = 'いぬ'), '2025-04-26 09:00:00', '2025-04-26 09:20:00', 3.1, 6.5, 200, '{"type": "LineString", "coordinates": [[139.7000, 35.6800], [139.7100, 35.6850]]}');