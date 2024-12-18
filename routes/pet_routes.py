# routes/pet_routes.py

from flask import Blueprint, request, jsonify, current_app
from extensions import db
from models.pet import Pet
from models.disease import Disease  # 必要に応じてインポート
from flask_jwt_extended import jwt_required, get_jwt_identity
import base64

pet_bp = Blueprint('pet_bp', __name__)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@pet_bp.route('/', methods=['POST'])
@jwt_required()
def add_pet():
    try:
        # Check if the request is multipart/form-data
        if not request.content_type.startswith('multipart/form-data'):
            return jsonify({'message': 'Content-Type must be multipart/form-data.'}), 400

        # Extract form data
        pet_name = request.form.get('Pet_name')
        gender = request.form.get('Gender')
        birth_date = request.form.get('Birth_date')
        neuter_spay_str = request.form.get('Neuter_Spay')
        neuter_spay = neuter_spay_str.lower() == 'true' if neuter_spay_str else False
        disease_id_str = request.form.get('disease_id')
        disease_id = int(disease_id_str) if disease_id_str and disease_id_str != '' else None

        # Validate required fields
        if not pet_name or not gender or not birth_date:
            return jsonify({'message': 'ペット名、性別、生年月日は必須です。'}), 400

        # Handle image upload
        image = None
        if 'Image' in request.files:
            image_file = request.files['Image']
            if image_file and image_file.filename != '':
                # Validate file type
                if not allowed_file(image_file.filename):
                    return jsonify({'message': '無効なファイルタイプです。'}), 400
                image = image_file.read()  # Read the binary data

        user_id = get_jwt_identity()
        new_pet = Pet(
            Pet_name=pet_name,
            Gender=gender,
            Birth_date=birth_date,
            Neuter_Spay=neuter_spay,
            disease_id=disease_id,
            User_id=user_id,
            Image=image  # Save the binary data
        )
        db.session.add(new_pet)
        db.session.commit()
        return jsonify({'message': 'ペットの登録が完了しました。'}), 201
    except Exception as e:
        current_app.logger.error(f"ペット登録エラー: {e}")
        db.session.rollback()
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500

@pet_bp.route('/', methods=['GET'])
@jwt_required()
def get_pets():
    try:
        user_id = get_jwt_identity()
        pets = Pet.query.filter_by(User_id=user_id).all()
        pet_list = []
        for pet in pets:
            pet_data = {
                'Pet_id': pet.Pet_id,
                'Pet_name': pet.Pet_name,
                'Gender': pet.Gender,
                'Birth_date': pet.Birth_date.strftime('%Y-%m-%d') if pet.Birth_date else None,
                'Neuter_Spay': pet.Neuter_Spay,
                'disease_id': pet.disease_id,
                'Image': base64.b64encode(pet.Image).decode('utf-8') if pet.Image else None
            }
            pet_list.append(pet_data)
        return jsonify({'pets': pet_list}), 200
    except Exception as e:
        current_app.logger.error(f"ペット一覧取得エラー: {e}")
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500

# DELETE /api/pets/<int:pet_id> - 特定のペットを削除
@pet_bp.route('/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    try:
        user_id = get_jwt_identity()
        pet = Pet.query.get_or_404(pet_id)

        db.session.delete(pet)
        db.session.commit()
        return jsonify({'message': 'ペットが削除されました。'}), 200
    except Exception as e:
        current_app.logger.error(f"ペット削除エラー: {e}")
        db.session.rollback()
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500

# POST /api/pets/<int:pet_id>/image - 画像登録
@pet_bp.route('/<int:pet_id>/image', methods=['POST'])
@jwt_required()
def upload_pet_image(pet_id):
    try:
        pet = Pet.query.get_or_404(pet_id)

        if not request.content_type or not request.content_type.startswith('multipart/form-data'):
            return jsonify({'message': 'Content-Type must be multipart/form-data.'}), 400

        if 'Image' not in request.files:
            return jsonify({'message': '画像ファイルが選択されていません。'}), 400

        image_file = request.files['Image']
        if image_file and image_file.filename != '':
            if not allowed_file(image_file.filename):
                return jsonify({'message': '無効なファイルタイプです。'}), 400
            image = image_file.read()
            pet.Image = image
            db.session.commit()
            return jsonify({'message': '画像が更新されました。'}), 200
        else:
            return jsonify({'message': '画像ファイルが不正です。'}), 400

    except Exception as e:
        current_app.logger.error(f"ペット画像更新エラー: {e}")
        db.session.rollback()
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500
