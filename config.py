import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base Configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'campus-connect-dev-secret-key-change-in-prod-2026'
    
    # Handle database URL with Render postgresql fix
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{os.path.join(basedir, 'campus_connect.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024)  # 16 MB max upload
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    ALLOWED_DOC_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'txt'}
    
    # Session security (Configured for iframe & cross-site embedding in AI Studio)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_NAME = 'campus_connect_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_PARTITIONED = True
    REMEMBER_COOKIE_NAME = 'campus_connect_remember'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'None'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    # CSRF Protection Settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = False
    WTF_CSRF_TIME_LIMIT = None  # Prevents CSRF expiry during long form filling
    WTF_CSRF_CHECK_DEFAULT = True
    
    # Application settings
    APP_NAME = "Campus Connect"
    COLLEGE_NAME = "Apex Institute of Technology & Science"
    COLLEGE_ADDRESS = "Knowledge City, Expressway Campus, Tech District"
    COLLEGE_EMAIL = "contact@apextech.edu"
    COLLEGE_PHONE = "+91 98765 43210"


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig if os.environ.get('FLASK_ENV') != 'production' else ProductionConfig
}
