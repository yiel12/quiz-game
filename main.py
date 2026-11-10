from quiz import Quiz
from quiz_game import QuizGame, input_number


def add_default_quizzes(game):
    """저장된 파일이 없을 때만 기본 퀴즈 5개 추가"""
    game.add_quiz(Quiz(
        "파이썬에서 리스트를 만들 때 쓰는 기호는?",
        ["( )", "[ ]", "{ }", "< >"], 2))
    game.add_quiz(Quiz(
        "화면에 출력하는 함수는?",
        ["input()", "print()", "len()", "str()"], 2))
    game.add_quiz(Quiz(
        "반복에 사용하는 키워드가 아닌 것은?",
        ["for", "while", "loop", "break"], 3))
    game.add_quiz(Quiz(
        "문자열의 길이를 구하는 함수는?",
        ["len()", "size()", "count()", "length()"], 1))
    game.add_quiz(Quiz(
        "주석을 작성할 때 쓰는 기호는?",
        ["//", "#", "/* */", "--"], 2))


def show_menu():
    """메뉴 화면 출력"""
    print("\n===== 퀴즈 게임 =====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def add_quiz_by_user(game):
    """사용자가 직접 퀴즈 추가"""
    question = input("문제를 입력하세요: ").strip()
    if question == "":                          # 빈 문제 방지
        print("문제가 비어 있어 취소합니다.")
        return
    choices = []
    for i in range(4):
        choice = input(f"{i + 1}번 보기: ")
        choices.append(choice)
    answer = input_number("정답 번호(1~4): ", 1, 4)  # 안전 입력
    game.add_quiz(Quiz(question, choices, answer))
    game.save()                                 # 추가 후 바로 저장!
    print("퀴즈가 추가되었습니다! ✅")


def show_quiz_list(game):
    """등록된 퀴즈 목록 출력"""
    print("\n----- 퀴즈 목록 -----")
    for i, quiz in enumerate(game.quizzes):
        print(f"{i + 1}. {quiz.question}")


def main():
    game = QuizGame()
    game.load()                       # 저장된 데이터 불러오기

    if not game.quizzes:              # 퀴즈가 하나도 없으면
        add_default_quizzes(game)     # 기본 퀴즈 넣기
        game.save()                   # 파일로 저장

    try:                              # Ctrl+C / 입력종료 안전처리
        while True:                   # 메뉴 반복
            show_menu()
            choice = input("선택: ").strip()

            if choice == "1":
                game.run()
                game.save()           # 점수 저장
            elif choice == "2":
                add_quiz_by_user(game)
            elif choice == "3":
                show_quiz_list(game)
            elif choice == "4":
                print(f"\n최고 점수: {game.best_score}점")
            elif choice == "5":
                print("게임을 종료합니다. 안녕히 가세요! 👋")
                break                 # 반복 종료
            else:
                print("1~5 사이의 번호를 입력하세요!")
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 안전하게 종료합니다.")
        game.save()                   # 종료 전 저장!


if __name__ == "__main__":
    main()

    