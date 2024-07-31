
from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import User, db  
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from app import mail, app   

userpass_recovery_bp = Blueprint('userpass_recovery_bp', __name__, url_prefix='/user')
userpass_recovery_bp = Api(userpass_recovery_bp)

class UserPasswordRecovery(Resource):  
    def post(self):
        data = request.get_json()
        email = data['email']

        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a unique recovery token
            recovery_token = create_recovery_token(user)

            # Send recovery email
            msg = Message('Password Recovery', recipients=[email])
            msg.body = f"To reset your password, click the link: http://localhost:5173/reset_password/{recovery_token}"

            try:
                mail.send(msg)
                return make_response({'message': 'Recovery email sent successfully'}, 200)
            except Exception as e:
                print(f"Error sending email: {e}")  
                return make_response({'message': 'Failed to send email', 'error': str(e)}, 500)
        else:
            return make_response({'message': 'Email not found'}, 404)

def create_recovery_token(user):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(user.email, salt='password-recovery-salt', expires_in=3600)  # Token expires in 1 hour

class UserResetPassword(Resource):
    def post(self):
        data = request.get_json()
        recovery_token = data['recovery_token']
        new_password = data['new_password']

        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = s.loads(recovery_token, salt='password-recovery-salt')

        user = User.query.filter_by(email=email).first()

        if user:
            hashed_password = generate_password_hash(new_password)  # Hash the new password

            user.password = hashed_password
            db.session.commit()

            return make_response({'message': 'Password reset successfully'}, 200)
        else:
            return make_response({'message': 'Invalid recovery token'}, 404)
        

userpass_recovery_bp.add_resource(UserPasswordRecovery, '/recovery_password')
userpass_recovery_bp.add_resource(UserResetPassword, '/reset_password')