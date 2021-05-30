from flask import Flask
from flask import request, jsonify
from Question import Question
from Quiz import Quiz
from Database import Database
from QuizUtility import QuizUtility
from User import User
app = Flask(__name__)


db = Database()
utility = QuizUtility()

@app.route('/create_questions', methods = ['POST'])
def createQuestion():
    questionJson = request.get_json()
    questions = questionJson['Questions']

    for question in questions:
        id = question.get('Id')
        question_description = question.get('question')
        options = question.get('options')
        correct_answer = question.get('correct_answer')
        q = Question(id, question_description , options, correct_answer)
        db.map_question_id[id] = q

    return "Questions Added Successfully"


@app.route('/create_quiz', methods = ['POST'])
def createQuiz():
    quizJson = request.get_json()
    quizes = quizJson['Quizes']

    for quiz in quizes:
        quid_id = quiz.get('Id')
        quiz_name = quiz.get('Name')
        quiz_questions = quiz.get('Questions_id')
        list_questions = []
        for quid in quiz_questions:
            q1 = db.map_question_id.get(quid)
            list_questions.append(q1)

        q = Quiz(quid_id, quiz_name, list_questions)
        db.map_quiz_id[quid_id] = q
        db.list_quiz.append(q)

    return "QUiz create successfully"


@app.route('/create_answer/<int:question_id>',methods = ['POST'])
def createAnswer(question_id):
    answerJson = request.get_json()
    answers = answerJson['Questions']

    for answer in answers:
        question_id = answer.get('question_id')
        options = answer.get('options')
        if question_id in db.map_question_id.keys():
            question = db.map_question_id.get(question_id)
            question.options = options
        else:
            return "Quesion_id: "+question_id+" does not exist";

    return "All questions updated with the provided Options"

@app.route('/getAllQuiz/<int:page>', methods = ['GET'])
def getAllQuiz(page):
    quiz = utility.getQuizByPage(db, page)
    answer = []
    for q in quiz:
        answer.append(str(q))
    return jsonify({"Quiz": answer}), 200


@app.route('/getResponse', methods = ['POST'])
def submitResponse():
    responses = request.get_json()
    responses = responses["Users"]

    for response in responses:
        userId = response.get("userId")
        quiz_id = response.get("quiz_id")
        question_id = response.get("question_id")
        answer = response.get("answer")
        reponse = utility.getResponse(db, response.get("question_id"), response.get("answer"))

        user = User(userId)
        user.quiz_Id = quiz_id
        user.question_id = question_id
        user.answer = answer
        db.map_user[userId] = user

    return "User response Noted!!"

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug =True)
