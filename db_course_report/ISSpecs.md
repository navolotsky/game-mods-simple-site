# Описание
## Наименование
game mods simple site

## Предметная область
Моды для компьютерных видеоигр: описание, изображения, ссылки на скачивание. Возможность хранения разных версий мода.

# Данные
Таблички БД
- core\_users - 
  таблица, предоставляемая Django по умолчанию
    - id
    - password
    - last\_login
    - is\_superuser
    - username
    - first\_name
    - last_name
    - email
    - is\_staff
    - is\_active
    - date\_joined
- user\_profiles
    - id
    - user\_id
    - avatar
    - description
- games
    - id
    - name
    - description
- mod\_categories
    - id
    - name
    - description
- mods\_n\_categories
    - id
    - mod\_id
    - category\_id
- mods
    - id
    - game\_id
    - author\_id
    - showed\_version\_id
    - hidden
- mod\_versions
    - id
    - mod\_id
    - title
    - short\_description
    - full\_description
    - main\_image\_id
    - number
    - comment
    - added\_at
    - last\_updated\_at
    - hidden
- mod\_images
    - id
    - file
- mod\_versions\_n\_images
  - id
  - mod_version_id
  - mod_image_id
- mod\_download\_links
    - id
    - mod\_version\_id
    - url
    - comment
    - added\_at
    - last\_updated\_at
- mod\_user\_ratings
    - id
    - user\_id
    - mod\_id
    - mod\_version\_id
    - rating
    - rated\_at
- mod\_user\_comments
    - id
    - user\_id
    - mod\_id
    - mod\_version\_id
    - text
    - added\_at
    - last\_updated\_at
    - hidden
## Для каждого элемента данных - ограничения
## Общие ограничения целостности

# Пользовательские роли
## Для каждой роли - наименование, ответственность, количество пользователей в этой роли?
postgres: root-пользователь, в приложении не используется, количество: 1

django_site_backend: для создания табличек в БД и работе с ними из Django ORM, количество: 1

django_test_site_backend: создание и использование БД во время прогона юнит-тестов, количество: 1

# UI / API 
API: REST API

UI: сайт

# Технологии разработки
Бэкенд: Python, Django, Django Rest Framework

Фронтенд: JavaScript, React
## Язык программирования
Python 3 и JavaScript
## СУБД
PostgreSQL
