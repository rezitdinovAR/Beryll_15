package main

import "gorm.io/gorm"

type Video struct {
	gorm.Model
	Url string `json:"url" gorm:"text;not null;default:null`
	Index   string `json:"index" gorm:"text;not null;default:null`
}
