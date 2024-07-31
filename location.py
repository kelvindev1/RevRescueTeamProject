from flask import Blueprint, make_response
from flask_restful import Resource, Api
from models import Location, db

location_bp = Blueprint('location_bp', __name__, url_prefix='/locations')
location_api = Api(location_bp)

class Locations(Resource):
    def get(self):
        locations = [location.to_dict() for location in Location.query.all()]
        return make_response(locations, 200)

location_api.add_resource(Locations, '/', strict_slashes=False)
