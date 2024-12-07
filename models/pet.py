from extensions import db
from sqlalchemy.orm import relationship

class Pet(db.Model):
    __tablename__ = 'Pet'

    Pet_id = db.Column(db.Integer, primary_key=True)
    Pet_name = db.Column(db.String(255), nullable=False)
    Image = db.Column(db.LargeBinary)
    Gender = db.Column(db.CHAR(1))
    Birth_date = db.Column(db.Date)
    Neuter_Spay = db.Column(db.Boolean)
    disease_id = db.Column(db.Integer, db.ForeignKey('Disease.disease_id'), nullable=True) 
    User_id = db.Column(db.Integer, db.ForeignKey('User.User_id'))

   # リレーションシップ
    disease = relationship('Disease', backref='pets')
    owner = relationship('User', backref='pets')