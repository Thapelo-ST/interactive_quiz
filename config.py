import os
import redis

# MongoDB configuration
MONGODB_SETTINGS = {
    'host': os.environ.get('MONGO_URI', 'mongodb://localhost:27017/your_database_name')
}

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))

# Secret key for session management
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Flask-Session configuration
SESSION_TYPE = 'redis'
SESSION_REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
