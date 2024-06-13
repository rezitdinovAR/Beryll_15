from pydantic import BaseModel
from typing import List

class Metadata(BaseModel):
    '''Мета информация - что-то не относящиеся к данным, например сессия, идентификатор пользователя, что годно'''
    user_id: str


class TextDataUrl(BaseModel):
    url: str
    description: str

class TextData(BaseModel):
    text: str

class FaissResponse(BaseModel):
    url: str
    index: int

class VideoData(BaseModel):
    mp4_base64: str

class VisualData(BaseModel):
    '''Изображение в формате wav закодированное в base64'''
    img_base64: str
    
class AudioData(BaseModel):
    '''Аудио в формате wav закодированное в base64'''
    wav_base64: str
    sample_rate: int

class TopResponse(BaseModel):
    top: str