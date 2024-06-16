from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status
import json
from typing import List

from schemas import FaissResponse, TextData, Metadata, TextDataUrl, TopResponse, TextDataUrls, TextDataDescription
from encoder import Encoder

router = APIRouter()
encoder = Encoder()       #инициализируем интерфейс взаимодействия с моделью


@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


path='/api'

@router.post(path + '/listen', tags=["Encoder"])
def transcribation(text:List[TextDataUrl]):
    print(text, type(text))
    urls = []
    descriptions = []
    
    for item in text:
        urls.append(item.url)
        descriptions.append(item.description)
    indexx = encoder.get_emb(urls,descriptions)
    #print(type(transcribation_response), type(transcribation_response[0]))
    print(indexx)
    return [FaissResponse(
        url=str(index[0]),
        index=int(index[1])
    ) for index in indexx]

@router.post(path + '/get', tags=["Encoder"])
def transcribation(text: TextData) :
    indexes = encoder.search(text.text)
    print(indexes, type(indexes))
    return indexes

@router.post(path + '/metric', tags=["Encoder"])
def transcribation(text: TextData) :
    indexes = encoder.search_four(text.text)
    print(indexes, type(indexes))
    return indexes

@router.post(path + '/set', tags=["Encoder"])
def transcribation(text: TextDataDescription):
    encoder.set_description(text.description)
    return text.description