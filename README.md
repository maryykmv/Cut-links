# Проект YaCut
«Проект YaCut»

## Оглавление
1. [Описание](#описание)
2. [Технологии](#технологии)
3. [Как запустить проект](#как-запустить-проект)
4. [Автор проекта](#автор-проекта)

## Описание
На большинстве сайтов адреса страниц довольно длинные, например, как у той страницы, на которой вы сейчас находитесь.
Делиться такими длинными ссылками не всегда удобно, а иногда и вовсе невозможно. 
Удобнее использовать короткие ссылки. Например, ссылки http://yacut.ru/lesson и http://yacut.ru/12e07d воспринимаются лучше,
чем https://practicum.yandex.ru/trainer/backend-developer/lesson/12e07d96-31f3-449f-abcf-e468b6a39061/. 
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой,
которую предлагает сам пользователь или предоставляет сервис.

Ключевые возможности сервиса:
 - генерация коротких ссылок и связь их с исходными длинными ссылками,
 - переадресация на исходный адрес при обращении к коротким ссылкам.
Пользовательский интерфейс сервиса — одна страница с формой. Эта форма должна состоять из двух полей:
 - обязательного для длинной исходной ссылки;
 - необязательного для пользовательского варианта короткой ссылки.
Пользовательский вариант короткой ссылки не должен превышать 16 символов.

Если пользователь предложит вариант короткой ссылки, который уже занят, то нужно сообщить пользователю об этом через уведомление:
Предложенный вариант короткой ссылки уже существует.
Существующая в базе данных ссылка должна остаться неизменной.
Если пользователь не заполнит поле со своим вариантом короткой ссылки, то сервис должен сгенерировать её автоматически. 
Формат для ссылки по умолчанию — шесть случайных символов, в качестве которых можно использовать:
 - большие латинские буквы,
 - маленькие латинские буквы,
 - цифры в диапазоне от 0 до 9.

Автоматически сгенерированная короткая ссылка должна добавляться в базу данных, но только если в ней ещё нет такого же идентификатора.
В противном случае нужно генерировать идентификатор заново.

API проекта доступен всем желающим. Сервис обслуживает два эндпоинта:
- /api/id/ — POST-запрос на создание новой короткой ссылки;
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.
Примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml; спецификация есть в репозитории yacut. 
Для удобной работы с документом воспользуйтесь онлайн-редактором Swagger Editor, в котором можно визуализировать спецификацию.

Коллекция запросов для Postman

В директории postman_collection сохранена коллекция запросов для отладки и проверки работы текущей версии проекта YaCut.
Когда проект будет готов обрабатывать запросы к API — импортируйте коллекцию в Postman и выполняйте запросы.


## Технологии
- Python 3.9
- Flask 2.0
- SQLAlchemy
- SQLite


## Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:maryykmv/yacut.git
```
- Переходим в директорию проекта:
```
cd yacut
```

- Создаем и активируем виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS:
    ```
    source venv/bin/activate
    ```

* Если у вас windows:
    ```
    source venv/scripts/activate
    ```

- Пример заполнения конфигурационного .env файла
```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=SECRET_KEY
TYPE_DB = sqlite:///
NAME_DB = db.sqlite3
```

- Обновляем менеджер пакетов pip:
```
pip install --upgrade pip
```

- Устанавливаем зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

- Создать базу для сохранения данных
```
flask db upgrade
```

- Запустит flask
```
flask run
```


## Автор проекта
_[Мария Константинова](https://github.com/maryykmv)_, python-developer
