package main

import (
	"archive/tar"
	"errors"
	"fmt"
	"io"
	"net/http"
)

func main() {
	fmt.Println("server started at :8080")
	http.ListenAndServe(":8080", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		rc := http.NewResponseController(w)
		err := rc.EnableFullDuplex()
		if err != nil {
			fmt.Println("Error enabling full duplex:", err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		defer r.Body.Close()

		fmt.Println("=============================================================")
		fmt.Println("Content-Type:", r.Header.Get("Content-Type"))
		fmt.Println("Transfer-Encoding:", r.Header.Get("Transfer-Encoding"))
		fmt.Println()

		w.Header().Set("Content-Type", "application/x-tar")
		w.WriteHeader(http.StatusOK)

		reader := r.Body

		tr := tar.NewReader(reader)
		tw := tar.NewWriter(w)
		defer tw.Close()
		for {
			h, err := tr.Next()
			if err != nil {
				if errors.Is(err, io.EOF) {
					break
				}
				fmt.Println("Finished reading tar:", err)
				return
			}
			fmt.Printf("Entry: Name=%s, Size=%d\n", h.Name, h.Size)
			fmt.Println("PAX Headers: ", h.PAXRecords)

			err = tw.WriteHeader(h)
			if err != nil {
				fmt.Println("Error writing header:", err)
				return
			}

			size, err := io.Copy(tw, tr)
			if err != nil {
				fmt.Println("Error copying data:", err)
				return
			}
			fmt.Printf("Read %d bytes\n", size)
			fmt.Println()
		}

		fmt.Println("Finished")
		fmt.Println()
		// tw.Close()
	}))
}
