# Simple Assessment Chatbot

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.10

#### Install Python using poetry

1) Download and install poetry from [here](https://pypi.org/project/poetry/)

2) create and Activate the environment:
```bash
$ poetry shell 
``` 


## Installation

### Install the required packages

```bash
$ poetry install
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. like `OPENAI_API_KEY` Value . 


### Build Dockerfiles for both Backend and UI Services
```bash

$ cp dockers/ChatBotServiceDockerfile ./ChatBotServiceDockerfile
$ docker build -t chatbotservice:latest -f ChatBotServiceDockerfile .
$ docker run -p 8000:8000 --name chatbotservice -e OPENAI_API_KEY=<your_api_key> chatbotservice:latest

$ cp dockers/ChatbotUIDockerfile ./ChatbotUIDockerfile
$ docker build -t chatbotui:latest -f ChatbotUIDockerfile .
$ docker run -p 8501:8501 --name chatbotui chatbotui:latest

```

### Run the FastAPI server 
```bash
$ uvicorn main:app --reload  
```

### API documentation
#### API Documentation - Swagger : 
This project uses Swagger to provide an interactive API documentation interface 
#### Accessing the Documentation:  
You can access the Swagger documentation by navigating to the following URL once the application is running. 

We have 2 endpoints :
1) upload file endpoint :
    1) Request_type: post
    2) Payload:pdf_file
    3) Response signal expectation :file uploaded success 
    4) Process :
        1) upload pdf_file.
        2) Extract text and process the data with split file to chunkes by langchain.
        3) embeddeing file_chunkes .
        4) store vector in Qdrent .
2) chat endpoint: 
    1) Request_type : post.
    2) Payload : user_query ,limit.
    3) Response signal expectation : get the best score response.
    4) Process : 
        1) apply search vector qdrant query .  

For more details please review OpenAPI.yaml .


### chatbot’s features and functionalities.  

1) Upload PDF document to prepare the chatbot knowledge base
2) Chunking the uploaded docs and embedding it using NLP techniques to prepare the chunks for semantic search
3) Store the embedding texts using vector database provider - we have used QDrant here -
4) Retrieve the response of user's questions with the highest score of accuracy 
 





