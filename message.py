from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, Message, User, Mechanic
from datetime import datetime


message_bp = Blueprint('message_bp', __name__, url_prefix='/messages')

messages_api = Api(message_bp)



class Messages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]
        return messages, 200


    def post(self):
        data = request.get_json()

        content = data.get('content')
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')


        if not all([content, sender_id, receiver_id]):
            return {"message": "Missing required fields"}, 400

        if not User.query.get(sender_id):
            return {"message": "Sender does not exist"}, 404
        
        if not Mechanic.query.get(receiver_id):
            return {"message": "Receiver does not exist"}, 404
        
        new_message = Message(
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id,
            sent_at=datetime.utcnow()
        )

        try:
            db.session.add(new_message)
            db.session.commit()

            message_dict = new_message.to_dict()
            response = make_response(message_dict, 201)
            return response
        
        except Exception as exc:
            db.session.rollback()
            return {"message": "Error creating Message", "error": str(exc)}, 500

messages_api.add_resource(Messages, '/', strict_slashes=False)



class MessageById(Resource):
    def get (self, id):
        message = Message.query.filter(Message.id == id).first()

        if not message:
            return {"message": "Message not found"}, 404
        return message.to_dict(), 200
    

    def patch(self, id):
        message = Message.query.get(id)

        if not message:
            return {"message": "Message not found"}, 404
        
        data = request.get_json()
        if 'content' in data:
            message.content = data['content']

        try:
            db.session.commit()
            return (message.to_dict()), 200
        except Exception as exc:
            db.session.rollback()
            return {"message": "Error updating Message", "error": str(exc)}, 500
        

    def delete(self, id):
        message = Message.query.filter_by(id=id).first()

        if not message:
            return {"message": "Error deleting Message"}, 404
        try:
            db.session.delete(message)
            db.session.commit()
            return {}, 204
        
        except Exception as exc:
            db.session.rollback()
            return {"message": "Error deleting Message", "error": str(exc)}, 500
    

messages_api.add_resource(MessageById, '/<int:id>')
    
