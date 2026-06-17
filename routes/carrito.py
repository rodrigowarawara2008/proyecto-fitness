from flask import Blueprint, session, redirect, render_template
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

    return redirect('/carrito')


@carrito_bp.route('/carrito')
def ver_carrito():

    if 'usuario_id' not in session:
        return redirect('/login')

    conexion = conectar()

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            carrito.id,
            productos.nombre,
            productos.precio,
            carrito.cantidad,
            (productos.precio * carrito.cantidad) AS subtotal
        FROM carrito
        INNER JOIN productos
            ON carrito.producto_id = productos.id
        WHERE carrito.usuario_id = %s
    """, (session['usuario_id'],))

    productos = cursor.fetchall()

    total = sum(
        float(p['subtotal'])
        for p in productos
    )

    cursor.close()
    conexion.close()

    return render_template(
        'carrito.html',
        productos=productos,
        total=total
    )


@carrito_bp.route('/eliminar_carrito/<int:id>')
def eliminar_carrito(id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM carrito WHERE id=%s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect('/carrito')