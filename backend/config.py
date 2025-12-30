"""Configuration for ConvoScope backend"""
import os
from pathlib import Path

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32).hex())
    DEBUG = False
    TESTING = False

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    UPLOAD_FOLDER = BASE_DIR / '.uploads'
    CACHE_FOLDER = BASE_DIR / '.cache'
    RESULTS_FOLDER = BASE_DIR / '.results'

    # Create directories if they don't exist
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    CACHE_FOLDER.mkdir(exist_ok=True)
    RESULTS_FOLDER.mkdir(exist_ok=True)

    # Upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'json'}

    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Analysis settings
    MAX_CONCURRENT_JOBS = 2
    JOB_TIMEOUT = 600  # 10 minutes
    CACHE_MAX_SIZE = 1024 * 1024 * 1024  # 1GB

    # Cleanup settings
    FILE_RETENTION_HOURS = 24


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

    # Use environment variables in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
