from fastapi import APIRouter, File, HTTPException, Header, UploadFile

from core import SonolusRequest
import helpers.replay as replay

router = APIRouter()

@router.post("/")
async def upload(
    request: SonolusRequest,
    upload_key: str = Header(alias='Sonolus-Upload-Key'),
    files: list[UploadFile] = File(...)
):
    files_map = {file.filename: file for file in files}
    data = replay.verify_upload_key(upload_key, request)

    replay_data = await files_map[data.data_hash].read()
    replay_configuration = await files_map[data.configuration_hash].read()

    info = replay.validate_replay_config(replay_configuration, data.engine_name)

    response = await request.app.api.upload_replay(
        replay_data,
        replay_configuration,
        data.level_name,
        data.user_id,
        data.engine_name,
        info.speed
    ).send()

    if response.status != 200:
        raise HTTPException(status_code=response.status, detail=request.state.loc.unknown_error)
    
    return {}