from pydantic import BaseModel
from typing import List

class VisualData(BaseModel):
    '''Изображение в формате wav закодированное в base64'''
    img_base64: list
    size: list


class TextData(BaseModel):
    '''Текстовая информация'''
    text: str
