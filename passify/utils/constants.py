"""Application constants"""
import os
import tempfile

# File paths
TEMP_DIR = tempfile.gettempdir()
HISTORY_FILE = os.path.join(TEMP_DIR, 'history.txt')

# Password settings
MAX_HISTORY = 100
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

# Default settings
DEFAULT_SETTINGS = {
    'length': 14,
    'use_upper': True,
    'use_lower': True,
    'use_digits': True,
    'use_special': False,
    'min_upper': 1,
    'min_lower': 1,
    'min_digits': 1
}