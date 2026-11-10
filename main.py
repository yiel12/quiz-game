from quiz import Quiz
from quiz_game import QuizGame

def main():
    game = QuizGame()        # 게임 객체 생성

    # 문제 만들기 (문제, 보기리스트, 정답번호)
    game.add_quiz(Quiz(
        "파이썬에서 리스트를 만들 때 쓰는 기호는?",
        ["( )", "[ ]", "{ }", "< >"],
        2
    ))
    game.add_quiz(Quiz(
        "화면에 출력하는 함수는?",
        ["input()", "print()", "len()", "str()"],
        2
    ))

    game.run()               # 게임 시작!

if __name__ == "__main__":
    main()
    