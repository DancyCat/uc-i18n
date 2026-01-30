from pydantic import BaseModel
from typing import Generic, Literal, Text, TypeAlias, TypeVar
from helpers.models.sonolus.misc import Tag, SRL
from helpers.models.sonolus.options import ServerForm

class UserItem(BaseModel):
    name: str
    source: str | None
    title: str
    handle: str | None
    tags: list[Tag]


class BackgroundItem(BaseModel):
    name: str
    source: str | None
    version: Literal[2] = 2
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: SRL
    data: SRL
    image: SRL
    configuration: SRL
    authorUser: UserItem | None


class ParticleItem(BaseModel):
    name: str
    source: str | None
    version: Literal[3] = 3
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: SRL
    data: SRL
    texture: SRL
    authorUser: UserItem | None


class EffectItem(BaseModel):
    name: str
    source: str | None
    version: Literal[5] = 5
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: SRL
    data: SRL
    audio: SRL
    authorUser: UserItem | None


class SkinItem(BaseModel):
    name: str
    source: str | None
    version: Literal[4] = 4
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: SRL
    data: SRL
    texture: SRL
    authorUser: UserItem | None


class EngineItem(BaseModel):
    name: str
    version: Literal[13] = 13
    title: str
    subtitle: str
    source: str | None
    author: str
    tags: list[Tag]
    description: str | None

    skin: SkinItem
    background: BackgroundItem
    effect: EffectItem
    particle: ParticleItem

    thumbnail: SRL
    playData: SRL
    watchData: SRL
    previewData: SRL
    tutorialData: SRL
    rom: SRL | None
    configuration: SRL
    authorUser: UserItem | None


class PostItem(BaseModel):
    name: str
    source: str | None
    version: Literal[1] = 1
    title: str
    time: int
    author: str
    tags: list[Tag]
    thumbnail: SRL | None
    authorUser: UserItem | None

T = TypeVar("T", SkinItem, BackgroundItem, EffectItem, ParticleItem)

class UseItem(BaseModel, Generic[T]):
    useDefault: bool
    item: T | None


class LevelItem(BaseModel):
    name: str
    source: str | None
    version: Literal[1] = 1
    rating: int
    title: str
    artists: str
    author: str
    tags: list[Tag]
    engine: EngineItem
    useSkin: UseItem[SkinItem]
    useBackground: UseItem[BackgroundItem]
    useEffect: UseItem[EffectItem]
    useParticle: UseItem[ParticleItem]
    cover: SRL
    bgm: SRL
    preview: SRL | None
    data: SRL
    authorUser: UserItem | None


class PlaylistItem(BaseModel):
    name: str
    source: str | None
    version: Literal[1] = 1
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    levels: list[LevelItem]
    thumbnail: SRL | None
    authorUser: UserItem | None


class RoomItem(BaseModel):
    name: str
    title: str
    subtitle: str
    master: str
    tags: list[Tag]
    cover: SRL | None
    bgm: SRL | None
    preview: SRL | None
    authorUser: UserItem | None


class ReplayItem(BaseModel):
    name: str
    source: str | None
    version: Literal[1] = 1
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    level: LevelItem
    data: SRL
    configuration: SRL
    authorUser: UserItem | None


ServerItem: TypeAlias = (
    PostItem
    | RoomItem
    | SkinItem
    | BackgroundItem
    | ParticleItem
    | EffectItem
    | RoomItem
    | PlaylistItem
    | ReplayItem
    | LevelItem
    | EngineItem
    | UserItem
)


class ServerItemCommunityComment(BaseModel):
    name: str
    author: str
    time: int  # ms epoch
    content: str
    actions: list[ServerForm]
    authorUser: UserItem | None


class ServerItemLeaderboard(BaseModel):
    name: str
    title: str | Text
    description: str | None


class ServerItemLeaderboardRecord(BaseModel):
    name: str
    rank: Text | str
    player: str
    value: Text | str
    playerUser: UserItem | None
