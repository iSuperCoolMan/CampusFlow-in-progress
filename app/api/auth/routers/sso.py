from fastapi import APIRouter, Request

from ..core.settings import sso


router = APIRouter(
    tags=["sso"],
    prefix="/auth/sso"
)


@router.get("/login/{sso_name}")
async def login(sso_name: str):
    sso_data = sso.get_sso_data_by_name(sso_name)

    async with sso_data.method:
        return await sso_data.method.get_login_redirect(params=sso_data.params)


@router.api_route("/callback/{sso_name}", methods=["GET", "POST"])
async def callback(request: Request, sso_name: str):
    sso_data = sso.get_sso_data_by_name(sso_name)

    async with sso_data.method:
        user = await sso_data.method.verify_and_process(request)

    return user