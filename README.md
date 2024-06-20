Reminder WhatsApp Bot
Описание проекта

Reminder WhatsApp Bot — это бот для установки и получения напоминаний через WhatsApp. Пользователи могут отправить
сообщение в определенном формате, и бот напомнит им о задаче в указанное время.
Стек технологий

    Python: Основной язык программирования проекта.
    Django: Веб-фреймворк для разработки и управления веб-приложениями.
    Celery: Асинхронная очередь задач для выполнения напоминаний.
    Twilio API: Сервис для отправки сообщений в WhatsApp.
    PostgreSQL: База данных для хранения напоминаний.
    Docker: Контейнеризация приложения для удобного развертывания и масштабирования.
    Git: Система контроля версий для управления исходным кодом проекта.

Install

git clone https://github.com/zhdaniukivan/whatsap_reminder.git

pip install --upgrade pip
pip install -r requirements.txt
в файле .env_exemple удаляете из названия часть _exemple
и прописываете свои данные для twilio.

Заускаем три окна терминала. Первый для django сервер:
cd path_to_your_project/Whatsapp_reminder
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

второй терминал для celery worker
cd path_to_your_project/Whatsapp_reminder
source .venv/bin/activate
celery -A reminder_whatsapp_bot worker --loglevel=info

третий для celery worker
cd path_to_your_project/Whatsapp_reminder
source .venv/bin/activate
celery -A reminder_whatsapp_bot beat --loglevel=info

Использование:
Отправьте сообщение в WhatsApp на номер предоставленный twilio
в формате ЧЧ:ММ текст напоминания. Например: 20:00 почистить зубы и ложиться спать 
В течение 10 секунд вам придет уведомление, что ваше напоминание установлено. 
В назначенное время вам придет уведомление с вашим напоминанием.