from typing import Literal
from pydantic import BaseModel

class ServerFileOptionValidationFile(BaseModel):
    type: Literal["file", "engineRom"]
    minSize: int | float | None
    maxSize: int | float | None

class ServerFileOptionValidationImage(BaseModel):
    type: Literal["image", "serverBanner", "postThumbnail", 
                  "playlistThumbnail", "levelCover", "skinThumbnail", 
                  "skinTexture", "backgroundThumbnail", "backgroundImage", 
                  "effectThumbnail", "particleThumbnail", "particleTexture",
                  "engineThumbnail", "roomCover"]
    minSize: int | float | None
    maxSize: int | float | None
    minWidth: int | float | None
    maxWidth: int | float | None
    minHeight: int | float | None
    maxHeight: int | float | None

class ServerFileOptionValidationAudio(BaseModel):
    type: Literal["audio", "levelBgm", "levelPreview", "roomBgm", "roomPreview"]
    minSize: int | float | None
    maxSize: int | float | None
    minLength: int | float | None
    maxLength: int | float | None

class ServerFileOptionValidationZip(BaseModel):
    type: Literal["zip", "effectAudio"]
    minSize: int | float | None
    maxSize: int | float | None

class ServerFileOptionValidationJson(BaseModel):
    type: Literal["levelData", "skinData", "backgroundData", 
                  "backgroundConfiguration", "effectData", "particleData", 
                  "enginePlayData", "engineWatchData", "enginePreviewData", 
                  "engineTutorialData", "engineConfiguration", "replayData", 
                  "replayConfiguration"]
    minSize: int | float | None
    maxSize: int | float | None