from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import VisualData, TextData
from ocr import OCR

router = APIRouter()
ocr = OCR()


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/recognize', tags=["Optical character recognition"], response_model=TextData)
def recognition(visual_message: VisualData) -> TextData:

    recognition_response = ocr.recognize(visual_message.img_base64)
    print(recognition_response)

    return TextData(
            text=" ".join(recognition_response)
        )
    