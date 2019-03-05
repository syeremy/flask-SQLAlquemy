import sqlite3

from flask_restful import Resource, reqparse

from models.user import User


class UserResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank!')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank!')

    def post(self):
        data = UserResource.parser.parse_args()
        user = (data['username'], data['password'])

        if User.find_by_username(data['username']):
            return {'message': 'user {} already exists'.format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_user_query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(insert_user_query, user)

        connection.commit()
        connection.close()

        return {'message': 'User {} created successfully'.format(data['username'])}, 201

