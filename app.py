from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
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
from user_auth import user_auth_bp, jwt, bcrypt
from admin_auth import admin_auth_bp, jwt, bcrypt
from mechanic_auth import mechanic_auth_bp, jwt, bcrypt
from datetime import timedelta


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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


migrate = Migrate(app, db)
db.init_app(app)

jwt.init_app(app)
bcrypt.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")

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




@app.route('/')
def index():
    return f'Welcome to phase 5 Project'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@socketio.on('join')  
def on_join(data):  
    room = data['assistanceRequestId']  
    join_room(room)  
    emit('status', {'msg': f'User has entered the room: {room}'}, room=room)  

@socketio.on('leave')  
def on_leave(data):  
    room = data['assistanceRequestId']  
    leave_room(room)  
    emit('status', {'msg': f'User has left the room: {room}'}, room=room)  

@socketio.on('message')  
def handle_message(data):  
    emit('message_response', {'msg': data['msg']}, room=data['assistanceRequestId'])




if __name__ == '__main__':
    socketio.run(app, port=5555, debug=True)