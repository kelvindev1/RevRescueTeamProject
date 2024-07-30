from flask import Blueprint
from flask_restful import Api, Resource
from models import Mechanic


mechanic_bp = Blueprint('mechanic_bp', __name__, url_prefix='/mechanics')

mechanic_api = Api(mechanic_bp)

class Mechanics(Resource):
    def get(self):
        mechanics = [mechanic.to_dict() for mechanic in Mechanic.query.all()]
        return mechanics, 200

mechanic_api.add_resource(Mechanics, '/')
    
