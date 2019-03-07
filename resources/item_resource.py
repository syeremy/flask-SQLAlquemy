import sqlite3

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from models.item import Item



class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every Item needs an store id')

    def get(self, _id):
        item = Item.find_by_id(_id)
        if item:
            return item.json(), 200
        return {'message': 'Item {} not found'.format(_id)}, 404

    @jwt_required()
    def put(self, _id):
        data = ItemResource.parser.parse_args()
        item = Item.find_by_id(_id)

        if item is None:
            # item = Item(data['name'], data['price'], data['store_id'])
            item = Item(**data)
        else:
            item.name = data['name']
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, _id):
        item = Item.find_by_id(_id)
        if item:
            item.delete_from_db()

        return {"message": "Item {} has been deleted.".format(_id)}


class ItemListResource(ItemResource):
    def get(self):
        # return {'items': [item.json() for item in Item.list()]}, 200
        return {'items': list(map(lambda item: item.json(), Item.list()))}

    @jwt_required()
    def post(self):
        # ItemResource.parser.add_argument('id', type=int, required=True, help='This field cannot be left blank!')
        data = ItemResource.parser.parse_args()
        name = data['name']

        if Item.find_by_name(name):
            return {'message': "An Item with id '{}' already exists.".format(name)}, 400

        item = Item(data['name'], data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201
