import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from sql_alchemy import database
from datetime import timedelta 

from resources.user import User, Users, CreateUser, UserAuth
from resources.parent import Parent, CreateParent, Parents
from resources.child import Child, CreateChild, ChildUseCase


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://{}:{}@{}:{}".format(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_DB"), os.getenv("POSTGRES_PORT"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "ASLDKAS;LKIO342342389098324"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=7200)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=7200)




api = Api(app)
jwt = JWTManager(app)
CORS(app)


@app.before_first_request
def create_database():
    database.create_all()


@jwt.token_in_blacklist_loader
def check_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalid_access_token():
    return jsonify({'message': 'You have been logged out.'}), 401


api.add_resource(CreateUser, '/api/auth/register')
api.add_resource(UserAuth, '/api/auth/login')
api.add_resource(User, '/api/user/<int:user_id>')
api.add_resource(Users, '/api/users')

api.add_resource(Parent, '/api/parent/<int:id>')
api.add_resource(CreateParent, '/api/parent')
api.add_resource(Parents, '/api/parents')

api.add_resource(Child, '/api/child/<int:id>')
api.add_resource(ChildUseCase, '/api/child/<parents>')
api.add_resource(CreateChild, '/api/child')


if __name__ == '__main__':
    database.init_app(app)
    app.run(host='0.0.0.0', debug=True)