from flask import Blueprint, request, jsonify
from models.question import Question
from models.pet import Pet  # Petモデルをインポート
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.gpt_api import get_gpt_response
from datetime import datetime

question_bp = Blueprint('question_bp', __name__)

@question_bp.route('/', methods=['POST'])
@jwt_required()
def post_question():
    data = request.get_json()
    user_id = get_jwt_identity()
    content = data.get('Content')
    pet_id = data.get('Pet_id')  # リクエストからPet_idを取得

    if not content:
        return jsonify({'message': '症状の内容が必要です。'}), 400

    if not pet_id:
        return jsonify({'message': 'ペットのIDが必要です。'}), 400

    # ペットの情報をデータベースから取得
    pet = Pet.query.filter_by(Pet_id=pet_id, User_id=user_id).first()
    if not pet:
        return jsonify({'message': 'ペットが見つかりません。'}), 404

    # ペットの情報をプロンプトに組み込む
    pet_info = f"""
    ペットの情報:
    名前: {pet.Pet_name}
    性別: {'オス' if pet.Gender == 'M' else 'メス'}
    生年月日: {pet.Birth_date}
    既往歴: {pet.disease.disease_name if pet.disease else 'なし'}
    """

    full_prompt = f"{pet_info}\nユーザーからの質問: {content}"

    ai_answer = get_gpt_response(full_prompt)
    new_question = Question(
        User_id=user_id,
        Content=content,
        AI_answer=ai_answer,
        Question_date=datetime.utcnow()
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({
        'Question_id': new_question.Question_id,
        'Content': new_question.Content,
        'AI_answer': new_question.AI_answer,
        'Question_date': new_question.Question_date
    }), 201