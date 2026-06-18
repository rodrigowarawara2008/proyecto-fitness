from flask import Blueprint, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

usuarios_bp = Blueprint('usuarios', __name__)

def conectar():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )

# =========================
# REGISTRO
# =========================
@usuarios_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            print("FORMULARIO DE REGISTRO RECIBIDO")
            nombre = request.form['nombre']
            correo = request.form['correo']
            password = generate_password_hash(request.form['password'])
            
            conexion = conectar()
            cursor = conexion.cursor()
            sql = """
            INSERT INTO usuarios
            (nombre, correo, password, es_admin)
            VALUES (%s,%s,%s, 0)
            """
            cursor.execute(sql, (nombre, correo, password))
            conexion.commit()
            print("USUARIO REGISTRADO CORRECTAMENTE")
            cursor.close()
            conexion.close()
            return redirect('/login')
        except Exception as e:
            print("ERROR EN REGISTRO:")
            print(e)
            return f"Error: {e}"
    
    return render_template('usuarios/registro.html')

# =========================
# LOGIN
# =========================
@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            correo = request.form['correo']
            password = request.form['password']
            
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
            usuario = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            if usuario:
                if check_password_hash(usuario['password'], password):
                    session['usuario_id'] = usuario['id']
                    session['nombre'] = usuario['nombre']
                    session['es_admin'] = usuario.get('es_admin', 0)  # <--- AGREGADO
                    return redirect('/inicio')
            
            return render_template('usuarios/login.html', error="Correo o contraseña incorrectos")
        
        except Exception as e:
            print("ERROR LOGIN:")
            print(e)
            return f"Error: {e}"
    
    return render_template('usuarios/login.html')

# =========================
# LOGOUT
# =========================
@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')