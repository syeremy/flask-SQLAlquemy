from flask_restful import Resource, Api, reqparse
from flask_restful import Resource
from flask_jwt import JWT, jwt_required
from models.store import Store


class StoreResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank!')

    def get(self, _id):
        store = Store.find_by_id(_id)

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def put(self, _id):
        data = StoreResource.parser.parse_args()
        item = Store.find_by_id(_id)

        if item is None:
            # item = Item(data['name'], data['price'], data['store_id'])
            item = Store(data['name'])
        else:
            item.name = data['name']

        item.save_to_db()
        return item.json()

    def delete(self, name):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store {} deleted'.format(name)}
        pass


class StoreListResource(Resource):

    def get(self):
        # return {'items': [item.json() for item in Item.list()]}, 200
        return {'stores': list(map(lambda item: item.json(), Store.list()))}

    def post(self):
        data = StoreResource.parser.parse_args()
        name = data['name']

        if Store.find_by_name(name):
            return {'message': 'A store with name {} already exists'.format(name)}, 400

        store = Store(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An Error occurred while creating the store'}, 500
        return store.json(), 201




