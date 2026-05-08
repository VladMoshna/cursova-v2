import random

MAX_ATTEMPTS = 7


def load_words_from_file(words):
    try:
        with open(words, 'r') as file:
            words = [word.strip().lower() for word in file.readlines()]
        return words
    except FileNotFoundError:
        print("Файл зі словами не знайдено!")
        return []


def choose_random_word(words_list):
    return random.choice(words_list)


def display_hangman(attempts_left):
    stages = [
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        """,
        """
           -----
           |   |
               |
               |
               |
               |
        """
    ]
    print(stages[MAX_ATTEMPTS - attempts_left])


def save_game_result(result, word, attempts):
    with open("game_history.txt", "a") as file:
        file.write(f"Result: {result}, Word: {word}, Attempts left: {attempts}\n")


def play_game():
    words = load_words_from_file("words.txt")
    if not words:
        return

    secret_word = choose_random_word(words)
    guessed_letters = set()
    correct_letters = set(secret_word)
    attempts_left = MAX_ATTEMPTS

    while attempts_left > 0:
        display_hangman(attempts_left)

        current_state = ""
        for letter in secret_word:
            if letter in guessed_letters:
                current_state += letter + " "
            else:
                current_state += "_ "
        print("Слово:", current_state)

        print("Використані літери:", guessed_letters)

        user_input = input("Введіть літеру або слово: ").lower()

        if len(user_input) > 1:
            if user_input == secret_word:
                print("Ви вгадали слово!")
                save_game_result("Win", secret_word, attempts_left)
                return
            else:
                print("Невірне слово!")
                attempts_left -= 1
                continue

        if user_input in guessed_letters:
            print("Ви вже вводили цю літеру!")
            continue

        guessed_letters.add(user_input)

        if user_input not in correct_letters:
            print("Неправильна літера!")
            attempts_left -= 1
        else:
            print("Правильна літера!")

        if correct_letters.issubset(guessed_letters):
            print("Ви перемогли! Слово:", secret_word)
            save_game_result("Win", secret_word, attempts_left)
            return

    print("Ви програли! Слово було:", secret_word)
    save_game_result("Lose", secret_word, attempts_left)


def show_game_history():
    try:
        with open("game_history.txt", "r") as file:
            print("\nІсторія ігор:")
            print(file.read())
    except FileNotFoundError:
        print("Історія ігор поки відсутня.")


def main_menu():
    while True:
        print("\nГРА ШИБЕНИЦЯ")
        print("1. Почати гру")
        print("2. Переглянути історію ігор")
        print("3. Вийти")

        choice = input("Оберіть пункт: ")

        if choice == "1":
            play_game()
        elif choice == "2":
            show_game_history()
        elif choice == "3":
            print("До побачення!")
            break
        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    main_menu()
