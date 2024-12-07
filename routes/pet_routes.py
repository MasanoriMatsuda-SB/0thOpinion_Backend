from flask import Blueprint, request, jsonify, current_app
from extensions import db  # 修正箇所
from models.pet import Pet
from models.disease import Disease  # 必要に応じてインポート
from flask_jwt_extended import jwt_required, get_jwt_identity

pet_bp = Blueprint('pet_bp', __name__)

@pet_bp.route('/', methods=['POST'])
@jwt_required()
def add_pet():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'データがありません。'}), 400

    user_id = get_jwt_identity()
    new_pet = Pet(
        Pet_name=data.get('Pet_name'),
        Gender=data.get('Gender'),
        Birth_date=data.get('Birth_date'),
        Neuter_Spay=data.get('Neuter_Spay'),
        disease_id=data.get('disease_id'),
        User_id=user_id
    )
    # 画像の処理が必要であれば、ここに追加
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'message': 'ペットの登録が完了しました。'}), 201

@pet_bp.route('/', methods=['GET'])
@jwt_required()
def get_pets():
    try:
        user_id = get_jwt_identity()
        pets = Pet.query.filter_by(User_id=user_id).all()
        pet_list = [{
            'Pet_id': pet.Pet_id,
            'Pet_name': pet.Pet_name,
            'Gender': pet.Gender,
            'Birth_date': pet.Birth_date,
            'Neuter_Spay': pet.Neuter_Spay,
            'disease_id': pet.disease_id
        } for pet in pets]
        return jsonify({'pets': pet_list}), 200
    except Exception as e:
        current_app.logger.error(f"ペット一覧取得エラー: {e}")
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500
