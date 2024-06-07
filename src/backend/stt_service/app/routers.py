from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import AudioMessage, TextMessage, Metadata, TextData
from asr import ASR

router = APIRouter()
listener = ASR()       #инициализируем интерфейс взаимодействия с моделью


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/listen', tags=["Transcribation"], response_model=TextMessage)
def trasncribation(audio_message: AudioMessage) -> TextMessage:
    '''
    Описание распознавания речи даби

    Алгоритм:
    1)получаем аудио в b64
    2)обрабатываем пайплайном модели (средство - интерфейс)
    3)возвращаем транскрибацию в бэк
    '''
    transcribation_response = listener.recognize(audio_message.data.wav_base64)

    return TextMessage(
        meta=Metadata(
          user_id=audio_message.meta.user_id
        ),
        data=TextData(
            text=transcribation_response
        )
    )