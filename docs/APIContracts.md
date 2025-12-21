# Документация API для Telegram RAG-бота

## 🚀 Быстрый старт
1. **URL API**: `http://localhost:8000` (локально)
2. **Документация (встроенная от FastAPI)**: `http://localhost:8000/docs`


## 📊 Спецификация эндпоинтов
**¡Внимание!** В начале везде пропущено `/api/v?`. Конкретную версию API можете уточнить у Саши.

### 1. Работа с коллекциями

#### 1.1. Получить список доступных коллекций

**GET** `/collections/?telegram_id=123456789`

**Content-Type:** -

```json
// Status: 200 OK
// Response: List[CollectionShort]
[
  {
    "collection_id": 2,
    "name": "Имущественное право"
  },
  {
    "collection_id": 3,
    "name": "Гражданское право"
  }
]	
```

#### 1.2. Добавить новую коллекцию

**POST** `/collections`

**Content-Type:** `application/json`

```json
// Request
{
  "telegram_id": 123456789,
  "name": "Архив анекдотов про порутчика Ржевского",
  "description": "Так, по рофлу создал",
  "is_public": True
}

// -------------------------

// Status 201: Created
// Response: CollectionShort
{
  "collection_id": 5,
  "name": "Архив анекдотов про порутчика Ржевского",
  "description": "Так, по рофлу создал",
  "is_public": True
}

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на создание коллекции"
}

// Status: 409 Conflict
// Response:
{
  "detail": "Коллекция с таким именем уже существует"
}
```

#### 1.3. Удалить коллекцию

**DELETE** `/collections/{collection_id}/?telegram_id=123456789`

**Content-Type:** -

```json
// Status: 204 No Content
// Response: -

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на удаление коллекции"
}

// Status: 404 Not Found
// Response:
{
  "detail": "Коллекция не найдена"
}
```

#### 1.4. Получить конкретную коллекцию

**GET** `/collections/{collection_id}/?telegram_id=123456789`

**Content-Type:** -

```json
// Status: 200 OK
// Response: Collection
{
  "collection_id": 7,
  "name": "Гражданское право Узбекистана",
  "description": "А вы что хотели тут увидеть?",
  "document_count": 28,
  "is_public": True,
  "created_at": "2020-20-20"
}

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на просмотр этой коллекции"
}

// Status: 404 Not Found
// Response:
{
  "detail": "Коллекция не найдена"
}
```

#### 1.5 Редактировать конкретную коллекцию

**PATCH** `/collections/{collection_id}`

**Content-Type:** `application/json`

```json
// Request
{
  "telegram_id": 123456789,
  "name": "НоВоЕ ИмЯ",
  "description": "АхАхАхАхА"
}

// Status: 204 No Content
// Response: -

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на редактирование этой коллекции"
}

// Status: 404 Not Found
// Response:
{
  "detail": "Коллекция не найдена"
}
```

### 2. Работа с документами

#### 2.1. Получить список доступных документов

**GET** `collections/{collection_id}/documents/?telegram_id=123456789`

**Content-Type:** -

```json
// Status: 200 OK
// Response: List[DocumentShort]
[
  {
    "document_id": 46,
    "collection_id": 4,
    "name": "ФЗ-231ю1"
  },
  {
    "document_id": 47,
    "collection_id": 4,
    "name": "Указ Президента №12 от 02.10.25"
  }
]
```

#### 2.2. Загрузить новый документ

**POST** `collections/{collection_id}/documents`

**Content-Type:** `multipart/form-data`

```json
// Request

telegram_id=123456789,
title="Закон о среднесборщиках",
description="это кто вообще"
url="rusgov.ru/law/2",
file=[doc.txt]


// -------------------------

// Status 201: Created
// Response: DocumentShort
{
  "document_id": 55,
  "collection_id": 3,
  "title": "Закон о среднесборщиках"
}

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на загрузку документов"
}

// Status: 409 Conflict
// Response:
{
  "detail": "Документ с таким названием уже существует"
}

// Status: 400 Bad Request
// Response:
{
  "detail": "Данный формат файлов не поддерживается"
}
```

#### 2.3 Удалить существующий документ

**DELETE** `/collections/{collection_id}/documents/{document_id}/?telegram_id=123456789`

**Content-Type:** -

```json
// Status: 204 No Content
// Response: -

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на удаление документов"
}

// Status: 404 Not found
// Response:
{
  "detail": "Документ не найден"
}
```

#### 2.4. Получить конкретный документ

**GET** `/collections/{collection_id}/documents/{document_id}/?telegram_id=123456789`

**Content-Type:** -

```json
// Status: 200 OK
// Response: Document
{
  "document_id": 432,
  "collection_id": 7,
  "title": "Случай от 02.03.1999",
  "description": "Летят в самолёте американец, немец и русский",
  "file_name": "case12.txt",
  "file_size": 12.2,
  "created_at": "2020-20-20",
  "metadata": {
    "url": "https://blabla.ru"
  }
}

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на просмотр этого документа"
}

// Status: 404 Not Found
// Response:
{
  "detail": "Документ не найден"
}
```

#### 2.5 Редактировать конкретный документ

**PATCH** `/collections/{collection_id}/documents/{document_id}`

**Content-Type:** `application/json`

```json
// Request
{
  "telegram_id": 123456789,
  "title": "НоВоЕ ИмЯ v2.0",
  "description": "Новое описание, всем привет!"
}

// Status: 204 No Content
// Response: -

// Errors
// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав на редактирование этого документа"
}

// Status: 404 Not Found
// Response:
{
  "detail": "Документ не найден"
}
```


### 3. RAG-система

#### 3.1. Отправить запрос

**POST** `/collections/{collection_id}/query`

**Content-Type:** `application/json`

```json
// Request
{
  "telegram_id": 123456789,
  "query_text": "Что будет если взорвать биотуалет?"
}

// Status: 200 OK
// Response: Message
{
  "message_id": 1245,
  "content": "В соответствие с законами РФ...",
  "role": "Bot",
  "sources": [   // List[DocumentRelevance] (возможны изменения)
    {            // По идее, len(List[...]) <= 5
      "collection_id": 7,
      "title": "Случай от 02.03.1999",
      "description": "Самолёт начинает падать, и обнаруживается, что у них только два парашюта",
      "file_name": "case12.txt",
      "file_size": 12.2,
      "created_at": "2020-20-20",
      "metadata": {
        "url": "https://blabla.ru"
      }
    },
    {
      "document_id": 245,
      "collection_id": 9,
      "title": "Записки охотника",
      "description": "Американец: дайте мне парашют! Мне нужно кормить семью!",
      "file_name": "okvotnik.pdf",
      "file_size": 22.2,
      "created_at": "1998-20-20",
      "metadata": {}
    },
    ...
  ]
}

// Errors
// Status: 404 Not Found
// Response:
{
  "detail": "Диалог не найден"
}

// Status: 404 Not Found
// Response:
{
  "detail": "Коллекция не найдена"
}

// Status: 429 Too Many Requests 
// Response:
{
  "detail": "Ваши бесплатные попытки кончились"
}
```

### 4. ~~Пробив~~ Поиск по базе

#### 4.1 Поиск в коллекции

**POST** `/collections/{collection_id}/find`

**Content-Type:** `application/json`

```json
// Request
{
  "telegram_id": 123456789,
  "number_of_sources": 3,
  "query_text": "Самоучитель игры на баяне"
}

// Status: 200 OK
// Response: List[DocumentRelevance] (возможны изменения)
```json
[
  {
    "document_id": 432,
    "title": "Самоучитель игры на баяне",
    "description": "Русский даёт ему рюкзак, американец прыгает. Немец: прыгай ты, я уже многое повидал",
    "file_name": "bayan.txt",
    "file_size": 12.2,
    "created_at": "2020-20-20",
    "metadata": {
      "url": "https://blabla.ru"
    }
  },
  {
    "document_id": 432,
    "title": "Байки кота Баяна",
    "description": "Русский: а ты? У нас же два парашюта. Немец: а с чем тогда американец прыгнул?",
    "file_name": "Bayan.txt",
    "file_size": 12.2,
    "created_at": "2020-20-20",
    "metadata": {
      "url": "https://blabla.ru"
    }
  },
  {
    "document_id": 432,
    "title": "Баянные анекдоты",
    "description": "Русский: ну ему же кормить семью надо, я и дал ему рюкзак с продуктами!",
    "file_name": "bayany.txt",
    "file_size": 12.2,
    "created_at": "2020-20-20",
    "metadata": {
      "url": "https://blabla.ru"
    }
  }
]


// Errors
// Status: 404 Not Found
// Response:
{
  "detail": "Коллекция не найдена"
}

// Status: 403 Forbidden
// Response:
{
  "detail": "У вас нет прав поиск в этой коллекции"
}

// Status: 429 Too Many Requests 
// Response:
{
  "detail": "Ваши бесплатные попытки кончились"
}
```

### 5. Платёжная система (WIP)
