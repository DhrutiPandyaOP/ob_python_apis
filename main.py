from flask import Flask
import importlib
import os
import sys
from config import Config
from logger_config import Logger

def create_app():
    """Application factory pattern with auto-reload"""
    app = Flask(__name__)

    # Enable debug mode and auto-reload
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'

    # Setup logging
    logger = Logger.get_logger()

    try:
        from welcome import welcome_bp
        app.register_blueprint(welcome_bp)
    except ImportError:
        logger.warning("Welcome module not found, using default route")
        # Fallback welcome route if welcome.py doesn't exist
        @app.route('/')
        def welcome():
            return '<h1>Welcome to Flask API Service</h1><p>API is running at /api</p>'

    # Auto-register API blueprints
    register_api_routes(app, logger)

    return app

def register_api_routes(app, logger):
    """Automatically register all API routes from api/ directory"""
    api_dir = 'api'
    api_prefix = Config.API_PREFIX

    if not os.path.exists(api_dir):
        logger.error(f"API directory '{api_dir}' not found")
        return

    # Get all Python files in api directory
    for filename in os.listdir(api_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # Remove .py extension

            try:
                # Import the module
                module = importlib.import_module(f'{api_dir}.{module_name}')

                # Check if module has a blueprint
                if hasattr(module, 'bp'):
                    app.register_blueprint(module.bp, url_prefix=api_prefix)
                else:
                    logger.warning(f"Module {module_name} has no 'bp' blueprint")

            except Exception as e:
                logger.error(f"Failed to import {module_name}: {str(e)}")

def main():
    """Main entry point with auto-reload enabled"""
    app = create_app()
    logger = Logger.get_logger()

    try:
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=True,
            use_reloader=True,
            use_debugger=True,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
