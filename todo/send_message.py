import smtplib
from email.mime.text import MIMEText
import json
import re
import os


def save_email_to_json(email):
    with open('emails.json', 'r+') as file:
        data = json.load(file)

        # Удаление данных из списка "emails"
        data["emails"] = []

        # Перемотка файла к началу перед записью
        file.seek(0)

        # Запись измененных данных обратно в файл
        json.dump(data, file, indent=4)

        # Обрезка файла до новой длины (если новый контент короче предыдущего)
        file.truncate()

    with open('emails.json', 'r+') as file:
        data = json.load(file)
        data['emails'].append(email)
        file.seek(0)
        json.dump(data, file, indent=4)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_emails_from_json():
    if os.path.exists('emails.json') and os.path.getsize('emails.json') > 0:
        with open('emails.json', 'r') as file:
            data = json.load(file)
            return data['emails']
    return []


def main():
    email = input("Введите вашу электронную почту: ").strip()

    if email == '':
        emails = get_emails_from_json()
        if emails:
            print(f"Электронная почта по умолчанию: {emails[0]}")
        else:
            print("Добавьте свою почту")
        return

    # Добавляем домен, если он отсутствует
    if '@' not in email:
        email = email + '@gmail.com'

    if is_valid_email(email):
        save_email_to_json(email)
        print(f"Электронная почта {email} успешно сохранена в файле emails.json")
    else:
        print("Некорректный формат электронной почты. Попробуйте снова.")


def send_email(message):
    with open('emails.json', 'r') as file:
        data = json.load(file)
        email_address = data["emails"][0]
        app_password = data["key_email"][0]

    # Создание сообщения
    msg = MIMEText(message)
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = 'SMS via Email'

    # Определите адрес SMTP-сервера вашего почтового провайдера
    smtp_server = 'smtp.gmail.com'  # для Gmail
    smtp_port = 587

    # Отправка сообщения
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, app_password)
        server.send_message(msg)


# time.sleep(5)
# print('Start')
# for i in range(100):
#     if i%10==0:
#         print(f"{i}%")
#     send_email(str(i))
# print('Finish')
