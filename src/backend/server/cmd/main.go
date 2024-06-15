package main

import (
	"fmt"
	"net/http"
	"time"
)

func main() {
	time.Sleep(10 * time.Second)
	ConnectDb()
	go SendFromCsv()

	http.HandleFunc("/api/search", SearchForFront)
	http.HandleFunc("/api/upload", UploadForFront)
	http.HandleFunc("/api/metric", SearchForMetric)

	fmt.Println("Server is listening on port 8910...")
	if err := http.ListenAndServe(":8910", nil); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}

}
