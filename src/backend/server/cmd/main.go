package main

import (
	"github.com/gofiber/fiber/v2"
)

func main() {
	ConnectDb()

	app := fiber.New()

	setupRoutes(app)

	app.Listen(":8667")
}

func setupRoutes(app *fiber.App) {
	app.Post("/api/listen", SaveVideo)
}
