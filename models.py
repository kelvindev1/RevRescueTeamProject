from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData(
    naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"}
)

db = SQLAlchemy(metadata=metadata)

# Admin manages users and mechanics
class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    serialize_rules = ('-users.admin', '-mechanics.admin')

    # Relationships
    users = db.relationship("User", back_populates="admin", cascade="all, delete-orphan")
    mechanics = db.relationship("Mechanic", back_populates="admin", cascade="all, delete-orphan")




# User interacts with mechanic through assistance requests
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    profile_picture = db.Column(db.String(255))
    car_info = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    serialize_rules = ('-admin', '-reviews_written', '-location', '-payments', '-assistance_requests', '-notifications_sent', '-notifications_received')

    # Relationships
    admin = db.relationship("Admin", back_populates="users")
    reviews_written = db.relationship("Review", back_populates="reviewer", cascade="all, delete-orphan")
    location = db.relationship("Location", back_populates="users")
    payments = db.relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    assistance_requests = db.relationship("AssistanceRequest", back_populates="user", cascade="all, delete-orphan")
    notifications_sent = db.relationship('Notification', foreign_keys='Notification.sender_user_id', back_populates='sender_user', cascade="all, delete-orphan")
    notifications_received = db.relationship('Notification', foreign_keys='Notification.receiver_user_id', back_populates='receiver_user', cascade="all, delete-orphan") 





# Mechanic interacts with user through assistance requests
class Mechanic(db.Model, SerializerMixin):
    __tablename__ = 'mechanics'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    profile_picture = db.Column(db.String(255))
    expertise = db.Column(db.String(300), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    serialize_rules = ('-admin', '-reviews_received', '-location', '-services', '-payments', '-assistance_requests', '-notifications_sent', '-notifications_received')

    # Relationships
    admin = db.relationship("Admin", back_populates="mechanics")
    reviews_received = db.relationship("Review", back_populates="mechanic", cascade="all, delete-orphan")
    location = db.relationship("Location", back_populates="mechanics")
    services = db.relationship('Service', back_populates='mechanic', cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="mechanic", cascade="all, delete-orphan")
    assistance_requests = db.relationship("AssistanceRequest", back_populates="mechanic", cascade="all, delete-orphan")
    notifications_sent = db.relationship('Notification', foreign_keys='Notification.sender_mechanic_id', back_populates='sender_mechanic', cascade="all, delete-orphan")
    notifications_received = db.relationship('Notification', foreign_keys='Notification.receiver_mechanic_id', back_populates='receiver_mechanic', cascade="all, delete-orphan")




class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    assistance_request_id = db.Column(db.Integer, db.ForeignKey('assistance_requests.id'))

    serialize_rules = ('-reviewer', '-mechanic', '-assistance_request')

    # Relationships
    reviewer = db.relationship('User', foreign_keys=[user_id], back_populates='reviews_written')
    mechanic = db.relationship('Mechanic', foreign_keys=[mechanic_id], back_populates='reviews_received')
    assistance_request = db.relationship('AssistanceRequest', back_populates='reviews')





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
    users = db.relationship('User', back_populates='location', cascade="all, delete-orphan")
    mechanics = db.relationship('Mechanic', back_populates='location', cascade="all, delete-orphan")





# Payment belongs to user and mechanic
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'))
    assistance_request_id = db.Column(db.Integer, db.ForeignKey('assistance_requests.id'))

    serialize_rules = ('-user', '-mechanic', '-assistance_request', '-commissions')

    # Relationships
    user = db.relationship("User", back_populates="payments")
    mechanic = db.relationship("Mechanic", back_populates="payments")
    assistance_request = db.relationship("AssistanceRequest", back_populates="payments")
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




# Assistance Request table for user-mechanic interaction
class AssistanceRequest(db.Model, SerializerMixin):
    __tablename__ = 'assistance_requests'

    id = db.Column(db.Integer, primary_key=True)
    request_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    resolved = db.Column(db.Boolean, default=False)

    serialize_rules = ('-user', '-mechanic', '-payments', '-reviews', '-messages')

    # Relationships
    user = db.relationship('User', back_populates='assistance_requests')
    mechanic = db.relationship('Mechanic', back_populates='assistance_requests')
    payments = db.relationship('Payment', back_populates='assistance_request', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='assistance_request', cascade="all, delete-orphan")
    messages = db.relationship('Notification', back_populates='assistance_request', cascade="all, delete-orphan")



class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    sender_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    receiver_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    sender_mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=True)
    receiver_mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=True)
    assistance_request_id = db.Column(db.Integer, db.ForeignKey('assistance_requests.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_rules = ('-assistance_request', '-sender_user', '-receiver_user', '-sender_mechanic', '-receiver_mechanic')


    #Relationships
    assistance_request = db.relationship('AssistanceRequest', back_populates='messages')
    sender_user = db.relationship('User', foreign_keys=[sender_user_id], back_populates='notifications_sent')
    receiver_user = db.relationship('User', foreign_keys=[receiver_user_id], back_populates='notifications_received')
    sender_mechanic = db.relationship('Mechanic', foreign_keys=[sender_mechanic_id], back_populates='notifications_sent')
    receiver_mechanic = db.relationship('Mechanic', foreign_keys=[receiver_mechanic_id], back_populates='notifications_received')



class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)