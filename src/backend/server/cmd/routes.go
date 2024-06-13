package main

import (
	"handlers"
	"github.com/gofiber/fiber/v2"
)

func setupRoutes(app *fiber.App) {
	app.Get("/client", handlers.ListFacts)

	app.Post("/fact", handlers.CreateFact)
}
