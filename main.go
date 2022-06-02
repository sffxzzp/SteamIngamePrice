package main

import (
	"io"
	"net/http"
	"os"
)

func httpGet(url string) ([]byte, bool) {
	resp, err := http.Get(url)
	if err != nil {
		return nil, true
	}
	defer resp.Body.Close()
	if resp.StatusCode == 200 {
		data, _ := io.ReadAll(resp.Body)
		return data, false
	} else {
		return nil, true
	}
}

func Handler(w http.ResponseWriter, r *http.Request) {
	appid := "730"
	apikey := os.Getenv("apikey")
	// apikey := "<apikey>"
	mod := r.URL.Query().Get("mod")
	var data []byte
	var err bool
	if mod == "schema" {
		data, err = httpGet("https://api.steampowered.com/IEconItems_" + appid + "/GetSchema/v2/?language=zh-CN&key=" + apikey)
	} else if mod == "price" {
		data, err = httpGet("https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?language=zh-CN&appid=" + appid + "&key=" + apikey)
	} else {
		w.WriteHeader(400)
		w.Write([]byte("Invalid mod"))
		return
	}
	if err {
		w.WriteHeader(500)
		w.Write([]byte("Network error"))
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Cache-Control", "public, max-age=14400, s-maxage=14400, stale-while-revalidate=14400")
	w.Write(data)
}

func main() {
	println("Listening on http://localhost:8080")
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/", fs)
	http.HandleFunc("/api/", Handler)
	http.ListenAndServe("127.0.0.1:8080", nil)
}

// http://127.0.0.1:8080/

// https://api.steampowered.com/IEconItems_730/GetSchema/v2/?key=<apikey>
// https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v1/?appid=730&key=<apikey>
