from fastapi import APIRouter

from helpers.models.sonolus.options import ServerForm
from helpers.models.sonolus.response import ServerResultInfo

router = APIRouter()

@router.get("/")
async def main():
    return ServerResultInfo(
        submits=[
            ServerForm(
                type="replay",
                title="#REPLAY",
                requireConfirmation=False,
                options=[]
            )
        ]
    )
