# Blogicum
# Прикладное программирование. Практика 10
# Студент: Еремченко Е.О.
```bash
#1. Клонировать репозиторий

  https://github.com/necron03/django_sprint3.git
  
  cd django_sprint3

#2. Cоздать и активировать виртуальное окружение

  python -m venv venv
  
  venv/Scripts/activate

#3. Установить зависимости из файла requirements.txt

  python -m pip install --upgrade pip
  
  pip install -r requirements.txt

#4 Выполнить миграции:

  python manage.py migrate

#5 Загрузить фикстуры:

  python manage.py loaddata db.json

#6. Запустить проект

  python manage.py runserver

#7. Перейти на локальный сервер

  http://127.0.0.1:8000/
