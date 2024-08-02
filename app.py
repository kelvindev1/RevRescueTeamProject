from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from models import db
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
from user_auth import user_auth_bp
from admin_auth import admin_auth_bp
from mechanic_auth import mechanic_auth_bp



app = Flask(__name__)
CORS(app, supports_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# run python then run import uuid then run uuid.uuid4().hex
app.config['SECRET_KEY'] = '18895d3dd34344728f4365a92988db5a'


migrate = Migrate(app, db)
jwt = JWTManager(app)



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




db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)



@app.route('/')
def index():
    return f'Welcome to phase 5 Project'



if __name__ == '__main__':
    app.run(port='5555', debug=True)