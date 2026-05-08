import random
from art import tprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.prompt import Prompt
from rich.theme import Theme


custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green"
})

console = Console(theme=custom_theme)
MAX_ATTEMPTS = 7

def load_words_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = [word.strip().lower() for word in file.readlines() if word.strip()]
        return words
    except FileNotFoundError:
        return []

def save_game_result(result, word, attempts):
    with open("game_history.txt", "a", encoding="utf-8") as file:
        file.write(f"Результат: {result}, Слово: {word}, Спроб залишилось: {attempts}\n")

def get_hangman_stage(attempts_left):
    stages = [
        "[danger]  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |[/]",
        "[danger]  +---+\n  |   |\n  O   |\n /|\\  |\n /    |[/]",
        "[warning]  +---+\n  |   |\n  O   |\n /|\\  |\n      |[/]",
        "[warning]  +---+\n  |   |\n  O   |\n /|   |\n      |[/]",
        "[yellow]  +---+\n  |   |\n  O   |\n  |   |\n      |[/]",
        "[yellow]  +---+\n  |   |\n  O   |\n      |\n      |[/]",
        "[green]  +---+\n  |   |\n      |\n      |\n      |[/]",
        "[bold green]  +---+\n      |\n      |\n      |\n      |[/]"
    ]
    return stages[attempts_left]

def display_game_screen(attempts_left, secret_word, guessed_letters):
    word_display = " ".join([f"[bold yellow]{l}[/]" if l in guessed_letters else "[white]_[/]" for l in secret_word])
    
    hangman_panel = Panel(get_hangman_stage(attempts_left), title="Статус", border_style="bright_blue")
    
    info_content = (
        f"\n[cyan]СЛОВО:[/] {word_display}\n\n"
        f"[magenta]ВИКОРИСТАНІ ЛІТЕРИ:[/] {', '.join(sorted(guessed_letters)) if guessed_letters else '---'}"
    )
    info_panel = Panel(info_content, title=f"Спроб: {attempts_left}", border_style="bright_blue")
    
    console.print(Columns([hangman_panel, info_panel]))

def play_game():
    words = load_words_from_file("words.txt")
    if not words:
        console.print(Panel("[danger]Файл 'words.txt' не знайдено або він порожній![/]"))
        return

    secret_word = random.choice(words)
    guessed_letters = set()
    correct_letters = set(secret_word)
    attempts_left = MAX_ATTEMPTS

    while attempts_left > 0:
        console.clear()
        tprint("SHYBENYTSYA", font="small")
        display_game_screen(attempts_left, secret_word, guessed_letters)

        user_input = Prompt.ask("\n[bold cyan]Введіть літеру або слово[/]").lower().strip()

        if not user_input:
            continue

        if len(user_input) > 1:
            if user_input == secret_word:
                break
            else:
                console.print("[danger]Неправильне слово![/]")
                attempts_left -= 1
                import time; time.sleep(1)
                continue

        if user_input in guessed_letters:
            console.print("[warning]Ви вже вводили цю літеру![/]")
            import time; time.sleep(1)
            continue

        guessed_letters.add(user_input)

        if user_input not in correct_letters:
            attempts_left -= 1
        
        if correct_letters.issubset(guessed_letters):
            break

    console.clear()
    if attempts_left > 0 or (locals().get('user_input') == secret_word):
        tprint("YOU WIN!", font="bulbhead")
        console.print(Panel(f"[success]ПЕРЕМОГА![/] Загадане слово: [bold yellow]{secret_word}[/]", expand=False))
        save_game_result("Перемога", secret_word, attempts_left)
    else:
        tprint("GAME OVER", font="bulbhead")
        console.print(Panel(f"[danger]ПРОГРАШ![/] Було загадано: [bold yellow]{secret_word}[/]", expand=False))
        save_game_result("Програш", secret_word, attempts_left)
    
    Prompt.ask("\nНатисніть [bold]Enter[/], щоб вийти в меню")

def show_game_history():
    console.clear()
    tprint("HISTORY", font="small")
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Результат", width=15)
    table.add_column("Слово", style="yellow")
    table.add_column("Спроби", justify="center")

    try:
        with open("game_history.txt", "r", encoding="utf-8") as file:
            for line in file:
                if "Результат:" in line:
                    parts = line.strip().split(", ")
                    res = parts[0].split(": ")[1]
                    word = parts[1].split(": ")[1]
                    att = parts[2].split(": ")[1]
                    
                    style = "green" if res == "Перемога" else "red"
                    table.add_row(f"[{style}]{res}[/]", word, att)
        console.print(table)
    except (FileNotFoundError, IndexError):
        console.print("[yellow]Історія ігор поки порожня.[/]")
    
    Prompt.ask("\nНатисніть [bold]Enter[/], щоб повернутися")

def main_menu():
    while True:
        console.clear()
        tprint("SHYBENYTSYA", font="block")
        
        menu_text = (
            "1. [bold green]Почати нову гру[/]\n"
            "2. [bold blue]Переглянути історію[/]\n"
            "3. [bold red]Вихід[/]"
        )
        console.print(Panel(menu_text, title="ГОЛОВНЕ МЕНЮ", subtitle="v2.0", expand=False))

        choice = Prompt.ask("Оберіть пункт", choices=["1", "2", "3"], default="1")

        if choice == "1":
            play_game()
        elif choice == "2":
            show_game_history()
        elif choice == "3":
            console.print("[bold yellow]До побачення![/]")
            break

if __name__ == "__main__":
    main_menu()
