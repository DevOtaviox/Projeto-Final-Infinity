from sqlalchemy import Column, Integer, String, Text
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
   
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
   
class EquipmentSafety(Base):
    __tablename__ = "equipment_safety"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(Text, nullable=True)