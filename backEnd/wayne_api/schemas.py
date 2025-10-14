from typing import Optional
from pydantic import BaseModel




# Vehicle Schemas
class VehicleBase(BaseModel):
    type: str
    model: str
    year: int
    class Config:
        from_attributes = True

class VehiclePublic(BaseModel):
    id: int
    type: str
    model: str
    year: int

    class Config:
        from_attributes = True

class VehiclePartialUpdate(BaseModel):
    type: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

    class Config:
        from_attributes = True

class VehicleList(BaseModel):
    vehicle: list[VehiclePublic]

# Equipment Schemas
class EquipmentBase(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True

class EquipmentPublic(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class EquipmentPartialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class EquipmentList(BaseModel):
    equipment: list[EquipmentPublic]

# Equipment Safety Schemas
class EquipmentSafetyBase(BaseModel):
    name: str
    status: str
    description: str

    class Config:
        from_attributes = True

class EquipmentSafetyPublic(BaseModel):
    id: int
    name: str
    status: str
    description: str

    class Config:
        from_attributes = True

class EquipmentSafetyPartialUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class EquipmentSafetyList(BaseModel):
    equipmentSafety: list[EquipmentSafetyPublic]


# User Schemas
class UserBase(BaseModel):
    name: str
    email: str
    password: str
    admin: bool = False

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    name: str
    email: str
    admin: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

class Message(BaseModel):
    mensagem: str