from random import randint, choice as rc
from faker import Faker
from app import app, db
from models import User, Mechanic, Message  # Adjusted import according to your models
from werkzeug.security import generate_password_hash
import random

fake = Faker()
image_urls = [
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/200",
    "https://via.placeholder.com/250",
]

# Sample vehicle makes and models
vehicle_makes = ["Toyota", "Ford", "Chevrolet", "Honda", "BMW"]
vehicle_models = ["Camry", "F-150", "Malibu", "Civic", "X5"]

with app.app_context():
    print("Deleting all records...")
    db.session.query(User).delete()
    db.session.query(Mechanic).delete()
    db.session.query(Message).delete()
    db.session.commit()

    print("Creating Users...")
    users = []
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        phone_number = fake.unique.phone_number()
        
        # Select a random image URL for the profile picture
        profilepicture = rc(image_urls)

        # Generate car info using random choices
        car_info = f"{rc(vehicle_makes)} {rc(vehicle_models)}"
        
        password = generate_password_hash("password123")  # Generate a password hash
        user = User(
            first_name=first_name, 
            last_name=last_name,
            email=email, 
            phone_number=phone_number,
            profilepicture=profilepicture, 
            car_info=car_info,
            password=password
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    print("Creating Mechanics...")
    mechanics = []
    for _ in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()  # Ensure unique email
        phone_number = fake.unique.phone_number()
        location = fake.city()
        expertise = fake.job()
        rating = randint(1, 5)  # Rating as an integer between 1 and 5
        bio = fake.sentence()
        password = generate_password_hash("password123")  # Generate a password hash
        mechanic = Mechanic(
            first_name=first_name, 
            last_name=last_name,
            email=email, 
            phone_number=phone_number,
            location=location, 
            expertise=expertise,
            rating=rating, 
            bio=bio,
            password=password
        )
        mechanics.append(mechanic)

    db.session.add_all(mechanics)
    db.session.commit()

    print("Creating Messages...")
    messages = []
    for _ in range(15):
        content = fake.sentence()
        sender_id = rc(users).id  # Random user sender
        receiver_id = rc(mechanics).id  # Random mechanic receiver
        message = Message(content=content, sender_id=sender_id, receiver_id=receiver_id)
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()

    print("Database seeding completed successfully.")
