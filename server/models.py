from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Float)
    is_in_stock = db.Column(db.Boolean)
    serialize_rules =('-some_field_to_exclude',)  # Adjust as needed for serialization")
    def __repr__(self):
        return f'<Plant {self.name} | In Stock: {self.is_in_stock}>'
