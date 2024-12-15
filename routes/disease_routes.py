# routes/disease_routes.py

from flask import Blueprint, request, jsonify, current_app
from extensions import db
from models.disease import Disease
from flask_jwt_extended import jwt_required

disease_bp = Blueprint('disease_bp', __name__)

# GET /api/diseases/ - 全ての疾病を取得
@disease_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_diseases():
    try:
        current_app.logger.debug("Fetching all diseases from the database.")
        diseases = Disease.query.all()
        current_app.logger.debug(f"Retrieved {len(diseases)} diseases.")
        disease_list = [{'disease_id': disease.disease_id, 'disease_name': disease.disease_name} for disease in diseases]
        return jsonify({'diseases': disease_list}), 200
    except AttributeError as ae:
        current_app.logger.error(f"疾病一覧取得エラー: {ae}")
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500
    except Exception as e:
        current_app.logger.error(f"疾病一覧取得エラー: {e}")
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500

# GET /api/diseases/<int:disease_id> - 特定の疾病を取得
@disease_bp.route('/<int:disease_id>', methods=['GET'])
@jwt_required()
def get_disease(disease_id):
    try:
        disease = Disease.query.get_or_404(disease_id)
        disease_data = {
            'disease_id': disease.disease_id,
            'disease_name': disease.disease_name
        }
        return jsonify({'disease': disease_data}), 200
    except Exception as e:
        current_app.logger.error(f"疾病取得エラー: {e}")
        return jsonify({'message': 'サーバーエラーが発生しました。'}), 500

