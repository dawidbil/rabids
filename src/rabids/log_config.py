import json
import logging
import os
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }

        if record.exc_info:
            log_data['error'] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> None:
    """Configure application-wide logging."""
    level_name = os.getenv('LOG_LEVEL', 'INFO')
    level = getattr(logging, level_name.upper(), logging.INFO)

    # Clear any existing handlers
    root_logger = logging.getLogger('rabids')
    root_logger.handlers.clear()

    root_logger.setLevel(level)
    root_logger.propagate = False  # Prevent duplicate logs

    # Console handler with JSON formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)


def load_api_keys() -> set[str]:
    """Load allowed API keys from environment variable."""
    api_keys_str = os.getenv('ALLOWED_API_KEYS', '')
    if not api_keys_str:
        raise ValueError('ALLOWED_API_KEYS environment variable must be set')
    return set(api_keys_str.split(','))
