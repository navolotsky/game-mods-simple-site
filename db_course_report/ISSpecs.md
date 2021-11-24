# Описание
## Наименование
game mods simple site

## Предметная область
Моды для компьютерных видеоигр: описание, изображения, ссылки на скачивание

# Данные
- users
    - id
    - username
    - vk_id
    - avatar
    - self_description
    - signed\_up\_at
    - last\_visited\_at
    - is_banned
    - ? average\_mod\_rating
    - ? average\_own\_mods_rating
- games
    - id
    - name
- mod_categories
    - id
    - name
- mods\_n\_categories
    - mod_id
    - category_id
- mod_versions
    - id
    - mod_id
    - main_image
    - title
    - short_description
    - full_description
    - additional_images
    - download_links
    - version_number
    - version_comment
    - added_at
    - last\_updated\_at
    - hidden
- mod\_main\_images
    - id
    - mod\_version\_id
    - image
- mod\_additional\_images
    - id
    - mod\_version\_id
    - image
- mod\_download\_links
    - mod\_version\_id
    - link
    - comment
    - added_at
    - last\_updated\_at
- mods
    - id
    - game_id
    - author_id
    - default\_showed\_version_id
    - hidden
    - ? views_number
- mod\_user\_ratings
    - user_id
    - mod_id
    - rating
    - rated_at
- mod\_user\_comments
    - user_id
    - mod_id
    - mod\_version\_id
    - content
    - added_at
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
