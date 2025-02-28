from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import subprocess
import os
import secrets
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Paths to user files
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')
ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')

# Load users from file
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {
        'admin': {'password': 'admin123', 'role': 'admin'},
        'usuario': {'password': 'usuario123', 'role': 'user'}
    }

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Load tokens from .env file
def load_tokens():
    tokens = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith('USER_TOKEN_'):
                    key, value = line.strip().split('=', 1)
                    tokens[key.replace('USER_TOKEN_', '')] = value
    return tokens

# Save a token to .env file
def save_token(username, token):
    tokens = load_tokens()
    tokens[username] = token
    with open(ENV_FILE, 'w') as f:
        for user, tok in tokens.items():
            f.write(f'USER_TOKEN_{user}={tok}\n')

# Initialize users
USERS = load_users()

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

    def get_token(self):
        tokens = load_tokens()
        return tokens.get(self.id, '')

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id, USERS[user_id]['role'])
    return None

# Decorator for admin-only routes
def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated

# Log actions
def save_log(action, user_id):
    try:
        with open('logs.json', 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'action': action,
        'user_id': user_id
    }
    logs.append(log_entry)
    with open('logs.json', 'w') as f:
        json.dump(logs, f, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username]['password'] == password:
            user = User(username, USERS[username]['role'])
            login_user(user)
            save_log('Login', username)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    username = current_user.id
    save_log('Logout', username)
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Clear execution area
@app.route('/limpiar_ejecucion', methods=['GET'])
@login_required
def limpiar_ejecucion():
    username = current_user.id
    save_log('Clear execution area', username)
    return jsonify({'message': 'Execution area cleared'})

# Execute sequence of scripts
@app.route('/ejecutar_secuencia', methods=['GET'])
@login_required
def ejecutar_secuencia():
    username = current_user.id
    save_log('Ejecutar secuencia de scripts', username)
    scripts = ['CODE/Alpha_Espai_#1.py', 'CODE/Alpha_Espai_#2.py', 'CODE/Alpha_Espai_#3.py', 'CODE/Alpha_Espai_#10.py', 'CODE/Alpha_Espai_#11.py', 'CODE/Alpha_Espai_#12.py']
    resultados = []
    
    for script in scripts:
        try:
            script_path = os.path.join(os.path.dirname(__file__), script)
            print(f"Resolved script path: {script_path}")
            resultado = subprocess.run(
                ['python3', script_path],
                capture_output=True,
                text=True,
                check=True,
                bufsize=1  # Line-buffered
            )
            resultado.check_returncode()  # Ensure any non-zero exit codes are raised
            print(f"Output for {script}: {resultado.stdout}")  # Ensuring output is captured
            resultados.append(f" {script}:\n{resultado.stdout}\n")
        except subprocess.CalledProcessError as e:
            resultados.append(f" {script} - Error:\n{e.stderr}\n")
        except FileNotFoundError:
            resultados.append(f" {script} - Error: Archivo no encontrado\n")
    
    return "\n".join(resultados)

# Perform deletion
@app.route('/ejecutar_borrado', methods=['GET'])
@login_required
def ejecutar_borrado():
    username = current_user.id
    save_log('Perform deletion', username)

    # Clear execution area before performing deletion
    app.test_client().get('/limpiar_ejecucion')

    try:
        script_path = os.path.join(os.path.dirname(__file__), 'CODE/Alpha_Espai_#borrado.py')
        resultado = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return f"✅ Deletion executed:\n{resultado.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ Error during deletion:\n{e.stderr}"
    except FileNotFoundError:
        return "❌ Error: Deletion script not found"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)