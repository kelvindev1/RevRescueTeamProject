from flask import Blueprint
from flask_restful import Api, Resource
from models import Message


message_bp = Blueprint('message_bp', __name__, url_prefix='/messages')

messages_api = Api(message_bp)

class Messages(Resource):
    def get(self):
        messages = [message.to_dict() for message in Message.query.all()]
        return messages, 200

messages_api.add_resource(Messages, '/')
    
