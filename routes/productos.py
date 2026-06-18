from flask import Blueprint, render_template
import mysql.connector
from config import Config

productos_bp = Blueprint('productos', __name__)

def conectar():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )

@productos_bp.route('/')
@productos_bp.route('/inicio')
def inicio():

    conexion = conectar()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM productos
        ORDER BY id DESC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        'inicio.html',
        productos=productos
    )