"""
Steals staff-picked levels from unch and uploads to the local fork

Requires requests and tqdm: pip install requests, tqdm
run from the uc-sonoserver directory

..please use for tests only..
"""

import requests
import json
from io import BytesIO
from helpers.models.api.levels import LevelList
from tqdm import tqdm

YOUR_BACKEND_ADDR = "http://127.0.0.1:8001"

request = requests.get("https://sono_api.untitledcharts.com/api/charts?staff_pick=1&type=advanced&sort_by=published_at", verify=False)
levels = LevelList.model_validate_json(request.text)

def make_url(author: str, id: str, asset_base_url: str, file_hash: str) -> str:
    return "/".join([asset_base_url, author, id, file_hash])

def download(link: str) -> BytesIO:
    request = requests.get(link)

    io = BytesIO(request.content)
    io.seek(0)

    return io

for level in tqdm(levels.data):
    requests.post(
        YOUR_BACKEND_ADDR + "/api/charts/upload/",
        data={
            "data": json.dumps({
                "rating": level.rating,
                "title": level.title,
                "artists": level.artists,
                "author": level.author,
                "includes_background": False,
                "includes_preview": False,
                "tags": level.tags
            })
        },
        files={
            "jacket_image": ("jacket.png", download(make_url(level.author, level.id, levels.asset_base_url, level.jacket_file_hash))),
            "chart_file": ("chart", download(make_url(level.author, level.id, levels.asset_base_url, level.chart_file_hash))),
            "audio_file": ("audio.mp3", download(make_url(level.author, level.id, levels.asset_base_url, level.music_file_hash)))
        },
        headers={
            "authorization": "eyJpZCI6ICJlMWJhNDFhNi1hMDQzLTQ5MTktYTQ2Ni05YTZkMWVkZWExMTMiLCAidXNlcl9pZCI6ICIxMTIwNjZiZWI0YjdhNDlkZTNlNGNlNjRlMmQ1YWRiZmJmNWNmZjZkM2RmMTI2YjVkYTg3NDhmNzZhZTZjNzg5IiwgInR5cGUiOiAiZ2FtZSJ9.f06deb0a5181b98bdcd960760d823f5556ff625b0917330b8b28d286ff8d0006"
        }
    )