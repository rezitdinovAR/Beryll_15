from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import VideoData, TextData, Metadata
from video2text import Video2Text

router = APIRouter()
video2text = Video2Text()       #инициализируем интерфейс взаимодействия с моделью


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/listen', tags=["Video2text"], response_model=TextData)
def trasncribation(video_data: VideoData) -> TextData:
    transcribation_response = video2text.test(video_data.mp4_base64)

    return TextData(
        text=transcribation_response
    )

