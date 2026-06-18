from app import conectar
from werkzeug.security import generate_password_hash

conexion = conectar()
cursor = conexion.cursor()

# Verificar si el usuario admin existe
cursor.execute("SELECT * FROM usuarios WHERE correo = 'admin@gmail.com'")
usuario = cursor.fetchone()

if not usuario:
    # Crear usuario admin
    password_hash = generate_password_hash('admin123')
    cursor.execute("""
        INSERT INTO usuarios (nombre, correo, password, es_admin)
        VALUES ('Administrador', 'admin@gmail.com', %s, 1)
    """, (password_hash,))
    conexion.commit()
    print("✅ Usuario admin creado correctamente")
    print("📧 Email: admin@gmail.com")
    print("🔑 Contraseña: admin123")
else:
    # Actualizar a admin si ya existe
    cursor.execute("UPDATE usuarios SET es_admin = 1 WHERE correo = 'admin@gmail.com'")
    conexion.commit()
    print("✅ Usuario admin actualizado correctamente")

cursor.close()
conexion.close()