from flask import Flask, jsonify
from config import Config
from extensions import db, jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # CORSの設定を追加
    CORS(app, resources={r"/api/*": {"origins": "https://tech0-gen-8-step3-app-node-9.azurewebsites.net"}})

    # モデルをインポート
    with app.app_context():
        from models.pet import Pet
        from models.disease import Disease
        from models.user import User
        # 他のモデルも同様にインポート

# ルートURLに対するエンドポイントを追加
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Welcome to 0thOpinion API'}), 200

    # ブループリントの登録
    from routes.user_routes import user_bp
    from routes.pet_routes import pet_bp
    from routes.question_routes import question_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(pet_bp, url_prefix='/api/pets')
    app.register_blueprint(question_bp, url_prefix='/api/questions')

    return app
