from database.utils import with_session, AsyncSession
from mail import models as mail_models


@with_session
async def create(session: AsyncSession = None, **kwargs) -> mail_models.Mail:
    model = mail_models.Mail(**kwargs)
    session.add(model)
    await session.commit()
    await session.refresh(model, attribute_names=["updated_at", "created_at"])
    return model
