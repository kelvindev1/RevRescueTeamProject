from random import randint, choice
from faker import Faker
from app import app, db
from models import Admin, User, Mechanic, Review, Service, Location, Payment, Commission, AssistanceRequest

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

# Sample service names and descriptions
service_names = ["Oil Change", "Brake Inspection", "Engine Repair", "Tire Rotation", "Battery Replacement"]
service_descriptions = ["Complete oil change service", "Brake inspection and maintenance", "Engine repair and diagnostics", "Tire rotation and alignment", "Battery testing and replacement"]

with app.app_context():
    print("Deleting all records...")
    db.session.query(User).delete()
    db.session.query(Mechanic).delete()
    db.session.query(Admin).delete()
    db.session.query(Review).delete()
    db.session.query(Service).delete()
    db.session.query(Location).delete()
    db.session.query(Payment).delete()
    db.session.query(Commission).delete()
    db.session.query(AssistanceRequest).delete()
    db.session.commit()

    print("Creating Locations...")
    locations = []
    for _ in range(5):  # Create 5 locations
        address = fake.address()
        location = Location(address=address)
        locations.append(location)
    db.session.add_all(locations)
    db.session.commit()

    print("Creating Admins...")
    admins = []
    for _ in range(2):  # Create 2 admins
        username = fake.user_name()
        email = fake.unique.email()
        password = fake.password()
        admin = Admin(username=username, email=email, password=password)
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
        location_id = choice([location.id for location in locations])
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
            location_id=location_id,
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
        location_id = choice([location.id for location in locations])
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
            location_id=location_id,
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

    print("Creating Services...")
    services = []
    for _ in range(20):  # Create 20 services
        name = choice(service_names)
        description = choice(service_descriptions)
        image_url = choice(image_urls)
        mechanic_id = choice([mechanic.id for mechanic in mechanics])
        service = Service(
            name=name,
            description=description,
            image_url=image_url,
            mechanic_id=mechanic_id
        )
        services.append(service)
    db.session.add_all(services)
    db.session.commit()

    print("Creating Assistance Requests...")
    assistance_requests = []
    for _ in range(10):  # Create 10 assistance requests
        user_id = choice([user.id for user in users])
        mechanic_id = choice([mechanic.id for mechanic in mechanics])
        message = fake.text()
        assistance_request = AssistanceRequest(
            user_id=user_id,
            mechanic_id=mechanic_id,
            message=message
        )
        assistance_requests.append(assistance_request)
    db.session.add_all(assistance_requests)
    db.session.commit()

    print("Creating Reviews...")
    reviews = []
    for _ in range(20):  # Create 20 reviews
        rating = choice(ratings)
        feedback = fake.text()
        user_id = choice([user.id for user in users])
        mechanic_id = choice([mechanic.id for mechanic in mechanics])
        assistance_request_id = choice([request.id for request in assistance_requests])
        review = Review(
            rating=rating,
            feedback=feedback,
            user_id=user_id,
            mechanic_id=mechanic_id,
            assistance_request_id=assistance_request_id
        )
        reviews.append(review)
    db.session.add_all(reviews)
    db.session.commit()

    # Refresh users, mechanics, and assistance requests to avoid DetachedInstanceError
    users = User.query.all()
    mechanics = Mechanic.query.all()
    assistance_requests = AssistanceRequest.query.all()

    print("Creating Payments...")
    payments = []
    for _ in range(20):  # Create 20 payments
        amount = round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=20, max_value=200), 2)
        status = fake.random_element(elements=("Completed", "Pending", "Failed"))
        user_id = choice([user.id for user in users])
        mechanic_id = choice([mechanic.id for mechanic in mechanics])
        assistance_request_id = choice([request.id for request in assistance_requests])
        payment = Payment(
            amount=amount,
            status=status,
            user_id=user_id,
            mechanic_id=mechanic_id,
            assistance_request_id=assistance_request_id
        )
        payments.append(payment)
    db.session.add_all(payments)
    db.session.commit()

    print("Creating Commissions...")
    commissions = []
    for _ in range(20):  # Create 20 commissions
        amount = round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=5, max_value=50), 2)
        payment_id = choice([payment.id for payment in payments])
        commission = Commission(
            amount=amount,
            payment_id=payment_id
        )
        commissions.append(commission)
    db.session.add_all(commissions)
    db.session.commit()

    print("Database populated successfully!")
