# Используем базовый образ с поддержкой CUDA от NVIDIA
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Обновляем список пакетов и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-dev \
    python3.10-venv \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libglib2.0-0
# Устанавливаем псевдонимы для python и pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

WORKDIR /code

COPY req.txt /code/req.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/req.txt
#RUN pip install git+https://github.com/m-bain/whisperx.git
RUN pip install av
RUN pip install ffmpeg-python
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install pillow

COPY app /code/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/code/app"

EXPOSE 82

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8666"]
