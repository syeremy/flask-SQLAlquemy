import sqlite3

from flask_restful import Resource, reqparse

from models.user import User


class UserResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank!')

    def post(self):
        data = UserResource.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message': 'user {} already exists'.format(data['username'])}, 400

        user = User(data['username'], data['password'])
        user.save_to_db()


        return {'message': 'User {} created successfully'.format(data['username'])}, 201

