class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):                          # 문제 출력 메서드
        print(self.question)
        for i, choice in enumerate(self.choices):
            print(f"{i + 1}. {choice}")

    def check(self, user_answer):            # 정답 확인 메서드 (4칸!)
        return user_answer == self.answer    # 맞으면 True, 틀리면 False

        