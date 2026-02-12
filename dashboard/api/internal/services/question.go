package services

import (
	"qpup.ottomata.online/api/internal/database"
	"qpup.ottomata.online/api/internal/models"
)

type QuestionService struct {
	br *database.Database
}

var QSvc QuestionService

func NewQuestionService(database *database.Database) QuestionService {
	QSvc = QuestionService{
		br: database,
	}
	return QSvc
}

func (qs *QuestionService) AddQuestion(question, answer, author string) error {
	_, err := qs.br.Conn.Exec("INSERT INTO questions(question, answer, author) VALUES (?, ?, ?)", question, answer, author)
	return err
}

func (qs *QuestionService) RetrieveQuestions(from string) ([]models.Question, error) {
	r, err := qs.br.Conn.Query("SELECT * FROM questions")
	if err != nil {
		return nil, err
	}
	defer r.Close()
	var questions = make([]models.Question, 1)
	for r.Next() {
		q := models.Question{
			ID:       0,
			Question: "",
			Answer:   "",
			Author:   "",
		}
		err = r.Scan(&q.ID, &q.Question, &q.Answer, &q.Author)
		if err != nil {
			return nil, err
		}
		questions = append(questions, q)
	}
	err = r.Err()
	if err != nil {
		return nil, err
	}
	return questions, nil
}
