from flask import Blueprint, request, make_response
from flask_restful import Resource, Api
from models import Service, db, Mechanic

service_bp = Blueprint('service_bp', __name__, url_prefix='/services')
service_api = Api(service_bp)

class Services(Resource):
    def get(self):
        services = Service.query.all()
        response_data = []
        
        for service in services:
            service_data = service.to_dict()
            mechanic = Mechanic.query.filter_by(id=service.mechanic_id).first()
            if mechanic:
                service_data['mechanic'] = {
                    'first_name': mechanic.first_name,
                    'last_name': mechanic.last_name,
                    'profile_picture': mechanic.profile_picture
                }
            response_data.append(service_data)

        return make_response(response_data, 200)
    
    def post(self):
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        image_url = data.get('image_url')
        mechanic_id = data.get('mechanic_id')

        if not all([name, description, image_url, mechanic_id]):
            return make_response({"message": "Missing required fields"}, 400)

        new_service = Service(
            name=name,
            description=description,
            image_url=image_url,
            mechanic_id=mechanic_id
        )

        try:
            db.session.add(new_service)
            db.session.commit()
            service_dict = new_service.to_dict()
            mechanic = Mechanic.query.filter_by(id=mechanic_id).first()
            if mechanic:
                service_dict['mechanic'] = {
                    'first_name': mechanic.first_name,
                    'last_name': mechanic.last_name,
                    'profile_picture': mechanic.profile_picture
                }
            return make_response({"service": service_dict}, 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error creating service", "error": str(e)}, 500)
        
service_api.add_resource(Services, '/', strict_slashes=False)



class ServiceById(Resource):
    def get(self, id):
        service = Service.query.filter(Service.id == id).first()
    
        if not service:
            return make_response({"message": "Service not found"}, 404)

        service_data = service.to_dict()
        mechanic = Mechanic.query.filter_by(id=service.mechanic_id).first()
        if mechanic:
            service_data['mechanic'] = {
                'first_name': mechanic.first_name,
                'last_name': mechanic.last_name,
                'profile_picture': mechanic.profile_picture
            }

        return make_response(service_data, 200)

    def patch(self, id):
        data = request.get_json()
        service = Service.query.filter(Service.id == id).first()

        if not service:
            return make_response({"message": "Service not found"}, 404)

        if 'name' in data:
            service.name = data['name']
        if 'description' in data:
            service.description = data['description']
        if 'image_url' in data:
            service.image_url = data['image_url']
        if 'mechanic_id' in data:
            service.mechanic_id = data['mechanic_id']

        try:
            db.session.commit()
            mechanic = Mechanic.query.filter_by(id=service.mechanic_id).first()
            service_data = service.to_dict()
            if mechanic:
                service_data['mechanic'] = {
                    'first_name': mechanic.first_name,
                    'last_name': mechanic.last_name,
                    'profile_picture': mechanic.profile_picture
                }
            return make_response({"service": service_data}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error updating service", "error": str(e)}, 500)

    def delete(self, id):
        service = Service.query.filter(Service.id == id).first()
        
        if not service:
            return make_response({"message": "Service not found"}, 404)

        try:
            db.session.delete(service)
            db.session.commit()
            return make_response({}, 204)
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error deleting service", "error": str(e)}, 500)

service_api.add_resource(ServiceById, '/<int:id>', strict_slashes=False)
