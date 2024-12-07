from extensions import db
from datetime import datetime

class Question(db.Model):
    __tablename__ = 'Question'

    Question_id = db.Column(db.Integer, primary_key=True)
    User_id = db.Column(db.Integer, db.ForeignKey('User.User_id'))
    Question_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    Content = db.Column(db.Text, nullable=False)
    AI_answer = db.Column(db.Text)
    Resolved = db.Column(db.Boolean, default=False)

    # 関連
    # 必要に応じて他の関連を追加
