from base64 import b64decode
import whisperx
import torch

#Интерфейс взаимодействия с Whisper
class ASR:

    def __init__(self):
        self.model_size = 'medium' if torch.cuda.is_available() else 'small' #модели см. orig whisperx
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu' #2v100 32GPU
        self.quant = 'float16' if torch.cuda.is_available() else 'int4' #квант. модели исп. int8/int4 при недостатке GPU Mem (влияет на результат)
        self.bs = 16 if torch.cuda.is_available() else 2 #размер батча исп меньшее значение пр недостатке GPU Mem (влияет на результат)
        self.model = whisperx.load_model(whisper_arch=self.model_size, device=self.device, compute_type=self.quant)

    def recognize(self, encoded_audio):
        #сохраняем файл в базу (в будущем)
        filename = 'out.wav' #здесь может быть ваш генератор


        with open(f'out.wav', 'wb') as f:
            bytes = b64decode(encoded_audio)
            f.write(bytes)


        audio = whisperx.load_audio(filename)

        #используем пайплайн нашей модели
        result = self.model.transcribe(audio, batch_size=self.bs)

        #форматируем ответ
        texts = []
        for segment in result["segments"]:
            texts.append(segment["text"])

        recognition = ' '.join(texts)

        return recognition