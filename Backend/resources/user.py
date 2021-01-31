from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST


attributes = reqparse.RequestParser()
attributes.add_argument('username', type=str)
attributes.add_argument('password', type=str)
attributes.add_argument('email', type=str)


class User(Resource):
    # /user/{user_id}
    @jwt_required
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404


    @jwt_required
    # /user/{user_id}
    def put(self, user_id):
        data = attributes.parse_args()
        
        user = UserModel.find_user(user_id)
        if user:
            user.update_user(data)
            return {'message': 'Updated user'}
        return {'message': 'User not found'}, 404


    @jwt_required
    # /user/{user_id}
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404


class Users(Resource):
    # /api/users
    @jwt_required
    def get(self):
        users = UserModel.users()
        temp_users = []
        if users:
            for user in users:
                data = {'user_id': user.user_id, 'username': user.username, 'password': user.password, 'email': user.email, 'createdAt': str(user.createdAt), 'updatedAt': str(user.updatedAt)}
                temp_users.append(data)
            return temp_users
        return {'message': 'There are no registered users'}, 404


class CreateUser(Resource):
    # /api/auth/register
    #@jwt_required
    def post(self):
        data = attributes.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "The User '{}' already exists.".format(data['username'])}

        user = UserModel(**data)
        user.save_user()
        return {"message": "User cread successfully!"}, 201


class UserAuth(Resource):
    # /api/auth/login
    def post(self):
        data = attributes.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token, 'user': user.json()}, 200
        return {'message': 'The email or password is incorrect'}, 401



