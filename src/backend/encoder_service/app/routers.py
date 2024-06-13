from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import FaissResponse, TextData, Metadata
from encoder import Encoder

router = APIRouter()
encoder = Encoder()       #инициализируем интерфейс взаимодействия с моделью


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/listen', tags=["Encoder"], response_model=FaissResponse)
def transcribation(text: TextData) -> FaissResponse:
    indexx = encoder.get_emb(text.url,text.description)
    #print(type(transcribation_response), type(transcribation_response[0]))
    print(str(text.url),int(indexx))
    return FaissResponse(
        url=str(text.url),
        index=int(indexx)
    )

