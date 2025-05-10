# Dev notes

## Getting started

For running the api you need:

* Python3.13 venv 
* Docker engine

First create a venv using `python3.13 -m venv venv`. 

Activate venv using `venv\Scripts\activate.ps1` or `source venv/bin/activate` on UNIX systems. Install all required libraries using `python -m pip install -r requirements.txt`

## Starting up (docker)


### development environment

1. Start the docker engine
2. run `docker compose up -d maria pma`
3. run `uvicorn api.main:app --reload` 
4. navigate to `http://127.0.0.1:8000/docs`

## Starting up (non docker)

> [!NOTE]
> For the non-docker variant you need to have a running MariaDB instance on a server or your client. The credentials are to be added to the `.env` file respecrively 

Run command `uvicorn api.main:app --reload` 

## Env file

```env
MYSQL_USER=karmify
MYSQL_PASSWORD=Karmify
MYSQL_HOST=example.com
MYSQL_DATABASE=karmify
MYSQL_PORT=3306
DEBUG=True
SECRET_KEY="your_secret_key"

``` 
> [!CAUTION]
> Setting `DEBUG=True` **WILL DELETE** the entire database when reloaded. ALL DATA WILL BE GONE _IRREVERSBLY_.

> [!CAUTION]
>  Also change your secret key. It is against any best practices and violates ISO 27001 (A.9, A.10 and A.12) fundamentally.
>
> Generate a unique key using `openssl rand -hex 64`
