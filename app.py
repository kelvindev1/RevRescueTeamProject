from flask import Flask, send_from_directory, render_template, request
from flask_migrate import Migrate
from flask_cors import CORS
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from redis import Redis
from models import db, ReportData
from user import user_bp
from mechanic import mechanic_bp
from admin import admin_bp
from review import review_bp
from service import service_bp
from location import location_bp
from payment import payment_bp
from commission import commission_bp
from assistance_request import assistance_request_bp
from notification import notification_bp
from user_auth import user_auth_bp, jwt, bcrypt
from admin_auth import admin_auth_bp, jwt, bcrypt
from mechanic_auth import mechanic_auth_bp, jwt, bcrypt
from datetime import timedelta, datetime
from extensions import mail
from passwordRecovery import bcrypt
from passwordRecovery import userpass_recovery_bp




app = Flask(__name__)
CORS(app, supports_credentials=True)



UPLOAD_FOLDER = 'uploads/profile_pictures'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# run python then run import uuid then run uuid.uuid4().hex
app.config['SECRET_KEY'] = '18895d3dd34344728f4365a92988db5a'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=20)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)
app.json.compact = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'eliud.koome@student.moringaschool.com'
app.config['MAIL_PASSWORD'] = 'vwqyisyngrmvdiae'
app.config['MAIL_DEFAULT_SENDER'] = 'eliud.koome@student.moringaschool.com'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

migrate = Migrate(app, db)
db.init_app(app)
mail.init_app(app) 

jwt.init_app(app)
bcrypt.init_app(app)


app.register_blueprint(user_bp)
app.register_blueprint(mechanic_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(review_bp)
app.register_blueprint(service_bp)
app.register_blueprint(location_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(commission_bp)
app.register_blueprint(assistance_request_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(user_auth_bp)
app.register_blueprint(admin_auth_bp)
app.register_blueprint(mechanic_auth_bp)
app.register_blueprint(userpass_recovery_bp)



# redis_store = Redis(host='localhost', port=6379)

# limiter = Limiter(
#     key_func=get_remote_address,
#     storage_uri="redis://localhost:6379",
#     app=app,
#     default_limits=["200 per day", "50 per hour"]
# )


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return 'Welcome to the phase 5 Project'

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/report', methods=['GET', 'POST'])  
def report():  
    report_data = []  

    if request.method == 'POST':  
        start_date = request.form.get('start_date')  
        end_date = request.form.get('end_date')  

        print("Start Date:", start_date)  
        print("End Date:", end_date)  

        if not start_date or not end_date:  
            return render_template('report.html', error="Start date or end date is missing.")  

        try:   
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()  
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()  

            report_data = ReportData.query.filter(  
                ReportData.date_field >= start_date,  
                ReportData.date_field <= end_date  
            ).all()  
        except ValueError:  
            return render_template('report.html', error="Invalid date format. Please use YYYY-MM-DD.")  

    return render_template('report.html', report_data=report_data)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
# redis-server