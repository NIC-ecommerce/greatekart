# Проект Greate Kart

## Как запустить проект на Python (для начала установите Python)

### На Linux/MacOS:


1. Установите Python с официального сайта Python, если его еще нет.

2. Откройте терминал bash и перейдите в директорию проекта.

3. Создайте виртуальное окружение в директории, содержащей файл requirements.txt:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

5. Выполните миграции базы данных:
    ```bash
    cd greate_kart/
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Создайте суперпользователя (опционально):
    ```bash
    python manage.py createsuperuser
    ```

7. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

### На Windows:

1. Установите Python с официального сайта Python, если его еще нет.

2. Откройте командную строку (cmd) и перейдите в директорию проекта.

3. Создайте виртуальное окружение:
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

4. Установите зависимости:
    ```cmd
    pip install -r requirements.txt
    ```

5. Выполните миграции базы данных:
    ```cmd
    cd greate_kart/
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Создайте суперпользователя (опционально):
    ```cmd
    python manage.py createsuperuser
    ```

7. Запустите сервер:
    ```cmd
    python manage.py runserver
    ```

## Как использовать проект

После запуска сервера вы сможете открыть приложение в вашем веб-браузере по адресу `http://127.0.0.1:8000/`.
После запуска сервера и создания суперпользователя можно перейти в админ панель сайта `http://127.0.0.1:8000/sec_login/`.


