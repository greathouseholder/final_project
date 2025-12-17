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
-  description (String)
-  file_name (String)  -- оригинальное название файла
-  file_size (Decimal) -- BigInt, если захотим хранить в байтах
-  created_at (DateTime)
-  path (String)       -- для загруженных файлов
-  metadata (JSON)     -- тут потенциально 'url' и пр.
-- -  content (Text) - было в доке Олега, но я считаю разумным
--                     хранить текст в Qdrant в payload
-- -  vector_embedding (Vector) - было в доке Олега;
--                                вектор мы храним в VDB (Qdrant)
```

#### Сообщение (Message) (строго говоря, хранить историю сообщений вообще необязательно. Эту таблицу можно не реализовывать)
```sql
Messages:
-  message_id (UUID, PK)
-  content (Text)
-  role (String)
-  sources (JSON)
-  created_at (DateTime)
```

### Use cases (примерные)
Весьма примерные. Я не углублялся в философию use cases, но у них в общем структура такая - это класс (а не функция), где в `__init__`  мы инициализируем всё нужное для работы (хороший пример это `SearchUC`, он уже написан), а в отдельном методе (у нас это `execute`) реализуем работу юзкейса. 

По поводу сущностей: use cases не должны зависить от API, так что возникает беда, что есть API-сущности, есть domain-сущности. Сейчас в domain лежит три старых файла с сущностями и один новый, `schemas.py`. Можно для use cases из `schemas.py` сущностей юзать, лучше так и делать. Потом приведём всё к единообразию.
#### Работа с юзерами
1. Проверить, является ли пользователь админом:
```python
class CheckAdminUC:
	def __init__(): ...
	
	async def execute(
          self,
		  user_id: int
		  ) -> bool:
      ...
```
2. По `telegram_id` получить `user_id`:
```python
class GetUserIdUC:
	def __init__(): ...
	
	async def execute(
          self,
		  telegram_id: int
		  ) -> int: # user_id
      ...
```
3. По `user_id` получить `telegram_id`:
```python
class GetTelegramIdUC:
	def __init__(): ...
	
	async def execute(
          self,
		  user_id: int
		  ) -> int: # telegram_id
      ...
```
#### Коллекции
2. Вывести список доступных пользователю коллекций:
```python
class GetAvaliableCollectionsUC:
	def __init__(): ...
	
    async def execute(
	      self,
		  user_id: int
		  ) -> List[Collection]:
      ...
```
3. Создание новой коллекции (если коллекция с таким названием существует - выбросить адекватную ошибку; либо из существующих ошибок Пайтона выбрать подходящую, либо написать свой кастомный класс ошибки, либо просто внятную подпись ошибки сделать):
```python
class CreateCollectionUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: CreateCollectionRequest # тут по идее должен быть user_id, а не telegram_id. эта проблема решается созданием отдельных domain-сущностей, т.е. придётся файл schemas.py редачить и менять там telegram_id на user_id
		  ) -> Collection:
      ...
```
4. Обновление данных коллекции (если коллекции нет, выбросить читаемую ошибку):
```python
class UpdateCollectionUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: UpdateCollectionRequest
		  ) -> None:
      ...
```
5. Удалить коллекцию (если коллекции нет, выбросить читаемую ошибку):
```python
class DeleteCollectionUC:
	def __init__(): ...
	
    async def DeleteCollectionUC(
	      self,
		  collection_id: int
		  ) -> None:
	  ...
```
6. Получить конкретную коллекцию (если коллекции нет, выбросить читаемую ошибку):
```python
class GetCollectionUC:
	def __init__(): ...
	
    async def GetCollectionUC(
	      self,
		  collection_id: int
		  ) -> Collection:
	  ...
```
#### Документы
7. Вывести список доступных пользователю документов в коллекции:
```python
class GetAvaliableDocumentsUC:
	def __init__(): ...
	
    async def execute(
	      self,
		  request: GetAvaliableDocumentRequest
		  ) -> List[Document]:
      ...
```
8. Загрузить документы в коллекцию (уже существует, лежит в `src/application/embeddings/`, необходимо дописать) (если коллекции нет, выбросить читаемую ошибку):
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
9. Обновление данных документа (если документа нет, выбросить читаемую ошибку):
```python
class UpdateDocumentUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: UpdateDocumentRequest
		  ) -> None:
      ...
```
10. Удалить документ (если документа нет, выбросить читаемую ошибку):
```python
class DeleteDocumentUC:
	def __init__(): ...
	
    async def DeleteDocumentUC(
	      self,
		  document_id: int
		  ) -> None:
	  ...
```
11. Получить конкретный документ (если документа нет, выбросить читаемую ошибку):
```python
class GetDocumentUC:
	def __init__(): ...
	
    async def GetDocumentUC(
	      self,
		  document_id: int
		  ) -> Document:
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
