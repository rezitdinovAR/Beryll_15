from pydantic import BaseModel


class Metadata(BaseModel):
    '''Мета информация - что-то не относящиеся к данным, например сессия, идентификатор пользователя, что годно'''
    user_id: str


class VideoData(BaseModel):
    mp4_base64: str


class TextData(BaseModel):
    '''Текстовая информация'''
    text: str