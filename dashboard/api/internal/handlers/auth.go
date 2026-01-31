package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/markbates/goth/gothic"
)

func Callback(w http.ResponseWriter, r *http.Request) {
	user, err := gothic.CompleteUserAuth(w, r)
	if err != nil {
		fmt.Fprintln(w, err)
		return
	}
	session, err := gothic.Store.Get(r, "auth-session")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	session.Values["user_id"] = user.UserID
	session.Values["name"] = user.Name
	session.Values["provider"] = user.Provider
	session.Values["access_token"] = user.AccessToken
	err = session.Save(r, w)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	http.Redirect(w, r, "http://localhost:8080/dashboard", http.StatusFound)
}

func Begin(w http.ResponseWriter, r *http.Request) {
	// try to get the user without re-authenticating
	if gothUser, err := gothic.CompleteUserAuth(w, r); err == nil {
		w.Write([]byte(gothUser.NickName))
	} else {
		gothic.BeginAuthHandler(w, r)
	}
}

func Logout(w http.ResponseWriter, r *http.Request) {
	session, err := gothic.Store.Get(r, "auth-session")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Clear session
	session.Values = make(map[interface{}]interface{})
	session.Options.MaxAge = -1

	err = session.Save(r, w)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]string{"message": "Logged out successfully"})
}
