import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import JSON

db = SQLAlchemy()

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    animal_name = db.Column(db.Text, nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    actual_route_distance_km = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    route_geojson = db.Column(JSON)
    stat_point = db.Column(db.Text)  # POINT型は一旦Textで管理するのが楽
    image_url = db.Column(db.Text)
    image_bounds = db.Column(JSON)

    runs = db.relationship('Run', backref='route', lazy=True)

class Run(db.Model):
    __tablename__ = 'runs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    route_id = db.Column(db.String(36), db.ForeignKey('routes.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    actual_distance_km = db.Column(db.Float)
    pace_min_per_km = db.Column(db.Float)
    calories = db.Column(db.Integer)
    track_geojson = db.Column(JSON)

    track_points = db.relationship('TrackPoint', backref='run', lazy=True)

class TrackPoint(db.Model):
    __tablename__ = 'track_points'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = db.Column(db.String(36), db.ForeignKey('runs.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    location = db.Column(db.Text)  # POINT型は一旦Textで管理
    distance_from_start = db.Column(db.Float)
    route_index = db.Column(db.Integer)
