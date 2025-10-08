from typing import Optional
from pydantic import BaseModel




# Vehicle Schemas
class VehicleBase(BaseModel):
    type: str
    model: str
    year: int

class VehiclePublic(BaseModel):
    id: int
    type: str
    model: str
    year: int

    class Config:
        orm_mode = True

class VehiclePartialUpdate(BaseModel):
    type: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

class VehicleList(BaseModel):
    vehicle: list[VehiclePublic]

# Equipment Schemas
class EquipmentBase(BaseModel):
    name: str
    description: str

class EquipmentPublic(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class EquipmentPartialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class EquipmentList(BaseModel):
    equipment: list[EquipmentPublic]

# Equipment Safety Schemas
class EquipmentSafetyBase(BaseModel):
    name: str
    status: str
    description: str

class EquipmentSafetyPublic(BaseModel):
    id: int
    name: str
    status: str
    description: str

    class Config:
        orm_mode = True

class EquipmentSafetyPartialUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class EquipmentSafetyList(BaseModel):
    equipmentSafety: list[EquipmentSafetyPublic]



