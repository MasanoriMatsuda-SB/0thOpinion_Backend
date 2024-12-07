from extensions import db

class Disease(db.Model):
    __tablename__ = 'Disease'

    disease_id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(100), nullable=False)

    # リレーションシップは Pet モデルで定義済み
