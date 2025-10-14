from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from wayne_api.database import get_session
from wayne_api.models import Vehicle
from wayne_api.schemas import VehicleBase, VehiclePublic, VehiclePartialUpdate, VehicleList
from wayne_api.dependencies import verify_token


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
    dependencies=[Depends(verify_token)],
)


@router.post("/", response_model=VehiclePublic, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleBase, session: Session = Depends(get_session), current_user=Depends(verify_token)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    vehicle = Vehicle(**vehicle.model_dump())
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.get("/", response_model=VehicleList, status_code=status.HTTP_200_OK)
def list_vehicles(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    query = session.scalars(select(Vehicle).offset(offset).limit(limit))
    vehicles = query.all()
    return {"vehicle": vehicles}


@router.get("/{vehicle_id}", response_model=VehiclePublic, status_code=status.HTTP_200_OK)
def get_vehicle(vehicle_id: int, session: Session = Depends(get_session)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return vehicle


@router.put("/{vehicle_id}", response_model=VehiclePublic, status_code=status.HTTP_201_CREATED)
def update_vehicle(vehicle_id: int, updated_vehicle: VehicleBase, session: Session = Depends(get_session), current_user=Depends(verify_token)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    for key, value in updated_vehicle.model_dump().items():
        setattr(vehicle, key, value)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.patch("/{vehicle_id}", response_model=VehiclePublic, status_code=status.HTTP_201_CREATED)
def partial_update_vehicle(vehicle_id: int, vehicle_update: VehiclePartialUpdate, session: Session = Depends(get_session), current_user=Depends(verify_token)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    update_data = vehicle_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vehicle, key, value)
    session.commit()
    session.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, session: Session = Depends(get_session), current_user=Depends(verify_token)):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    session.delete(vehicle)
    session.commit()