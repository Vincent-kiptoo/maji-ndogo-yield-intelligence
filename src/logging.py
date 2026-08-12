"""
This module provides a reusable logger factory that configures logging for both console and file outputs.
The logger supports configurable log levels and automatically creates log directories if they do not exists
"""

import os
import logging

def get_logger(name: str, level: str = "INFO", log_file: str = "logs/pipeline.log") -> logging.Logger:
    """
    Returns a configured logger that writes to both 
    """