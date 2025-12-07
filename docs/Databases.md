# Databases for RAG TG Bot
### Типы баз
1. Relation DB: хранение данных о пользователях, админах, существующих коллекциях, _документах_. Стек: `sqlite3`, `sqlalchemy` или `mongo` (можем выбрать)
2. Vector DB: хранение документов в векторизованном формате + хранение метаданных. Стек: `qdrant`
3. Key-Value Store: хранение кеша эмбеддингов запросов. Стек: `redis`

## Реляционные базы данных
### Задачи:
1. Спроектировать базу данных (описать сущности)
2. Написать use cases для базы данных (создание БД, добавление документа...)
3. Написать интерфейс абстрактной базы данных
4. Написать реализацию интерфейса (`sqlite3`, `sqlachemy`)
5. *(Саша) Настроить Dependency Injections*
6. *(Саша) Написать ручки*
7. *(Тим) Понять, что изменилось в API и соответственно отредактировать бота*
8. *(Дима) Настроить DB в Docker*

### Сущности (модифицированные требования от Олега)
#### Пользователь (User)
```sql
Users:
-  user_id (UUID, PK)
-  telegram_id (String)  -- или Integer/BigInt
-  created_at (DateTime)
-  role (String)         -- юзер или админ
```

#### Коллекция документов (DocumentCollection)
```sql
Collections:
-  collection_id (UUID, PK) -- используется в Qdrant!
-  name (String)
-  description (Text)
-  document_count (Integer/BigInt)
-  owner_id (UUID, FK)
-  is_public (Boolean)
-  created_at (DateTime)
```
#### Документ (Document)
```sql
Documents:
-  document_id (UUID, PK)
-  collection_id (UUID, FK)
-  title (String)
-  metadata (JSON)     -- тут потенциально 'url' и пр.
-  file_name (String)  -- оригинальное название файла
-  file_size (Decimal) -- BigInt, если захотим хранить в байтах
-  created_at (DateTime)
-- -  content (Text) - было в доке Олега, но я считаю разумным
--                     хранить текст в Qdrant
-- -  vector_embedding (Vector) - было в доке Олега;
--                                вектор мы храним в VDB (Qdrant)
```
#### Диалог (Conversation)
```sql
Conversations:
-  conversation_id (UUID, PK)
-  user_id (UUID, FK)
-  collection_id (UUID, FK)
-  created_at (DateTime)
-  updated_at (DateTime)
```
#### Сообщение (Message)
```sql
Messages:
-  message_id (UUID, PK)
-  conversation_id (UUID, FK)
-  content (Text)
-  role (String)
-  sources (JSON)
-  created_at (DateTime)
```

### Use cases (примерные)
*Прим:* use cases описывают бизнес-логику, находятся в `src/application/` и зависят только от `domain` и абстрактных интерфейсов из `adapters`.
*Прим:* сущности взяты из `api/v1/schemas.py`, по-хорошему надо переопределить их и закинуть в `domain` (Саша).
1. Создание новой коллекции:
```python
class CreateCollectionUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: DatabaseCreateRequest
		  ) -> DatabaseCreateResponse:
      ...
```
2. Проверить, является ли пользователь админом:
```python
class CheckAdminUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: Request
		  ) -> bool:
      ...
```
3. Вывести список доступных пользователю коллекций:
```python
class GetAvaliableCollectionsUC:
	def __init__(): ...
	
    async def execute(
	      self,
		  user_id: int
		  ) -> DatabasesGetResponse:
      ...
```
4. Удалить коллекцию:
```python
class DeleteCollectionUC:
	def __init__(): ...
	
    async def DeleteCollectionUC(
	      self,
		  collection_id: int
		  ) -> DatabaseDeleteResponse:
	  ...
```
5. Загрузить документы в коллекцию (уже существует, лежит в `src/application/embeddings/`, необходимо дописать):
```python
class  LoadingUC:
	__slots__  = ("_vdb_gateway",  "_embedder",  "_chunk_adapter")
	
	def  __init__(): ...

	async def execute(
		  self, 
		  request:  LoadDataRequest
		  ) -> Result[str,  Any]:
      ...
```
### Абстрактный интерфейс и реализация
Они должны содержать такой набор методов, чтобы use cases работали. В `adapters` много примеров абстрактных интерфейсов и реализаций.

## Векторные базы данных
### Задачи:
1. Спроектировать базу данных
2. *(Дима) Проверить написанный интерфейс*
3. *(Саша) Настроить Dependency Injections*
4. *(Саша) Написать ручки*
5. *(Дима) Настроить DB в Docker*
#### Структура
Мы используем `qdrant`. Структура документа должна быть примерно следующей:
```json
{
    "id": "chunk_123",                // уникальный ID чанка
    "vector": [0.1, 0.2, ...],        // эмбеддинг
    "payload": {
        "document_id": "doc_456",     // связь с SQLite
        "collection_id": "coll_789",  // связь с коллекцией
        "chunk_id": "chunk_123",      // связь с таблицей (а она будет?)
        "text": "Текст чанка...",     // текст для поиска
        "metadata": {                 // дополнительные данные, пример
            "author": "Иванов И.И.",
            "year": 2023
        }
    }
}
```
## Redis
TBD.