from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
from routes import data,nlp
from stores.llm.LLMProviderFactory import LLMProviderFactory 
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory 
from helpers.config import get_settings
app = FastAPI()  

async def startup_span():
    settings = get_settings()
    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                                embedding_size=settings.EMBEDDING_MODEL_SIZE) 
    
    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()


async def shutdown_span():
    app.vectordb_client.disconnect()

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(data.data_router) 
app.include_router(nlp.nlp_router)