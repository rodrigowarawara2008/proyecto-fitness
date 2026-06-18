from flask import Flask, render_template, redirect, session, request
from config import Config
import mysql.connector

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# ============================================
# FUNCIÓN PARA CONECTAR A LA BASE DE DATOS
# ============================================
def conectar():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )

# ============================================
# IMPORTAR BLUEPRINTS
# ============================================
from routes.usuarios import usuarios_bp
from routes.productos import productos_bp
from routes.carrito import carrito_bp

# ============================================
# REGISTRAR BLUEPRINTS
# ============================================
app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(carrito_bp)

# ============================================
# RUTA PRINCIPAL
# ============================================
@app.route('/')
def index():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    print(f"📦 Productos encontrados: {len(productos)}")
    return render_template('inicio.html', productos=productos)

# ============================================
# RUTA DE INICIO (después del login)
# ============================================
@app.route('/inicio')
def inicio():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('inicio.html', productos=productos)

# ============================================
# RUTA AGREGAR CARRITO
# ============================================
@app.route('/agregar_carrito/<int:producto_id>')
def agregar_carrito(producto_id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    if not producto:
        return redirect('/')
    
    carrito = session.get('carrito', [])
    
    for item in carrito:
        if item['id'] == producto_id:
            item['cantidad'] += 1
            session['carrito'] = carrito
            session.modified = True
            return redirect('/carrito')
    
    carrito.append({
        'id': producto['id'],
        'nombre': producto['nombre'],
        'precio': float(producto['precio']),
        'cantidad': 1
    })
    
    session['carrito'] = carrito
    session.modified = True
    return redirect('/carrito')

# ============================================
# RUTA CARRITO
# ============================================
@app.route('/carrito')
def carrito():
    carrito_items = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    return render_template('carrito.html', carrito=carrito_items, total=total)

# ============================================
# ELIMINAR DEL CARRITO
# ============================================
@app.route('/eliminar_carrito/<int:producto_id>')
def eliminar_carrito(producto_id):
    carrito = session.get('carrito', [])
    carrito = [item for item in carrito if item['id'] != producto_id]
    session['carrito'] = carrito
    session.modified = True
    return redirect('/carrito')

# ============================================
# ACTUALIZAR CANTIDAD
# ============================================
@app.route('/actualizar_carrito/<int:producto_id>', methods=['POST'])
def actualizar_carrito(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    carrito = session.get('carrito', [])
    
    for item in carrito:
        if item['id'] == producto_id:
            if cantidad > 0:
                item['cantidad'] = cantidad
            else:
                carrito = [i for i in carrito if i['id'] != producto_id]
            break
    
    session['carrito'] = carrito
    session.modified = True
    return redirect('/carrito')

# ============================================
# VACIAR CARRITO
# ============================================
@app.route('/vaciar_carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    return redirect('/carrito')

# ============================================
# FINALIZAR COMPRA
# ============================================
@app.route('/finalizar_compra')
def finalizar_compra():
    carrito = session.get('carrito', [])
    if not carrito:
        return redirect('/carrito')
    
    session['carrito'] = []
    session.modified = True
    return render_template('compra_exitosa.html')

# ============================================
# COMPRA EXITOSA
# ============================================
@app.route('/compra_exitosa')
def compra_exitosa():
    return render_template('compra_exitosa.html')

# ============================================
# PANEL DE ADMINISTRACIÓN
# ============================================

# Verificar si el usuario es admin
def es_admin():
    if 'usuario_id' not in session:
        return False
    
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT es_admin FROM usuarios WHERE id = %s", (session['usuario_id'],))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    return usuario and usuario.get('es_admin', 0) == 1

# Panel de administración
@app.route('/admin')
def admin_panel():
    if not es_admin():
        return redirect('/login')
    
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('admin.html', productos=productos)

# Agregar producto
@app.route('/admin/agregar', methods=['GET', 'POST'])
def admin_agregar_producto():
    if not es_admin():
        return redirect('/login')
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio'))
        stock = int(request.form.get('stock', 0))
        categoria = request.form.get('categoria')
        imagen = request.form.get('imagen')
        
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, categoria, imagen))
        conexion.commit()
        cursor.close()
        conexion.close()
        
        return redirect('/admin')
    
    return render_template('agregar_producto.html')

# Editar producto
@app.route('/admin/editar/<int:producto_id>', methods=['GET', 'POST'])
def admin_editar_producto(producto_id):
    if not es_admin():
        return redirect('/login')
    
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = float(request.form.get('precio'))
        stock = int(request.form.get('stock', 0))
        categoria = request.form.get('categoria')
        imagen = request.form.get('imagen')
        
        sql = """
            UPDATE productos 
            SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria=%s, imagen=%s
            WHERE id=%s
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, categoria, imagen, producto_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect('/admin')
    
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    return render_template('editar_producto.html', producto=producto)

# Eliminar producto
@app.route('/admin/eliminar/<int:producto_id>')
def admin_eliminar_producto(producto_id):
    if not es_admin():
        return redirect('/login')
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return redirect('/admin')

# ============================================
# EJECUTAR LA APLICACIÓN
# ============================================
if __name__ == '__main__':
    app.run(debug=True)