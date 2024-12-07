from flask import Blueprint, request, jsonify
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
