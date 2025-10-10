from sqlalchemy import Column, Integer, String, Text, Boolean
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, unique=True, index=True, nullable=False)
    password = Column("password", String, nullable=False)
    admin = Column("admin", Boolean, default=False) # True for admin users, False for regular users

    def __init__(self, name: str, email: str, password: str, admin: bool = False):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin


class Vehicle(Base):
    __tablename__ = "vehicles"



    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    type = Column("type" , String) # terrestrial, aquatic, aerial
    model = Column("model" ,String, nullable=False)
    year = Column("year", Integer, nullable=True)

    def __init__(self, type: str, model: str, year: int):
        self.type = type
        self.model = model
        self.year = year
   

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=True)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
   

class EquipmentSafety(Base):
    __tablename__ = "equipment_safety"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    status = Column("status", Boolean) # True for operational, False for non-operational
    description = Column("description", Text, nullable=True)

    def __init__(self, name: str, status: Boolean, description: str):
        self.name = name
        self.status = status
        self.description = description
