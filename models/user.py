from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'User'

    User_id = db.Column(db.Integer, primary_key=True)
    User_name = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Screen_name = db.Column(db.String(255))
    Sex = db.Column(db.CHAR(1))
    Birth_date = db.Column(db.Date)
    Address = db.Column(db.String(255))
    Email = db.Column(db.String(255))

    # 関連
    questions = relationship('Question', backref='user', lazy=True)

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def get_id(self):
        return str(self.User_id)
