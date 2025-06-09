# mini-rag-app
This is minimal implementation of RAG model for question answering.

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