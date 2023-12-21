import uuid

from sqlalchemy.orm import Session

from fides.api.api.v1.endpoints.health import is_email_messaging_enabled
from fides.api.models.fides_user import FidesUser
from fides.api.models.fides_user_invite import FidesUserInvite
from fides.api.schemas.messaging.messaging import (
    MessagingActionType,
    UserInviteBodyParams,
)
from fides.api.schemas.redis_cache import Identity
from fides.api.service.messaging.message_dispatch_service import dispatch_message
from fides.config import FidesConfig


def invite_user(db: Session, config: FidesConfig, user: FidesUser):
    """Generates a user invite and sends the invite code to the user via email."""

    if is_email_messaging_enabled(db):
        invite_code = str(uuid.uuid4())
        FidesUserInvite.create(
            db=db, data={"username": user.username, "invite_code": invite_code}
        )
        dispatch_message(
            db,
            action_type=MessagingActionType.USER_INVITE,
            to_identity=Identity(email=user.email_address),
            service_type=config.notifications.notification_service_type,
            message_body_params=UserInviteBodyParams(
                username=user.username, invite_code=invite_code
            ),
        )