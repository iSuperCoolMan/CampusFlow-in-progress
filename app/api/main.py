from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.routers.base import router as base_router
from .auth.routers.sso import router as sso_router


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

app.include_router(base_router, prefix="/auth")
app.include_router(sso_router, prefix="/auth/sso")