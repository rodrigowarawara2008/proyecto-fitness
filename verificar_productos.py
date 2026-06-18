from app import conectar

try:
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    
    # Verificar cuántos productos hay
    cursor.execute("SELECT COUNT(*) as total FROM productos")
    resultado = cursor.fetchone()
    total = resultado['total'] if resultado else 0
    
    print(f"📊 Total de productos en la base de datos: {total}")
    
    if total == 0:
        print("⚠️ No hay productos en la base de datos")
        print("💡 Agregando productos de prueba...")
        
        # Productos de prueba
        productos_prueba = [
            ('Barra Z para bíceps', 'Barra curva de acero para ejercicios de brazo', 95.00, 10, 'Equipamiento', ''),
            ('Cinturón de levantamiento', 'Cinturón de cuero para sentadillas y peso muerto', 140.00, 12, 'Equipamiento', ''),
            ('Cuerda para saltar', 'Cuerda de velocidad ajustable', 30.00, 45, 'Fitness', ''),
            ('Guantes de gimnasio', 'Par de guantes con soporte de muñeca', 60.00, 35, 'Accesorios', ''),
            ('Colchoneta de yoga', 'Mat antideslizante 1.5m x 60cm', 90.00, 18, 'Fitness', ''),
            ('Banda elástica de resistencia', 'Banda de látex para ejercicios de fuerza', 45.00, 40, 'Fitness', ''),
            ('Shaker para proteína', 'Vaso mezclador de 600ml con malla anti-grumos', 35.00, 50, 'Accesorios', ''),
            ('Creatina Monohidratada 300g', 'Creatina pura para fuerza y rendimiento', 150.00, 25, 'Suplementos', '')
        ]
        
        for producto in productos_prueba:
            sql = """
                INSERT INTO productos (nombre, descripcion, precio, stock, categoria, imagen)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, producto)
        
        conexion.commit()
        print(f"✅ {len(productos_prueba)} productos agregados correctamente")
    else:
        print("✅ Ya hay productos en la base de datos")
        # Mostrar productos existentes
        cursor.execute("SELECT id, nombre, precio FROM productos LIMIT 5")
        productos = cursor.fetchall()
        print("📋 Primeros 5 productos:")
        for p in productos:
            print(f"  - ID: {p['id']} | {p['nombre']} | Bs. {p['precio']}")
    
    cursor.close()
    conexion.close()
    print("✅ Verificación completada")
    
except Exception as e:
    print(f"❌ ERROR: {e}")