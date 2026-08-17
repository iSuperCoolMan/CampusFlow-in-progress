from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.base import router as base_router
from .routers.sso import router as sso_router

app = FastAPI(
    title="Auth",
    openapi_prefix="/auth/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Не рекомендуется в продакшене
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
app.include_router(sso_router, prefix="/sso")