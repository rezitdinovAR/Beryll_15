package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strings"
	"time"
)

func SendFromCsv() {
	filePath := "/code/cmd/yappy_hackaton_2024_400k.csv"

	file, err := os.Open(filePath)
	if err != nil {
		fmt.Printf("Ошибка открытия файла: %v\n", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.Comma = ','

	i := 0
	ii := 0
	average := 0.0
	sendData := make([]SendUrl, 0)
	for {
		timeStart := time.Now()
		record, err := reader.Read()
		if err != nil {
			break
		}
		var desc string
		if len(record) > 1 {
			desc = strings.TrimSpace(strings.Join(record[1:], ""))
		}
		videoURL := strings.TrimSpace(record[0])

		var testUrl SaveUrl
		ii++
		fmt.Println(ii)
		if error := DB.Db.Where("url = ?", videoURL).First(&testUrl); error.Error != nil {
			i++
			sendData = append(sendData, SendUrl{Url: videoURL, Description: desc})
			if i%4 == 0 {
				DownloadToModelAny(sendData, "http://encoder_service:8666/api/listen")
				GetDescription(Description{Description: sendData[0].Description}, "http://encoder_service:8666/api/set")
				GetDescription(Description{Description: sendData[1].Description}, "http://encoder_service:8666/api/set")
				GetDescription(Description{Description: sendData[2].Description}, "http://encoder_service:8666/api/set")
				GetDescription(Description{Description: sendData[3].Description}, "http://encoder_service:8666/api/set")
				timeDiff := time.Now().Sub(timeStart).Seconds()
				average += timeDiff
				fmt.Println("download timeDiff: " + fmt.Sprintf("%.2f", timeDiff)) //+ " average: " + fmt.Sprintf("%.2f", average/float64(i)))
				sendData = make([]SendUrl, 0)
			}
		} else {
			if ii <= 6311 {
				GetDescription(Description{Description: desc}, "http://encoder_service:8666/api/set")
			}
			testUrl.Description = desc
			println("Update desc: " + desc)
			DB.Db.Save(&testUrl)
			println("Already upload: " + videoURL)
		}
	}
}
