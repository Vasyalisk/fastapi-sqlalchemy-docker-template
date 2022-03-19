from pydantic import BaseModel


class SendTestEmailRequest(BaseModel):
    to_emails: list[str]


class SendTestEmailResponse(BaseModel):
    is_sent: bool
