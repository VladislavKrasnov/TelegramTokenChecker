import telebot
import json
import os
from colorama import init, Fore
import sys

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_valid_token(token, username):
    filename = "valid_tokens.json"
    data = []

    if os.path.exists(filename):
        with open(filename, "r") as file:
            data = json.load(file)

    if not any(entry["token"] == token for entry in data):
        data.append({"token": token, "username": username})
        with open(filename, "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(Fore.GREEN + f"Токен и юзернейм сохранены в {filename}")
    else:
        print(Fore.YELLOW + "Токен уже существует в файле.")

def check_token(token, save=True):
    try:
        bot = telebot.TeleBot(token)
        bot_info = bot.get_me()
        username = bot_info.username
        print(Fore.CYAN + f"Юзернейм бота: {username}")
        if save:
            save_valid_token(token, username)
    except Exception as e:
        print(Fore.RED + f"Ошибка: {e}")

def check_tokens_from_file(file_path):
    if not os.path.exists(file_path):
        print(Fore.RED + f"Файл {file_path} не найден.")
        return

    with open(file_path, "r") as file:
        tokens = file.read().splitlines()

    for token in tokens:
        if token.strip():
            print(Fore.BLUE + "\n======= Проверка токена =======")
            check_token(token)

    print(Fore.GREEN + "\n======= Все токены проверены =======")

def main():
    while True:
        clear_screen()
        print(Fore.MAGENTA + "======= Меню =======")
        print(Fore.MAGENTA + "1. Проверка единичного токена")
        print(Fore.MAGENTA + "2. Проверка токенов из файла")
        print(Fore.MAGENTA + "0. Выход")

        choice = input(Fore.YELLOW + "Введите номер режима (1, 2 или 0): ").strip()
        clear_screen()

        if choice == "1":
            token = input(Fore.YELLOW + "Введите токен вашего Telegram-бота: ").strip()
            print(Fore.BLUE + "\n======= Проверка токена =======")
            check_token(token, save=False)
            print(Fore.GREEN + "\n======= Проверка завершена =======")
        elif choice == "2":
            file_path = input(Fore.YELLOW + "Введите путь до файла с токенами: ").strip()
            check_tokens_from_file(file_path)
        elif choice == "0":
            print(Fore.GREEN + "Выход из программы.")
            sys.exit()
        else:
            print(Fore.RED + "Неверный выбор. Попробуйте снова.")

        input(Fore.YELLOW + "\nНажмите Enter, чтобы продолжить...")
        clear_screen()

if __name__ == "__main__":
    main()