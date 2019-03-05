from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from resources.user_resource import UserResource
from security import authenticate, identity
from resources.item_resource import ItemResource, ItemListResource

app = Flask(__name__)
app.secret_key = 'syeremy_secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # endpoint : /auth


api.add_resource(ItemResource, '/items/<int:_id>')
api.add_resource(ItemListResource, '/items')
api.add_resource(UserResource, '/users')

if __name__ == "__main__":
    app.run(port=5002, debug=True)

