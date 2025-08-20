"""Test configuration and fixtures"""
import pytest
import os
import tempfile
from unittest.mock import patch
from passify import create_app


@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()


@pytest.fixture
def test_history_file():
    """Create a temporary history file for testing"""
    # Create a temporary test file path
    test_file = os.path.join(tempfile.gettempdir(), 'test_history.txt')
    
    # Ensure the file doesn't exist at start
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Patch the HISTORY_FILE constant
    with patch('passify.utils.constants.HISTORY_FILE', test_file):
        yield test_file
    
    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)