from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import EmbeddingResponse, TextData, Metadata
from encoder import Encoder

router = APIRouter()
encoder = Encoder()       #инициализируем интерфейс взаимодействия с моделью


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/listen', tags=["Encoder"], response_model=TextData)
def transcribation(text: TextData) -> EmbeddingResponse:
    transcribation_response = encoder.encode(text.text)
    print(type(transcribation_response), type(transcribation_response[0]))
    strt = (';'.join([str(x) for x in transcribation_response]))
    print(type(strt))
    return EmbeddingResponse(
        text=strt
    )

