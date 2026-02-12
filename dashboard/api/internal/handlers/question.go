package handlers

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/markbates/goth/gothic"
	"qpup.ottomata.online/api/internal/services"
)

func NewQuestion(w http.ResponseWriter, r *http.Request) {
	session, err := gothic.Store.Get(r, "auth-session")
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Check if user is authenticated
	userID, ok := session.Values["user_id"]
	if !ok || userID == nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	var rcvd struct {
		Question string `json:"question"`
		Answer   string `json:"answer"`
	}
	userData := map[string]any{
		"id":       session.Values["user_id"],
		"name":     session.Values["name"],
		"provider": session.Values["provider"],
	}
	json.NewDecoder(r.Body).Decode(&rcvd)
	err = services.QSvc.AddQuestion(rcvd.Question, rcvd.Answer, userData["name"].(string))
	if err != nil {
		log.Println("Error while adding question: ", err)
		w.WriteHeader(http.StatusInternalServerError)
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]bool{
		"success": true,
	})
}

func GetQuestions(w http.ResponseWriter, r *http.Request) {
	session, err := gothic.Store.Get(r, "auth-session")
	if err != nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// Check if user is authenticated
	userID, ok := session.Values["user_id"]
	if !ok || userID == nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}
	q, err := services.QSvc.RetrieveQuestions("*")
	if err != nil {
		log.Println(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(q)

}
