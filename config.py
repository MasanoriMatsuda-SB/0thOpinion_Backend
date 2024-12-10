import os
from dotenv import load_dotenv

# .envファイルのパスを指定（プロジェクトのルートディレクトリに配置）
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))  # config.pyがappディレクトリ内にある場合

class Config:
    # セキュリティキー
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # データベース接続情報
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    MYSQL_SSL_CA = os.getenv('MYSQL_SSL_CA')  # SSL証明書のパスを環境変数から取得

    # SQLAlchemyのデータベースURIにSSLパラメータを追加
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
        f"?charset=utf8mb4&ssl_ca={MYSQL_SSL_CA}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
