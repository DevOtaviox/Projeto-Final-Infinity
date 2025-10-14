from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from wayne_api.database import get_session
from wayne_api.models import EquipmentSafety
from wayne_api.schemas import EquipmentSafetyBase, EquipmentSafetyPublic, EquipmentSafetyPartialUpdate, EquipmentSafetyList
from wayne_api.dependencies import verify_token
router = APIRouter(
    prefix="/equipment-safety",
    tags =["Equipment Safety"],
    dependencies=[Depends(verify_token)]
)

@router.post("/", response_model=EquipmentSafetyPublic, status_code=status.HTTP_201_CREATED)
def create_equipment_safety(equipment_safety: EquipmentSafetyBase, session: Session = Depends(get_session), current_user = Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    equipment_safety = EquipmentSafety(**equipment_safety.model_dump())
    session.add(equipment_safety)
    session.commit()
    session.refresh(equipment_safety)
    return equipment_safety


@router.get("/", response_model=EquipmentSafetyList)
def list_equipment_safety(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    query = session.scalars(select(EquipmentSafety).offset(offset).limit(limit))
    all_equipment = query.all()
    return {"equipmentSafety": all_equipment}


@router.get("/{equipment_safety_id}", response_model=EquipmentSafetyPublic)
def get_equipment_safety(equipment_safety_id: int, session: Session = Depends(get_session)):
    equipment_safety = session.get(EquipmentSafety, equipment_safety_id)
    if not equipment_safety:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment Safety not found")
    return equipment_safety

@router.put("/{equipment_safety_id}", response_model=EquipmentSafetyPublic)
def update_equipment_safety(equipment_safety_id: int, updated_equipment_safety: EquipmentSafetyBase, session: Session = Depends(get_session), current_user = Depends(verify_token)):
    equipment_safety = session.get(EquipmentSafety, equipment_safety_id)
    if not equipment_safety:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment Safety not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    for key, value in updated_equipment_safety.model_dump().items():
        setattr(equipment_safety, key, value)
    session.commit()
    session.refresh(equipment_safety)
    return equipment_safety


@router.patch("/{equipment_safety_id}", response_model=EquipmentSafetyPublic)
def partial_update_equipment_safety(equipment_safety_id: int, equipment_safety_update: EquipmentSafetyPartialUpdate, session: Session = Depends(get_session), current_user = Depends(verify_token)):
    equipment_safety = session.get(EquipmentSafety, equipment_safety_id)
    if not equipment_safety:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment Safety not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    update_data = equipment_safety_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(equipment_safety, key, value)
    session.commit()
    session.refresh(equipment_safety)
    return equipment_safety

@router.delete("/{equipment_safety_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment_safety(equipment_safety_id: int, session: Session = Depends(get_session), current_user = Depends(verify_token)):
    equipment_safety = session.get(EquipmentSafety, equipment_safety_id)
    if not equipment_safety:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment Safety not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    session.delete(equipment_safety)
    session.commit()