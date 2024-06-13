# Используйте официальный образ Golang как базовый
FROM golang:1.18 as builder

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте go.mod и go.sum в контейнер
COPY app/go.mod app/go.sum ./

# Скопируйте исходный код приложения в контейнер
COPY app/ .

