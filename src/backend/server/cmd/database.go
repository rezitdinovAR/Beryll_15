package main

import (
	"fmt"
	"log"
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

type Dbinstance struct {
	Db *gorm.DB
}

var DB Dbinstance

func ConnectDb() {
	dsn := fmt.Sprintf("host=db user=postgres password=postgres dbname=postgres port=5432")

	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})

	if err != nil {
		log.Fatal("Failed to connect to database. \n", err)
		os.Exit(2)
	}

	log.Println("connected")
	db.Logger = logger.Default.LogMode(logger.Silent)

	log.Println("running migrations")

	db.AutoMigrate(&SaveUrl{})

	DB = Dbinstance{
		Db: db,
	}
}

func WriteToDbAny(videos []SaveUrl) {
	for _, v := range videos {
		fmt.Println("write to db: " + string(v.Description) + string(v.Index) + v.Url)
		DB.Db.Create(&v)
	}
}

func SearchInDb(indexes []int) (urls []SaveUrl) {
	DB.Db.Where("index IN ?", indexes).Find(&urls)
	fmt.Println("read from db: " + string(len(urls)))
	return urls
}
