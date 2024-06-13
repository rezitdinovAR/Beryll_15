package handlers

import (
	"server/database"
	"server/models"
	"github.com/gofiber/fiber/v2"
)

func SaveVideo(c *fiber.Ctx) error {
	video := new(models.Video)
	if err := c.BodyParser(video); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"message": err.Error(),
		})
	}

	database.DB.Db.Create(&video)

	return c.Status(200).JSON(video)
}
