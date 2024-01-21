from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from redis import StrictRedis

app = Flask(__name__)

# MariaDB (MySQL) Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:test@mariadb:3306/mariadb-example'
db = SQLAlchemy(app)

# MongoDB Configuration
mongo_client = MongoClient('mongodb://admin:test@mongo:27017')
mongo_db = mongo_client['mongo-example']

# Redis Configuration
redis_client = StrictRedis(host='redis', port=6379, password='test')

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

    return render_template('index.html', mariadb_status=mariadb_status, mongo_status=mongo_status, redis_status=redis_status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
