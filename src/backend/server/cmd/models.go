package main

import "gorm.io/gorm"

type SendUrl struct {
	Url         string `json:"url" gorm:"text;not null;default:null`
	Description string `json:"description" gorm:"text;not null;default:null`
}

type SendLink struct {
	Link        string `json:"link" gorm:"text;not null;default:null`
	Description string `json:"description" gorm:"text;not null;default:null`
}

type Request struct {
	SearchText string `json:"text" gorm:"text;not null;default:null`
}

type Ids struct {
	Ids []int `json:"indexes" gorm:"not null;default:null`
}

type SaveUrl struct {
	gorm.Model
	Url         string `json:"url" gorm:"text;not null;default:null`
	Index       int    `json:"index" gorm:"int;not null;default:null`
	Description string `json:"description" gorm:"text;not null;default:null`
}
