from datetime import datetime
from flask_restful import Resource, reqparse
from flask_restful import inputs

from models.subscription import SubscriptionModel
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('member_id',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('subscription_date',
                          type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S'),                                 
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('pres_id',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('refill',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('m_location',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('sub_status',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_sub_parser = reqparse.RequestParser()
_sub_parser.add_argument('member_id',
                        type = int,
                        required = True,
                        help="This field is required")
_sub_parser.add_argument('id',
                        type = int,
                        required = True,
                        help="This field is required")
                        
class SubscriptionRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if SubscriptionModel.find_by_member_id(data['member_id']):
            return {'message': "A user with this member id already exists"}, 400

        member_id = SubscriptionModel(**data)
        member_id.save_to_db()

        return {"message": "Membership created successfully"}, 201

class Subscription(Resource):
    @classmethod
    def get(self , member_id):
        mem = SubscriptionModel.find_by_member_id(member_id)
        if not mem:
            return {'message' : 'Not found'} , 404
        return mem.json()

    # @classmethod
    # def post(self, member_id):
    #     if SubscriptionModel.find_by_id(member_id):
    #         return {'message': "A member with this id '{}' already exists.".format(member_id)}, 404

    #     subscriber = SubscriptionModel(member_id)
    #     try:
    #         subscriber.save_to_db()
    #     except:
    #         return {'message': "An error occurred while creating the subscription."}, 500

    #     return subscriber.json(), 201

    @classmethod
    def delete(self, member_id):
        subscriber = SubscriptionModel.find_by_member_id(member_id)
        if subscriber:
            subscriber.delete_from_db()

        return {'message': 'Subscriber deleted'}
        

class Unsubscribe(Resource):
    def post(self):
        data = _sub_parser.parse_args()
        mem_id = data['member_id']
        if SubscriptionModel.find_by_member_id(mem_id):
            return {'Subscription_Status' : False}

class SubscriptionList(Resource):
    def get(self):
        return {'subscription': [x.json() for x in SubscriptionModel.find_all()]}