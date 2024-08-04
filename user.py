from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'uploads/profile_pictures'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


user_bp = Blueprint('user_bp', __name__, url_prefix='/users')
user_api = Api(user_bp)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        for user in users:
            if user['profile_picture']:
                user['profile_picture'] = f"http://127.0.0.1:5555/uploads/{user['profile_picture']}"
        return make_response(users, 200)
    
    def post(self):
        data = request.form.to_dict()
        file = request.files.get('profile_picture')

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        location = data.get('location')
        phone_number = data.get('phone_number')
        car_info = data.get('car_info')
        password = data.get('password')

        if not file:
            return {"message": "Profile picture is required"}, 400
        
        if file.filename == '':
            return {"message": "No selected file"}, 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
        else:
            return {"message": "File type not allowed"}, 400
        
        if not all([first_name, last_name, username, email, location, phone_number, car_info, password]):
            return {"message": "Missing required fields"}, 400
        
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 400
        
        if User.query.filter_by(phone_number=phone_number).first():
            return {"message": "Phone number already exists"}, 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            location=location,
            profile_picture=filename,
            car_info=car_info,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            user_dict = new_user.to_dict()
            user_dict['profile_picture'] = f"http://127.0.0.1:5555/uploads/{user_dict['profile_picture']}"
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
        
        user_dict = user.to_dict()
        if user_dict['profile_picture']:
            user_dict['profile_picture'] = f"http://127.0.0.1:5555/uploads/{user_dict['profile_picture']}"
        return user_dict, 200

    # def patch(self, id):
    #     user = User.query.get(id)
    #     if not user:
    #         return {"message": "User not found"}, 404
        
    #     data = request.get_json()
        
    #     if 'first_name' in data:
    #         user.first_name = data['first_name']
    #     if 'last_name' in data:
    #         user.last_name = data['last_name']
    #     if 'username' in data:
    #         user.username = data['username']
    #     if 'email' in data:
    #         user.email = data['email']
    #     if 'phone_number' in data:
    #         user.phone_number = data['phone_number']
    #     if 'location' in data:
    #         user.location = data['location']
    #     if 'profile_picture' in data:
    #         user.profile_picture = data['profile_picture']
    #     if 'car_info' in data:
    #         user.car_info = data['car_info']
        
    #     try:
    #         db.session.commit()
    #         return user.to_dict(), 200
    #     except Exception as e:
    #         db.session.rollback()
    #         return {"message": "Error updating user", "error": str(e)}, 500


    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return {"message": "User not found"}, 404

        data = request.form.to_dict()

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                data['profile_picture'] = filename

        for key, value in data.items():
            setattr(user, key, value)
        
        try:
            db.session.commit()
            user_dict = user.to_dict()
            if user_dict['profile_picture']:
                user_dict['profile_picture'] = f"http://127.0.0.1:5555/uploads/{user_dict['profile_picture']}"
            return user_dict, 200
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating User", "error": str(e)}, 500
        


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