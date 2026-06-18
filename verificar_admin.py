from app import conectar

conexion = conectar()
cursor = conexion.cursor(dictionary=True)
cursor.execute("SELECT id, nombre, correo, es_admin FROM usuarios WHERE correo = 'admin@gmail.com'")
usuario = cursor.fetchone()
cursor.close()
conexion.close()

if usuario:
    print(f"👤 Usuario: {usuario['nombre']}")
    print(f"📧 Email: {usuario['correo']}")
    print(f"👑 ¿Es admin? {'SÍ' if usuario['es_admin'] == 1 else 'NO'}")
else:
    print("❌ Usuario no encontrado")