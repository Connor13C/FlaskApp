from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store ')

    @jwt_required
    def get(self, name):
        item = ItemModel.select(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
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

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
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
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}
        return {'items': [item['name'] for item in items], 'message': 'More data available if logged in.'}
