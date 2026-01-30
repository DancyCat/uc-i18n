from pydantic import BaseModel
from helpers.sonolus_typings import Icon, ServerInfoButtonType, Text

class Tag(BaseModel):
    title: Text | str
    icon: Icon | str | None


class SRL(BaseModel):
    hash: str | None
    url: str | None


class SIL(BaseModel):
    address: str
    name: str

class ServerInfoItemButton(BaseModel):
    type: ServerInfoButtonType
    title: Text | str | None
    icon: Icon | str | None
    badgeCount: int | None
    infoType: str | None
    itemName: str | None

class ServerMessage(BaseModel):
    message: str

class ReplayConfiguration(BaseModel):
    options: list[int | float]
    optionNames: list[Text | str] | None