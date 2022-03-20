from pydantic import BaseSettings
from jinja2 import Environment, PackageLoader, select_autoescape


class MailSettings(BaseSettings):
    FROM_EMAIL: str
    EMAIL_TEMPLATES_PATH: str = "/backend/mail/templates/"
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 465
    EMAIL_USE_TLS: bool = True
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str

    @property
    def registered_templates(self):
        return [
            "reset_password",
            "verify_email",
        ]

    class Config:
        case_sensitive = True


settings = MailSettings()

email_environment = Environment(
    loader=PackageLoader("mail"),
    autoescape=select_autoescape()
)
