from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.subscription import *
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.medicine import Medicine, MedicineList
from resources.store import *
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "dev"
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}



api.add_resource(Store, '/store/<string:name>')
api.add_resource(Order, '/order')
api.add_resource(StoreList, '/stores')

api.add_resource(SubscriptionRegister, '/addsubscribe')
api.add_resource(Subscription, '/subscription/<int:member_id>')
api.add_resource(Unsubscribe , '/unsubscribe')
api.add_resource(SubscriptionList , '/subscriber') #not working

api.add_resource(Medicine, '/medicine/<string:name>')
api.add_resource(MedicineList, '/medicines')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
