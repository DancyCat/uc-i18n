from typing import Literal
from pydantic import BaseModel
from datetime import datetime

from core import SonolusRequest
from helpers.datetime_to_str import datetime_to_str
from helpers.models.api.charts import Chart
from helpers.models.api.misc import PublicAccount
from helpers.models.sonolus.item import ReplayItem, ServerItemLeaderboardRecord
from helpers.models.sonolus.misc import SRL, Tag
from helpers.owoify import handle_uwu
from helpers.sonolus_typings import Grade

# XXX: plans for future - pretiffy all of this
# and probably delete some models

class ReplayUploadData(BaseModel):
    engine: str
    grade: Grade
    nperfect: int
    ngreat: int
    ngood: int
    nmiss: int
    arcade_score: int
    accuracy_score: int
    speed: float

    @property
    def shortened_grade(self) -> str:
        return {
            "allPerfect": "AP",
            "fullCombo": "FC",
            "pass": "P",
            "fail": "X"
        }[self.grade]

class LeaderboardRecord(ReplayUploadData):
    submitter: str
    replay_data_hash: str
    replay_config_hash: str
    chart_id: str
    public_chart: bool

class LeaderboardRecordDBResponse(LeaderboardRecord): # XXX: remove optional fields
    display_name: str
    id: int
    created_at: datetime
    chart_prefix: str
    owner: bool | None
    mod: bool | None = None

class LeaderboardRecordWithAccount(LeaderboardRecordDBResponse):
    account: PublicAccount

class LeaderboardInfo(BaseModel):
    pageCount: int | None = None
    data: list[LeaderboardRecordWithAccount]

    def to_record_list(self, page: int = 1) -> list[ServerItemLeaderboardRecord]:
        leaderboards = []

        for i, record in enumerate(self.data):
            leaderboards.append(
                ServerItemLeaderboardRecord(
                    name=f"UnCh-{record.chart_id}-{record.id}",
                    rank=f"#{i + ((page - 1) * 10) + 1}",
                    player=record.display_name,
                    value=f"{record.shortened_grade} {record.arcade_score}", # TODO: different leaderboard types -> different.. these
                    playerUser=record.account.to_user_item()
                )
            )

class LeaderboardRecordInfo(BaseModel):
    data: LeaderboardRecordDBResponse
    chart: Chart
    submitter: PublicAccount
    asset_base_url: str

    @property
    def subtitle(self) -> str:
        string = f"{self.data.shortened_grade} | {self.data.arcade_score} / {self.data.accuracy_score} | {self.data.nperfect} / {self.data.ngreat} / {self.data.ngood} / {self.data.nmiss}"

        if self.data.speed != 1:
            string += f" | {self.data.speed}x"

        return string 

    def _make_url(self, asset_base_url: str, chart_prefix: str, user_id: str, hash: str) -> str:
        return f"{asset_base_url}/{chart_prefix}/replays/{user_id}/{hash}"

    def to_replay_item(self, request: SonolusRequest) -> ReplayItem:
        asset_base_url = self.asset_base_url.removesuffix("/")
        loc = request.state.loc

        level = self.chart.to_level_item(
            request,
            self.asset_base_url,
            request.state.levelbg,
        )

        time_str = datetime_to_str(self.data.created_at)
        date_str = handle_uwu(
            loc.time_ago(time_str),
            request.state.localization,
            request.state.uwu
        )

        return ReplayItem(
            name=f"UnCh-{level.name}-{self.data.id}",
            source=request.app.base_url,
            title=level.title,
            subtitle=self.subtitle,
            author=self.data.display_name,
            tags=[Tag(title=date_str, icon="clock")],
            level=level,
            data=SRL(
                hash=self.data.replay_data_hash,
                url=self._make_url(asset_base_url, self.data.chart_prefix, self.data.submitter, self.data.replay_data_hash)
            ),
            configuration=SRL(
                hash=self.data.replay_config_hash,
                url=self._make_url(asset_base_url, self.data.chart_prefix, self.data.submitter, self.data.replay_config_hash)
            ),
            authorUser=self.submitter.to_user_item()
        )
    
class DeleteLeaderboardRecord(LeaderboardRecordDBResponse):
    chart_title: str | None = None

class PublicLeaderboardRecordList(BaseModel):
    data: list[LeaderboardRecordInfo]
    pageCount: int | None = None

    def to_replay_items(self, request: SonolusRequest) -> list[ReplayItem]:
        return [record.to_replay_item(request) for record in self.data]