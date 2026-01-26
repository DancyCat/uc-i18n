from datetime import datetime
from pydantic import BaseModel

from core import SonolusRequest
from helpers.models.api.misc import PublicAccount
from helpers.models.sonolus.item import ServerItemCommunityComment
from helpers.models.sonolus.options import ServerForm
from helpers.owoify import handle_uwu

class Comment(BaseModel):
    id: int
    commenter: str
    username: str | None = None
    content: str
    created_at: int
    deleted_at: int | None = None
    account: PublicAccount
    chart_id: str
    owner: bool | None = None

    def to_server_item_community_comment(self, request: SonolusRequest, is_mod: bool | None = None) -> ServerItemCommunityComment:
        return ServerItemCommunityComment(
            name=str(self.id),
            author=handle_uwu(
                self.username,
                request.state.localization,
                request.state.uwu,
                symbols=False
            ),
            time=self.created_at,
            content=handle_uwu(
                self.content, request.state.localization, request.state.uwu
            ),
            actions=(
                [
                    ServerForm(
                        type="delete",
                        title="#DELETE",
                        icon="delete",
                        requireConfirmation=True,
                        options=[]
                    )
                ]
                if (self.owner or is_mod)
                and not self.deleted_at
                else []
            ),
            authorUser=self.account.to_user_item()
        )

class DeleteCommentResponse(BaseModel):
    id: int
    commenter: str
    username: str | None = None
    content: str
    created_at: datetime # XXX (backend): can't inherit from Comment because of this datetime
    deleted_at: datetime | None = None
    chart_id: str
    owner: bool | None = None
    mod: bool | None = None

class CommentList(BaseModel):
    data: list[Comment]
    pageCount: int
    mod: bool | None = None
    admin: bool | None = None

    def to_server_item_community_comments(self, request: SonolusRequest) -> list[ServerItemCommunityComment]:
        return [comment.to_server_item_community_comment(request, self.mod) for comment in self.data]