import pytest
import streamlit as st
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import setup_logger

def test_setup_logger():
    """Test that the logger is set up correctly"""
    logger = setup_logger()
    assert logger is not None
    assert logger.name == 'chat_app'
    assert logger.level == 10  # DEBUG level

def test_logger_handlers():
    """Test that the logger has the correct handlers"""
    logger = setup_logger()
    assert len(logger.handlers) == 2  # Should have file and stream handlers
    
    # Check handler types
    handler_types = [type(handler) for handler in logger.handlers]
    assert RotatingFileHandler in handler_types
    assert logging.StreamHandler in handler_types
    
    # Check handler levels
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            assert handler.level == logging.DEBUG
        elif isinstance(handler, logging.StreamHandler):
            assert handler.level == logging.INFO 