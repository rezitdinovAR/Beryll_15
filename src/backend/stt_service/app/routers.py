from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import AudioData, TextData
from asr import ASR

router = APIRouter()
listener = ASR()       #инициализируем интерфейс взаимодействия с моделью


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/listen', tags=["Transcribation"], response_model=TextData)
def trasncribation(audio_message: AudioData) -> TextData:
    '''
    Описание распознавания речи даби

    Алгоритм:
    1)получаем аудио в b64
    2)обрабатываем пайплайном модели (средство - интерфейс)
    3)возвращаем транскрибацию в бэк
    '''
    transcribation_response = listener.recognize(audio_message.wav_base64)

    return TextData(
            text=transcribation_response
        )
    