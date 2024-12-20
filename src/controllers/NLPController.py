from .BaseController import BaseController
from stores.llm.LLMEnums import DocumentTypeEnum 
from typing import List
import json
from stores.llm import OpenAIProvider
from stores.vectordb import QdrantDBProvider
from helpers.constants import AppConstants


class NLPController(BaseController):

    def __init__(self, vectordb_client:QdrantDBProvider ,embedding_client:OpenAIProvider):
        super().__init__()

        self.vectordb_client:QdrantDBProvider = vectordb_client
        self.embedding_client:OpenAIProvider = embedding_client
    
    
    def get_vector_db_collection_info(self):
        collection_info = self.vectordb_client.get_collection_info(collection_name=AppConstants.QDRANT_COLLECTION_NAME)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, chunks:list):

        # step2: manage items
        texts = [ c.page_content for c in chunks ]
        metadata = [ c.metadata for c in  chunks]
        vectors = [
            self.embedding_client.embed_text(text=text, document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # step3: create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=AppConstants.QDRANT_COLLECTION_NAME,
            embedding_size=self.embedding_client.embedding_size,
        )

        # step4: insert into vector db
        _ = self.vectordb_client.insert_many(
            collection_name=AppConstants.QDRANT_COLLECTION_NAME,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
        )

        return True

    def search_vector_db_collection(self, text: str, limit: int = 10):

        # step2: get text embedding vector
        vector = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False

        # step3: do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=AppConstants.QDRANT_COLLECTION_NAME,
            vector=vector,
            limit=limit
        )

        if not results:
            return False

        return results
    
    