from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, AssistanceRequest, User, Mechanic
from twilio.rest import Client
import os


assistance_request_bp = Blueprint('assistance_request_bp', __name__, url_prefix='/assistance_requests')
assistance_request_api = Api(assistance_request_bp)



def get_twilio_client():
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class AssistanceRequests(Resource):
    def get(self):
        assistancerequests = [assistancerequest.to_dict() for assistancerequest in AssistanceRequest.query.all()]
        return make_response(assistancerequests, 200)
    

    def post(self):
        data = request.get_json()

        user_id = data.get('user_id')
        mechanic_id = data.get('mechanic_id')
        message = data.get('message')
        resolved = data.get('resolved', False)

        if not all([user_id, mechanic_id, message]):
            return {"message": "Missing required fields"}, 400

        user = User.query.get(user_id)
        mechanic = Mechanic.query.get(mechanic_id)

        if not user:
            return {"message": "User with given ID does not exist"}, 400

        if not mechanic:
            return {"message": "Mechanic with given ID does not exist"}, 400

        new_request = AssistanceRequest(
            user_id=user_id,
            mechanic_id=mechanic_id,
            message=message,
            resolved=resolved
        )

        try:
            db.session.add(new_request)
            db.session.commit()

            client = get_twilio_client()

            message = client.messages.create(
                body=f"A new assistance request has been made: {message}",
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=mechanic.phone_number
            )
            
            request_dict = new_request.to_dict()
            response = make_response(request_dict, 201)
            return response
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating assistance request", "error": str(e)}, 500


assistance_request_api.add_resource(AssistanceRequests, '/', strict_slashes=False)



class AssistanceRequestById(Resource):
    def get(self, id):
        assistancerequest = AssistanceRequest.query.filter(AssistanceRequest.id == id).first()
        
        if not assistancerequest:
            return {"message": "AssistanceRequest not found"}, 404
        return assistancerequest.to_dict(), 200

    def patch(self, id):
        data = request.get_json()
        assistancerequest = AssistanceRequest.query.filter_by(id=id).first()

        if not assistancerequest:
            return {"message": "AssistanceRequest not found"}, 404
        
        if 'message' in data:
            assistancerequest.message = data['message']
        if 'resolved' in data:
            assistancerequest.resolved = data['resolved']

        try:
            db.session.commit()
            return assistancerequest.to_dict(), 200
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating assistance request", "error": str(e)}, 500


    def delete(self, id):
        assistancerequest = AssistanceRequest.query.filter_by(id=id).first()

        if not assistancerequest:
            return {"message": "Assistancerequest not found"}, 404
        
        try:
            db.session.delete(assistancerequest)
            db.session.commit()
            return {}, 204
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting user", "error": str(e)}, 500
        
assistance_request_api.add_resource(AssistanceRequestById, '/<int:id>')