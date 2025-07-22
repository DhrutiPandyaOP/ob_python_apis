import logging
import logging.handlers
import os
from datetime import datetime
from config import Config

class Logger:
    _instance = None
    _logger = None
    _logs = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_logger()
        return cls._instance

    @classmethod
    def _setup_logger(cls):
        """Setup logger configuration"""
        cls._logger = logging.getLogger('flask_api')
        cls._logger.setLevel(getattr(logging, Config.LOG_LEVEL))

        # Clear existing handlers
        cls._logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
        )

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=Config.LOG_MAX_BYTES,
            backupCount=Config.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(detailed_formatter)
        cls._logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(detailed_formatter)
        cls._logger.addHandler(console_handler)

        # Custom handler to store logs in memory
        memory_handler = cls.MemoryHandler()
        cls._logger.addHandler(memory_handler)

    class MemoryHandler(logging.Handler):
        def emit(self, record):
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.name,
                'function': record.funcName,
                'line': record.lineno
            }
            Logger._logs.append(log_entry)

            # Keep only last 1000 logs in memory
            if len(Logger._logs) > 1000:
                Logger._logs = Logger._logs[-1000:]

    @classmethod
    def get_logger(cls):
        """Get logger instance"""
        if cls._logger is None:
            cls()
        return cls._logger

    @classmethod
    def get_logs(cls, limit=100, level=None):
        """Get logs from memory"""
        logs = cls._logs

        # Filter by level if specified
        if level:
            logs = [log for log in logs if log['level'] == level.upper()]

        # Return last 'limit' logs
        return logs[-limit:]
