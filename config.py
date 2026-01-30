# config.py
import os

class Config:
    """Application configuration"""
    MONGODB_URI = os.environ.get('MONGODB_URI')
    MONGODB_DB = 'github_webhooks'
    EVENTS_COLLECTION = 'events'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5000))