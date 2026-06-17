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

@usuarios_bp.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        password = generate_password_hash(request.form['password'])

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO usuarios(nombre,correo,password)
        VALUES(%s,%s,%s)
        """

        cursor.execute(sql,(nombre,correo,password))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect('/login')

    return render_template('registro.html')

@usuarios_bp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        correo = request.form['correo']
        password = request.form['password']

        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE correo=%s",
            (correo,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario and check_password_hash(
            usuario['password'],
            password
        ):

            session['usuario_id'] = usuario['id']
            session['nombre'] = usuario['nombre']

            return redirect('/inicio')

    return render_template('login.html')

@usuarios_bp.route('/logout')
def logout():

    session.clear()

    return redirect('/')