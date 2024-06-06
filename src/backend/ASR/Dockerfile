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

# Устанавливаем псевдонимы для python и pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

WORKDIR /code

COPY req.txt /code/req.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir --upgrade git+https://github.com/m-bain/whisperx.git
RUN pip install --no-cache-dir --upgrade -r /code/req.txt

COPY cons /code/cons

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/code/cons"

CMD ["python", "/code/cons/ASRApp.py"]