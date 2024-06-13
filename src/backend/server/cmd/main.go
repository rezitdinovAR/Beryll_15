package main

import (
	"server/database"
	"server/handlers"
	"github.com/gofiber/fiber/v2"
)

func main() {
	database.ConnectDb()

	app := fiber.New()

	setupRoutes(app)

	app.Listen(":8667")
}

func setupRoutes(app *fiber.App) {
	app.Post("/api/listen", handlers.SaveVideo)
}
