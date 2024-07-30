from flask import Blueprint
from flask_restful import Api, Resource
from models import User


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

user_api = Api(user_bp)

class Welcome(Resource):  
    def get(self):  
        return {'message': 'Welcome to phase 4 Project'}
user_api.add_resource(Welcome, '/')


class Users(Resource):
    def get(self):
        users = [user.to_json() for user in User.query.filter_by(id=id)]
        return users, 200

user_api.add_resource(Users, '/users')
    
