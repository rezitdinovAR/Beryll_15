from sentence_transformers import SentenceTransformer
from typing import List
import requests
import base64
import ffmpeg
import av
import os
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from fuzzywuzzy import process
from schemas import VideoData, VisualData, AudioData
import faiss
import numpy as np
from faiss_in import Faiss
from PIL import Image
import multiprocessing
from multiprocessing import set_start_method

try:
    multiprocessing.set_start_method('spawn')
except RuntimeError:
    pass

class Encoder():

    ''' Initialize the parameters for the model '''
    def __init__(self):
        self.model = SentenceTransformer('./models/distiluse-base-multilingual-cased-v2/snapshots/03a0532331151aeb3e1d2e602ffad62bb212a38d') 
        self.faiss_base = Faiss()
        self.counter = 0

    def encode(self, texts) -> List[float]:
        embeddings = self.model.encode(texts)
        return [embedding.tolist() for embedding in embeddings]


    def download_video(self, url, filename):

        try:
            response = requests.get(url, stream=True)
        except Exception as e:
            print("Шамиль пидор: ", url)
        else:
            response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        else:
            print(f"Failed to download video. Status code: {response.status_code}")
                

    def extract_audio_video(self,input_file, audio_output):
    # Извлечение аудио дорожки в формате WAV с частотой дискретизации 16000 Гц
        try:
            (
                ffmpeg
                .input(input_file)
                .output(audio_output, acodec='pcm_s16le', ar='16000')
                .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:  # Перехватываем исключение ffmpeg.Error
            print("Ошибка при выполнении ffmpeg:")
            print("stdout:", e.stdout.decode('utf-8'))  # Выводим стандартный поток вывода
            print("stderr:", e.stderr.decode('utf-8'))  # Выводим поток ошибок
            return False  # Повторно вызываем исключение для дальнейшей обработки или журналирования
    def get_frames(self,filename,image_filename):
        container = av.open(filename)
        frame_count=0
        size = [0,0]
        for frame in container.decode(video=0):
            #print("++++++++++++++++++++++++++")
            try:
                if isinstance(frame, av.video.frame.VideoFrame):
                    frame_count += 1
                    if frame_count % 300 == 0:
                        image = frame.to_image()
                        if size == [0,0]:
                            size = [image.size[0],image.size[0]]
                        #print(str(image_filename)+'%04d.jpg' % frame.index)
                        frame.to_image().save(str(image_filename)+'%04d.jpg' % frame.index)
                        
            except AttributeError as e:
                print(f"Ошибка при обработке кадра: {e}")
        return size
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
    
    def get_uniq_texts(self,texts):
        unique_texts = []
        text_result=""
        def is_unique(text, existing_texts, threshold=90):
            for existing in existing_texts:
                if process.extractOne(text, [existing])[1] >= threshold:
                    return False
            return True

        for text in texts:
            if is_unique(text, unique_texts):
                unique_texts.append(text)
        
        for text in unique_texts:
            if text[-1]==".":
                text_result+=text+" "
            else:
                text_result+=text+". "
        return text_result

    def process_single(self,data):
            video_filename,audio_filename,image_filename,video_url = data
            self.download_video(video_url,video_filename)
            video_base64=self.file_to_base64(video_filename)
            booler = self.extract_audio_video(video_filename, audio_filename)
            if booler !=False:
                audio_base64 = self.file_to_base64(audio_filename)
            else:
                audio_base64 = ""
            size = self.get_frames(video_filename,image_filename)
            images_base64 = []

            for root, subdirs, files in os.walk("."):
                for file in files:
                    #print(os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg') and image_filename==str(os.path.splitext(file)[0])[:-1])

                    if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg') and image_filename in str(os.path.splitext(file)[0]):
                        images_base64.append(self.file_to_base64(os.path.join(root, file)))
                        os.remove(os.path.join(root, file))
            return video_base64, audio_base64, images_base64, size, booler 
    
    def getter(self,video_filenames,audio_filenames,image_filenames,video_urls,i):
        results = self.process_single((video_filenames[i],audio_filenames[i],image_filenames[i],video_urls[i]))
        return results
    
    def get_emb(self,video_urls,descriptions):
        
        video_filenames = ["temp1.mp4","temp2.mp4","temp3.mp4","temp4.mp4"]
        audio_filenames = ["temp1.wav","temp2.wav","temp3.wav","temp4.wav"]
        image_filenames = ["temp1","temp2","temp3","temp4"]
        
        results = []
        video_base64s = []
        audio_base64s = []
        images_base64s = []
        size = []
        bools  = []
        for i in range(len(video_urls)):
            
            result = self.getter(video_filenames,audio_filenames,image_filenames,video_urls,i)
            #print(len(result))
            video_base64, audio_base64, images_base64, siz, bool = result
            #print(len(video_base64))
            video_base64s.append(video_base64)
            audio_base64s.append(audio_base64)
            images_base64s.append(images_base64)
            size.append(siz)
            bools.append(bool)
            
        #print(len(results))
        #video_base64s, audio_base64s, images_base64s, size, bools = zip(*results)
        api_endpoints = {
            "v2t":"http://video2text_service:85/api/listen",
            "ocr":"http://ocr_service:81/api/recognize",
            "asr":"http://stt_service:82/api/listen",
        }

        data = {
            "v2t":[VideoData(mp4_base64=video_base64).dict() for video_base64 in video_base64s],
            "ocr":[VisualData(img_base64=images_base64s[i], size = size[i]).dict() for i in range(len(video_urls))],
            "asr":[AudioData(wav_base64=audio_base64,sample_rate=16000).dict() for audio_base64 in audio_base64s]
        }
        responsess =  []
        with ThreadPoolExecutor(max_workers=len(api_endpoints)*len(video_urls)) as executor:
            for i in range(len(video_urls)):
                responses = []
                for typ in data.keys():
                    if typ=="ocr":
                        
                        if size[i] == [0,0]:
                            responses.append("")
                            continue
                    elif typ=="asr":  
                        if bools[i] == False:
                            responses.append("")
                            continue
                    future = executor.submit(self.send_to_api, api_endpoints[typ], data[typ][i]) 
                    status_code, response = future.result()
                    response_text = response.text
                    responses.append(response_text)
                responses.append(descriptions[i])
                responsess.append(responses)

                
                
        
        for i in range((len(video_urls))):
            self.faiss_base.write_indexx(self.encode(responsess[i]),[0,1,2,3])

        k = self.faiss_base.counter-((len(video_urls))-1)
        res = []
        for i in range(len(video_urls)):
            res.append([video_urls[i],k])
            k+=1
        return res
                
    def search(self,text):
        x = self.encode(text)
        return self.faiss_base.search_all([x for i in range(4)], k=10)
    
    def search_four(self,text):
        x = self.encode(text)
        return self.faiss_base.search_four([x for i in range(4)], k=4)

    def set_description(self,text):
        faiss.write_indexx([self.enocde(text) for i in range(4)],[3])
        
