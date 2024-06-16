package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

func UploadForFront(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Не тот метод", http.StatusBadRequest)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Ошибка чтения тела запроса", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	var requestData SendLink
	err = json.Unmarshal(body, &requestData)
	if err != nil {
		http.Error(w, "Ошибка разбора JSON", http.StatusBadRequest)
		return
	}
	fmt.Println("Отправка в модель с фронта:")
	request := SendUrl{Url: requestData.Link, Description: requestData.Description}

	DownloadToModelAny([]SendUrl{request}, "http://encoder_service:8666/api/listen")

	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	_, err = w.Write(body)
	if err != nil {
		http.Error(w, "Ошибка при отправке ответа", http.StatusInternalServerError)
		return
	}
}

func SearchForFront(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Не тот метод", http.StatusBadRequest)
		return
	}

	requestData := r.URL.Query().Get("text")

	dbData := SearchInModel(Request{SearchText: requestData}, "http://encoder_service:8666/api/get")
	if len(dbData) > 10 {
		//
	}
	if dbData == nil {
		http.Error(w, "Ошибка поиска в модели", http.StatusNotFound)
	}

	response, err := json.Marshal(dbData)
	if err != nil {
		http.Error(w, "Ошибка формирования ответа", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, err = w.Write(response)
	if err != nil {
		http.Error(w, "Ошибка при отправке ответа", http.StatusInternalServerError)
		return
	}
}

func SearchForMetric(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Не тот метод", http.StatusBadRequest)
		return
	}

	requestData := r.URL.Query().Get("text")

	dbData := SearchInModel(Request{SearchText: requestData}, "http://encoder_service:8666/api/metric")
	if len(dbData) > 4 {

	}
	if dbData == nil {
		http.Error(w, "Ошибка поиска в модели", http.StatusNotFound)
	}

	response, err := json.Marshal(dbData)
	if err != nil {
		http.Error(w, "Ошибка формирования ответа", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, err = w.Write(response)
	if err != nil {
		http.Error(w, "Ошибка при отправке ответа", http.StatusInternalServerError)
		return
	}
}

func DownloadToModelAny(requestData []SendUrl, url string) {
	jsonData, err := json.Marshal(requestData)
	if err != nil {
		fmt.Println("Error marshaling request data:", err)
		return
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Println("Error making POST request:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		var resData []SaveUrl
		if err := json.NewDecoder(resp.Body).Decode(&resData); err != nil {
			fmt.Println("Error decoding response data:", err)
			return
		}

		if len(resData) != len(requestData) {
			fmt.Println("request and responce not equal")
			return
		} else {
			for i, _ := range resData {
				resData[i].Description = requestData[i].Description
				//fmt.Println("перенос описания:" + resData[i].Description + " " + requestData[i].Description)
			}
		}

		WriteToDbAny(resData)
	} else {
		fmt.Println("Error: received status code", resp.StatusCode)
	}
}

func SearchInModel(requestData Request, url string) []SaveUrl {
	timeStart := time.Now()

	jsonData, err := json.Marshal(requestData)
	if err != nil {
		fmt.Println("Error marshaling request data:", err)
		return nil
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Println("Error making POST request:", err)
		return nil
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		var resData []int
		if err := json.NewDecoder(resp.Body).Decode(&resData); err != nil {
			fmt.Println("Error decoding response data:", err)
			return nil
		}

		urls := SearchInDb(resData)
		fmt.Println("search timeDiff: " + fmt.Sprintf("%.2f", time.Now().Sub(timeStart).Seconds()))
		return urls

	} else {
		fmt.Println("Error: received status code", resp.StatusCode)
	}
	return nil
}
