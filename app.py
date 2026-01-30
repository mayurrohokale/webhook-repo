from flask import Flask
from flask_cors import CORS
from config import Config
from database import Database
from routes import webhook_bp, api_bp, init_routes

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db = Database(
        uri=app.config['MONGODB_URI'],
        db_name=app.config['MONGODB_DB'],
        collection_name=app.config['EVENTS_COLLECTION']
    )
    
    # Initialize routes with database
    init_routes(db)
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(api_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=app.config['DEBUG'],
        port=app.config['PORT']
    )