from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

metadata = MetaData(
    naming_convention={
       "fk":"fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s" 
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin, UserMixin):
    id = db.Column(db.String, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_pic = db.Column(db.String, nullable=False)