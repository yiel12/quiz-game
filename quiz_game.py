from quiz import Quiz

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def show_result(self):                      # 결과 출력 메서드
        total = len(self.quizzes)               # 전체 문제 수
        print("===== 게임 종료 =====")
        print(f"총 {total}문제 중 {self.score}개 정답!")
        print(f"점수: {self.score}/{total}")

    def run(self):                          # 게임 실행 메서드
        for quiz in self.quizzes:           # 문제를 하나씩 꺼냄
            quiz.show()                     # 문제 출력
            answer = int(input("정답 번호: "))   # 사용자 입력 받기
            if quiz.check(answer):          # 정답 확인
                print("정답입니다! ⭕\n")
                self.score += 1             # 점수 +1
            else:
                print("틀렸습니다! ❌\n")
        self.show_result()                  # ⬅️ 게임 끝나면 결과 출력!
        