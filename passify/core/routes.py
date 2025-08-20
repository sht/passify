"""Route definitions for the application"""
import io
from flask import Blueprint, render_template, request, redirect
from flask import url_for, session, send_file, Response

from passify.core.password_generator import PasswordGenerator
from passify.models.history import PasswordHistory
from passify.utils.constants import DEFAULT_SETTINGS
from passify.components.display import PasswordDisplay, Card
from passify.components.forms import PasswordForm

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    """Main page for password generation"""
    error = None
    password = None
    
    # Initialize settings from session or defaults
    if 'settings' not in session:
        session['settings'] = DEFAULT_SETTINGS.copy()
    
    if request.method == 'POST':
        try:
            # Get form values
            settings = {
                'length': int(request.form.get('length', 14)),
                'use_upper': request.form.get('use_upper') is not None,
                'use_lower': request.form.get('use_lower') is not None,
                'use_digits': request.form.get('use_digits') is not None,
                'use_special': request.form.get('use_special') is not None,
                'min_upper': int(request.form.get('min_upper', 1) if request.form.get('use_upper') else 0),
                'min_lower': int(request.form.get('min_lower', 1) if request.form.get('use_lower') else 0),
                'min_digits': int(request.form.get('min_digits', 1) if request.form.get('use_digits') else 0),
            }
            
            # Update session settings
            session['settings'] = settings
            
            # Generate password
            generator = PasswordGenerator(**settings)
            password = generator.generate()
            
            # Save to history
            PasswordHistory.save(password)
            
        except Exception as e:
            error = str(e)
    
    # Pass current settings to template
    settings = session.get('settings', DEFAULT_SETTINGS)
    
    # For server-side rendering, always use regular templates
    return render_template('index.html', 
                          password=password, 
                          error=error, 
                          settings=settings)

@main_bp.route('/history')
def history():
    """Password history page"""
    history_entries = PasswordHistory.get_all()
    return render_template('history.html', history=history_entries)

@main_bp.route('/export')
def export_history():
    """Export password history as file download"""
    content = PasswordHistory.export()
    if not content:
        return Response("No history to export", mimetype="text/plain")
    
    # Create in-memory file
    buffer = io.BytesIO(content.encode('utf-8'))
    buffer.seek(0)
    
    # Create response
    return send_file(
        buffer,
        mimetype="text/plain",
        as_attachment=True,
        download_name="password_history.txt"
    )

@main_bp.route('/clear', methods=['POST'])
def clear_history():
    """Clear all password history"""
    PasswordHistory.clear()
    return redirect(url_for('main.history'))