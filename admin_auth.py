from flask_jwt_extended import JWTManager, get_jwt, create_access_token, current_user, jwt_required, create_refresh_token
from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from models import Admin, db, TokenBlocklist
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone, timedelta

admin_auth_bp = Blueprint('admin_auth_bp', __name__,url_prefix='/admin_auth')
admin_auth_api = Api(admin_auth_bp)

bcrypt = Bcrypt()
jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return Admin.query.filter_by(id=identity).first()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

# signup
register_args =reqparse.RequestParser()
register_args.add_argument('username')
register_args.add_argument('email')
register_args.add_argument('password')
register_args.add_argument('password2')

class Register(Resource):
    def post(self):
        data = register_args.parse_args()
        if data.get('password') != data.get('password2'):
            return {"msg": "Passwords don't Match"}
        
        if Admin.query.filter_by(username=data.get('username')).first():
            return {"msg": "Username already exists"}
        
        if Admin.query.filter_by(email=data.get('email')).first():
            return {"msg": "Email already registered"}
        
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_admin = Admin(username=data.get('username'), email=data.get('email'), password = hashed_password)

        db.session.add(new_admin)
        db.session.commit()

        return {'msg': "Admin registration Successful"}
admin_auth_api.add_resource(Register, '/register')


# login
login_args = reqparse.RequestParser()
login_args.add_argument('email')
login_args.add_argument('password')

class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        admin = Admin.query.filter_by(email=data.get('email')).first()
        
        if not admin:
            return {"msg": "Admin does not Exist"}, 404
        
        if not bcrypt.check_password_hash(admin.password, data.get('password')):
            return {"msg": "Incorrect Password"}, 401
        
        access_token = create_access_token(identity=admin.id)
        refresh_token = create_refresh_token(identity=admin.id)

        response = make_response({"msg": "Login successful"})
        response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite='Lax')
        response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite='Lax')

        return response
    
    @jwt_required(refresh = True)
    def get(self):
        token = create_access_token(identity=current_user.id)
        return {"token": token}

admin_auth_api.add_resource(Login, '/login')


class Logout(Resource):
    @jwt_required()
    def get(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return jsonify(msg="JWT revoked")

admin_auth_api.add_resource(Logout,'/logout')