from flask_jwt_extended import JWTManager, get_jwt, create_access_token, current_user, jwt_required, create_refresh_token, get_jwt_identity
from flask import Blueprint, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse
from flask_bcrypt import Bcrypt
from models import User, db, TokenBlocklist
from datetime import datetime, timezone, timedelta
import os
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError



UPLOAD_FOLDER = 'uploads/profile_pictures'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


user_auth_bp = Blueprint('user_auth_bp', __name__, url_prefix='/user_auth')
user_auth_api = Api(user_auth_bp)

bcrypt = Bcrypt()
jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None



#Register
register_args =reqparse.RequestParser()
register_args.add_argument('first_name', type=str, required=True, help='First name is required')
register_args.add_argument('last_name', type=str, required=True, help='Last name is required')
register_args.add_argument('username', type=str, required=True, help='Username is required')
register_args.add_argument('email', type=str, required=True, help='Email is required')
register_args.add_argument('phone_number', type=str, required=True, help='Phone number is required')
register_args.add_argument("car_info", type=str, required=True, help='Car Info is required')
register_args.add_argument('password', type=str, required=True, help='Password is required')
register_args.add_argument('password2', type=str, required=True, help='Confirm password is required')


class Register(Resource):
    def post(self):
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        if 'profile_picture' not in request.files:
            return {"msg": "No file part"}, 400

        file = request.files['profile_picture']
        
        if file.filename == '':
            return {"msg": "No selected file"}, 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
        else:
            return {"msg": "File type not allowed"}, 400
        
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        car_info = request.form.get('car_info')
        password = request.form.get('password')
        password2 = request.form.get('password2')


        if password != password2:
            return {"msg": "Passwords don't match"}, 400
        
        if User.query.filter_by(username=username).first():
            return {"msg": "User already exists"}, 400
        
        if User.query.filter_by(email=email).first():
            return {"msg": "Email already registered"}, 400

        if User.query.filter_by(phone_number=phone_number).first():
            return {"msg": "Phone Number already exists"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            car_info=car_info,
            profile_picture=filename,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return {'msg': "User registration successful"}, 201
        except IntegrityError as e:
            db.session.rollback()
            if 'unique constraint' in str(e.orig):
                return {"msg": "User already exists"}, 400
            return {"msg": "Error creating user", "error": str(e)}, 500
        except Exception as e:
            db.session.rollback()
            return {"msg": "An error occurred", "error": str(e)}, 500
        
user_auth_api.add_resource(Register, '/register')




# login
login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, required=True, help='Email is required')
login_args.add_argument('password', type=str, required=True, help='Password is required')

class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()
        
        if not user:
            return {"msg": "User does not Exist"}, 404
        
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            return {"msg": "Incorrect Password"}, 401
        
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=user.id)


        response_data = {
            "msg": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture": user.profile_picture,
                "car_info": user.car_info
            }
        }
        response = make_response(jsonify(response_data))

        response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite='Lax')
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite='Lax')

        return response
    
    @jwt_required(refresh=True)
    def get(self):
        token = create_access_token(identity=current_user.id)
        return {"token": token}

user_auth_api.add_resource(Login, '/login')


class Logout(Resource):
    @jwt_required()
    def get(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)

        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()

        response = make_response(jsonify(msg="JWT revoked"))

        response.set_cookie("access_token", "", expires=0, httponly=True, secure=True, samesite='Lax')
        response.set_cookie("refresh_token", "", expires=0, httponly=True, secure=True, samesite='Lax')
        return response
    
user_auth_api.add_resource(Logout,'/logout')


class CurrentUserResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user:
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "profile_picture": user.profile_picture,
                "car_info": user.car_info,
            }
        else:
            return {"msg": "User not found"}, 404

user_auth_api.add_resource(CurrentUserResource, '/current_user')

class PasswordReset(Resource):
    reset_args = reqparse.RequestParser()
    reset_args.add_argument('email', type=str, required=True, help='Email is required')

    def post(self):
        data = self.reset_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()

        if not user:
            return {"msg": "User not found"}, 404
        
        reset_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return {"msg": "Password reset link sent", "reset_token": reset_token}, 200

user_auth_api.add_resource(PasswordReset, '/password_reset')