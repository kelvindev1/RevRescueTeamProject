from models import db, Payment
from flask import Blueprint, make_response, request
from flask_restful import Api, Resource

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/payments')
payment_api = Api(payment_bp)


class Payments(Resource):
    def get(self):
        payments = [payment.to_dict() for payment in Payment.query.all()]
        return make_response(payments, 200)


payment_api.add_resource(Payments , '/', strict_slashes=False)
