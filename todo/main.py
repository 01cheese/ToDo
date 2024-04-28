import os
from prompt_toolkit import prompt
import msvcrt
import paint
import send_message
import pandas as pd
import difflib
import youtube

# For send message, you need special gmail key ex: xxxx xxxx xxxx xxxx
# Copy key to json and write your gmail

file_path = 'text.txt'
undo_file = 'undo_file.txt'
excel_path = 'excel.xlsx'
save_path = r'C:\Users\zelen\Desktop\youtube' # your path for YT-video

helpme = [
    "a         ->   add text",
    "d         ->   delete text",
    "helpme    ->   help with program",
    "u         ->   undo",
    "setting   ->   setting",
    "send      ->   send mail",
    "excel     ->   create excel",
    "paint     ->   open paint",
    "*X        ->   *num for change",
    "s         ->   search at word",
    "date      ->   open calendar"
    "exit      ->   exit program",
    "just paste link YT for download mp4 in 720p"
]

setting_items = ["Notifications", "Autorun", "T9", "Email", "Exit"]


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def shortening_text():
    clear_console()
    with open(file_path, 'r') as file:
        lines = file.readlines()

    print(lines[0].replace('\n', ''))
    print(lines[1].replace('\n', ''))
    print('...')
    print(lines[-2].replace('\n', ''))
    print(lines[-1].replace('\n', ''))


def count_lines():
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return len(lines)


def print_menu(menu_items, selected_index):
    os.system('cls')
    shortening_text()
    print('=====================')
    for index, item in enumerate(menu_items):
        if index == selected_index:
            print(f"> {item}")
        else:
            print(f"  {item}")


def notifications():
    print("Notifications")


def t9():
    print("T9")


def setting():
    selected_index = 0
    while True:
        print_menu(setting_items, selected_index)

        key = msvcrt.getch()
        if key == b'\xe0':  # обработка специальных клавиш, таких как стрелки
            key = msvcrt.getch()
            if key == b'H':  # стрелка вверх
                selected_index = (selected_index - 1) % len(setting_items)
            elif key == b'P':  # стрелка вниз
                selected_index = (selected_index + 1) % len(setting_items)
        elif key == b'\r':  # Enter
            if setting_items[selected_index] == "Exit":
                print("Exit the program.")
                break
            elif setting_items[selected_index] == 'Notifications':
                notifications()
            elif setting_items[selected_index] == 'Autorun':
                pass
            elif setting_items[selected_index] == 'T9':
                t9()
            elif setting_items[selected_index] == 'Email':
                send_message.main()


def add_text(text):
    with open(file_path, 'a') as file:
        file.write(f"{count_lines() + 1}. {text}\n")


def delete_line(line_number):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        print("No text.")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'r') as file:
        content = file.read()

    with open(undo_file, 'w') as f:
        f.write(content)

    if line_number < 1 or line_number > len(lines):
        print(f"Lines with number {line_number} does not exist.")
        return

    del lines[line_number - 1]

    with open(file_path, 'w') as file:
        for index, line in enumerate(lines, 1):
            file.write(f"{index}. {line.split('. ', 1)[1]}")

    print(f"Line with number {line_number} successfully removed from the file.")


def change_text(action):
    start_index = action.find('*') + 1
    number = int(action[start_index:])

    with open('text.txt', 'r') as file:
        lines = file.readlines()

    # Проверяем, что номер строки в допустимом диапазоне
    if 1 <= number <= len(lines):
        # Запрашиваем новый текст строки
        my_line = lines[number - 1]
        index = my_line.find('.') + 2
        index_my_line = my_line[:index]
        my_line_without_index = my_line[index:]

        edited_string = prompt(f"Editing a line -> ", default=my_line_without_index.replace('\n', ''))

        new_line = index_my_line + format(edited_string)

        # Обновляем строку в списке
        lines[number - 1] = new_line + '\n'

        # Открываем файл для записи
        with open('text.txt', 'w') as file:
            # Записываем обновленные строки обратно в файл
            file.writelines(lines)

        print("The row was successfully updated.")
    else:
        print("Invalid line number.")


def print_text():
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        print("Hi, no posts yet. You can write helpme)")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        print(line.strip())


def txt_to_excel(txt_file, excel_file):
    # Чтение данных из текстового файла
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    # Создание DataFrame из списка строк
    df = pd.DataFrame(lines, columns=['Your List'])

    # Сохранение данных в Excel файл
    df.to_excel(excel_file, index=False)


def find_similar_words_in_lines(word):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    count = 0
    for line_number, line in enumerate(lines, 1):
        words = line.strip().split()
        matches = difflib.get_close_matches(word, words)

        if matches:
            print(line.strip())
        else:
            count += 1
    if count == len(lines):
        print('No similarities found')


def deadline_text(action):
    start_index = action.find('date') + 4
    number = int(action[start_index:])

    with open('text.txt', 'r') as file:
        lines = file.readlines()

    # Проверяем, что номер строки в допустимом диапазоне
    if 1 <= number <= len(lines):
        # Запрашиваем новый текст строки
        my_line = lines[number - 1]
        index = my_line.find('.') + 2
        index_my_line = my_line[:index]
        my_line_without_index = my_line[index:]

        edited_string = prompt(f"Editing a line -> ", default=my_line_without_index.replace('\n', ''))

        new_line = index_my_line + format(edited_string)

        # Обновляем строку в списке
        lines[number - 1] = new_line + '\n'

        # Открываем файл для записи
        with open('text.txt', 'w') as file:
            # Записываем обновленные строки обратно в файл
            file.writelines(lines)

        print("The row was successfully updated.")
    else:
        print("Invalid line number.")


def undo():
    with open(undo_file, 'r') as f:
        content = f.read()

    # Запись содержимого в файл копии
    with open(file_path, 'w') as f:
        f.write(content)


def base():
    print_text()
    action = input('Action: ')

    if action == 'a':
        shortening_text()
        add_text(input('Write your text: '))
    elif action == "d":
        delete_line(int(input('Why number line delete? ')))
    elif action == "u":
        shortening_text()
        undo()
    elif '//yout' in action:
        shortening_text()
        youtube.download_video(action, save_path, resolution='720p')
        input()
    elif action == 'helpme':
        shortening_text()
        for line in helpme:
            print(line.strip())
        input()

    elif '*' in action:
        change_text(action)
    elif action == 'setting':
        shortening_text()
        setting()
    elif action == 'send':
        shortening_text()
        what_send = input("What do you want to send? (lst/mes): ")
        if what_send == 'lst':
            with open(file_path, 'r') as file:
                lines = file.readlines()

            lines = [email.strip() for email in lines]
            lines = "\n".join(lines)
            send_message.send_email(lines)
            print('List sent')
            input()
        elif what_send == 'mes':
            message_text = input('Enter text to send: ')
            send_message.send_email(message_text)
            print('Text sent')
            input()
    elif action == 'excel':
        shortening_text()
        txt_to_excel(file_path, excel_path)
        print("The file was successfully converted")
        input()
    elif action == 'paint':
        shortening_text()
        paint.main()
    elif action == 's':
        shortening_text()
        word = input("Write the word to search: ")
        find_similar_words_in_lines(word)
        input()
    elif 'date' in action:
        shortening_text()
        deadline_text(action)
        input()
    elif action == 'exit':
        clear_console()
        exit()
    else:
        pass


if __name__ == "__main__":
    while True:
        clear_console()
        base()
