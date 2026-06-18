from app import conectar

try:
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificar si la columna imagen existe
    cursor.execute("SHOW COLUMNS FROM productos LIKE 'imagen'")
    resultado = cursor.fetchone()
    
    if not resultado:
        print("🔧 Agregando columna 'imagen' a la tabla productos...")
        cursor.execute("ALTER TABLE productos ADD COLUMN imagen VARCHAR(255) NULL")
        conexion.commit()
        print("✅ Columna 'imagen' agregada correctamente")
    else:
        print("✅ La columna 'imagen' ya existe")
    
    cursor.close()
    conexion.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")