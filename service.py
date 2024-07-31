from flask import Blueprint, request, make_response
from flask_restful import Resource, Api
from models import Service, db

service_bp = Blueprint('service_bp', __name__, url_prefix='/services')
service_api = Api(service_bp)



class Services(Resource):
    def get(self):
        services = [service.to_dict() for service in Service.query.all()]
        return make_response(services, 200)
    
    def post(self):
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        image_url = data.get('image_url')

        if not all([name, description, image_url]):
            return {"message": "Missing required fields"}, 400


        new_service = Service(
            name=name,
            description=description,
            image_url=image_url
        )

        try:
            db.session.add(new_service)
            db.session.commit()
            service_dict = new_service.to_dict()
            return make_response(service_dict, 201)
            
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating service", "error": str(e)}, 500

service_api.add_resource(Services, '/', strict_slashes=False)




# class ServiceById(Resource):
#     def get(self, id):
#         service = Service.query.filter(Service.id == id).first()

#         if not service:
#             return {"msg": "Service not found"}, 404

#         return service.to_dict(), 200

# service_api.add_resource(ServiceById, "/<int:id")