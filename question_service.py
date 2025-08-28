from sqlite_repo import QuestionRepo, QuestionSourceRepo, SessionQuestionRepo


class QuestionService:
    def __init__(
        self,
        q_repository: QuestionRepo,
        qsrc_repository: QuestionSourceRepo,
        qsess_repository: SessionQuestionRepo,
    ):
        self.q_repo = q_repository
        self.qsrc_repo = qsrc_repository
        self.qsess_repo = qsess_repository

    def generate_all_for_session(self, session_id: int):
        qsrc_entries = self.qsrc_repo.fetch_many({})
        for entry in qsrc_entries:
            question_entry = self.q_repo.create(entry.id)
            self.qsess_repo.create(session_id, question_entry.id)
            
