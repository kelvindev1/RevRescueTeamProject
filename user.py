from flask import Blueprint
from flask_restful import Api, Resource


user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

user_api = Api(user_bp)

class Welcome(Resource):  
    def get(self):  
        return {'message': 'Welcome to phase 4 Project'}
    

user_api.add_resource(Welcome, '/')