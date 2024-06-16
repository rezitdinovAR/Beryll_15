# Beryll_15

## Описание
Реализация сервиса Similarity Search для кейса Yappi на ЛЦТ 2024.
Схема прототипа решения находится в [docs/diagrams](./docs/diagrams/1.png)

## Требования
1. GPU Nvidia Tesla V100 с вычислительным типом float16 и >= 16Gb Memory
2. Docker Engine, следуйте [docs/docker.md](./docs/docker.md)
3. Nvidia Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

## Установка и использование
1. Склонируйте репозиторий:
  ```bash
  git clone git@github.com:rezitdinovAR/ASR_SD.git
  ```
2. Наиль напиши куда какие веса моделей класть
3. Запсук сервисов:
  ```bash
  docker-compose up -d
  ```

## Документация
Сервис представляет собой 6 контейнеров:
- stt_service_container - Пайплайн распознавания речи
- ocr_service_container - Пайплайн оптического распознавания символов
- encoder_service_container - Пайплайн энкодер модели совмещённый с добавлением в индекс векторного поиска FAISS
- postgres_container - Контейнер базы данных
- server_container - Контейнер серверной части на Go

### STT service
Данный контейнер содержит пайплайн распознавания речи. Используется модель семейства whisper, реализации whisperx: https://github.com/m-bain/whisperX <br />
Используемые схемы сообщений описаны в [src/backend/stt_service/app/tags.py](./src/backend/stt_service/app/tags.py)

#### Взаимодействие
Данный контейнер получает http запросы от encoder_service и возвращает транскрибацию соответствующего аудио.

### OCR service
Данный контейнер содержит пайплайн распознавания изображений. Используется композиция моделей и методов детекции CRAFT + ResNet + LSTM + CTC с различными декодерами в данной реализации используется один и жадных декодеров: https://github.com/JaidedAI/EasyOCR<br />
Используемые схемы сообщений описаны в [src/backend/stt_service/app/tags.py](./src/backend/ocr_service/app/tags.py)

#### Взаимодействие
Данный контейнер получает http запросы от encoder_service и возвращает распознавание батча соответствующих кадров видео.

### Encoder service
Пайплайн энкодер модели совмещённый с добавлением в индекс векторного поиска FAISS<br />
Используемые схемы сообщений описаны в [src/backend/encoder_service/app/tags.py](./src/backend/encoder_service/app/tags.py)

#### Взаимодействие
Данный контейнер получает http запросы от server_container обрабатывает видео для отпраки в каждый отдельный сервис пайпланов, после получения ответов обрабатывает их и осуществляет пайплайн модели Encoder НАИЛЬ ДОБАВЬ НАЗВАНИЕ МОДЕЛИ С ССЫЛКОЙ, добавляя полученные эмбеддинги в индекс векторного поиска

НАИЛЬ, ШАМИЛЬ и ВОВА ДОПИШИТЕ ПО server_container и FAISS и фронту
## API ручки
После запуска сервиса на локальной машине ручки будут находится по следующим адресам: НАПИШИТЕ СЮДА ГДЕ БУДЕТ РУЧКА <br />
Так же предоставляется сервис с фронтом расположенный по адресу: НАШ ДОМЕН <br />
API ручка: РУЧКА ГДЕ ЛЕЖИТ <br />

## Контакты
**В случае вопросов обращаться:**
1. Telegram: [t.me/rezitdinovAR](https://t.me/rezitdinovAR)
2. e-mail: rezitdinovar@mail.ru
