from models import db, Commission
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource

commission_bp = Blueprint('commission_bp', __name__, url_prefix='/commissions')
commission_api = Api(commission_bp)

class Commissions(Resource):
    def get(self):
        commissions = [commission.to_dict() for commission in Commission.query.all()]
        return make_response(jsonify(commissions), 200)

commission_api.add_resource(Commissions, '/', strict_slashes=False)


