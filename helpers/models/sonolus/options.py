from typing import Literal, Annotated
from pydantic import BaseModel, ConfigDict, Field
from helpers.models.sonolus.misc import SIL
from helpers.sonolus_typings import Icon, ItemType, Text


class ServerCollectionItemOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["collectionItem"] = "collectionItem"
    itemType: ItemType

class ServerTextOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["text"] = "text"
    default: str = Field(validation_alias="def", serialization_alias="def")
    placeholder: Text | str
    limit: int
    shortcuts: list[str]

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerTextAreaOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["textArea"] = "textArea"
    default: str = Field(validation_alias="def", serialization_alias="def")
    placeholder: Text | str
    limit: int
    shortcuts: list[str]

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerSliderOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["slider"] = "slider"
    default: int | float = Field(validation_alias="def", serialization_alias="def")
    min: int | float
    max: int | float
    step: int | float
    unit: Text | str | None = None

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerToggleOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["toggle"] = "toggle"
    default: bool = Field(validation_alias="def", serialization_alias="def")

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerOption_Value(BaseModel):
    name: str
    title: Text | str

class ServerSelectOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["select"] = "select"
    default: str = Field(validation_alias="def", serialization_alias="def")
    values: list[ServerOption_Value]

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerMultiOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["multi"] = "multi"
    default: list[bool] = Field(validation_alias="def", serialization_alias="def")
    values: list[ServerOption_Value]

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerServerItemOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["serverItem"] = "serverItem"
    itemType: ItemType
    default: SIL | None = Field(None, validation_alias="def", serialization_alias="def")
    allowOtherServers: bool

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerServerItemsOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["serverItems"] = "serverItems"
    itemType: ItemType
    default: list[SIL] = Field(validation_alias="def", serialization_alias="def")
    allowOtherServers: bool
    limit: int

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

class ServerCollectionItemOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["collectionItem"] = "collectionItem"
    itemType: ItemType

class ServerFileOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal["file"] = "file"
    default: str = Field(validation_alias="def", serialization_alias="def")

    model_config = ConfigDict(
        by_alias=True, 
        alias_priority=2, 
    )

ServerOption = (
    ServerTextOption
    | ServerTextAreaOption
    | ServerSliderOption
    | ServerToggleOption
    | ServerSelectOption
    | ServerMultiOption
    | ServerServerItemOption
    | ServerServerItemsOption
    | ServerCollectionItemOption
    | ServerFileOption
)

class ServerForm(BaseModel):
    type: str
    title: Text | str
    icon: Icon | str | None = None
    description: str | None = None
    help: str | None = None
    requireConfirmation: bool
    options: list[Annotated[ServerOption, Field(discriminator="type")]]