from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig

from .settings import uris, email, email_token
from ..api.schemas.user import Token

mail_config = ConnectionConfig(
    MAIL_USERNAME=email.USERNAME,
    MAIL_PASSWORD=email.PASSWORD,
    MAIL_FROM=email.USERNAME,
    MAIL_PORT=email.PORT,
    MAIL_SERVER=email.HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

def send_verification_email(email_to_recieve: str, token: Token):
    verification_url = f"{uris.BASE_URI}/verify-email?token={token}"

    html = f"""
    <p>Thanks for signing up! Please click the link below to verify your email:</p>
    <a href="{verification_url}">Verify Email</a>
    <p>This link expires in {email_token.EXPIRE_MINUTES} minutes.</p>
    """

    message = MessageSchema(
        subject="FastAPI Email Verification",
        recipients=[email_to_recieve],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(mail_config)
    fm.send_message(message)