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
    location = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255))
    car_info = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))


    # Relationships
    admin = db.relationship("Admin", back_populates="users")



# Mechanic interacts with user through assistance requests
class Mechanic(db.Model, SerializerMixin):
    __tablename__ = 'mechanics'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=False)
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
