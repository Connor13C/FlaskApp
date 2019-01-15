from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.select(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.select(name):
            return {'message': f'Store {name} already exists'}, 400
        store = StoreModel(name)
        try:
            store.save()
        except:
            return {'message': 'Something went wrong'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.select(name)
        if store:
            store.delete()
        return {'message': 'Store deleted'}


class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
