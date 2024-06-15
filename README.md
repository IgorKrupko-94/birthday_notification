# BIRTHDAYS_NOTIFICATION

## О чём проект:

Главная цель приложения - отслеживание дней рождения сотрудников.
Каждый день в 9:00 приложение отправляет уведомление со списком именинников
на почту сотрудникам, при условии, что сотрудник подписан на именинника,
а также при согласии на получение уведомлений.
Также в данном приложении реализована возможность отправки сообщений с
поздравлением прямо на почту.


Для запуска проекта необходима установка Docker. 
Скачать его можно по ссылке:
```
https://www.docker.com/products/docker-desktop/
```

Для установки на сервере Docker, Docker Compose:
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```


### Запуск проекта через docker-compose

Клонируйте репозиторий и перейдите в него в командной строке:
``` 
git clone git@github.com:IgorKrupko-94/birthday_notification.git
```
``` 
cd birthday_notification
```

Для работы с приложением необходимо создать файл .env и прописать туда
нужные переменные окружения:
```
SECRET_KEY=something_secret_key # Указываем свой секретный ключ
DEBUG=1 # Указываем режим работы (0 - рабочий, 1 - с отладкой)
ALLOWED_HOSTS=127.0.0.1,localhost # Указываем доступные хосты

DB_ENGINE=django.db.backends.postgresql # Указываем, что работаем с postgresql
DB_NAME=something_db # Имя базы данных
POSTGRES_USER=postgres # Логин для подключения к базе данных
POSTGRES_PASSWORD=something_password # Пароль для подключения к БД (установите свой)
DB_HOST=db # Название сервиса (контейнера)
DB_PORT=5432 # Порт для подключения к БД

CELERY_BROKER_URL=redis://localhost:6379/0 # Указываем адрес брокера
CELERY_RESULT_BACKEND=redis://localhost:6379/0 # Указываем адрес бэкенда

EMAIL_HOST=something_host # Указываем SMTP-хостинг
EMAIL_PORT=something_port # Указываем порт SMTP-хостинга
EMAIL_HOST_USER=something_host # Указываем почту для отправки сообщений
EMAIL_HOST_PASSWORD=something_password # Указываем пароль приложения
DEFAULT_FROM_EMAIL=something_email # Указываем дефолтный адрес почты отправителя
DEFAULT_TO_EMAIL=something_email # Указываем дефолтный адрес почты получателя
```
В папке проекта оставлен файл .env.example с такой же инструкцией по заполнению.

Создать и запустить контейнеры Docker
```
docker-compose up -d
```

После успешной сборки выполнить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```

Создайте суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Либо это можно сделать в консоли десктопной версии Docker.

Соберите статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```


### Некоторые примеры эндпоинтов с результатами:

1. Создание пользователя: POST-запрос
```
http://localhost:8000/auth/users/
```
Тело запроса:
```
{
    "username": "Alex",
    "password": "Alex15@",
    "birth_date": "15.06.1996",
    "email": "alexgagarin12@gmail.com",
    "first_name": "Alexei",
    "last_name": "Gagarin"
}
```
Ответ:
```
{
    "username": "Alex",
    "birth_date": "15.06.1996",
    "first_name": "Alexei",
    "last_name": "Gagarin",
    "email": "alexgagarin12@gmail.com"
}
```

2. Получение токена: POST-запрос
```
http://localhost:8000/auth/jwt/create/
```
Тело запроса:
```
{
    "username": "Alex",
    "password": "Alex15@"
}
```
Ответ:
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxODUxNzkwMSwiaWF0IjoxNzE4NDMxNTAxLCJqdGkiOiJkYjRjYmRiZWFhMWY0MmQ1OTE4MGE3ODRjZTVmOWMxMyIsInVzZXJfaWQiOjh9.bV1H_jedarzURthwRuDF5Q_zev36yDv1VlkUMZiX5b8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4NTE3OTAxLCJpYXQiOjE3MTg0MzE1MDEsImp0aSI6IjVlNzYzYjFjYTQzZjQ3ZmQ4ZTg2OTBjMzM3YmNkY2QyIiwidXNlcl9pZCI6OH0.MIdk7oKLYg7clAZXwBBqlYtOqnA-oRpv_itYSmkXLX0"
}
```

3. Получить/обновить зарегистрированного пользователя: GET/PUT/PATCH-запрос
```
http://localhost:8000/auth/users/
```
Тело запроса:
```
{
    "username": "Alex",
    "password": "Alex15@",
    "birth_date": "09.03.1934",
    "email": "alexgagarin12@gmail.com",
    "first_name": "Alexei",
    "last_name": "Gagarin"
}
```
Ответ:
```
{
    "username": "Alex",
    "birth_date": "09.03.1934",
    "first_name": "Alexei",
    "last_name": "Gagarin",
    "email": "alexgagarin12@gmail.com"
}
```

4. Получение списка всех пользователей: GET-запрос
```
http://localhost:8000/api/v1/users/
```
Ответ:
```
[
    {
        "id": 7,
        "username": "Alex",
        "first_name": "Alexei",
        "last_name": "Gagarin",
        "email": "alexgagarin12@gmail.com"
        "birth_date": "09.03.1934",
        "is_notification_agree": true
    },
    {
        "id": 6,
        "username": "Suzy",
        "first_name": "Suzy",
        "last_name": "Grigoryan",
        "email": "suzy29@gmail.com",
        "birth_date": "15.06.1970",
        "is_notification_agree": true
    },
    {
        "id": 5,
        "username": "Dima",
        "first_name": "Dima",
        "last_name": "Morozov",
        "email": "dima@gmail.com",
        "birth_date": "12.07.1996",
        "is_notification_agree": true
    }
]
```

5. Получение именинников: GET-запрос
```
http://localhost:8000/api/v1/users/get_birthday_users
```
Ответ:
```
[
    {
        "id": 6,
        "username": "Suzy",
        "first_name": "Suzy",
        "last_name": "Grigoryan",
        "email": "suzy29@gmail.com",
        "birth_date": "15.06.1970",
        "is_notification_agree": true
    }
]
```

6. Получение подписок пользователя: GET-запрос
```
http://localhost:8000/api/v1/users/get_following
```
Ответ:
```
[
    {
        "id": 6,
        "username": "Suzy",
        "first_name": "Suzy",
        "last_name": "Grigoryan",
        "email": "suzy29@gmail.com",
        "birth_date": "15.06.1970",
        "is_notification_agree": true
    }
]
```

7. Получение подписчиков пользователя: GET-запрос
```
http://localhost:8000/api/v1/users/get_followers
```
Ответ:
```
[
    {
        "id": 6,
        "username": "Suzy",
        "first_name": "Suzy",
        "last_name": "Grigoryan",
        "email": "suzy29@gmail.com",
        "birth_date": "15.06.1970",
        "is_notification_agree": true
    },
    {
        "id": 5,
        "username": "Dima",
        "first_name": "Dima",
        "last_name": "Morozov",
        "email": "dima@gmail.com",
        "birth_date": "12.07.1996",
        "is_notification_agree": true
    },
]
```

8. Создание подписки: POST-запрос
```
http://localhost:8000/api/v1/follow/5
```

9. Удаление подписки: DELETE-запрос
```
http://localhost:8000/api/v1/unfollow/5
```

10. Отправка сообщения с поздравлением: POST-запрос
```
http://localhost:8000/api/v1/congratulate/5
```
Тело запроса:
```
{
    "message": "С днём рождения!!!"
}
```



## Author
# Igor Krupko