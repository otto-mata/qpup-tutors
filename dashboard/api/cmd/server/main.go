package main

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/gorilla/sessions"
	"github.com/joho/godotenv"
	"github.com/markbates/goth"
	"github.com/markbates/goth/gothic"
	"qpup.ottomata.online/api/auth/internal/auth"
	"qpup.ottomata.online/api/auth/internal/handlers"
	"qpup.ottomata.online/api/auth/internal/middleware"
)

type AuthResponse struct {
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	ExpiresIn    int    `json:"expires_in"`
	RefreshToken string `json:"refresh_token"`
	Scope        string `json:"scope"`
	CreatedAt    int    `json:"created_at"`
	ValidUntil   int    `json:"secret_valid_until"`
}

func main() {
	err := godotenv.Load()

	if err != nil {
		log.Fatalf("An error occurred while loading .en file: %s\n", err.Error())
	}

	store := sessions.NewCookieStore([]byte(os.Getenv("SESSION_SECRET")))
	store.Options = &sessions.Options{
		Path:     "/",
		MaxAge:   86400 * 7, // 7 days
		HttpOnly: true,      // Prevents JavaScript access
		Secure:   false,     // Set to true in production with HTTPS
	}
	gothic.Store = store

	r := mux.NewRouter()
	r.Use(middleware.Cors)
	r.Use(middleware.Log)
	goth.UseProviders(auth.New(os.Getenv("FT_UID"), os.Getenv("FT_SECRET"), os.Getenv("FT_REDIR")))
	r.HandleFunc("/auth/{provider}/callback", handlers.Callback).Methods("Get")
	r.HandleFunc("/auth/{provider}", handlers.Begin).Methods("Get")
	r.HandleFunc("/api/user", handlers.GetUser).Methods("GET")
	r.HandleFunc("/api/logout", handlers.Logout).Methods("POST")
	http.ListenAndServe(":3000", r)
}
