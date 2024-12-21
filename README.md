# Applab_Assessment_chatbot

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
# API Documentation - Swagger : 
This project uses Swagger to provide an interactive API documentation interface 
# Accessing the Documentation:  
You can access the Swagger documentation by navigating to the following URL once the application is running: 
```bash
$ http://localhost:<PORT>docs
``` 
we have 2 endpoint :
1) upload file endpoint 
    request: post
    payload:pdf_file
    response signal expectation :file uploaded success 
    process :
    1) upload pdf_file
    2) Extract text and process the data with split file to chunkes y langchain
    3) embeddeing file_chunkes 
    4) store vector in Qdatent 
2) chat endpoint
    request : post
    payload : user_query ,limit(number of the responce)
    response signal expectation : get the best score response
    process : 
    1) apply search vector qdrant query  


### chatbot’s features and functionalities. 



### application overview : 


