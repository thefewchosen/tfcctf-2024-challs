package main

import (
	"crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"pngiphy/bot"
)

var port = os.Getenv("PORT")
var imageDir = "static/images/"
var templateDir = "templates/"
var images = []string{"2a2c51b7a7e5bc2d", "6917207b9bcdfe4e", "3e4a0f21b894ec55", "207b9b21b894e2e5"}

func generateRandomName() string {
	b := make([]byte, 8)
	rand.Read(b)
	return fmt.Sprintf("%x", b)
}

func index(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content Type", "text/html")
	http.ServeFile(w, r, templateDir+"index.html")
}

func getImages(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content Type", "application/json")
	json.NewEncoder(w).Encode(images)
}

func uploadImage(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		w.Header().Add("Content Type", "text/html")
		http.ServeFile(w, r, templateDir+"upload.html")
	} else if r.Method == http.MethodPost {
		// Get the file from the request
		file, _, err := r.FormFile("file")
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		defer file.Close()

		// Generate a random name for the new file
		newFileName := generateRandomName()
		images = append(images, newFileName)

		newFile, err := os.Create(imageDir + newFileName)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer newFile.Close()

		// Copy the uploaded file to the new file
		_, err = io.Copy(newFile, file)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// Respond with the new file name
		fmt.Fprint(w, "File uploaded successfully")
	} else {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func reportImage(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		id := r.FormValue("id")
		if id == "" {
			http.Error(w, "Missing id", http.StatusBadRequest)
			return
		}

		// Call the bot
		bot.BotVisit(id)
		fmt.Fprint(w, "Image reported")
	}
}

func main() {
	// initialize a Chrome browser instance on port 4444
	bot.InitChromedriver()

	http.HandleFunc("/", index)
	http.HandleFunc("/upload", uploadImage)
	http.HandleFunc("/uploads", getImages)
	http.HandleFunc("/report", reportImage)

	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Healthcheck
	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "pong")
	})

	log.Println("Listening on port " + port)
	http.ListenAndServe("127.0.0.1:"+port, nil)
}
