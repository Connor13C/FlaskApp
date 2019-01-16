from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store ')

    @jwt_required()
    def get(self, name):
        item = ItemModel.select(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.select(name):
            return {'message': f'An item with name {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save()
        except:
            return {'message': 'Something went wrong'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.select(name)
        if item:
            item.delete()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.select(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save()
        return item.json(), 201


class Items(Resource):
    @staticmethod
    def get():
        return {'items': [item.json() for item in ItemModel.find_all()]}
