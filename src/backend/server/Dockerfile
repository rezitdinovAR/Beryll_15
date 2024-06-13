FROM golang:1.20.4

WORKDIR /usr/src/app

COPY . .
RUN go mod init server
RUN go get 	"github.com/gofiber/fiber/v2" "gorm.io/driver/postgres" "gorm.io/gorm" "gorm.io/gorm/logger"
RUN go build -o ./tmp/main ./cmd
RUN ./tmp/main