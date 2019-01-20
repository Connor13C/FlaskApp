from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt
from models.user import UserModel
from blacklist import BLACKLIST


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': f'User with name {data["username"]} already exists'}, 400
        UserModel(**data).save_to_db()
        return {'message': 'User created successfully'}, 201


class User(Resource):
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'User successfully logged out.'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
