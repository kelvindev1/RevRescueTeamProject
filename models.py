from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",})

db = SQLAlchemy(metadata=metadata)



class User(db.Model):
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



    #Relationships
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    assistance_requests = db.relationship('AssistanceRequest', back_populates='user')



class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    profilepicture = db.Column(db.String(255))
    location = db.Column(db.String(255))
    specialty = db.Column(db.String(100))
    rating = db.Column(db.Numeric(3, 2), default=0.00)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    #Relationships
    messages_received = db.relationship('Message', back_populates='receiver', lazy=True, cascade='all, delete-orphan')
    assistance_requests = db.relationship('AssistanceRequest', back_populates='mechanic', cascade='all, delete-orphan')




class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)



    #Relationships
    sender = db.relationship('User', back_populates='messages_sent')  
    receiver = db.relationship('Mechanic', back_populates='messages_received')




class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('credit_card', 'paypal', 'bank_transfer'), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed'), default='pending')
    transaction_id = db.Column(db.String(255), nullable = False, unique=True)
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    request_id = db.Column(db.Integer, db.ForeignKey('assistance_requests.id'), nullable=False)


    # Relationships
    assistance_request = db.relationship('AssistanceRequest', back_populates='payment', uselist=False)




class AssistanceRequest(db.Model):
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


    #Relationships
    user = db.relationship('User', back_populates='assistance_requests')
    mechanic = db.relationship('Mechanic', back_populates='assistance_requests')
    payment = db.relationship('Payment', back_populates='assistance_requests', uselist=False)



class Review(db.Model):
    __table__name = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)


    #Relationships
    reviewer = db.relationship('User', foreign_keys=[user_id], back_populates='reviews_written')
    mechanic = db.relationship('Mechanic', foreign_keys=[mechanic_id], back_populates='reviews_received')