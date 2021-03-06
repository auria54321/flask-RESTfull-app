from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'

jwt = JWT(app, authenticate, identity_function)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler(callable)
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=2)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api.add_resource(Item, '/items/<name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    app.run(port=5050, debug=True)

