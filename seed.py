from random import randint, choice
from faker import Faker
from app import app, db
from models import Admin, User, Mechanic, Review, Service, Location, Payment, Commission, AssistanceRequest, Notification, ReportData, Visit

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
    db.session.query(Notification).delete()
    db.session.query(ReportData).delete()
    db.session.query(Visit).delete()
    db.session.commit()

    print("Creating Locations...")
    locations = [Location(address=fake.address()) for _ in range(5)]
    db.session.add_all(locations)
    db.session.commit()

    print("Creating Admins...")
    admins = [Admin(username=fake.user_name(), email=fake.unique.email(), password=fake.password()) for _ in range(2)]
    db.session.add_all(admins)
    db.session.commit()

    print("Creating Users...")
    users = []
    for _ in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.user_name(),
            email=fake.unique.email(),
            phone_number=fake.unique.phone_number(),
            location_id=choice([location.id for location in locations]),
            profile_picture=choice(image_urls),
            car_info=f"{choice(vehicle_makes)} {choice(vehicle_models)}",
            password=fake.password(),
            admin_id=choice([admin.id for admin in admins])
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    print("Creating Mechanics...")
    mechanics = []
    for _ in range(5):
        mechanic = Mechanic(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.user_name(),
            email=fake.unique.email(),
            phone_number=fake.unique.phone_number(),
            location_id=choice([location.id for location in locations]),
            profile_picture=choice(image_urls),
            expertise=fake.job(),
            experience_years=randint(1, 10),
            bio=fake.text(),
            password=fake.password(),
            admin_id=choice([admin.id for admin in admins])
        )
        mechanics.append(mechanic)
    db.session.add_all(mechanics)
    db.session.commit()

    print("Creating Services...")
    services = [
        Service(
            name=choice(service_names),
            description=choice(service_descriptions),
            image_url=choice(image_urls),
            mechanic_id=choice([mechanic.id for mechanic in mechanics])
        )
        for _ in range(20)
    ]
    db.session.add_all(services)
    db.session.commit()

    print("Creating Assistance Requests...")
    assistance_requests = [
        AssistanceRequest(
            user_id=choice([user.id for user in users]),
            mechanic_id=choice([mechanic.id for mechanic in mechanics]),
            message=fake.text()
        )
        for _ in range(10)
    ]
    db.session.add_all(assistance_requests)
    db.session.commit()

    print("Creating Reviews...")
    reviews = [
        Review(
            rating=choice(ratings),
            feedback=fake.text(),
            user_id=choice([user.id for user in users]),
            mechanic_id=choice([mechanic.id for mechanic in mechanics]),
            assistance_request_id=choice([request.id for request in assistance_requests])
        )
        for _ in range(20)
    ]
    db.session.add_all(reviews)
    db.session.commit()

    # Refresh users, mechanics, and assistance requests to avoid DetachedInstanceError
    users = User.query.all()
    mechanics = Mechanic.query.all()
    assistance_requests = AssistanceRequest.query.all()

    print("Creating Payments...")
    payments = [
        Payment(
            amount=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=20, max_value=200), 2),
            status=choice(["Completed", "Pending", "Failed"]),
            user_id=choice([user.id for user in users]),
            mechanic_id=choice([mechanic.id for mechanic in mechanics]),
            assistance_request_id=choice([request.id for request in assistance_requests])
        )
        for _ in range(20)
    ]
    db.session.add_all(payments)
    db.session.commit()

    print("Creating Commissions...")
    commissions = [
        Commission(
            amount=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=5, max_value=50), 2),
            payment_id=choice([payment.id for payment in payments])
        )
        for _ in range(20)
    ]
    db.session.add_all(commissions)
    db.session.commit()

    print("Creating Notifications...")
    notifications = [
        Notification(
            sender_user_id=choice([user.id for user in users] + [None]),
            receiver_user_id=choice([user.id for user in users] + [None]),
            sender_mechanic_id=choice([mechanic.id for mechanic in mechanics] + [None]),
            receiver_mechanic_id=choice([mechanic.id for mechanic in mechanics] + [None]),
            assistance_request_id=choice([request.id for request in assistance_requests]),
            message=fake.text()
        )
        for _ in range(20)
    ]
    db.session.add_all(notifications)
    db.session.commit()

    print("Creating Report Data...")
    reportdata = [
        ReportData(
            column1=fake.name(),
            column2=fake.email(),
            date_field=fake.date_this_year()
        )
        for _ in range(50)
    ]
    db.session.add_all(reportdata)
    db.session.commit()

    print("Creating Visits...")
    user_ids = [user.id for user in users]
    visits = [
        Visit(
            date=fake.date_between(start_date='-10d', end_date='today'),
            count=fake.random_int(min=0, max=20),
            user_id=choice(user_ids)  # Choose a random user ID from the list
        )
        for _ in range(50)
    ]
    db.session.add_all(visits)
    db.session.commit()

    print("Database populated successfully!")
