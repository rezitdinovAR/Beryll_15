import numpy as np
import av
import os, sys
import torch
from transformers import AutoImageProcessor, AutoTokenizer, VisionEncoderDecoderModel, AutoModelForSeq2SeqLM
import argparse, json
import base64

class Video2Text():
    ''' Initialize the parameters for the model '''
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # load pretrained processor, tokenizer, and model
        self.image_processor = AutoImageProcessor.from_pretrained("./models/MCG-NJU--videomae-base/snapshots/dc740ceda42fce44faed2ea03c6d447db72f6af9")
        self.tokenizer = AutoTokenizer.from_pretrained("./models/gpt2/snapshots/607a30d783dfa663caf39e06633721c8d4cfcd7e")
        self. model = VisionEncoderDecoderModel.from_pretrained("./models/timesformer-gpt2-video-captioning/snapshots/069a6e90d062792f1d43504da94641be20a23f7f").to(self.device)

        self.translate_tokenizer = AutoTokenizer.from_pretrained("./models/Helsinki-NLP--opus-mt-en-ru/snapshots/bb09c99d180016eac6819df3dae68edb1690fdee")
        self.translate_model = AutoModelForSeq2SeqLM.from_pretrained("./models/Helsinki-NLP--opus-mt-en-ru/snapshots/bb09c99d180016eac6819df3dae68edb1690fdee")

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
        inputs = self.translate_tokenizer(caption, return_tensors="pt")
        output = self.translate_model.generate(**inputs, max_new_tokens=100)
        out_text = self.translate_tokenizer.batch_decode(output, skip_special_tokens=True)
        return out_text[0]   
                

