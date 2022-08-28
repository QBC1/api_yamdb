# ОТЗЫВНИК

Данное api приложение позволяет легко развернуть серверную часть для организации сбора и обработки отзывов для различных ресурсов.

# Установка.
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/QBC1/api_yamdb.git
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
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

### Допольнительное описание доступно по ip:/redoc/