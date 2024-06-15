FROM golang:1.20.4

WORKDIR /code

RUN mkdir ./previews

COPY cmd ./cmd
COPY go.mod .
COPY go.sum .
RUN go build -o main ./cmd

ENTRYPOINT [ "/code/main" ]





