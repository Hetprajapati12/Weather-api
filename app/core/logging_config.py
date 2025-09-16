"""
Logging configuration module for the Weather API application.
Sets up structured logging with proper formatting and levels.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from .config import config


class LoggingConfiguration:
    """
    Manages logging configuration for the application.
    Sets up file and console logging with proper formatting.
    """
    
    _configured: bool = False
    
    @classmethod
    def setup_logging(cls) -> None:
        """
        Configure logging for the application.
        Sets up both file and console handlers with appropriate formatting.
        """
        if cls._configured:
            return
        
        # Create logs directory if it doesn't exist
        log_path = Path(config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            filename=config.log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to root logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        cls._configured = True
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: The name of the logger (usually __name__)
            
        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)