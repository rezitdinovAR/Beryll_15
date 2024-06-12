from sentence_transformers import SentenceTransformer
from typing import List
import requests
import base64
import ffmpeg
import av
import os
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel

from schemas import VideoData, VisualData, AudioData



class Encoder():
    ''' Initialize the parameters for the model '''
    def __init__(self):
        self.model = SentenceTransformer('distiluse-base-multilingual-cased-v2')  
    
    def encode(self, text) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def download_video(self,url, filename):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        else:
            print(f"Failed to download video. Status code: {response.status_code}")
                

    def extract_audio_video(self,input_file, audio_output):
    # Извлечение аудио дорожки в формате WAV с частотой дискретизации 16000 Гц
        (
            ffmpeg
            .input(input_file)
            .output(audio_output, acodec='pcm_s16le', ar='16000')
            .run(overwrite_output=True, quiet=True)
        )

    def get_frames(self,filename):
        video = av.open(filename)

        for packet in video.demux():
            for frame in packet.decode():
                if frame.type == 'video' and frame.index%300==0:
                    frame.to_image().save('temp%04d.jpg' % frame.index)
                    print(frame.index)
    
    def file_to_base64(self,filename):
        with open(filename, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        return encoded_string.decode('utf-8')
    
    def send_to_api(self, url, data):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)
        return response.status_code, response
    
    def get_emb(self,video_url):
        video_filename = "temp.mp4"
        audio_filename = "temp.wav"
        
        self.download_video(video_url,video_filename)
        self.extract_audio_video(video_filename, audio_filename)
        self.get_frames(video_filename)

        video_base64 = self.file_to_base64(video_filename)
        audio_base64 = self.file_to_base64(audio_filename)

        images_base64 = []
        for root, subdirs, files in os.walk("."):
            for file in files:
                if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
                    images_base64.append(self.file_to_base64(os.path.join(root, file)))

        api_endpoints = {
            "v2t":"http://localhost:85/api/listen",
            "ocr":"http://localhost:81/api/recognize",
            "asr":"http://localhost:80/api/listen",
        }

        data = {
            "v2t":VideoData(mp4_base64=video_base64),
            "ocr":[VisualData(img_base64=image_base64) for image_base64 in images_base64],
            "asr":AudioData(wav_base64=audio_base64,sample_rate=16000)
        }
        responses =  []
        with ThreadPoolExecutor(max_workers=len(api_endpoints)) as executor:
            for typ in data.keys():
                if typ == "v2t" or typ == "asr":
                    future = executor.submit(self.send_to_api, api_endpoints[typ], data[typ])
                    status_code, response = future.result()
                    response_text = response.text
                    responses.append(response_text)
                
                else:
                    texts=[]
                    futures = [executor.submit(self.send_to_api, api_endpoints[typ], dat) for dat in data[typ]]
                    for future in futures:
                        status_code, response = future.result()
                        response_text = response.text
                        texts.append(response_text)
                        responses.append("text")
                



