from .BaseController import BaseController
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from helpers.constants import AppConstants

class ProcessController(BaseController):

    def __init__(self):
        super().__init__()

    def get_file_content(self, file_path: str):

        loader =PyMuPDFLoader(file_path)
        return loader.load()

    def process_file_content(self, file_content: list,
                            chunk_size: int=100, overlap_size: int=20):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks


    def generate_chunks(self, file_path:str):
        file_content = self.get_file_content(file_path)
        file_chunks = self.process_file_content(
            file_content=file_content,
            chunk_size=AppConstants.CHUNK_SIZE,
            overlap_size=AppConstants.OVERLAP_SIZE
        )
        return file_chunks


