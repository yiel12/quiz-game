from quiz import Quiz

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0

    def add_quiz(self, quiz):        # 문제 추가 메서드
        self.quizzes.append(quiz)    # 리스트에 문제 하나 추가
        