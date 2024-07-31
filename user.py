from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, User
from werkzeug.security import generate_password_hash


user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

user_api = Api(user_bp)


class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)
    
    def post(self):
            data = request.get_json()

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username')
            email = data.get('email')
            phone_number = data.get('phone_number')
            profilepicture = data.get('profilepicture')
            car_info = data.get('car_info')
            password = data.get('password')

            if not all([first_name, last_name, username, email, phone_number, profilepicture, car_info, password]):
                return {"message": "Missing required fields"}, 400
            
            if User.query.filter_by(username=username).first():
                return {"message": "Username already exists"}, 400

            if User.query.filter_by(email=email).first():
                return {"message": "Email already exists"}, 400
            
            if User.query.filter_by(phone_number=phone_number).first():
                return {"message": "Phone number already exists"}, 400
            

            hashed_password = generate_password_hash(data['password'])

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone_number=phone_number,
                profilepicture=profilepicture,
                car_info=car_info,
                password=hashed_password
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                user_dict = new_user.to_dict()
                response = make_response(user_dict, 201)
                return response
            
            except Exception as e:
                db.session.rollback()
                return {"message": "Error creating user", "error": str(e)}, 500

user_api.add_resource(Users, '/', strict_slashes=False)
    


class UserById(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()

        if not user:
            return {"message": "User not found"}, 404
        return user.to_dict(), 200
    


    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return {"message": "User not found"}, 404
        
        data = request.get_json()
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'profilepicture' in data:
            user.profilepicture = data['profilepicture']
        if 'car_info' in data:
            user.car_info = data['car_info']
        
        try:
            db.session.commit()
            return (user.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating user", "error": str(e)}, 500



    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        if not user:
            return {"message": "User not found"}, 404
        
        try:
            db.session.delete(user)
            db.session.commit()
            return {}, 204
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting user", "error": str(e)}, 500

user_api.add_resource(UserById, '/<int:id>')  