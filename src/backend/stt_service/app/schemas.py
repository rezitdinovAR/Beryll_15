from pydantic import BaseModel

class AudioData(BaseModel):
    '''Аудио в формате wav закодированное в base64'''
    wav_base64: str
    sample_rate: int


class TextData(BaseModel):
    '''Текстовая информация'''
    text: str

