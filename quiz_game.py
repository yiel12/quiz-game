import json                 # JSON 파일 처리용
import os                   # 임시 파일을 안전하게 교체할 때 사용
import shutil               # 백업 파일 복사에 사용
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
        state_path = "state.json"
        backup_path = "state.json.bak"
        temp_path = "state.json.tmp"

        try:
            # 먼저 임시 파일에 완전히 기록한 뒤 교체해, 저장 도중 원본이
            # 비어 버리는 상황을 줄입니다.
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # 현재 파일을 백업해 두면 다음 저장에서 문제가 생겨도
            # 직전 저장 내용을 복구할 수 있습니다.
            if os.path.exists(state_path):
                shutil.copy2(state_path, backup_path)
            os.replace(temp_path, state_path)
        except OSError as error:
            print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def load(self):
        state_path = "state.json"
        backup_path = "state.json.bak"

        def read_state(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("저장 파일의 형식이 올바르지 않습니다.")
            quizzes = [
                Quiz(q["question"], q["choices"], q["answer"])
                for q in data["quizzes"]
            ]
            for quiz_data in data["quizzes"]:
                if (
                    not isinstance(quiz_data, dict)
                    or not isinstance(quiz_data.get("question"), str)
                    or not isinstance(quiz_data.get("choices"), list)
                    or len(quiz_data["choices"]) != 4
                    or not all(isinstance(choice, str) for choice in quiz_data["choices"])
                    or type(quiz_data.get("answer")) is not int
                    or not 1 <= quiz_data["answer"] <= 4
                ):
                    raise ValueError("퀴즈 데이터의 형식이 올바르지 않습니다.")
            best_score = data.get("best_score", 0)
            if type(best_score) is not int or best_score < 0:
                raise ValueError("최고 점수의 형식이 올바르지 않습니다.")
            return quizzes, best_score

        try:
            self.quizzes, self.best_score = read_state(state_path)
        except FileNotFoundError:
            # 첫 실행이면 main.py에서 기본 퀴즈를 넣습니다.
            return
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            # 현재 파일이 손상되었으면 백업 파일을 먼저 확인합니다.
            try:
                restored_quizzes, restored_score = read_state(backup_path)
                shutil.copy2(backup_path, state_path)
                self.quizzes = restored_quizzes
                self.best_score = restored_score
                print("⚠️ 저장 파일이 손상되어 백업 파일에서 복구했습니다.")
            except FileNotFoundError:
                print("⚠️ 저장 파일과 백업이 없어 기본 데이터로 시작합니다.")
                self.quizzes = []
                self.best_score = 0
            except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError):
                print("⚠️ 저장 파일과 백업이 모두 손상되어 기본 데이터로 시작합니다.")
                self.quizzes = []
                self.best_score = 0
        except OSError as error:
            print(f"⚠️ 저장 파일을 읽지 못했습니다: {error}")
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


