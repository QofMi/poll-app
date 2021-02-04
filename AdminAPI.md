# Описание API Администратора

#### GET - admin/api/polls

Получение списка всех опросов.

Ответ:
```
[
    {
        "id":           Идентификатор,
        "title":        "Название",
        "description":  "Описание",
        "start_date":   "YYYY-MM-DD",
        "finish_date":  "YYYY-MM-DD"
    },
]
```

#### POST - admin/api/polls

Создание нового опроса.

Запрос:
```
{
    "title":        "Название",
    "description":  "Описание",
    "start_date":   "YYYY-MM-DD",
    "finish_date":  "YYYY-MM-DD"
}
```

Ответ:
```
{
    "id":           Идентификатор,
    "title":        "Название",
    "description":  "Описание",
    "start_date":   "YYYY-MM-DD",
    "finish_date":  "YYYY-MM-DD"
}
```

#### GET - admin/api/polls/<id>

Получение информации об опросе

Ответ:
```
{
    "id":           Идентификатор,
    "title":        "Название",
    "description":  "Описание",
    "start_date":   "YYYY-MM-DD",
    "finish_date":  "YYYY-MM-DD",
    "questions": [
        {
            "id":       Идентификатор,
            "type":     "Тип вопроса (TEXT, CHOICE, MULTIPLE_CHOICE)",
            "text":     "Текст вопроса",
            "poll":     Идентификатор опроса,
            "options": [ - только для CHOICE, MULTIPLE_CHOICE
                {
                    "id":        Идентификатор,
                    "index":     Индекс(Число),
                    "text":      "Текст варианта ответа",
                    "question":   Идентификатор вопроса
                },
            ]
        }
    ]
}
```

#### PATCH - admin/api/polls/<id>

Редактирование опроса

Запрос:
```
{
    "title":        "Название",
    "description":  "Описание",
    "start_date":   "YYYY-MM-DD", - нельзя изменить
    "finish_date":  "YYYY-MM-DD"
}
```

Ответ:
```
{
    "id":           Идентификатор,
    "title":        "Название",
    "description":  "Описание",
    "start_date":   "YYYY-MM-DD",
    "finish_date":  "YYYY-MM-DD"
}
```

#### DELETE - admin/api/polls/<id>
Удаление опроса

Ответ:
```
"Object was deleted"
```

#### GET - admin/api/polls/<id>/questions

Получение списка вопросов

Ответ:
```
[
    {
        "id":     Идентификатор вопроса,
        "type":   "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
        "text":   "Текст вопроса",
        "poll":   Идентификатор опроса
    },
]
```

#### POST - admin/api/polls/<id>/questions

Создание вопроса для опроса

Запрос:
```
{
    "type": "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
    "text": "Текст вопроса"
}
```

Ответ:
```
{
    "id":    Идентификатор вопроса,
    "type":  "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
    "text":  "Текст вопроса",
    "poll":  Идентификатор опроса
}
```

#### GET - admin/api/polls/<id>/questions/<id>

Получение вопроса по идентификатору

Ответ:
```
{
    "id":    Идентификатор вопроса,
    "type":  "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
    "text":  "Текст вопроса",
    "poll":  Идентификатор опроса
}
```

#### PATCH - admin/api/polls/<id>/questions/<id>

Редактирование вопроса

Запрос:
```
{
    "type":  "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
    "text":  "Текст вопроса"
}
```

Ответ:
```
{
    "id":    Идентификатор вопроса,
    "type":  "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
    "text":  "Текст вопроса",
    "poll":  Идентификатор опроса
}
```

#### DELETE - admin/api/polls/<id>/questions/<id>

Удаление вопроса

Ответ:
```
"Question was deleted!"
```

#### GET - admin/api/polls/<id>/questions/<id>/options

Получение списка вариантов ответа для вопросов тип CHOICE и MULTIPLE_CHOICE

Ответ:
```
[
    {
    "id":       Идентификатор вопроса,
    "type":     "Тип вопроса", - TEXT, CHOICE, MULTIPLE_CHOICE
    "text":     "Текст вопроса",
    "poll":     Идентификатор опроса,
    "options": [ - только для CHOICE, MULTIPLE_CHOICE
        {
            "id":       Идентификатор варианта,
            "index":    Индекс,
            "text":     "Текст варианта",
            "question": Идентификатор вопроса
        }
      ]
    }
]
```

#### POST - admin/api/polls/<id>/questions/<id>/options

Создание вариантов ответа для вопросов типа CHOICE и MULTIPLE_CHOICE

Запрос:
```
{
    "index": "Индекс",
    "text": "Текст варианта"
}
```

Ответ:
```
{
    "id":       Идентификатор варианта,
    "index":    Индекс,
    "text":     "Текст варианта",
    "question": Идентификатор вопроса
}
```

#### GET - admin/api/polls/<id>/questions/<id>/options/<id>

Получение варианта ответа по идентификатору

Ответ:
```
{
    "id":       Идентификатор варианта,
    "index":    Индекс,
    "text":     "Текст варианта",
    "question": Идентификатор вопроса
}
```

#### PATCH - admin/api/polls/<id>/questions/<id>/options/<id>

Редактирование варианта ответа

Запрос:
```
{
    "index":    Индекс,
    "text":     "Текст варианта",
}
```

Ответ:
```
{
    "id":       Идентификатор варианта,
    "index":    Индекс,
    "text":     "Текст варианта",
    "question": Идентификатор вопроса
}
```

#### DELETE - admin/api/polls/<id>/questions/<id>/options/<id>

Удаление варианта ответа

Ответ:
```
"Option was deleted!"
```
