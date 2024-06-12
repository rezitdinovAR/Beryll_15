import requests
import ffmpeg
import base64
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
import time

class VideoData(BaseModel):
    mp4_base64: str

class TextData(BaseModel):
    text: str

def download_video(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        print(f"Failed to download video. Status code: {response.status_code}")

def extract_audio_video(input_file, audio_output):
    # Извлечение аудио дорожки в формате WAV с частотой дискретизации 16000 Гц
    (
        ffmpeg
        .input(input_file)
        .output(audio_output, acodec='pcm_s16le', ar='16000')
        .run(overwrite_output=True, quiet=True)
    )
    

def file_to_base64(filename):
    with open(filename, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string.decode('utf-8')

def send_to_api(url, video_data):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=video_data, headers=headers)
    return response.status_code, response

def get_emb(video_url):
    # Скачивание видео
    video_filename = "temp.mp4"
    audio_filename = "temp.wav"
    download_video(video_url, video_filename)
    extract_audio_video(video_filename,audio_filename)
    # Преобразование файла в Base64
    video_base64 = file_to_base64(video_filename)
    audio_base64 = file_to_base64(audio_filename)

    # Отправка данных в API
    api_endpoints = {
        "v2t":"http://localhost:85/api/listen",
        # Добавьте больше URL API по мере необходимости
    }

    emb_api = "http://localhost:86/api/listen"

    data = {"v2t": VideoData(mp4_base64=video_base64).dict()}

    with ThreadPoolExecutor(max_workers=len(api_endpoints)) as executor:
        futures = [executor.submit(send_to_api, api_endpoints["v2t"], data["v2t"]) for api in ["v2t"]]
        
        for future in futures:
            status_code, response = future.result()
            response_text = response.text
            if status_code:
                print(f"Response from API {status_code}")
            else:
                print(f"Error sending request: {response_text}")
    start_time=time.time()
    response = requests.post(emb_api, json=TextData(text=response_text).dict(), headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        data = response.json()["text"].split(";")
    #print(response.status_code,data,time.time()-start_time)


get_emb('https://cdn-st.rutubelist.ru/media/50/0a/a56eb2824b93a57c3f4ad7e02ddd/fhd.mp4')


