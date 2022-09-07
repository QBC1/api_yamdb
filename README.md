# Отзывник.

  

Данное api приложение позволяет легко развернуть серверную часть для организации сбора и обработки отзывов для различных ресурсов.

  

## Установка и запуск.

Для работы с приложением Вам потребуется:

* django==2.2.16

* jangorestframework==3.12.4

* pytest==6.2.4

* pytest-django==4.4.0

* pytest-pythonpath==0.7.3

* requests==2.26.0

* Pillow==8.3.1

* sorl-thumbnail==12.7.0

* djoser

* django-filter

  

Клонировать репозиторий и перейти в него в командной строке:

  

```

git clone https://github.com/QBC1/api_yamdb.git

```

  

Создать и активировать виртуальное окружение:

  

```

python -m venv venv

```

  

```

source venv/Scripts/activate # для запуска в среде Windows

```

```

source venv/bin/activate # для запуска в среде Linux

```

  
  

Установить зависимости из файла requirements.txt:

  

```

python -m pip install --upgrade pip

```

  

```

pip install -r requirements.txt

```

  

Выполнить миграции:

  

```

cd yatube_api

```

  

```

python manage.py migrate

```

  

Запустить проект:

  

```

python manage.py runserver

```

  

## Работа с приложением

  

запросы к API начинаются с /api/v1/

  
  

# Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.

2.  **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.

3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).

4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

  

# Пользовательские роли

-  **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

-  **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.

-  **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.

-  **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

-  **Суперюзер Django** — обладет правами администратора (`admin`)

  

### /auth/signup/

  

#### POST
```
{
	"email": "string",
	"username": "string"
}
```
##### Описание:

  

Получить код подтверждения на переданный `email`.

  

Права доступа: **Доступно без токена.**

  

Использовать имя 'me' в качестве `username` запрещено.

  

Поля `email` и `username` должны быть уникальными.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

  

##### Ответ
```
{
	"email": "string",
	"username": "string"
}
```

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |


### /auth/token/

  

#### POST

```
{
	"email": "string",
	"username": "string"
}
```
##### Описание:

  
Получение JWT-токена в обмен на username и confirmation code.

  

Права доступа: **Доступно без токена.**

  
  

##### Ответ
```
{
   "token": "string"
}
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 404 | Пользователь не найден |

  

### /categories/

  

#### GET

##### Описание:

Получить список всех категорий

Права доступа: **Доступно без токена**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| search | query | Поиск по названию категории | No | string |

  

##### Ответ
```
  [
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

  

#### POST
```
{
  "name": "string",
  "slug": "string"
}
```

##### Описание:

Создать категорию.

  

Права доступа: **Администратор.**

  

Поле `slug` каждой категории должно быть уникальным.

  
  

##### Ответ
```
{
  "name": "string",
  "slug": "string"
}
```
  

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /categories/{slug}/

  

#### DELETE

##### Описание:

  
Удалить категорию.
  
Права доступа: **Администратор.**

    

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| slug | path | Slug категории | Yes | string |

  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Категория не найдена |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /genres/

  

#### GET

##### Описание:

  

Получить список всех жанров.

  

Права доступа: **Доступно без токена**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| search | query | Поиск по названию жанра | No | string |

  

##### Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
 ```
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

  

#### POST
```
{
	"name": "string",
	"slug": "string"
}
```
##### Описание:

  

Добавить жанр.

  

Права доступа: **Администратор**.

  

Поле `slug` каждого жанра должно быть уникальным.

  
  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /genres/{slug}/

  

#### DELETE

##### Описание:

  

Удалить жанр.

  

Права доступа: **Администратор**.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| slug | path | Slug жанра | Yes | string |

  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Жанр не найден |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /titles/

  

#### GET

##### Описание:

  

Получить список всех объектов.

  

Права доступа: **Доступно без токена**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| category | query | фильтрует по полю slug категории | No | string |
| genre | query | фильтрует по полю slug жанра | No | string |
| name | query | фильтрует по названию произведения | No | string |
| year | query | фильтрует по году | No | integer |

  

##### Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
 ```

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

  

#### POST
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
##### Описание:

  

Добавить новое произведение.

  

Права доступа: **Администратор**.

  

Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

  

При добавлении нового произведения требуется указать уже существующие категорию и жанр.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

  

##### Ответ
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
 ```
| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /titles/{titles_id}/

  

#### GET

##### Описание:

  

Информация о произведении

  
  

Права доступа: **Доступно без токена**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| titles_id | path | ID объекта | Yes | integer |

  

##### Ответ
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
  ```
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Объект не найден |

  

#### PATCH
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
##### Описание:

  

Обновить информацию о произведении

  
  

Права доступа: **Администратор**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| titles_id | path | ID объекта | Yes | integer |

  

##### Ответ
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Объект не найден |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

#### DELETE

##### Описание:

  

Удалить произведение.

  

Права доступа: **Администратор**.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| titles_id | path | ID объекта | Yes | integer |

  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Произведение не найдено |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /titles/{title_id}/reviews/

  

#### GET

##### Описание:

  

Получить список всех отзывов.

  

Права доступа: **Доступно без токена**.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |

  

##### Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Произведение не найдено |

  

#### POST
```
{
  "text": "string",
  "score": 1
}
```
##### Описание:

  

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.

  

Права доступа: **Аутентифицированные пользователи.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |

  

##### Ответ

  ```
  {
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
  ```

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 404 | Произведение не найдено |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:user,moderator,admin |

  

### /titles/{title_id}/reviews/{review_id}/

  

#### GET

##### Описание:

  

Получить отзыв по id для указанного произведения.

  

Права доступа: **Доступно без токена.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

  

##### Ответ
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
 ``` 

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Произведение или отзыв не найден |

  

#### PATCH
```
{
  "text": "string",
  "score": 1
}
```
##### Описание:

  

Частично обновить отзыв по id.

  

Права доступа: **Автор отзыва, модератор или администратор.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

  

##### Ответ
```{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Произведение не найдено |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:user,moderator,admin |

  

#### DELETE

##### Описание:

  

Удалить отзыв по id

  

Права доступа: **Автор отзыва, модератор или администратор.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Произведение или отзыв не найдены |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:user,moderator,admin |

  

### /titles/{title_id}/reviews/{review_id}/comments/

  

#### GET

##### Описание:

  

Получить список всех комментариев к отзыву по id

  

Права доступа: **Доступно без токена.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

  

##### Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Не найдено произведение или отзыв |

  

#### POST
```
{
  "text": "string"
}
```
##### Описание:

  

Добавить новый комментарий для отзыва.

  

Права доступа: **Аутентифицированные пользователи.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |

  

##### Ответ
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 404 | Не найдено произведение или отзыв |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:user,moderator,admin |

  

### /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

  

#### GET

##### Описание:

  

Получить комментарий для отзыва по id.

  

Права доступа: **Доступно без токена.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |
| comment_id | path | ID комментария | Yes | integer |

  

##### Ответ
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 404 | Не найдено произведение, отзыв или комментарий |

  

#### PATCH
```
{
  "text": "string"
}
```

##### Описание:

  

Частично обновить комментарий к отзыву по id.

  

Права доступа: **Автор комментария, модератор или администратор**.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |
| comment_id | path | ID комментария | Yes | integer |

  

##### Ответ
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Не найдено произведение, отзыв или комментарий |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:user,moderator,admin |

  

#### DELETE

##### Описание:

  

Удалить комментарий к отзыву по id.

  

Права доступа: **Автор комментария, модератор или администратор**.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title_id | path | ID произведения | Yes | integer |
| review_id | path | ID отзыва | Yes | integer |
| comment_id | path | ID комментария | Yes | integer |

  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Не найдено произведение, отзыв или комментарий |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:user,moderator,admin |

  

### /users/

  

#### GET

##### Описание:

  

Получить список всех пользователей.

  

Права доступа: **Администратор**

  
  

##### Параметры

  
| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| search | query | Поиск по имени пользователя (username) | No | string |

  

##### Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
  
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | read:admin |

  

#### POST
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
##### Описание:

  

Добавить нового пользователя.

  

Права доступа: **Администратор**

  

Поля `email` и `username` должны быть уникальными.

  
  

##### Ответ
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
  

| Code | Description |
| ---- | ----------- |
| 201 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /users/{username}/

  

#### GET

##### Описание:

  

Получить пользователя по username.

  

Права доступа: **Администратор**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| username | path | Username пользователя | Yes | string |

  

##### Ответ
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Пользователь не найден |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | read:admin |

  

#### PATCH
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
##### Описание:

  

Изменить данные пользователя по username.

  

Права доступа: **Администратор.**

  

Поля `email` и `username` должны быть уникальными.

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| username | path | Username пользователя | Yes | string |

  

##### Ответ
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Пользователь не найден |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

#### DELETE

##### Описание:

  

Удалить пользователя по username.

  

Права доступа: **Администратор.**

  
  

##### Параметры

  

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| username | path | Username пользователя | Yes | string |

  

##### Ответ

  

| Code | Description |
| ---- | ----------- |
| 204 | Удачное выполнение запроса |
| 401 | Необходим JWT-токен |
| 403 | Нет прав доступа |
| 404 | Пользователь не найден |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin |

  

### /users/me/

  

#### GET

##### Описание:

  

Получить данные своей учетной записи

  

Права доступа: **Любой авторизованный пользователь**

  
  

##### Ответ
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |

  

##### Доступ

  

| Security Schema | Scopes |

| --- | --- |

| jwt-token | read:admin,moderator,user |

  

#### PATCH
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```
##### Описание:

  

Изменить данные своей учетной записи

  

Права доступа: **Любой авторизованный пользователь**

  

Поля `email` и `username` должны быть уникальными.

  
  

##### Ответ
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
  

| Code | Description |
| ---- | ----------- |
| 200 | Удачное выполнение запроса |
| 400 | Отсутствует обязательное поле или оно некорректно |

  

##### Доступ

  

| Security Schema | Scopes |
| --- | --- |
| jwt-token | write:admin,moderator,user |