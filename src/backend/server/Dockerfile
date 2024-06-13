FROM golang:1.20.4

WORKDIR /code

RUN go install github.com/air-verse/air@latest

COPY cmd /code/cmd
COPY tmp /code/tmp
COPY go.mod /code
COPY go.sum /code



