"""
Serves notifications.

Before 1.1.0, posts handled both announcements and notifications
Since buttons now support item type, it was logical to split them
However, Sonolus only passes the type for /info requests, not /list
Considering this (and that it looks better split up), moving notifications here was probably the best decision

NOTE: /users/{user_id} is reserved for user profiles
"""

from fastapi import APIRouter
from core import SonolusRequest
from helpers.models.sonolus.item_section import PostItemSection
from helpers.models.sonolus.response import ServerItemInfo
from helpers.data_compilers import compile_banner

router = APIRouter()

@router.get("/", response_model=ServerItemInfo)
async def main(request: SonolusRequest):
    locale = request.state.loc
    banner_srl = await request.app.run_blocking(compile_banner)
    auth = request.headers.get("Sonolus-Session")

    response = await request.app.api.get_notifications(only_unread=True).send(auth)

    notifs = response.data.to_posts(request)
    if notifs:
        sections = [
            PostItemSection(
                title=locale.notification.UNREAD,
                icon="bell",
                description=locale.notification.NOTIFICATION_DESC_UNREAD,
                items=notifs
            )
        ]
    else:
        sections = [
            PostItemSection(
                title=locale.notification.NOTIFICATION,
                icon="bell",
                description=locale.notification.NOTIFICATION_DESC,
                items=[]
            )
        ]
    
    return ServerItemInfo(
        sections=sections,
        banner=banner_srl if banner_srl else None
    )
