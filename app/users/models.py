from app import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    about_me = db.Column(db.String(100), nullable=True)
    last_seen = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"User('{self.email}')"
    
    def hash_password(self):
        hashed_password = bcrypt.generate_password_hash(self.password)
        self.password = hashed_password
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)