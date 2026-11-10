from quiz import Quiz        # quiz.py의 Quiz 클래스를 가져옴

class QuizGame:
    def __init__(self):
        self.quizzes = []    # 여러 문제를 담을 리스트
        self.score = 0       # 점수
        