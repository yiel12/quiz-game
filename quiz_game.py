import json                 # JSON 파일 처리용
from quiz import Quiz

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.best_score = 0          # ⬅️ 최고 점수 추가됨!

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def save(self):                  # ⬅️ 저장 메서드 추가됨!
        data = {
            "quizzes": [
                {"question": q.question, "choices": q.choices, "answer": q.answer}
                for q in self.quizzes
            ],
            "best_score": self.best_score
        }
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):                  # ⬅️ 불러오기 메서드 추가됨!
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [
                Quiz(q["question"], q["choices"], q["answer"])
                for q in data["quizzes"]
            ]
            self.best_score = data.get("best_score", 0)
        except FileNotFoundError:
            pass                     # 파일 없으면 넘어감 (첫 실행)

    def show_result(self):
        total = len(self.quizzes)
        print("===== 게임 종료 =====")
        print(f"총 {total}문제 중 {self.score}개 정답!")
        print(f"점수: {self.score}/{total}")

    def run(self):
        self.score = 0               # ⬅️ 게임 시작할 때 점수 초기화
        for quiz in self.quizzes:
            quiz.show()
            answer = int(input("정답 번호: "))
            if quiz.check(answer):
                print("정답입니다! ⭕\n")
                self.score += 1
            else:
                print("틀렸습니다! ❌\n")
        if self.score > self.best_score:    # ⬅️ 최고 점수 갱신
            self.best_score = self.score
        self.show_result()

        