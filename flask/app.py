from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from redis import StrictRedis
from openai import OpenAI

app = Flask(__name__)

# MariaDB (MySQL) Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:test@mariadb:3306/mariadb-example'
db = SQLAlchemy(app)

# MongoDB Configuration
mongo_client = MongoClient('mongodb://admin:test@mongo:27017')
mongo_db = mongo_client['mongo-example']

# Redis Configuration
redis_client = StrictRedis(host='redis', port=6379, password='test')

# OpenAI configuration
openai_client = OpenAI(base_url="http://192.168.1.100:5001/v1", api_key="sk-1234")

@app.route('/')
def hello():
    # Test MariaDB Connection
    mariadb_status = "MariaDB connection successful"
    try:
        db.engine.connect()
    except Exception as e:
        mariadb_status = f"Error connecting to MariaDB: {str(e)}"

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

    

    return render_template('index.html', mariadb_status=mariadb_status, mongo_status=mongo_status, redis_status=redis_status, qdrant_status=qdrant_status, openai_status=openai_status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
