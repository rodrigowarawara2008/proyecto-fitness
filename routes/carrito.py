from flask import Blueprint, session, redirect
import mysql.connector
from config import Config

carrito_bp = Blueprint('carrito', __name__)

def conectar():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )

@carrito_bp.route('/agregar_carrito/<int:producto_id>')
def agregar_carrito(producto_id):

    if 'usuario_id' not in session:
        return redirect('/login')

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO carrito
        (usuario_id, producto_id, cantidad)
        VALUES (%s,%s,%s)
    """, (
        session['usuario_id'],
        producto_id,
        1
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/inicio')