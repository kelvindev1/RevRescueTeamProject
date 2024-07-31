from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"}
)

db = SQLAlchemy(metadata=metadata)

# Admin manages users and mechanics
class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    serialize_rules = ('-users.admin', '-mechanics.admin')

    # Relationships
    users = db.relationship("User", back_populates="admin")
    mechanics = db.relationship("Mechanic", back_populates="admin")


# User interacts with mechanic through assistance requests
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    profile_picture = db.Column(db.String(255))
    car_info = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    # Relationships
    admin = db.relationship("Admin", back_populates="users")
    reviews_written = db.relationship("Review", back_populates="reviewer")
    location = db.relationship("Location", back_populates="users")
    payments = db.relationship("Payment", back_populates="user")


# Mechanic interacts with user through assistance requests
class Mechanic(db.Model, SerializerMixin):
    __tablename__ = 'mechanics'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    profile_picture = db.Column(db.String(255))
    expertise = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    # Relationships
    admin = db.relationship("Admin", back_populates="mechanics")
    reviews_received = db.relationship("Review", back_populates="mechanic")
    location = db.relationship("Location", back_populates="mechanics")
    services = db.relationship('Service', back_populates='mechanic')
    payments = db.relationship("Payment", back_populates="mechanic")


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

    serialize_rules = ('-reviewer', '-mechanic')

    # Relationships
    reviewer = db.relationship('User', foreign_keys=[user_id], back_populates='reviews_written')
    mechanic = db.relationship('Mechanic', foreign_keys=[mechanic_id], back_populates='reviews_received')


# Service offered by mechanics
class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

    serialize_rules = ('-mechanic',)

    # Relationships
    mechanic = db.relationship('Mechanic', back_populates='services')


# Location for users and mechanics
class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    
    serialize_rules = ('-users', '-mechanics')

    # Relationships
    users = db.relationship('User', back_populates='location')
    mechanics = db.relationship('Mechanic', back_populates='location')


# Payment belongs to user and mechanic
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'))

    serialize_rules = ('-user', '-mechanic', '-commissions')

    # Relationships
    user = db.relationship("User", back_populates="payments")
    mechanic = db.relationship("Mechanic", back_populates="payments")
    commissions = db.relationship("Commission", back_populates="payment", cascade="all, delete-orphan")


# Commission belongs to the payment
class Commission(db.Model, SerializerMixin):
    __tablename__ = 'commissions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))

    serialize_rules = ('-payment',)

    # Relationships
    payment = db.relationship("Payment", back_populates="commissions")
