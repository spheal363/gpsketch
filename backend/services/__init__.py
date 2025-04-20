"""
サービス層モジュール
アプリケーションロジックやバックエンド処理（ルート生成、通知、推薦など）を提供します。
"""

# 必要に応じてサービスをインポートしてエクスポート
from .route_service import generate_running_route


# バージョン情報（任意）
__version__ = '0.1.0'