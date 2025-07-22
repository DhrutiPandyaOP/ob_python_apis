from main import create_app
from logger_config import Logger

# Create the application instance
app = create_app()
logger = Logger.get_logger()

if __name__ == "__main__":
    app.run()
