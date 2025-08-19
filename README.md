# mini-rag-app
This is minimal implementation of RAG model for question answering inspired by [mini-rag](https://github.com/bakrianoo/mini-rag).

## Requirements
- pthon 3.8 or later 
### Install python using miniConda
1) Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/install)
2) Create a new environment using the following command:
```
$ conda create -n mini-rag-app python=3.8

```

3) Activate the environment 
``` bash
$ conda activate mini-rag-app 

```

# Installation
### install the required packages
```bash
$ pip install -r requirements.txt
```
### Setup the environment variables
```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file Like `OPENAI_API_KEY` value.

## Run Docker Compose Services

```bash
$ cd docker
$ cd .env.example .env

```

- update `.env`  with your credentials

## Run the FastAPI server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Postman collection
Download the POSTMAN collection from [assets/mini-rag-app.postman_collection.json](assets/mini-rag-app.postman_collection.json)



### docker cleaning 

```bash
$ docker stop $(docker ps -aq)
$ docker rm $(docker ps -aq)  
$ docker rmi $(docker images -q)
$ docker volume rm $(docker docker volume ls -q)
$ docker system prune --all  
```