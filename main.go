package main

import (
	"io"
	"net/http"
)

type ()

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
	// todo
}

func main() {
	http.HandleFunc("/", Handler)
	http.ListenAndServe("127.0.0.1:8080", nil)
}

// https://api.steampowered.com/IEconItems_730/GetSchema/v0002/?key=<apikey>
// https://api.steampowered.com/ISteamEconomy/GetAssetPrices/v0001/?appid=730&class_name0=def_index&class_value0=4842&key=<apikey>
