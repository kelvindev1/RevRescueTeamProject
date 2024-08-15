from flask import Blueprint, request, make_response
from flask_restful import Resource, Api
from models import Service, db, Mechanic
from flask_jwt_extended import jwt_required, get_jwt_identity

service_bp = Blueprint('service_bp', __name__, url_prefix='/services')
service_api = Api(service_bp)



class Services(Resource):
    @jwt_required()
    def get(self):
        current_mechanic_id = get_jwt_identity()
        search_query = request.args.get('search', '').lower()

        services_query = (
            Service.query
            .join(Mechanic)
            .filter(Service.mechanic_id == current_mechanic_id)
        )

        if search_query:
            services_query = services_query.filter(
                (Service.name.ilike(f"%{search_query}%")) |
                (Mechanic.first_name.ilike(f"%{search_query}%")) |
                (Mechanic.last_name.ilike(f"%{search_query}%"))
            )

        services = services_query.all()

        response_data = [
            {
                **service.to_dict(),
                'mechanic': {
                    'first_name': service.mechanic.first_name,
                    'last_name': service.mechanic.last_name,
                    'profile_picture': service.mechanic.profile_picture
                }
            }
            for service in services
        ]

        return make_response(response_data, 200)
    


    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
        
            current_mechanic_id = get_jwt_identity()

            name = data.get('name')
            description = data.get('description')
            image_url = data.get('image_url')

            if not all([name, description, image_url]):
                return make_response({"message": "Missing required fields"}, 400)

            new_service = Service(
                name=name,
                description=description,
                image_url=image_url,
                mechanic_id=current_mechanic_id
            )

            
            db.session.add(new_service)
            db.session.commit()

            
            service_dict = new_service.to_dict()

            
            mechanic = Mechanic.query.get(current_mechanic_id)
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
    @jwt_required()
    def get(self, id):
        current_mechanic_id = get_jwt_identity()
        service = Service.query.filter(Service.id == id, Service.mechanic_id == current_mechanic_id).first()
        
        if not service:
            return make_response({"message": "Service not found or access denied"}, 404)

        service_data = service.to_dict()
        mechanic = Mechanic.query.get(service.mechanic_id)
        
        if mechanic:
            service_data['mechanic'] = {
                'first_name': mechanic.first_name,
                'last_name': mechanic.last_name,
                'profile_picture': mechanic.profile_picture
            }

        return make_response(service_data, 200)

    @jwt_required() 
    def patch(self, id):
        current_mechanic_id = get_jwt_identity()
        service = Service.query.filter(Service.id == id, Service.mechanic_id == current_mechanic_id).first()

        if not service:
            return make_response({"message": "Service not found or access denied"}, 404)

        data = request.get_json() or {}
        if 'name' in data:
            service.name = data['name']
        if 'description' in data:
            service.description = data['description']
        if 'image_url' in data:
            service.image_url = data['image_url']

        try:
            db.session.commit()
            service_data = service.to_dict()
            mechanic = Mechanic.query.get(service.mechanic_id)
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

    @jwt_required() 
    def delete(self, id):
        """Delete a service by its ID."""
        current_mechanic_id = get_jwt_identity()
        service = Service.query.filter(Service.id == id, Service.mechanic_id == current_mechanic_id).first()
        
        if not service:
            return make_response({"message": "Service not found or access denied"}, 404)

        try:
            db.session.delete(service)
            db.session.commit()
            return{}, 204
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Error deleting service", "error": str(e)}, 500)

service_api.add_resource(ServiceById, '/<int:id>', strict_slashes=False)



class AllServices(Resource):
    def get(self):
        """Retrieve a list of services, optionally filtered by search query."""
        search_query = request.args.get('search', '').lower()
        services_query = Service.query.join(Mechanic)

        if search_query:
            services_query = services_query.filter(
                (Service.name.ilike(f"%{search_query}%")) |
                (Mechanic.first_name.ilike(f"%{search_query}%")) |
                (Mechanic.last_name.ilike(f"%{search_query}%"))
            )

        services = services_query.all()

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
service_api.add_resource(AllServices, '/all', strict_slashes=False)