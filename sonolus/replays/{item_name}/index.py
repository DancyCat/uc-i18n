from fastapi import APIRouter, HTTPException

from core import SonolusRequest
from helpers.models.sonolus.item import ReplayItem
from helpers.models.sonolus.options import ServerForm
from helpers.models.sonolus.response import ServerItemDetails

router = APIRouter()

@router.get("/")
async def get(request: SonolusRequest, item_name: str):
    level_name, replay_id = item_name.removesuffix("UnCh-").split("-")
    auth = request.headers.get("Sonolus-Session")

    replay_response = await request.app.api.get_record(level_name, int(replay_id)).send(auth)

    if replay_response.status != 200:
        raise HTTPException(status_code=replay_response.status)
    
    level_response = await request.app.api.get_chart(item_name).send(auth)

    if replay_response.status != 200:
        raise HTTPException(status_code=level_response.status)
    
    asset_base_url = level_response.data.asset_base_url.removesuffix("/")

    replay_item = replay_response.data.to_replay_item(
        await request.app.run_blocking(
            level_response.data.data.to_level_item,
            request,
            asset_base_url,
            request.state.levelbg,
        ),
        request
    )

    actions = [
        ServerForm(
            type="delete",
            title="#DELETE",
            icon="delete",
            requireConfirmation=True
        )
    ] if replay_response.data.data.owner or replay_response.data.data.mod else []

    return ServerItemDetails(
        item=replay_item,
        actions=actions,
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )