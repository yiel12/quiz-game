from quiz import Quiz

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def run(self):                          # 게임 실행 메서드
        for quiz in self.quizzes:           # 문제를 하나씩 꺼냄
            quiz.show()                     # 문제 출력
            answer = int(input("정답 번호: "))   # 사용자 입력 받기
            if quiz.check(answer):          # 정답 확인
                print("정답입니다! ⭕\n")
                self.score += 1             # 점수 +1
            else:
                print("틀렸습니다! ❌\n")

                