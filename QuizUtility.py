from Database import Database

class QuizUtility:

    def startQuiz(self, db, quizId):
        quiz = db.map_quiz_id.get(quizId)
        return quiz.list_questions

    def getResponse(self, db, question_id, answer):
        question = db.map_question_id.get(question_id)
        if answer == question.correct_answer:
            return True
        else:
            return False

    def getQuizByPage(self, db, page):
        page_size = 1

        start  = page* page_size
        end    = page* page_size + page_size
        return db.list_quiz[start:end]

