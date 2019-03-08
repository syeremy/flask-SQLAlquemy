from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from resources.user_resource import UserResource
from security import authenticate, identity
from resources.item_resource import ItemResource, ItemListResource
from resources.store_resource import StoreResource, StoreListResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# disables the Flask SQLAlchemy tracker, no the SQLAlchemy tracker itself.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'syeremy_secret_key'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # endpoint : /auth


api.add_resource(ItemResource, '/items/<int:_id>')
api.add_resource(ItemListResource, '/items')
api.add_resource(UserResource, '/users')
api.add_resource(StoreResource, '/stores/<int:_id>')
api.add_resource(StoreListResource, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5002, debug=True)

