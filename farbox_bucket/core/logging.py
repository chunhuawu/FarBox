"""
Centralized logging configuration to replace DEBUG flags.
Provides proper logging levels and structured logging support.
"""
import logging
import sys
from typing import Optional
from pathlib import Path


class LoggerManager:
    """
    Centralized logger management.
    Replaces scattered DEBUG flags with proper logging.
    """

    _configured = False

    @classmethod
    def configure(
        cls,
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        format_string: Optional[str] = None,
    ) -> None:
        """
        Configure application-wide logging.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for logs
            format_string: Custom format string
        """
        if cls._configured:
            return

        if format_string is None:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(format_string))
        root_logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(format_string))
            root_logger.addHandler(file_handler)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a logger instance.

        Args:
            name: Logger name (usually __name__)

        Returns:
            Logger instance
        """
        if not cls._configured:
            cls.configure()
        return logging.getLogger(name)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance (convenience function).

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return LoggerManager.get_logger(name)
