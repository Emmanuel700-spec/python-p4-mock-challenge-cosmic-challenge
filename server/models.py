from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Scientist(db.Model):
    __tablename__ = 'scientists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    field_of_study = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'field_of_study': self.field_of_study
            # Missions omitted
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    distance_from_earth = Column(Integer, nullable=True)
    nearest_star = Column(String, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance_from_earth': self.distance_from_earth,
            'nearest_star': self.nearest_star
        }

class Mission(db.Model):
    __tablename__ = 'missions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    scientist_id = Column(Integer, ForeignKey('scientists.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planets.id'), nullable=False)

    scientist = relationship('Scientist', backref='missions')
    planet = relationship('Planet', backref='missions')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientist_id': self.scientist_id,
            'planet_id': self.planet_id
        }
