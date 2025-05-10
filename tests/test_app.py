import pytest
import streamlit as st
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