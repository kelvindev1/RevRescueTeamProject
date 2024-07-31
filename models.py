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

    serialize_rules = ('-messages_sent',)

    # Relationships
    messages_sent = db.relationship('Message', back_populates='sender', cascade='all, delete-orphan')


class Mechanic(db.Model, SerializerMixin):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    location = db.Column(db.String, nullable=False)
    profilepicture = db.Column(db.String(255))
    expertise = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    serialize_rules = ('-messages_received',)

    # Relationships
    messages_received = db.relationship('Message', back_populates='receiver', cascade='all, delete-orphan')


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
# Payment belongs to user and mechanic
class Payment(db.Model, SerializerMixin):
    _tablename_ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'))

    user = db.relationship("User", back_populates="payments")
    mechanic = db.relationship("Mechanic", back_populates="payments")
    commissions = db.relationship("Commission", back_populates="payment", cascade="all, delete-orphan")

    serialize_rules = ('-user.payments', '-mechanic.payments', '-commissions.payment')
