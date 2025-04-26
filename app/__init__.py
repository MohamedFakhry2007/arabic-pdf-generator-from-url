import os
from flask import Flask
from loguru import logger
from dotenv import load_dotenv

# Configure logger
logger.add("logs/app.log", rotation="10 MB", level="INFO")

def create_app():
    """
    Factory function to create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance
    """
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app from config.py
    from app.config import Config
    app.config.from_object(Config)
    
    # Register routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    logger.info("Application initialized successfully")
    return app