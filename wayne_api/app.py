from fastapi import FastAPI

from wayne_api.routers.equipment_routers import router as equipment_routers
from wayne_api.routers.equipment_safety_routers import router as equipment_safety_routers
from wayne_api.routers.vehicles_routers import router as vehicles_routers
from wayne_api.routers.auth_routers import router as auth_routers



app = FastAPI(
    tiltle="Wayne API",
    description="API for Wayne Project",
)



app.include_router(equipment_routers)
app.include_router(equipment_safety_routers)
app.include_router(vehicles_routers)
app.include_router(auth_routers)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

