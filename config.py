import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # API Configuration
    API_PREFIX = os.getenv('API_PREFIX', '/api/v1')

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
