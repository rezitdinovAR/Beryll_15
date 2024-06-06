import torch
import whisperx

class ASR:
    
    #init models and parameters
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.batch_size = 2 # reduce if low on GPU memory
        self.model = whisperx.load_model("medium", self.device, compute_type="int8") # change to "int8" if low on GPU mem (may reduce accuracy)
        

    #transcribe into segments with speech
    def transcribation(self, audio):
        result = self.model.transcribe(audio, batch_size=self.batch_size)
        return result["segments"]
