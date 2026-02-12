package database

import (
	"database/sql"
	"errors"
	"fmt"
	"os"

	_ "github.com/mattn/go-sqlite3"
)

type Database struct {
	Conn *sql.DB
}

func NewConnection(filename string) (*Database, error) {
	dbase := &Database{
		Conn: nil,
	}
	var err error
	_, err = os.Stat(filename)
	firstTime := false
	if err != nil && errors.Is(err, os.ErrNotExist) {
		_, err = os.Create(filename)
		if err != nil {
			return nil, fmt.Errorf("while creating new file: %s", err.Error())
		}
		firstTime = true
	}
	dbase.Conn, err = sql.Open("sqlite3", filename)
	if err != nil {
		return nil, err
	}
	if firstTime {
		initMig, err := os.ReadFile("migrations/init.sql")
		if err != nil {
			return nil, fmt.Errorf("while applying initialization migration: %s", err.Error())
		}
		if _, err := dbase.Conn.Exec(string(initMig)); err != nil {
			return nil, fmt.Errorf("while applying initialization migration: %s", err.Error())
		}
	}
	return dbase, nil
}
