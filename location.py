from flask import Blueprint, request, make_response
from flask_restful import Resource, Api
from models import Location, db

location_bp = Blueprint('location_bp', __name__, url_prefix='/locations')
location_api = Api(location_bp)

class Locations(Resource):
    def get(self):
        locations = [location.to_dict() for location in Location.query.all()]
        return make_response(locations, 200)
    
    def post(self):
        data = request.get_json()
        address = data.get('address')

        if not address:
            return make_response({"message": "Missing required fields"}, 400)

        new_location = Location(address=address)

        try:
            db.session.add(new_location)
            db.session.commit()
            location_dict = new_location.to_dict()
            return make_response(location_dict, 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error creating location", "error": str(e)}, 500)

class LocationById(Resource):
    def get(self, id):
        location = Location.query.filter(Location.id == id).first()
    
        if not location:
            return make_response({"message": "Location not found"}, 404)

        return make_response(location.to_dict(), 200)

    def put(self, id):
        # Update an existing location
        data = request.get_json()
        location = Location.query.filter(Location.id == id).first()

        if not location:
            return make_response({"message": "Location not found"}, 404)

        address = data.get('address', location.address)

        location.address = address

        try:
            db.session.commit()
            return make_response(location.to_dict(), 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error updating location", "error": str(e)}, 500)

    def delete(self, id):
        location = Location.query.filter(Location.id == id).first()
        
        if not location:
            return make_response({"message": "Location not found"}, 404)

        try:
            db.session.delete(location)
            db.session.commit()
            return make_response({}, 204)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error deleting location", "error": str(e)}, 500)

location_api.add_resource(Locations, '/', strict_slashes=False)
location_api.add_resource(LocationById, '/<int:id>', strict_slashes=False)
