from flask_restful import Resource, reqparse
from models.medicine import MedicineModel
from models.store import StoreModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('ins_number',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('address',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('phy_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('pres_id',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('med_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred while creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class Order(Resource):

    def post(self):

        data = _user_parser.parse_args()
        med = data['med_name']
        if MedicineModel.find_by_name(med):
            return {'message': "Your order was successfull"}
        else:
            return {'message': "Medicine is not available"}

        # if StoreModel.find_by_name(store_name):
        #     if MedicineModel.find_by_name(med_name):
        #        return {'message' : "Your order was successfull"}
        #     else:
        #         return {'message' : "Medicine is not available"}
        # else:
        #     return {'message' : "Entered store name is not valid"}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.find_all()]}
