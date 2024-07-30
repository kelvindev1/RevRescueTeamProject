from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db
from user import user_bp

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)


app.register_blueprint(user_bp)

db.init_app(app)
api=Api(app)


@app.route('/')
def index():
    return f'Welcome to phase 5 Project'

if __name__ == '__main__':
    app.run(port='5555', debug=True)