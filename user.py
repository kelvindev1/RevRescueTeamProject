from flask import Blueprint, make_response
from flask_restful import Api, Resource
from models import User


user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

user_api = Api(user_bp)



class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)


user_api.add_resource(Users, '/')
    
