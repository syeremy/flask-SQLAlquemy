import sqlite3

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from models.item import Item

items = []


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank!')

    def get(self, _id):
        item = Item.find_by_id(_id)
        if item:
            return item.json(), 200
        return {'message': 'Item {} not found'.format(_id)}, 404

    @jwt_required()
    def put(self, _id):
        data = ItemResource.parser.parse_args()
        item = Item.find_by_id(_id)
        updated_item = Item(_id, data['name'], data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                updated_item.update()
            except:
                raise
                return {"message": "An error occurred updating the item."}
        return updated_item.json()

    @jwt_required()
    def delete(self, _id):
        global items
        items = list(filter(lambda item: item['id'] != _id, items))
        return {'message': 'item {} deleted'.format(_id)}


class ItemListResource(ItemResource):
    def get(self):
        return {'items': items}, 200

    @jwt_required()
    def post(self):
        # ItemResource.parser.add_argument('id', type=int, required=True, help='This field cannot be left blank!')
        data = ItemResource.parser.parse_args()
        name = data['name']

        if Item.find_by_name(name):
            return {'message': "An Item with id '{}' already exists.".format(name)}, 400

        item = Item(0, data['name'], data['price'])
        item.insert()
        return item.json(), 201
