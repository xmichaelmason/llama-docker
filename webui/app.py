from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from redis import StrictRedis
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MariaDB (MySQL) Configuration
mariadb_user = os.getenv("MYSQL_USER")
mariadb_password = os.getenv("MYSQL_PASSWORD")
mariadb_port = os.getenv("MYSQL_PORT")
mariadb_database = os.getenv("MYSQL_DATABASE")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{mariadb_user}:{mariadb_password}@mariadb:{mariadb_port}/{mariadb_database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MongoDB Configuration
mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
mongo_port = os.getenv("MONGO_PORT")
mongo_client = MongoClient(f'mongodb://{mongo_user}:{mongo_password}@mongo:{mongo_port}')
mongo_db = mongo_client['mongo-example']

# Redis Configuration
redis_client = StrictRedis(host='redis', port=os.getenv("REDIS_PORT"), password=os.getenv("REDIS_PASSWORD"))

# OpenAI configuration
openai_client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    mariadb_status = "MariaDB connection successful"
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT DATABASE()") ) # Execute SQL query to fetch the current database name
        current_database = result.scalar()
        mariadb_status = f"Connected to MariaDB database: {current_database}"
    except Exception as e:
        mariadb_status = f"Error connecting to MariaDB: {str(e)}"
    finally:
        db.close()

    # Test MongoDB Connection
    mongo_status = "MongoDB connection successful"
    try:
        mongo_client.server_info()
    except Exception as e:
        mongo_status = f"Error connecting to MongoDB: {str(e)}"

    # Test Redis Connection
    redis_status = "Redis connection successful"
    try:
        redis_client.ping()
    except Exception as e:
        redis_status = f"Error connecting to Redis: {str(e)}"

    openai_status = "OpenAI connection successful"
    try:
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )
        openai_status = chat_completion.choices[0].message.content
    except Exception as e:
        openai_status = f"Error connecting to OpenAI: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "mariadb_status": mariadb_status, "mongo_status": mongo_status, "redis_status": redis_status, "openai_status": openai_status})