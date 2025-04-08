package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/aiyyra/umh/api"
	"github.com/sonh/qs"
)

func main() {
	Ping()
	test := api.Reserve()
	// print(test)

	jsonData := test

	var data map[string]interface{}
	err := json.Unmarshal([]byte(jsonData), &data)
	if err != nil {
		fmt.Printf("could not unmarshal json: %s\n", err)
		return
	}

	// fmt.Printf("json map: %v\n", data)
	// os.WriteFile("big_marhsall.json", []byte(test), os.ModePerm)
}

func Ping() {
	url := "https://api.datasource.cybotrade.rs/cryptoquant/btc/exchange-flows/reserve"
	url = "https://api.datasource.cybotrade.rs/cryptoquant/btc/status/entity-list"

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Add("accept", "application/json")
	req.Header.Add("X-API-KEY", "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn")

	type Query struct {
		Type string `qs:"type"`
		// Window string `qs:"window"`
		// From       string `qs:"from"`
		// To         string `qs:"to"`
		Start_time int64 `qs:"start_time"`
		End_time   int64 `qs:"end_time"`
		Limit      int64 `qs:"limit"`
		// Flatten    bool   `qs:"flatten"`
		// Exchange string `qs:"exchange"`
	}

	query := &Query{
		Type: "exchange",
		// Window: "day",
		// From:       "20191003T220000",
		// To:         "20191004T220000",
		Start_time: 1735689600,
		End_time:   1738368000,
		Limit:      1,
		// Flatten:    true,
		// Exchange: "binance",
	}

	encoder := qs.NewEncoder()
	values, err := encoder.Values(query)
	if err != nil {
		// Handle error
		fmt.Println(err)
	}

	req.URL.RawQuery = values.Encode()

	// print(req.URL.RawQuery)

	res, _ := http.DefaultClient.Do(req)
	defer res.Body.Close()

	body, _ := io.ReadAll(res.Body)

	// fmt.Println(res)
	fmt.Println(string(body))

}
