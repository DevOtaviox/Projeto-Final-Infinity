from fastapi import FastAPI
from wayne_api.routers.equipment_routers import router as equipment_routers
from wayne_api.routers.equipment_safety_routers import router as equipment_safety_routers
from wayne_api.routers.vehicles_routers import router as vehicles_routers

app = FastAPI(
    tiltle="Wayne API",
    description="API for Wayne Project",
)


app.include_router(equipment_routers, prefix="/equipment")
app.include_router(equipment_safety_routers, prefix="/equipment-safety")
app.include_router(vehicles_routers, prefix="/vehicles")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

