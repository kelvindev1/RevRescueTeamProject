from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, Notification, User, Mechanic, AssistanceRequest  # Added AssistanceRequest import

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/notifications')
notification_api = Api(notification_bp)

class Notifications(Resource):
    def get(self):
        notifications = [notification.to_dict() for notification in Notification.query.all()]
        return make_response(notifications, 200)

    def post(self):
        data = request.get_json()
        sender_user_id = data.get('sender_user_id')
        receiver_user_id = data.get('receiver_user_id')
        sender_mechanic_id = data.get('sender_mechanic_id')
        receiver_mechanic_id = data.get('receiver_mechanic_id')
        assistance_request_id = data.get('assistance_request_id')
        message = data.get('message')

        if not all([assistance_request_id, message]):
            return {"message": "Missing required fields"}, 400

        if sender_user_id:
            sender = User.query.get(sender_user_id)
        elif sender_mechanic_id:
            sender = Mechanic.query.get(sender_mechanic_id)
        else:
            return {"message": "Sender not found"}, 404

        if receiver_user_id:
            recipient = User.query.get(receiver_user_id)
        elif receiver_mechanic_id:
            recipient = Mechanic.query.get(receiver_mechanic_id)
        else:
            return {"message": "Recipient not found"}, 404

        assistance_request = AssistanceRequest.query.get(assistance_request_id)
        if not assistance_request:
            return {"message": "Assistance request not found"}, 404

        new_notification = Notification(
            sender_user_id=sender_user_id,
            receiver_user_id=receiver_user_id,
            sender_mechanic_id=sender_mechanic_id,
            receiver_mechanic_id=receiver_mechanic_id,
            assistance_request_id=assistance_request_id,
            message=message
        )

        try:
            db.session.add(new_notification)
            db.session.commit()
            notification_dict = new_notification.to_dict()
            return make_response(notification_dict, 201)
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating notification", "error": str(e)}, 500

notification_api.add_resource(Notifications, '/', strict_slashes=False)

class NotificationById(Resource):
    def get(self, id):
        notification = Notification.query.get(id)
        if not notification:
            return {"message": "Notification not found"}, 404
        return make_response(notification.to_dict(), 200)

    def patch(self, id):
        data = request.get_json()
        notification = Notification.query.get(id)
        
        if not notification:
            return {"message": "Notification not found"}, 404
        
        if 'reply_message' in data:
            notification.reply_message = data['reply_message']
        if 'is_read' in data:
            notification.is_read = data['is_read']
        
        try:
            db.session.commit()
            notification_dict = notification.to_dict()
            return make_response(notification_dict, 200)
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating notification", "error": str(e)}, 500

    def delete(self, id):
        notification = Notification.query.get(id)
        if not notification:
            return {"message": "Notification not found"}, 404

        try:
            db.session.delete(notification)
            db.session.commit()
            return {"message": "Notification deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting notification", "error": str(e)}, 500

notification_api.add_resource(NotificationById, '/<int:id>')
