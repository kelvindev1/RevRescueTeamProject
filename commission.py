from models import db, Commission, Payment  # Ensure Payment is imported
from flask import Blueprint, make_response, request
from flask_restful import Api, Resource

commission_bp = Blueprint('commission_bp', __name__, url_prefix='/commissions')
commission_api = Api(commission_bp)

class Commissions(Resource):
    def get(self):
        commissions = [commission.to_dict() for commission in Commission.query.all()]
        return make_response(commissions, 200)

    def post(self):
        data = request.get_json()

        amount = data.get('amount')
        payment_id = data.get('payment_id')

        # Validate required fields
        if amount is None or payment_id is None:
            return {"message": "Missing required fields"}, 400

        # Validate payment_id
        if not Payment.query.get(payment_id):
            return {"message": "Payment with given ID does not exist"}, 400

        # Create a new Commission
        new_commission = Commission(
            amount=amount,
            payment_id=payment_id
        )

        try:
            db.session.add(new_commission)
            db.session.commit()
            commission_dict = new_commission.to_dict()
            response = make_response(commission_dict, 201)
            return response
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating commission", "error": str(e)}, 500

commission_api.add_resource(Commissions, '/', strict_slashes=False)



class CommissionById(Resource):
    def get(self, id):
        commission = Commission.query.filter(Commission.id == id).first()

        if not commission:
            return {"message": "Commission not found"}, 404

        return commission.to_dict(), 200

    def delete(self, id):
        commission = Commission.query.filter_by(id=id).first()

        if not commission:
            return {"message": "Commission not found"}, 404
        
        try:
            db.session.delete(commission)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting commission", "error": str(e)}, 500

    def patch(self, id):
        data = request.get_json()
        commission = Commission.query.filter_by(id=id).first()

        if not commission:
            return {"message": "Commission not found"}, 404

        if 'amount' in data:
            commission.amount = data['amount']
        if 'payment_id' in data:
            # Validate payment_id
            if not Payment.query.get(data['payment_id']):
                return {"message": "Payment with given ID does not exist"}, 400
            commission.payment_id = data['payment_id']

        try:
            db.session.commit()
            commission_dict = commission.to_dict()
            return make_response(commission_dict, 200)
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating commission", "error": str(e)}, 500

commission_api.add_resource(CommissionById, '/<int:id>')
