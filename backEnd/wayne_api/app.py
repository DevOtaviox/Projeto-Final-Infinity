from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wayne_api.routers.equipment_routers import router as equipment_routers
from wayne_api.routers.equipment_safety_routers import router as equipment_safety_routers
from wayne_api.routers.vehicles_routers import router as vehicles_routers
from wayne_api.routers.auth_routers import router as auth_routers



app = FastAPI(
    tittle="Wayne API",
    description="API for Wayne Project",
)

# Habilita CORS para desenvolvimento local (ajuste origens em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(equipment_routers)
app.include_router(equipment_safety_routers)
app.include_router(vehicles_routers)
app.include_router(auth_routers)


