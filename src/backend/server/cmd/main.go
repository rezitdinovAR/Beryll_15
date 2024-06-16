package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	time.Sleep(15 * time.Second)
	ConnectDb()
	go SendFromCsv()
	deleteOldRecords()

	http.HandleFunc("/api/search", SearchForFront)
	http.HandleFunc("/search", Search)
	http.HandleFunc("/index", UploadForFront)
	http.HandleFunc("/api/upload", UploadForFront)
	http.HandleFunc("/api/metric", SearchForMetric)

	fmt.Println("Server is listening on port 8910...")
	if err := http.ListenAndServe(":8910", corsMiddleware(http.DefaultServeMux)); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}

}

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			return
		}

		next.ServeHTTP(w, r)
	})
}

func deleteOldRecords() {
	var records []SaveUrl

	DB.Db.Find(&records)

	urlToLatestRecord := make(map[string]SaveUrl)

	for _, record := range records {
		if existingRecord, exists := urlToLatestRecord[record.Url]; !exists || record.CreatedAt.After(existingRecord.CreatedAt) {
			urlToLatestRecord[record.Url] = record
		}
	}

	for _, record := range records {
		if existingRecord, exists := urlToLatestRecord[record.Url]; exists && record.CreatedAt.After(existingRecord.CreatedAt) {
			fmt.Printf("Повторяющееся поле: %+v\n", record.Index)
		}
	}

	// Удаляем записи, которые не являются самыми новыми для их имени
	for _, record := range records {
		if latestRecord, exists := urlToLatestRecord[record.Url]; exists && uint(record.Index) != uint(latestRecord.Index) {
			DB.Db.Delete(&record)
			fmt.Printf("Deleted record: %+v\n", record.Index)
		}
	}
}
