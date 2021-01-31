from sql_alchemy import database
from datetime import datetime


class UserModel(database.Model):
    __tablename__ = "user"

    user_id = database.Column(database.Integer, primary_key=True)

    username = database.Column(database.String(128), unique=True)
    password = database.Column(database.String(128))
    email = database.Column(database.String(128), nullable=False)
    createdAt = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = database.Column(database.DateTime, onupdate=datetime.utcnow)


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


    def json(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'createdAt': str(self.createdAt),
            'updatedAt': str(self.updatedAt)
        }


    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None


    @classmethod
    def users(cls): 
        users = cls.query.all()
        if users:
            return users
        return None


    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user
        return None 

        
    def update_user(self, data):
        if data.username:
            self.username = data.username
        if data.password:
            self.password = data.password
        if data.email:
            self.email = data.email
        database.session.commit()


    def save_user(self):
        database.session.add(self)
        database.session.commit()


    def delete_user(self):
        database.session.delete(self)
        database.session.commit()