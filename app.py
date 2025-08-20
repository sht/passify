"""
PassifyApp - Main application entry point
A secure password generator with customizable settings
"""
from passify import create_app

# Create the Flask application
app = create_app()

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)