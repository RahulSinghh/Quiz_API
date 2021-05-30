
class Quiz :

    def __init__(self, quid_id, quiz_name, list_questions):
        self.quiz_id = quid_id
        self.quiz_name = quiz_name
        self.list_questions = list_questions

    def __str__(self):
        return str(self.quiz_id)+": "+str(self.quiz_name)

