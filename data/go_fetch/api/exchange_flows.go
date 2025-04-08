package api

import (
	"fmt"
	"io"
	"net/http"

	"github.com/sonh/qs"
)

func Reserve() string {
	url := "https://api.datasource.cybotrade.rs/cryptoquant/btc/exchange-flows/reserve"

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Add("accept", "application/json")
	req.Header.Add("X-API-KEY", "iheM86n8mn8vC3vjOE444vlVTP5sTuBb71FJuVKQc5UqdIBn")

	type Query struct {
		Exchange string `qs:"exchange"`
		Window   string `qs:"window"`
		// From     string `qs:"from"`
		// To       string `qs:"to"`
		// Start_time int64  `qs:"start_time,comma"`
		// End_time   int64  `qs:"end_time"`
		Limit int64 `qs:"limit"`
		// Flatten    bool   `qs:"flatten"`
	}

	query := &Query{
		Exchange: "all_exchange",
		Window:   "day",
		// From:     "20191003",
		// To:       "20191004T220000",
		// Start_time: 1735689600,
		// End_time:   1738368000,
		Limit: 20,
		// Flatten:    true,
	}

	encoder := qs.NewEncoder()
	values, err := encoder.Values(query)
	if err != nil {
		// Handle error
		fmt.Println(err)
	}

	req.URL.RawQuery = values.Encode()

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		println(err)
	}

	defer res.Body.Close()

	body, _ := io.ReadAll(res.Body)

	return string(body)
}
