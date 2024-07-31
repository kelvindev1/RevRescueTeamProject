from random import randint, choice
from faker import Faker
from app import app, db
from models import Admin, User, Mechanic

# Initialize Faker and other data
fake = Faker()
image_urls = [
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/200",
    "https://via.placeholder.com/250",
]

# Sample vehicle makes and models
vehicle_makes = ["Toyota", "Ford", "Chevrolet", "Honda", "BMW"]
vehicle_models = ["Camry", "F-150", "Malibu", "Civic", "X5"]

# Sample review ratings
ratings = [1, 2, 3, 4, 5]

with app.app_context():
    print("Deleting all records...")
    db.session.query(User).delete()
    db.session.query(Mechanic).delete()
    db.session.query(Admin).delete()
    db.session.commit()

    print("Creating Admins...")
    admins = []
    for _ in range(2):  # Create 2 admins
        username = fake.user_name()
        email = fake.unique.email()
        password = fake.password()
        admin = Admin(
            username=username,
            email=email,
            password=password
        )
        admins.append(admin)
    db.session.add_all(admins)
    db.session.commit()

    print("Creating Users...")
    users = []
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        username = fake.user_name()
        phone_number = fake.unique.phone_number()
        location = fake.city()
        profile_picture = choice(image_urls)
        car_info = f"{choice(vehicle_makes)} {choice(vehicle_models)}"
        password = fake.password()
        admin_id = choice([admin.id for admin in admins])  # Assign a random admin
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            location=location,
            profile_picture=profile_picture,
            car_info=car_info,
            password=password,
            admin_id=admin_id
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    print("Creating Mechanics...")
    mechanics = []
    for _ in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        phone_number = fake.unique.phone_number()
        location = fake.city()
        profile_picture = choice(image_urls)
        expertise = fake.job()
        rating = randint(1, 5)
        bio = fake.text()
        password = fake.password()
        admin_id = choice([admin.id for admin in admins])  # Assign a random admin
        mechanic = Mechanic(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            location=location,
            profile_picture=profile_picture,
            expertise=expertise,
            rating=rating,
            bio=bio,
            password=password,
            admin_id=admin_id
        )
        mechanics.append(mechanic)
    db.session.add_all(mechanics)
    db.session.commit()

    print("Database populated successfully!")
