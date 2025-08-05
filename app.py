import os
import random
import string
import secrets
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate secure random secret key

HISTORY_FILE = 'history.txt'
MAX_HISTORY = 100
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

# Default settings that will be used if not in session
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

def generate_password(length, use_upper, use_lower, use_digits, use_special, min_upper, min_lower, min_digits):
    if not (use_upper or use_lower or use_digits or use_special):
        raise ValueError("At least one character type must be selected.")

    if length < (min_upper + min_lower + min_digits):
        raise ValueError("Length is too short for the minimum counts specified.")

    chars = ''
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += SPECIAL_CHARACTERS

    password = []
    password += random.choices(string.ascii_uppercase, k=min_upper) if use_upper else []
    password += random.choices(string.ascii_lowercase, k=min_lower) if use_lower else []
    password += random.choices(string.digits, k=min_digits) if use_digits else []

    remaining = length - len(password)
    if remaining > 0:
        password += random.choices(chars, k=remaining)

    random.shuffle(password)
    return ''.join(password)

def save_to_history(password):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    entry = f"{now} | {password}\n"
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            f.write(entry)
        return

    with open(HISTORY_FILE, 'r') as f:
        lines = f.readlines()
    lines.append(entry)
    if len(lines) > MAX_HISTORY:
        lines = lines[-MAX_HISTORY:]
    with open(HISTORY_FILE, 'w') as f:
        f.writelines(lines)

def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines[::-1]]  # newest first

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    password = None
    
    # Initialize settings from session or defaults
    if 'settings' not in session:
        session['settings'] = DEFAULT_SETTINGS.copy()
    
    if request.method == 'POST':
        try:
            # Get form values
            length = int(request.form.get('length', 14))
            use_upper = request.form.get('use_upper') is not None
            use_lower = request.form.get('use_lower') is not None
            use_digits = request.form.get('use_digits') is not None
            use_special = request.form.get('use_special') is not None
            min_upper = int(request.form.get('min_upper', 1 if use_upper else 0))
            min_lower = int(request.form.get('min_lower', 1 if use_lower else 0))
            min_digits = int(request.form.get('min_digits', 1 if use_digits else 0))
            
            # Save user preferences to session
            session['settings'] = {
                'length': length,
                'use_upper': use_upper,
                'use_lower': use_lower,
                'use_digits': use_digits,
                'use_special': use_special,
                'min_upper': min_upper,
                'min_lower': min_lower,
                'min_digits': min_digits
            }
            
            # Generate password with user settings
            password = generate_password(
                length, use_upper, use_lower, use_digits, use_special,
                min_upper, min_lower, min_digits
            )
            save_to_history(password)
        except Exception as e:
            error = str(e)
    
    # Pass current settings to template
    settings = session.get('settings', DEFAULT_SETTINGS)
    return render_template('index.html', password=password, error=error, settings=settings)

@app.route('/history')
def history():
    history = get_history()
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
