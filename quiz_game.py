import json                 # JSON 파일 처리용
from quiz import Quiz


def input_number(prompt, min_num, max_num):
    """min_num ~ max_num 범위의 숫자만 받는 안전한 입력 함수"""
    while True:
        text = input(prompt).strip()        # 앞뒤 공백 제거
        if text == "":                      # 빈 입력(그냥 Enter)
            print("입력이 없습니다. 다시 입력하세요.")
            continue
        if not text.isdigit():              # 숫자가 아님 (abc 등)
            print("숫자만 입력하세요.")
            continue
        num = int(text)
        if num < min_num or num > max_num:  # 범위 밖
            print(f"{min_num}~{max_num} 사이로 입력하세요.")
            continue
        return num                          # 통과하면 반환


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.best_score = 0

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def save(self):
        data = {
            "quizzes": [
                {"question": q.question, "choices": q.choices, "answer": q.answer}
                for q in self.quizzes
            ],
            "best_score": self.best_score
        }
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [
                Quiz(q["question"], q["choices"], q["answer"])
                for q in data["quizzes"]
            ]
            self.best_score = data.get("best_score", 0)
        except FileNotFoundError:
            pass                                    # 첫 실행 → 기본 데이터 사용
        except (json.JSONDecodeError, KeyError):    # 파일 손상 처리
            print("⚠️ 저장 파일이 손상되어 기본 데이터로 시작합니다.")
            self.quizzes = []
            self.best_score = 0

    def show_result(self):
        total = len(self.quizzes)
        print("===== 게임 종료 =====")
        print(f"총 {total}문제 중 {self.score}개 정답!")
        print(f"점수: {self.score}/{total}")

    def run(self):
        if not self.quizzes:                # 퀴즈 없을 때 처리
            print("풀 수 있는 퀴즈가 없습니다.")
            return
        self.score = 0                      # 게임 시작할 때 점수 초기화
        for quiz in self.quizzes:
            quiz.show()
            answer = input_number("정답 번호(1~4): ", 1, 4)  # 안전 입력
            if quiz.check(answer):
                print("정답입니다! ⭕\n")
                self.score += 1
            else:
                print("틀렸습니다! ❌\n")
        if self.score > self.best_score:    # 최고 점수 갱신
            self.best_score = self.score
        self.show_result()

        