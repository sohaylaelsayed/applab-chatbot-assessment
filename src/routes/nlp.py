import logging
from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
from routes.schemes.nlp import PushRequest, SearchRequest
from controllers import NLPController
from models import ResponseSignal


logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(prefix="/api/v1/nlp")


@nlp_router.post("/index/search")
async def search_index(request: Request, search_request: SearchRequest):
    
    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client
    )

    results = nlp_controller.search_vector_db_collection(text=search_request.text, limit=search_request.limit
    )

    if not results:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.VECTORDB_SEARCH_ERROR.value
                }
            )
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTORDB_SEARCH_SUCCESS.value,
            "results": [ result.dict()  for result in results ]
        }
    )

