from pydantic import BaseModel


class Metadata(BaseModel):
    '''Мета информация - что-то не относящиеся к данным, например сессия, идентификатор пользователя, что угодно'''
    user_id: str


class VisualData(BaseModel):
    '''Изображение в формате wav закодированное в base64'''
    img_base64: str


class TextData(BaseModel):
    '''Текстовая информация'''
    text: str


class VisualMessage(BaseModel):
    '''Формат визуального сообщения для фронта'''
    meta: Metadata
    data: VisualData

class TextMessage(BaseModel):
    '''Формат тектового сообщения для фронта'''
    meta: Metadata
    data: TextData