"""
Serves notifications.

Before 1.1.0, posts handled both announcements and notifications
Since buttons now support item type, it was logical to split them
However, Sonolus only passes the type for /info requests, not /list
Considering this (and that it looks better split up), moving notifications here was probably the best decision

NOTE: /users/{user_id} is reserved for user profiles
"""

from fastapi import APIRouter, Query
from fastapi import HTTPException, status

from core import SonolusRequest
from helpers.paginate import list_to_pages
from helpers.models.sonolus.response import ServerItemList

router = APIRouter()

@router.get("/", response_model=ServerItemList)
async def main(
    request: SonolusRequest,
    page: int = Query(0, ge=0),
):
    locale = request.state.loc
    auth = request.headers.get("Sonolus-Session")

    if auth:
        response = await request.app.api.get_notifications(only_unread=False).send(auth)
        data = response.data.to_posts(request)
    if not (auth and data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=locale.notification.none_past,
        )

    pages = list_to_pages(data, request.app.get_items_per_page("posts"))
    if len(pages) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=locale.items_not_found("notifications")
        )
    
    try:
        items = pages[page]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="hi stop hitting our api thanks",
        )

    return ServerItemList(
        pageCount=len(pages),
        items=items
    )
