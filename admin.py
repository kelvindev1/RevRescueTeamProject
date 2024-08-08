from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, Admin as AdminModel

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admins')

admin_api = Api(admin_bp)

class Admin(Resource):
    def get(self):
        search_query = request.args.get('search', '').lower()

        if search_query:
            admins = AdminModel.query.filter(
                (AdminModel.email.ilike(f"%{search_query}%")) |
                (AdminModel.username.ilike(f"%{search_query}%"))
            ).all()
        else:
            admins = AdminModel.query.all()
            
        admins_list = [admin.to_dict() for admin in admins]
        return make_response(admins_list, 200)

    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return {"message": "Missing required fields"}, 400

        if AdminModel.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        new_admin = AdminModel(
            username=username,
            email=email,
            password=password
        )

        try:
            db.session.add(new_admin)
            db.session.commit()
            admin_dict = new_admin.to_dict()
            response = make_response(admin_dict, 201)
            return response

        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating Admin", "error": str(e)}, 500
        
admin_api.add_resource(Admin, '/', strict_slashes=False)




class AdminById(Resource):
    def get(self, id):
        admin = AdminModel.query.filter(AdminModel.id == id).first()

        if not admin:
            return {"message": "Admin not found"}, 404
        return admin.to_dict(), 200

    def patch(self, id):
        admin = AdminModel.query.filter(AdminModel.id == id).first()

        if not admin:
            return {"message": "Admin not found"}, 404

        data = request.get_json()
        if 'username' in data:
            admin.username = data['username']
        if 'email' in data:
            if AdminModel.query.filter(AdminModel.email == data['email']).first():
                return {"message": "Email already exists"}, 400
            admin.email = data['email']
        if 'password' in data:
            admin.password = data['password']

        try:
            db.session.commit()
            return admin.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating Admin", "error": str(e)}, 500


    def delete(self, id):
        admin = AdminModel.query.filter(AdminModel.id == id).first()

        if not admin:
            return {"message": "Admin not found"}, 404

        try:
            db.session.delete(admin)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting Admin", "error": str(e)}, 500
        
    
admin_api.add_resource(AdminById, '/<int:id>')