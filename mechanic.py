from flask import Blueprint, make_response, request
from flask_restful import Api, Resource
from models import db, Mechanic
from werkzeug.security import generate_password_hash

mechanic_bp = Blueprint('mechanic_bp', __name__, url_prefix='/mechanics')

mechanic_api = Api(mechanic_bp)

class Mechanics(Resource):
    def get(self):
        mechanics = [mechanic.to_dict() for mechanic in Mechanic.query.all()]
        return mechanics, 200
    
    def post(self):
        data = request.get_json()

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username= data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        location = data.get('location')
        profile_picture = data.get('profile_picture')
        expertise = data.get('expertise')
        experience_years = data.get('experience_years')
        bio = data.get('bio')
        password = data.get('password')

        if not all([first_name, last_name, email, username, phone_number, location, profile_picture, expertise, experience_years, password]):
            return {"message": "Missing required fields"}, 400
        
        if Mechanic.query.filter_by(username=username).first():
            return {"message": "username already exists"}, 400
        
        if Mechanic.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400
        
        if Mechanic.query.filter_by(phone_number=phone_number).first():
            return {"message": "Phone number already exists"}, 400

        hashed_password = generate_password_hash(password)

        new_mechanic = Mechanic(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            phone_number=phone_number,
            location=location,
            profile_picture=profile_picture,
            expertise=expertise,
            experience_years=experience_years,
            bio=bio,
            password=hashed_password
        )

        try:
            db.session.add(new_mechanic)
            db.session.commit()
            mechanic_dict = new_mechanic.to_dict()
            response = make_response(mechanic_dict, 201)
            return response
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating Mechanic", "error": str(e)}, 500

mechanic_api.add_resource(Mechanics, '/', strict_slashes=False)

class MechanicById(Resource):
    def get(self, id):
        mechanic = Mechanic.query.filter(Mechanic.id == id).first()

        if not mechanic:
            return {"message": "Mechanic not found"}, 404
        return mechanic.to_dict(), 200
    
    def patch(self, id):
        mechanic = Mechanic.query.get(id)
        if not mechanic:
            return {"message": "Mechanic not found"}, 404
        
        data = request.get_json()
        
        if 'first_name' in data:
            mechanic.first_name = data['first_name']
        if 'last_name' in data:
            mechanic.last_name = data['last_name']
        if 'username' in data:
            mechanic.username = data['username']
        if 'email' in data:
            mechanic.email = data['email']
        if 'phone_number' in data:
            mechanic.phone_number = data['phone_number']
        if 'location' in data:
            mechanic.location = data['location']
        if 'profile_picture' in data:
            mechanic.profile_picture = data['profile_picture']
        if 'expertise' in data:
            mechanic.expertise = data['expertise']
        if 'experience_years' in data:
            mechanic.experience_years = data['experience_years']
        if 'bio' in data:
            mechanic.bio = data['bio']
        
        try:
            db.session.commit()
            return (mechanic.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating Mechanic", "error": str(e)}, 500

    def delete(self, id):
        mechanic = Mechanic.query.filter_by(id=id).first()

        if not mechanic:
            return {"message": "Mechanic not found"}, 404
        
        try:
            db.session.delete(mechanic)
            db.session.commit()
            return {}, 204
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting Mechanic", "error": str(e)}, 500

mechanic_api.add_resource(MechanicById, '/<int:id>')