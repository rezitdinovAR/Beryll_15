from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import VisualMessage, TextMessage, Metadata, TextData
from ocr import OCR

router = APIRouter()
ocr = OCR()


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/recognize', tags=["Optical character recognition"], response_model=TextMessage)
def recognition(visual_message: VisualMessage) -> TextMessage:

    recognition_response = ocr.recognize(visual_message.data.img_base64)
    print(recognition_response)

    return TextMessage(
        meta=Metadata(
          user_id=visual_message.meta.user_id
        ),
        data=TextData(
            text=recognition_response
        )
    )