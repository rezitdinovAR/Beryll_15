package main

import (
	"github.com/gofiber/fiber/v2"
)

func SaveVideo(c *fiber.Ctx) error {
	video := new(Video)
	if err := c.BodyParser(video); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}

	DB.Db.Create(&video)

	return c.Status(200).JSON(video)
}
