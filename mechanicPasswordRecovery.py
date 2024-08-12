from flask import Blueprint, make_response, request, current_app
from flask_restful import Api, Resource
from models import Mechanic, db
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

mechanicpassword_bp = Blueprint('mechanicpassword_bp', __name__, url_prefix='/mechanic')
mechanicpassword_recovery_api = Api(mechanicpassword_bp)


class MechanicPasswordRecovery(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')

        mechanic = Mechanic.query.filter_by(email=email).first()

        if mechanic:
            recovery_token = create_recovery_token(mechanic)

            subject = 'Password Recovery'
            body = f"To reset your password, click the link: http://localhost:5173/reset-password/{recovery_token}"

            try:
                send_email(email, subject, body)
                return make_response({'message': 'Reset Email Sent'}, 200)
            except Exception as e:
                return make_response({'message': 'Failed to send email', 'error': str(e)}, 500)
        else:
            return make_response({'message': 'Email not found'}, 404)

def create_recovery_token(mechanic, expires_in=3600):
    s = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'],
        salt='password-recovery-salt'
    )
    return s.dumps(mechanic.email, salt='password-recovery-salt')

mechanicpassword_recovery_api.add_resource(MechanicPasswordRecovery, '/recovery_password', strict_slashes=False)



class MechanicResetPassword(Resource):
    def post(self):
        data = request.get_json()
        recovery_token = data.get('recovery_token')
        new_password = data.get('new_password')

        if not recovery_token or not new_password:
            return make_response({'message': 'Missing New Password'}, 400)

        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='password-recovery-salt')

        try:
            email = s.loads(recovery_token, salt='password-recovery-salt')

        except Exception as e:
            return make_response({'message': 'Invalid or expired recovery token'}, 400)

        mechanic = Mechanic.query.filter_by(email=email).first()

        if mechanic:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

            mechanic.password = hashed_password
            db.session.commit()

            return make_response({'message': 'Password Reset Successful'}, 200)
        else:
            return make_response({'message': 'Mechanic not found'}, 404)
        
mechanicpassword_recovery_api.add_resource(MechanicResetPassword, '/reset_password', strict_slashes=False)


def send_email(to_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = current_app.config['MAIL_USERNAME']
    password = current_app.config['MAIL_PASSWORD']

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(from_email, password)  
            server.sendmail(from_email, [to_email], msg.as_string())
    except Exception as e:
        raise e