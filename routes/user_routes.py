from flask import Blueprint, request, jsonify
from models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'データがありません。'}), 400

    email = data.get('Email')
    password = data.get('Password')
    if not email or not password:
        return jsonify({'message': 'メールアドレスとパスワードは必須です。'}), 400

    user = User.query.filter_by(Email=email).first()
    if user:
        return jsonify({'message': '既に登録されています。'}), 400

    new_user = User(
        User_name=data.get('User_name'),
        Screen_name=data.get('Screen_name'),
        Sex=data.get('Sex'),
        Birth_date=data.get('Birth_date'),
        Address=data.get('Address'),
        Email=email
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'ユーザー登録が成功しました。'}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'データがありません。'}), 400

    email = data.get('Email')
    password = data.get('Password')
    if not email or not password:
        return jsonify({'message': 'メールアドレスとパスワードは必須です。'}), 400

    user = User.query.filter_by(Email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.User_id))
        return jsonify({'access_token': access_token, "screen_name": user.Screen_name}), 200
    else:
        return jsonify({'message': 'ログインに失敗しました。'}), 401
