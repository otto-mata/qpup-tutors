package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/markbates/goth/gothic"
)

func GetUser(w http.ResponseWriter, r *http.Request) {
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

	// Return user data
	userData := map[string]any{
		"id":       session.Values["user_id"],
		"login":    session.Values["login"],
		"name":     session.Values["name"],
		"provider": session.Values["provider"],
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(userData)
}
