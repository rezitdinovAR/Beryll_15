from pydantic import BaseModel


class Metadata(BaseModel):
    '''Мета информация - что-то не относящиеся к данным, например сессия, идентификатор пользователя, что годно'''
    user_id: str


class AudioData(BaseModel):
    '''Аудио в формате wav закодированное в base64'''
    wav_base64: str
    sample_rate: int


class TextData(BaseModel):
    '''Текстовая информация'''
    text: str


class AudioMessage(BaseModel):
    '''Формат Аудио сообщения для фронта'''
    meta: Metadata
    data: AudioData

class TextMessage(BaseModel):
    '''Формат тектового сообщения для фронта'''
    meta: Metadata
    data: TextData