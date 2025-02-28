from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import subprocess
import os
import secrets
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Cambiar esto en producción

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Ruta al archivo de usuarios
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

# Ruta al archivo .env para almacenar tokens
ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')

# Cargar usuarios desde archivo
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {
                'admin': {
                    'password': 'admin123',
                    'role': 'admin'
                },
                'usuario': {
                    'password': 'usuario123',
                    'role': 'user'
                }
            }
    return {
        'admin': {
            'password': 'admin123',
            'role': 'admin'
        },
        'usuario': {
            'password': 'usuario123',
            'role': 'user'
        }
    }

# Guardar usuarios en archivo
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Función para cargar tokens desde el archivo .env
def load_tokens():
    tokens = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith('USER_TOKEN_'):
                    key, value = line.strip().split('=', 1)
                    tokens[key.replace('USER_TOKEN_', '')] = value
    return tokens

# Función para guardar un token en el archivo .env
def save_token(username, token):
    tokens = load_tokens()
    tokens[username] = token
    with open(ENV_FILE, 'w') as f:
        for user, tok in tokens.items():
            f.write(f'USER_TOKEN_{user}={tok}\n')

# Inicializar usuarios desde archivo
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

def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'Se requieren permisos de administrador'}), 403
        return f(*args, **kwargs)
    return decorated

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
            save_log('Inicio de sesión', username)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    username = current_user.id
    save_log('Cierre de sesión', username)
    logout_user()
    flash('Has cerrado sesión correctamente')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/ejecutar_secuencia', methods=['GET'])
@login_required
def ejecutar_secuencia():
    username = current_user.id
    save_log('Ejecutar secuencia de scripts', username)
    #scripts = ['CODE/Alpha_Espai_#1.py', 'CODE/Alpha_Espai_#2.py', 'CODE/Alpha_Espai_#3.py', 'CODE/Alpha_Espai_#3b.py']
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

@app.route('/ejecutar_borrado', methods=['GET'])
@login_required
def ejecutar_borrado():
    username = current_user.id
    save_log('Ejecutar borrado', username)
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'CODE/Alpha_Espai_#borrado.py')
        print(f"Resolved script path: {script_path}")
        resultado = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return f"✅ Borrado ejecutado:\n{resultado.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ Error en el borrado:\n{e.stderr}"
    except FileNotFoundError:
        return "❌ Error: Archivo Alpha_Espai_#4.py no encontrado"

@app.route('/api/ejecutar_secuencia', methods=['POST'])
@login_required
def api_ejecutar_secuencia():
    username = current_user.id
    save_log('Ejecutar secuencia de scripts (API)', username)
    #scripts = ['CODE/Alpha_Espai_#1.py', 'CODE/Alpha_Espai_#2.py', 'CODE/Alpha_Espai_#3.py', 'CODE/Alpha_Espai_#3b.py']
    scripts = ['CODE/Alpha_Espai_#1.py', 'CODE/Alpha_Espai_#2.py', 'CODE/Alpha_Espai_#3.py','CODE/Alpha_Espai_#10.py', 'CODE/Alpha_Espai_#11.py', 'CODE/Alpha_Espai_#12.py']
    resultados = []
    
    for script in scripts:
        try:
            script_path = os.path.join(os.path.dirname(__file__), script)
            print(f"\nEjecutando {script}...")
            proceso = subprocess.Popen(
                ['/Library/Frameworks/Python.framework/Versions/3.12/bin/python3', script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                env={**os.environ, 'PYTHONUNBUFFERED': '1'}  # Forzar salida sin buffer
            )
            
            # Capturar la salida en tiempo real
            stdout_data = []
            stderr_data = []
            
            while True:
                stdout_line = proceso.stdout.readline()
                stderr_line = proceso.stderr.readline()
                
                if stdout_line:
                    print(f"Salida de {script}: {stdout_line.strip()}")
                    stdout_data.append(stdout_line)
                if stderr_line:
                    print(f"Error de {script}: {stderr_line.strip()}")
                    stderr_data.append(stderr_line)
                    
                if not stdout_line and not stderr_line and proceso.poll() is not None:
                    break
            
            stdout_output = ''.join(stdout_data)
            stderr_output = ''.join(stderr_data)
            
            if proceso.returncode == 0:
                resultados.append({
                    'script': script,
                    'output': stdout_output if stdout_output else "Script ejecutado correctamente sin salida",
                    'status': 'success'
                })
            else:
                resultados.append({
                    'script': script,
                    'output': stderr_output if stderr_output else "Error sin mensaje",
                    'status': 'error'
                })
        except Exception as e:
            print(f"Exception for {script}: {str(e)}")
            resultados.append({
                'script': script,
                'output': str(e),
                'status': 'error'
            })
    
    return jsonify(resultados)

@app.route('/api/token', methods=['POST'])
@login_required
@require_admin
def generar_token():
    username = current_user.id
    save_log('Generar token API', username)
    
    # Generar nuevo token
    new_token = secrets.token_urlsafe(32)
    
    # Guardar el nuevo token
    save_token(username, new_token)
    
    return jsonify({
        'message': 'Token generado correctamente',
        'token': new_token
    })

@app.route('/api/tokens', methods=['GET'])
@login_required
@require_admin
def listar_tokens():
    username = current_user.id
    save_log('Listar tokens API', username)
    
    tokens = load_tokens()
    user_token = tokens.get(username, '')
    
    return jsonify({'success': True, 'tokens': [user_token]})

@app.route('/admin/users', methods=['GET'])
@login_required
@require_admin
def list_users():
    username = current_user.id
    save_log('Listar usuarios', username)
    return jsonify({
        'users': [{
            'username': username,
            'role': data['role']
        } for username, data in USERS.items()]
    })

@app.route('/admin/users', methods=['POST'])
@login_required
@require_admin
def create_user():
    username = current_user.id
    save_log('Crear usuario', username)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not username or not password:
        return jsonify({'error': 'Se requiere username y password'}), 400
    
    if username in USERS:
        return jsonify({'error': 'El usuario ya existe'}), 409
    
    if role not in ['admin', 'user']:
        return jsonify({'error': 'Rol inválido'}), 400
    
    USERS[username] = {
        'password': password,
        'role': role
    }
    save_users(USERS)
    
    return jsonify({
        'message': 'Usuario creado correctamente',
        'user': {'username': username, 'role': role}
    })

@app.route('/admin/users/<username>', methods=['PUT'])
@login_required
@require_admin
def update_user(username):
    admin_username = current_user.id
    save_log(f'Actualizar usuario: {username}', admin_username)
    if username not in USERS:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    if 'password' in data:
        USERS[username]['password'] = data['password']
    if 'role' in data:
        if data['role'] not in ['admin', 'user']:
            return jsonify({'error': 'Rol inválido'}), 400
        USERS[username]['role'] = data['role']
    
    save_users(USERS)
    return jsonify({
        'message': 'Usuario actualizado correctamente',
        'user': {'username': username, 'role': USERS[username]['role']}
    })

@app.route('/admin/users/<username>', methods=['DELETE'])
@login_required
@require_admin
def delete_user(username):
    admin_username = current_user.id
    save_log(f'Eliminar usuario: {username}', admin_username)
    if username not in USERS:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    if username == current_user.id:
        return jsonify({'error': 'No puedes eliminar tu propio usuario'}), 400
    
    if username == 'admin':
        return jsonify({'error': 'No se puede eliminar el usuario admin'}), 400
    
    del USERS[username]
    save_users(USERS)
    return jsonify({'message': 'Usuario eliminado correctamente'})

@app.route('/get_logs')
@login_required
@require_admin
def get_logs():
    try:
        with open('logs.json', 'r') as f:
            logs = json.load(f)
        return jsonify({'success': True, 'logs': logs})
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'success': False, 'error': 'No hay registros disponibles'})

@app.route('/borrar_logs', methods=['POST'])
@login_required
def borrar_logs():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'No tienes permisos para realizar esta acción'})
    
    try:
        # Guardar un log vacío
        with open('logs.json', 'w') as f:
            json.dump([], f, indent=4)
        
        # Registrar la acción de borrado
        save_log('Borrado de logs', current_user.id)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
