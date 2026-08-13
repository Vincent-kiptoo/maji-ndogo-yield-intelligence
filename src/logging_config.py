"""
This module provides a reusable logger factory that configures logging for both console and file outputs.
The logger supports configurable log levels and automatically creates log directories if they do not exists
"""

import os
import logging

def get_logger(name: str, level: str = "INFO", log_file: str = "logs/pipeline.log") -> logging.Logger:
    """
    Returns a configured logger that writes to both the console and a file.
    safe to call multiple times without duplicating handlers
    """
    logger = logging.getLogger(name)
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt = "%(asctime)s | %(name)s | %(levelname)s | %(message)s", 
        datefmt ="%Y-%m-%d %H:%M:%S" 
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.propagate = False

    return logger