"""
アプリケーション設定モジュール
"""

class Config:
    # データベース接続設定
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@mysql:3306/touka_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INIT_DB = False