from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from wayne_api.database import get_session
from wayne_api.models import Equipment, User
from wayne_api.schemas import EquipmentBase, EquipmentPublic, EquipmentPartialUpdate, EquipmentList
from wayne_api.dependencies import verify_token

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"],
    dependencies=[Depends(verify_token)],
)


@router.post("/", response_model=EquipmentPublic, status_code=status.HTTP_201_CREATED)
def create_equipment(equipment: EquipmentBase, session: Session = Depends(get_session), current_user: User = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    equipment = Equipment(**equipment.model_dump())
    session.add(equipment)
    session.commit()
    session.refresh(equipment)
    return equipment


@router.get("/", response_model=EquipmentList)
def list_equipment(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    query = session.scalars(select(Equipment).offset(offset).limit(limit))
    equipments = query.all()
    return {"equipment": equipments}


@router.get("/{equipment_id}", response_model=EquipmentPublic)
def get_equipment(equipment_id: int, session: Session = Depends(get_session)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentPublic)
def update_equipment(equipment_id: int, updated_equipment: EquipmentBase, session: Session = Depends(get_session), current_user: User = Depends(verify_token)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    for key, value in updated_equipment.model_dump().items():
        setattr(equipment, key, value)
    session.commit()
    session.refresh(equipment)
    return equipment


@router.patch("/{equipment_id}", response_model=EquipmentPublic)
def partial_update_equipment(equipment_id: int, equipment_update: EquipmentPartialUpdate, session: Session = Depends(get_session), current_user: User = Depends(verify_token)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    update_data = equipment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(equipment, key, value)
    session.commit()
    session.refresh(equipment)
    return equipment


@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int, session: Session = Depends(get_session), current_user: User = Depends(verify_token)):
    equipment = session.get(Equipment, equipment_id)
    if not equipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    session.delete(equipment)
    session.commit()
