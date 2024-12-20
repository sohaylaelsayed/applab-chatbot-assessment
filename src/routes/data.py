import logging
from fastapi import HTTPException, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.constants import AppConstants
from helpers.config import Settings, get_settings
from controllers import DataController, ProcessController, NLPController
import aiofiles
from models import ResponseSignal

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data")

@data_router.post("/upload")
async def upload_data(request: Request, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    """
    Upload pdf file and processing it
    """
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, result_signal)

    file_path = data_controller.get_target_filepath()

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
        logger.debug("File has been uploaded successfully")
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ResponseSignal.FILE_UPLOAD_FAILED.value)

    try:
        process_controller = ProcessController()
        file_chunks = process_controller.generate_chunks(file_path)
        if file_chunks is None or len(file_chunks) == 0:
            raise Exception(ResponseSignal.EMPTY_CHUNKS.value)
        logger.debug("File has been processed to multiple chunks successfully")
    except Exception as e:
        logger.error(f"Error while processing file: {e}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ResponseSignal.FILE_PROCESS_FAILED.value)

    try:
        nlp_controller = NLPController(
            vectordb_client=request.app.vectordb_client,
            embedding_client=request.app.embedding_client,
        )
        nlp_controller.index_into_vector_db(chunks=file_chunks)
        logger.debug("File chunks has been embedded and stored in target NLP provider successfully")
    except Exception as e:
        logger.error(f"Error while embedding file chunks: {e}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, ResponseSignal.FILE_PROCESS_FAILED.value)

    return JSONResponse({"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value}) 




