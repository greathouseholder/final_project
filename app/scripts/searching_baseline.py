import asyncio

import pandas as pd
from qdrant_client import AsyncQdrantClient
from tqdm.asyncio import tqdm_asyncio

from src.core.application.searching.schemas.search import SearchRequest
from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings import BGEEmbedder
from src.infra.adapters.llm.openaiGenerator import OpenAIClient
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.promts.jinjaPrompter import JinjaPrompter
from src.infra.adapters.rerank import BGEReranker
from src.infra.adapters.validation.validate_preprocessor import ValidatorPreprocessing
from src.infra.adapters.vdb.qdrantGateway import QdrantGateway

uc = SearchUC(
    vdb_gateway=QdrantGateway(client=AsyncQdrantClient(host='localhost', port=6333)),
    embedder=BGEEmbedder(),
    llm_adapter=LLMPreprocessor(
        client=OpenAIClient(),
        prompter=JinjaPrompter(),
        validator=ValidatorPreprocessing()
    ),
    reranker=BGEReranker()
)

questions = pd.read_csv('../data/questions_clean.csv')

async def search_baseline(query: str, collection: str):
    response = await uc.execute(
        request=SearchRequest(
            query=query,
            collection_name=collection,
            model='deepseek-r1'
        )
    )
    return response

async def mark_all_questions(collection: str):
    documents = []
    for index, row in tqdm_asyncio(questions.iterrows(), total=len(questions), desc="Отвечаем на вопросы"):
        response = await search_baseline(row['query'], collection)
        documents.append([res.metadata.get('web_id') for res in response])

    questions['web_ids'] = documents + [[] for _ in range(questions.shape[0] - len(documents))]
    questions.to_csv('../data/questions_marked.csv', index=False)
