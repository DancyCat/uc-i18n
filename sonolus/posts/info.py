from fastapi import APIRouter
from core import SonolusRequest
from helpers.models.sonolus.item_section import PostItemSection
from helpers.models.sonolus.response import ServerItemInfo
from helpers.data_compilers import (
    compile_banner,
    compile_static_posts_list,
    sort_posts_by_newest
)

router = APIRouter()

from helpers.owoify import handle_item_uwu


@router.get("/", response_model=ServerItemInfo)
async def main(request: SonolusRequest):
    uwu_level = request.state.uwu
    banner_srl = await request.app.run_blocking(compile_banner)

    data = await request.app.run_blocking(
        compile_static_posts_list, request.app.base_url
    )

    data = sort_posts_by_newest(data)
    sections = [
        PostItemSection(
            title="#NEWEST",
            icon="post",
            items=[
                post.to_post_item()
                for post in
                handle_item_uwu(data[:5], request.state.localization, uwu_level)
            ]
        ),
    ]
    
    return ServerItemInfo(
        sections=sections,
        banner=banner_srl if banner_srl else None
    )
