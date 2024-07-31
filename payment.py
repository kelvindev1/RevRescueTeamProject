from models import db, Payment, User, Mechanic, AssistanceRequest
from flask import Blueprint, make_response, request
from flask_restful import Api, Resource

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/payments')
payment_api = Api(payment_bp)

class Payments(Resource):
    def get(self):
        payments = [payment.to_dict() for payment in Payment.query.all()]
        return make_response(payments, 200)

    def post(self):
        data = request.get_json()

        amount = data.get('amount')
        status = data.get('status')
        user_id = data.get('user_id')
        mechanic_id = data.get('mechanic_id')
        assistance_request_id = data.get('assistance_request_id')

        # Validate required fields
        if not all([amount, status]):
            return {"message": "Missing required fields"}, 400

        if user_id and not User.query.get(user_id):
            return {"message": "User with given ID does not exist"}, 400
        if mechanic_id and not Mechanic.query.get(mechanic_id):
            return {"message": "Mechanic with given ID does not exist"}, 400
        if assistance_request_id and not AssistanceRequest.query.get(assistance_request_id):
            return {"message": "AssistanceRequest with given ID does not exist"}, 400

        new_payment = Payment(
            amount=amount,
            status=status,
            user_id=user_id,
            mechanic_id=mechanic_id,
            assistance_request_id=assistance_request_id
        )

        try:
            db.session.add(new_payment)
            db.session.commit()
            payment_dict = new_payment.to_dict()
            response = make_response(payment_dict, 201)
            return response
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating payment", "error": str(e)}, 500

payment_api.add_resource(Payments, '/', strict_slashes=False)



class PaymentById(Resource):
    def get(self, id):
        payment = Payment.query.filter(Payment.id == id).first()

        if not payment:
            return {"message": "Payment not found"}, 404
        return payment.to_dict(), 200

    def patch(self, id):
        data = request.get_json()
        payment = Payment.query.filter_by(id=id).first()

        if not payment:
            return {"message": "Payment not found"}, 404

        # Update fields if provided
        if 'amount' in data:
            payment.amount = data['amount']
        if 'status' in data:
            payment.status = data['status']
        if 'user_id' in data:
            if not User.query.get(data['user_id']):
                return {"message": "User with given ID does not exist"}, 400
            payment.user_id = data['user_id']
        if 'mechanic_id' in data:
            if not Mechanic.query.get(data['mechanic_id']):
                return {"message": "Mechanic with given ID does not exist"}, 400
            payment.mechanic_id = data['mechanic_id']
        if 'assistance_request_id' in data:
            if not AssistanceRequest.query.get(data['assistance_request_id']):
                return {"message": "AssistanceRequest with given ID does not exist"}, 400
            payment.assistance_request_id = data['assistance_request_id']

        try:
            db.session.commit()
            payment_dict = payment.to_dict()
            return make_response(payment_dict, 200)
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating payment", "error": str(e)}, 500

    def delete(self, id):
        payment = Payment.query.filter_by(id=id).first()

        if not payment:
            return {"message": "Payment not found"}, 404
        
        try:
            db.session.delete(payment)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting payment", "error": str(e)}, 500



payment_api.add_resource(PaymentById, '/<int:id>')