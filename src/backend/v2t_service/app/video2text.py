import numpy as np
import av
import os, sys
import torch
from transformers import AutoImageProcessor, AutoTokenizer, VisionEncoderDecoderModel
import argparse, json
import base64

class Video2Text():
    ''' Initialize the parameters for the model '''
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # load pretrained processor, tokenizer, and model
        self.image_processor = AutoImageProcessor.from_pretrained("MCG-NJU/videomae-base")
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self. model = VisionEncoderDecoderModel.from_pretrained("Neleac/timesformer-gpt2-video-captioning").to(self.device)

    def test(self,base64_string):
        data = base64.b64decode(base64_string)
        video_path='/code/app/temp_file.mp4'
        with open(video_path, 'wb') as f:
            f.write(data)
        container = av.open(video_path)

        # extract evenly spaced frames from video
        seg_len = container.streams.video[0].frames
        clip_len = self.model.config.encoder.num_frames
        indices = set(np.linspace(0, seg_len, num=clip_len, endpoint=False).astype(np.int64))
        frames = []
        container.seek(0)
        for i, frame in enumerate(container.decode(video=0)):
            if i in indices:
                frames.append(frame.to_ndarray(format="rgb24"))

        # generate caption
        gen_kwargs = {
            "min_length": 10, 
            "max_length": 20, 
            "num_beams": 8,
        }
        pixel_values = self.image_processor(frames, return_tensors="pt").pixel_values.to(self.device)
        tokens = self.model.generate(pixel_values, **gen_kwargs)
        caption = self.tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]

        return caption    
                

