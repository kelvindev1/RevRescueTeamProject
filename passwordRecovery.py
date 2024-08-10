from flask import Blueprint, make_response, request, current_app
from flask_restful import Api, Resource
from models import User, db
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from flask_bcrypt import Bcrypt
# from app import app

bcrypt = Bcrypt()
# bcrypt = Bcrypt(app)


# Blueprint and API initialization
userpass_recovery_bp = Blueprint('userpass_recovery_bp', __name__, url_prefix='/user')
userpass_recovery_api = Api(userpass_recovery_bp)

class UserPasswordRecovery(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')

        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a unique recovery token
            recovery_token = create_recovery_token(user)
            print(f"Generated recovery token: {recovery_token}")  # Debugging line

            # Prepare recovery email content
            subject = 'Password Recovery'
            body = f"To reset your password, click the link: http://localhost:5173/reset-password/{recovery_token}"

            # Send recovery email using custom SMTP function
            try:
                send_email(email, subject, body)
                return make_response({'message': 'Recovery email sent successfully'}, 200)
            except Exception as e:
                print(f"Error sending email: {e}")
                return make_response({'message': 'Failed to send email', 'error': str(e)}, 500)
        else:
            return make_response({'message': 'Email not found'}, 404)

def create_recovery_token(user, expires_in=3600):  # Default expiration time set to 1 hour
    s = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'],
        salt='password-recovery-salt'
    )
    return s.dumps(user.email, salt='password-recovery-salt')

class UserResetPassword(Resource):
    def post(self):
        data = request.get_json()
        recovery_token = data.get('recovery_token')
        new_password = data.get('new_password')

        # Debugging print statements
        # print(f"Received recovery token: {recovery_token}")
        # print(f"Received new password: {new_password}")

        if not recovery_token or not new_password:
            return make_response({'message': 'Missing recovery token or new password'}, 400)

        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='password-recovery-salt')

        try:
            email = s.loads(recovery_token, salt='password-recovery-salt')
            # print(f"Token is valid for email: {email}")  # Debugging line
        except Exception as e:
            print(f"Exception details: {e}")  
            return make_response({'message': 'Invalid or expired recovery token'}, 400)

        user = User.query.filter_by(email=email).first()

        if user:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')  # Hash the new password

            user.password = hashed_password
            db.session.commit()

            return make_response({'message': 'Password reset successfully'}, 200)
        else:
            return make_response({'message': 'User not found'}, 404)

def send_email(to_email, subject, body):
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = current_app.config['MAIL_USERNAME']
    password = current_app.config['MAIL_PASSWORD']

    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(from_email, password)  
            server.sendmail(from_email, [to_email], msg.as_string())  # Send email
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e  

def register_userpass_recovery_bp(app):
    userpass_recovery_api.add_resource(UserPasswordRecovery, '/recovery_password', strict_slashes=False)
    userpass_recovery_api.add_resource(UserResetPassword, '/reset_password', strict_slashes=False)
    app.register_blueprint(userpass_recovery_bp)
