from app import conectar

try:
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificar si la columna es_admin existe
    cursor.execute("SHOW COLUMNS FROM usuarios LIKE 'es_admin'")
    resultado = cursor.fetchone()
    
    if not resultado:
        print("🔧 Agregando columna 'es_admin' a la tabla usuarios...")
        cursor.execute("ALTER TABLE usuarios ADD COLUMN es_admin TINYINT(1) DEFAULT 0")
        conexion.commit()
        print("✅ Columna 'es_admin' agregada correctamente")
    else:
        print("✅ La columna 'es_admin' ya existe")
    
    cursor.close()
    conexion.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")