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
#### Проверка на админа
1. Проверить, является ли пользователь админом:
```python
class CheckAdminUC:
	def __init__(): ...
	
	async def execute(
          self,
		  telegram_id: int
		  ) -> bool:
      ...
```
#### Коллекции
2. Вывести список доступных пользователю коллекций:
```python
class GetAvaliableCollectionsUC:
	def __init__(): ...
	
    async def execute(
	      self,
		  telegram_id: int
		  ) -> List[Collection]: # domain сущность; не написана
      ...
```
3. Создание новой коллекции:
```python
class CreateCollectionUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: CreateCollectionRequest # use case сущность; не написана
		  ) -> Collection: # domain сущность; не написана
      ...
```
4. Обновление данных коллекции:
```python
class UpdateCollectionUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: UpdateCollectionRequest # use case сущность; не написана
		  ) -> None:
      ...
```
5. Удалить коллекцию:
```python
class DeleteCollectionUC:
	def __init__(): ...
	
    async def DeleteCollectionUC(
	      self,
		  collection_id: int
		  ) -> None:
	  ...
```
6. Получить конкретную коллекцию:
```python
class GetCollectionUC:
	def __init__(): ...
	
    async def GetCollectionUC(
	      self,
		  collection_id: int
		  ) -> Collection: # domain сущность; не написана
	  ...
```
#### Документы
7. Вывести список доступных пользователю документов в коллекции:
```python
class GetAvaliableDocumentsUC:
	def __init__(): ...
	
    async def execute(
	      self,
		  request: GetAvaliableDocumentRequest # use case сущность; не написана
		  ) -> List[Document]: # domain сущность; не написана
      ...
```
8. Загрузить документы в коллекцию (уже существует, лежит в `src/application/embeddings/`, необходимо дописать):
```python
class  LoadingUC:
	__slots__  = ("_vdb_gateway",  "_embedder",  "_chunk_adapter")
	
	def  __init__(): ...

	async def execute(
		  self, 
		  request:  LoadDataRequest # use case сущность; написана; 
		  ) -> Result[str,  Any]: # что это 😭???
		  					      # учитывая новый API,
								  # необходимо возвращать
								  # сущность Document
		# вернее говоря, надо разобраться, что у нас с сущностями
		# CoreDocument и пр, и, как один из вариантов, отнаследоваться
		# от CoreDocument, чтобы создать новую сущность, которую
		# можно вернуть в API, чтобы преобразовать там всё с кайфом
		# пишите Саше короче
      ...
```
9. Обновление данных документа:
```python
class UpdateDocumentUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: UpdateDocumentRequest # use case сущность; не написана
		  ) -> None:
      ...
```
10. Удалить коллекцию:
```python
class DeleteDocumentUC:
	def __init__(): ...
	
    async def DeleteDocumentUC(
	      self,
		  document_id: int
		  ) -> None:
	  ...
```
11. Получить конкретный документ:
```python
class GetDocumentUC:
	def __init__(): ...
	
    async def GetDocumentUC(
	      self,
		  document_id: int
		  ) -> Document: # domain сущность; не написана
	  ...
```
#### Диалоги ~~(тет-а-тет, до утра за «жили-были»)~~
6. Вывести список доступных пользователю диалогов:
```python
class GetAvaliableConversationsUC:
	def __init__(): ...
	
    async def execute(
	      self,
		  telegram_id: int
		  ) -> List[Conversation]: # domain сущность; не написана
      ...
```
7. Создание нового диалога:
```python
class CreateConversationUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: CreateConversationRequest # use case сущность; не написана
		  ) -> Conversation: # domain сущность; не написана
      ...
```
8. Обновление данных диалога:
```python
class UpdateConversationUC:
	def __init__(): ...
	
	async def execute(
          self,
		  request: UpdateConversationRequest # use case сущность; не написана
		  ) -> None:
      ...
```
9. Удалить диалог:
```python
class DeleteConversationUC:
	def __init__(): ...
	
    async def DeleteConversationUC(
	      self,
		  conversation_id: int
		  ) -> None:
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