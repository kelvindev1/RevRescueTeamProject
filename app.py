from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db
from user import user_bp
from mechanic import mechanic_bp
from admin import admin_bp
from review import review_bp
from service import service_bp
from location import location_bp


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# run python then run import uuid then run uuid.uuid4().hex
app.config['SECRET_KEY'] = '18895d3dd34344728f4365a92988db5a'


migrate = Migrate(app, db)


app.register_blueprint(user_bp)
app.register_blueprint(mechanic_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(review_bp)
app.register_blueprint(service_bp)
app.register_blueprint(location_bp)

db.init_app(app)
api=Api(app)


@app.route('/')
def index():
    return f'Welcome to phase 5 Project'

if __name__ == '__main__':
    app.run(port='5555', debug=True)