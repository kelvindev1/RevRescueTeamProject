from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",}
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    profilepicture = db.Column(db.String(255))
    car_info = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    serialize_rules = ('-messages_sent', '-assistance_requests', '-reviews_written', '-notifications', '-locations')

    # Relationships
    messages_sent = db.relationship('Message', back_populates='sender')
    assistance_requests = db.relationship('AssistanceRequest', back_populates='user')
    reviews_written = db.relationship('Review', back_populates='reviewer')
    notifications = db.relationship('Notification', back_populates='user')
    locations = db.relationship('Location', back_populates='user')


class Mechanic(db.Model, SerializerMixin):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    profilepicture = db.Column(db.String(255))
    expertise = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    serialize_rules = ('-messages_received', '-assistance_requests', '-reviews_received', '-services')

    # Relationships
    messages_received = db.relationship('Message', back_populates='receiver')
    assistance_requests = db.relationship('AssistanceRequest', back_populates='mechanic')
    reviews_received = db.relationship('Review', back_populates='mechanic')
    services = db.relationship('Service', back_populates='mechanic')


class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

    serialize_rules = ('-sender', '-receiver')

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = db.relationship('Mechanic', foreign_keys=[receiver_id], back_populates='messages_received')


class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('credit_card', 'paypal', 'bank_transfer'), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed'), default='pending')
    transaction_id = db.Column(db.String(255), nullable=False, unique=True)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    request_id = db.Column(db.Integer, db.ForeignKey('assistance_requests.id'), nullable=False)

    serialize_rules = ('-assistance_request',)

    # Relationships
    assistance_request = db.relationship('AssistanceRequest', foreign_keys=[request_id], back_populates='payment', uselist=False)


class AssistanceRequest(db.Model, SerializerMixin):
    __tablename__ = 'assistance_requests'

    id = db.Column(db.Integer, primary_key=True)
    issue_description = db.Column(db.Text, nullable=False)
    urgency_level = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    status = db.Column(db.Enum('pending', 'in_progress', 'completed'), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)

    serialize_rules = ('-user', '-mechanic', '-payment')

    # Relationships
    user = db.relationship('User', back_populates='assistance_requests')
    mechanic = db.relationship('Mechanic', back_populates='assistance_requests')
    payment = db.relationship('Payment', foreign_keys=[payment_id], back_populates='assistance_request', uselist=False)


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


class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-user',)

    # Relationships
    user = db.relationship('User', back_populates='notifications')


class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-user',)

    # Relationships
    user = db.relationship('User', back_populates='locations')


class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

    serialize_rules = ('-mechanic',)

    # Relationships
    mechanic = db.relationship('Mechanic', back_populates='services')