from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import routers


app = FastAPI(
    title="CampusFlow",
    openapi_prefix="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Не рекомендуется в продакшене
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers.__all__:
    app.include_router(router)