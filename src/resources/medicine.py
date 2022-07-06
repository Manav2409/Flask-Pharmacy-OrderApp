from flask_restful import Resource, reqparse
from flask_jwt_extended import *
from models.medicine import MedicineModel


class Medicine(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every medicine needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        medicine = MedicineModel.find_by_name(name)
        if medicine:
            return medicine.json()
        return {'message': 'Medicine not found'}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if MedicineModel.find_by_name(name):
            return {'message': "An medicine with name '{}' already exists".format(name)}, 400

        data = Medicine.parser.parse_args()

        medicine = MedicineModel(name, **data)

        try:
            medicine.save_to_db()
        except:
            return {"message": "An error occurred inserting the medicine."}, 500

        return medicine.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        medicine = MedicineModel.find_by_name(name)
        if medicine:
            medicine.delete_from_db()
            return {'message': 'Medicine deleted'}
        return {'message': 'Medicine not found.'}, 404

    def put(self, name):

        data = Medicine.parser.parse_args()
        medicine = MedicineModel.find_by_name(name)

        if medicine:
            medicine.price = data['price']
        else:
            medicine = MedicineModel(name, **data)

        medicine.save_to_db()
        return medicine.json()


class MedicineList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        medicines = [medicine.json() for medicine in MedicineModel.find_all()]
        if user_id:
            return {'medicines': medicines}, 200
        return {
            'medicines': [medicine['name'] for medicine in medicines],
            'message': "More data available if you log in."
        }, 200
