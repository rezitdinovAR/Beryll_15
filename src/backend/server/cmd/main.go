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

	http.HandleFunc("/api/search", SearchForFront)
	http.HandleFunc("/api/upload", UploadForFront)
	http.HandleFunc("/api/metric", SearchForMetric)

	fmt.Println("Server is listening on port 8910...")
	if err := http.ListenAndServe(":8910", corsMiddleware(http.DefaultServeMux)); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}

}

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "http://localhost:5173")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			return
		}

		next.ServeHTTP(w, r)
	})
}
