"""
PassifyApp - A secure password generator application
"""
from flask import Flask

def create_app():
    """Initialize the Flask application"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Import and register blueprints
    from passify.core.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Secret key
    import secrets
    app.secret_key = secrets.token_hex(16)
    
    return app