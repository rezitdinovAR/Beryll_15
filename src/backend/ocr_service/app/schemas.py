from pydantic import BaseModel

class VisualData(BaseModel):
    '''Изображение в формате wav закодированное в base64'''
    img_base64: str


class TextData(BaseModel):
    '''Текстовая информация'''
    text: str
