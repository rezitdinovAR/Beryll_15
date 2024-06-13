package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/jackc/pgx/v4/pgxpool"
)

var dbpool *pgxpool.Pool

type RequestData struct {
	URL   string `json:"url"`
	Index int    `json:"index"`
}

func main() {
	// Подключение к базе данных
	databaseUrl := "postgres://postgres:postgres@localhost:5432/yappy"
	var err error
	dbpool, err = pgxpool.Connect(context.Background(), databaseUrl)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v\n", err)
	}
	defer dbpool.Close()

	http.HandleFunc("/api/listen", handleGetUrl)
	fmt.Println("Server is listening on port 8667...")
	log.Fatal(http.ListenAndServe(":8667", nil))
	fmt.Println("hi")
	time.Sleep(1 * time.Second)
}

func handleGetUrl(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	var data RequestData
	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		http.Error(w, "Failed to decode JSON body", http.StatusBadRequest)
		return
	}

	receivedAt := time.Now()

	// Вставка данных в базу данных
	_, err = dbpool.Exec(context.Background(), "INSERT INTO videos (url, received_at, idx) VALUES ($1, $2, $3)", data.URL, receivedAt, data.Index)
	if err != nil {
		http.Error(w, "Failed to insert data", http.StatusInternalServerError)
		log.Printf("Failed to insert data: %v\n", err)
		return
	}

	fmt.Fprintf(w, "Data inserted successfully")
}

