package main

import (
	"fmt"
	"io"
	"net/http"

	"github.com/sonh/qs"
)

func main() {
	Ping()
}
func Ping() {
	url := "https://api.datasource.cybotrade.rs/cryptoquant/btc/exchange-flows/reserve"

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Add("accept", "application/json")
	req.Header.Add("X-API-KEY", "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn")

	type Query struct {
		// Type       string `qs:"type"`
		Window     string `qs:"window"`
		Start_time int64  `qs:"start_time,comma"`
		// End_time   int64  `qs:"end_time"`
		Limit int64 `qs:"limit"`
		// Flatten    bool   `qs:"flatten"`
		Exchange string `qs:"exchange"`
	}

	query := &Query{
		// Type:       "exchange",
		Window:     "day",
		Start_time: 1735689600,
		// End_time:   1738368000,
		Limit: 1,
		// Flatten:    true,
		Exchange: "binance",
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
