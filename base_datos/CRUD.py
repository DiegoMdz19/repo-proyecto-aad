import libsql
import envyte


db_url = envyte.get("DB_URL")
api_token = envyte.get("API_TOKEN")

conn = libsql.connect("proyectoaad", sync_url=db_url, auth_token=api_token)
cursor = conn.cursor()



def insertar_proveedores():
    try:
        nombre = input("Nombre: ").strip()
        telefono = input("Telefono: ").strip()
        direccion = input("Direccion: ").strip()
        cif =input("CIF:").strip()

        if not nombre or not telefono  or not direccion or not cif:
            print("No se permiten campos vacios.")
            return

        cursor.execute("""
            INSERT INTO proveedores (nombre, telefono, direccion, CIF)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion,cif))
        conn.commit()
        print("Proveedor insertado correctamente.")
    except Exception as e:
        print("Error al insertar proveedor:", e)


def insertar_piezas():
    try:
        nombre = input("Nombre: ").strip()
        descripcion = input("Descripcion: ").strip()
        precio = float(input("Precio: ").strip())
        stock = int(input("Stock: ").strip())
        id_proveedor = int(input("ID del proveedor: ").strip())

        cursor.execute("""
            INSERT INTO piezas (nombre, descripcion, precio, stock, id_proveedor)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, precio, stock, id_proveedor))
        conn.commit()
        print("Pieza insertada correctamente.")
    except Exception as e:
        print("Error al insertar pieza:", e)


def insertar_clientes():
    try:
        nombre = input("Nombre: ").strip()
        telefono = input("Telefono: ").strip()
        direccion = input("Direccion: ").strip()
        cif = input("CIF:").strip()

        cursor.execute("""
            INSERT INTO clientes (nombre,telefono,direccion,CIF)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion, cif))
        conn.commit()
        print("Cliente insertado correctamente.")
    except Exception as e:
        print("Error al insertar cliente:", e)


def insertar_pedidos():
    try:
        id_cliente = int(input("ID cliente: ").strip())
        fecha_pedido = input("Fecha pedido (YYYY-MM-DD): ").strip()
        estado = input("Estado: ").strip()
        total = float(input("Total: ").strip())

        cursor.execute("""
            INSERT INTO pedidos (id_cliente, fecha_pedido, estado, total)
            VALUES (?, ?, ?, ?)
        """, (id_cliente, fecha_pedido, estado, total))
        conn.commit()
        print("Pedido insertado correctamente.")
    except Exception as e:
        print("Error al insertar pedido:", e)


def insertar_elementos_pedido():
    try:
        id_pedido = int(input("ID pedido: ").strip())
        id_pieza = int(input("ID pieza: ").strip())
        cantidad = int(input("Cantidad: ").strip())
        precio_unitario = float(input("Precio unitario: ").strip())

        cursor.execute("""
            INSERT INTO elementos_pedido (id_pedido, id_pieza, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (id_pedido, id_pieza, cantidad, precio_unitario))
        conn.commit()
        print("Elemento insertado correctamente.")
    except Exception as e:
        print("Error al insertar elemento:", e)


def insertar_facturas():
    try:
        id_pedido = int(input("ID pedido: ").strip())
        fecha_emision = input("Fecha emision (YYYY-MM-DD): ").strip()
        importe_base = float(input("Importe base: ").strip())
        iva = float(input("IVA: ").strip())
        total = float(input("Total: ").strip())

        cursor.execute("""
            INSERT INTO facturas (id_pedido, fecha_emision, importe_base, iva, total)
            VALUES (?, ?, ?, ?, ?)
        """, (id_pedido, fecha_emision, importe_base, iva, total))
        conn.commit()
        print("Factura insertada correctamente.")
    except Exception as e:
        print("Error al insertar factura:", e)


def actualizar(tabla, campo_id, id_valor, columna, nuevo_valor):
    try:
        cursor.execute(f"UPDATE {tabla} SET {columna} = ? WHERE {campo_id} = ?", (nuevo_valor, id_valor))
        conn.commit()
        print("Registro actualizado correctamente.")
    except Exception as e:
        print("Error al actualizar:", e)


def eliminar(tabla, campo_id, id_valor):
    try:
        cursor.execute(f"DELETE FROM {tabla} WHERE {campo_id} = ?", (id_valor,))
        conn.commit()
        print("Registro eliminado correctamente.")
    except Exception as e:
        print("Error al eliminar:", e)


def mostrar(tabla):
    try:
        cursor.execute(f"SELECT * FROM {tabla}")
        columnas = [desc[0] for desc in cursor.description]
        resultados = cursor.fetchall()
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print(lista_diccionarios)
        return lista_diccionarios
    except Exception as e:
        print("Error al mostrar datos:", e)
        return []

def menu():
    while True:
        print("\n=== MENU CRUD ===")
        print("\n--- OPERACIONES BÁSICAS ---")
        print("1. Insertar proveedor")
        print("2. Mostrar proveedores")
        print("3. Actualizar proveedor")
        print("4. Eliminar proveedor")
        print("5. Insertar pieza")
        print("6. Mostrar piezas")
        print("7. Insertar cliente")
        print("8. Mostrar clientes")
        print("9. Insertar pedido")
        print("10. Mostrar pedidos")
        print("11. Insertar elemento de pedido")
        print("12. Mostrar elementos de pedido")
        print("13. Insertar factura")
        print("14. Mostrar facturas")
        print("15. Actualizar registro generico")
        print("16. Eliminar registro generico")
        
        print("\n--- CONSULTAS COMPLEJAS ---")
        print("17. Clientes con pedidos activos")
        print("18. Piezas por proveedor con stock")
        print("19. Pedidos detallados con facturas")
        print("20. Estadísticas de ventas por mes")
        print("21. Top 10 clientes por gasto")
        print("22. Unión proveedores y clientes")
        print("23. Piezas más caras que el promedio")
        print("24. Pedidos del último mes")
        print("25. Clientes agrupados por ciudad")
        print("26. Resumen de estados de pedidos")
        
        print("\n--- BÚSQUEDAS Y FILTROS ---")
        print("27. Buscar piezas por nombre")
        print("28. Filtrar pedidos por fecha")
        
        print("\n--- Procedimientos almacenados ---")
        print("29. Calcular total pedido con IVA")
        print("30. Actualizar stock de pieza")
        print("31. Generar reporte de ventas por proveedor")
        
        print("\n--- CONSULTAS COMPLEJAS DE ALMACENADOS ---")
        print("33. Ventas por mes con comparación")
        print("34. Clientes con más pedidos")
        print("35. Piezas más vendidas")
        print("36. Proveedores con más piezas")
        print("37. Facturas por mes")
        print("38. Pedidos por estado")

        print("\n--- SALIR ---")

        print("39. Salir")

        opcion = input("Elige una opcion: ").strip()

        if opcion == "1":
            insertar_proveedores()
        elif opcion == "2":
            mostrar("proveedores")
        elif opcion == "3":
            try:
                id_valor = int(input("ID proveedor: "))
                columna = input("Columna a actualizar: ").strip()
                nuevo_valor = input("Nuevo valor: ").strip()
                actualizar("proveedores", "id_proveedor", id_valor, columna, nuevo_valor)
            except Exception as e:
                print("Error:", e)
        elif opcion == "4":
            try:
                id_valor = int(input("ID proveedor: "))
                eliminar("proveedores", "id_proveedor", id_valor)
            except Exception as e:
                print("Error:", e)
        elif opcion == "5":
            insertar_piezas()
        elif opcion == "6":
            mostrar("piezas")
        elif opcion == "7":
            insertar_clientes()
        elif opcion == "8":
            mostrar("clientes")
        elif opcion == "9":
            insertar_pedidos()
        elif opcion == "10":
            mostrar("pedidos")
        elif opcion == "11":
            insertar_elementos_pedido()
        elif opcion == "12":
            mostrar("elementos_pedido")
        elif opcion == "13":
            insertar_facturas()
        elif opcion == "14":
            mostrar("facturas")
        elif opcion == "15":
            try:
                tabla = input("Nombre de la tabla: ").strip()
                campo_id = input("Nombre del campo ID (ej. id_cliente): ").strip()
                id_valor = int(input("ID del registro: "))
                columna = input("Columna a actualizar: ").strip()
                nuevo_valor = input("Nuevo valor: ").strip()
                actualizar(tabla, campo_id, id_valor, columna, nuevo_valor)
            except Exception as e:
                print("Error:", e)
        elif opcion == "16":
            try:
                tabla = input("Nombre de la tabla: ").strip()
                campo_id = input("Campo ID: ").strip()
                id_valor = int(input("ID del registro a eliminar: "))
                eliminar(tabla, campo_id, id_valor)
            except Exception as e:
                print("Error:", e)
        elif opcion == "17":
            consulta_clientes_con_pedidos_activos()
        elif opcion == "18":
            consulta_piezas_por_proveedor_con_stock()
        elif opcion == "19":
            consulta_pedidos_detallados_con_facturas()
        elif opcion == "20":
            estadisticas_ventas_por_mes()
        elif opcion == "21":
            top_clientes_por_gasto()
        elif opcion == "22":
            consulta_union_proveedores_clientes()
        elif opcion == "23":
            consulta_subconsulta_piezas_caras()
        elif opcion == "24":
            consulta_pedidos_ultimo_mes()
        elif opcion == "25":
            consulta_clientes_por_ciudad()
        elif opcion == "26":
            consulta_estado_pedidos_resumen()
        elif opcion == "27":
            buscar_piezas_por_nombre()
        elif opcion == "28":
            filtrar_pedidos_por_fecha()
        elif opcion == "29":
            calcular_total_pedido()
        elif opcion == "30":
            actualizar_stock()
        elif opcion == "31":
            reporte_proveedor()
        elif opcion == "33":
            consulta_ventas_por_mes_con_comparacion()
        elif opcion == "34":
            consulta_clientes_con_mas_pedidos()
        elif opcion == "35":
            consulta_piezas_mas_vendidas()
        elif opcion == "36":
            consulta_proveedores_con_mas_piezas()
        elif opcion == "37":
            consulta_facturas_por_mes()
        elif opcion == "38":
            consulta_pedidos_por_estado()
        elif opcion == "39":
            print("Saliendo del programa...")
            break
        else:
            print("Opcion no valida.")


# 1. CONSULTAS COMPLEJAS CON MÚLTIPLES TABLAS Y CONDICIONES

def consulta_clientes_con_pedidos_activos():
    """Consulta que muestra clientes con pedidos activos (no cancelados)"""
    try:
        cursor.execute("""
            SELECT DISTINCT c.id_cliente, c.nombre, c.telefono, c.direccion,
                   COUNT(p.id_pedido) as total_pedidos,
                   SUM(p.total) as total_gastado
            FROM clientes c
            INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
            WHERE p.estado NOT IN ('cancelado')
            GROUP BY c.id_cliente, c.nombre, c.telefono, c.direccion
            HAVING COUNT(p.id_pedido) > 0
            ORDER BY total_gastado DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== CLIENTES CON PEDIDOS ACTIVOS ===")
        for cliente in lista_diccionarios:
            print(f"ID: {cliente['id_cliente']} | {cliente['nombre']} | "
                  f"Pedidos: {cliente['total_pedidos']} | Total: €{cliente['total_gastado']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en consulta de clientes con pedidos activos:", e)
        return []

def consulta_piezas_por_proveedor_con_stock():
    """Consulta que agrupa piezas por proveedor con información de stock"""
    try:
        cursor.execute("""
            SELECT pv.nombre as proveedor, 
                   COUNT(pi.id_pieza) as total_piezas,
                   AVG(pi.precio) as precio_promedio,
                   SUM(pi.stock) as stock_total,
                   MIN(pi.precio) as precio_minimo,
                   MAX(pi.precio) as precio_maximo
            FROM proveedores pv
            INNER JOIN piezas pi ON pv.id_proveedor = pi.id_proveedor
            WHERE pi.stock > 0
            GROUP BY pv.id_proveedor, pv.nombre
            ORDER BY stock_total DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PIEZAS POR PROVEEDOR (CON STOCK) ===")
        for proveedor in lista_diccionarios:
            print(f"{proveedor['proveedor']}: {proveedor['total_piezas']} piezas | "
                  f"Stock: {proveedor['stock_total']} | Precio promedio: €{proveedor['precio_promedio']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en consulta de piezas por proveedor:", e)
        return []

def consulta_pedidos_detallados_con_facturas():
    """Consulta compleja que une pedidos, clientes, elementos y facturas"""
    try:
        cursor.execute("""
            SELECT p.id_pedido, c.nombre as cliente, p.fecha_pedido, p.estado, p.total,
                   f.fecha_emision, f.importe_base, f.iva, f.total as total_factura,
                   COUNT(ep.id_elemento) as elementos_pedido
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            LEFT JOIN facturas f ON p.id_pedido = f.id_pedido
            LEFT JOIN elementos_pedido ep ON p.id_pedido = ep.id_pedido
            WHERE p.total > 1000
            GROUP BY p.id_pedido, c.nombre, p.fecha_pedido, p.estado, p.total,
                     f.fecha_emision, f.importe_base, f.iva, f.total
            ORDER BY p.total DESC
            LIMIT 20
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PEDIDOS DETALLADOS (MAYORES A €1000) ===")
        for pedido in lista_diccionarios:
            print(f"Pedido #{pedido['id_pedido']} | {pedido['cliente']} | "
                  f"Estado: {pedido['estado']} | Total: €{pedido['total']:.2f} | "
                  f"Elementos: {pedido['elementos_pedido']}")
        return lista_diccionarios
    except Exception as e:
        print("Error en consulta de pedidos detallados:", e)
        return []

# 2. CONSULTAS DE BÚSQUEDA Y FILTRADO

def buscar_piezas_por_nombre():
    """Búsqueda de piezas por nombre con LIKE"""
    try:
        termino = input("Ingrese término de búsqueda para piezas: ").strip()
        if not termino:
            print("Término de búsqueda vacío.")
            return []
        
        cursor.execute("""
            SELECT pi.nombre, pi.precio, pi.stock, pv.nombre as proveedor
            FROM piezas pi
            INNER JOIN proveedores pv ON pi.id_proveedor = pv.id_proveedor
            WHERE pi.nombre LIKE ? OR pi.nombre LIKE ?
            ORDER BY pi.precio ASC
        """, (f'%{termino}%', f'%{termino.upper()}%'))
        
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print(f"\n=== RESULTADOS DE BÚSQUEDA: '{termino}' ===")
        for pieza in lista_diccionarios:
            print(f"{pieza['nombre']} | €{pieza['precio']:.2f} | "
                  f"Stock: {pieza['stock']} | Proveedor: {pieza['proveedor']}")
        return lista_diccionarios
    except Exception as e:
        print("Error en búsqueda de piezas:", e)
        return []

def filtrar_pedidos_por_fecha():
    """Filtro de pedidos por rango de fechas"""
    try:
        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
        fecha_fin = input("Fecha fin (YYYY-MM-DD): ").strip()
        
        cursor.execute("""
            SELECT p.id_pedido, c.nombre as cliente, p.fecha_pedido, p.estado, p.total
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.fecha_pedido BETWEEN ? AND ?
            ORDER BY p.fecha_pedido DESC
        """, (fecha_inicio, fecha_fin))
        
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print(f"\n=== PEDIDOS ENTRE {fecha_inicio} Y {fecha_fin} ===")
        for pedido in lista_diccionarios:
            print(f"Pedido #{pedido['id_pedido']} | {pedido['cliente']} | "
                  f"{pedido['fecha_pedido']} | {pedido['estado']} | €{pedido['total']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en filtro de pedidos por fecha:", e)
        return []

# 3. CONSULTAS DE AGREGACIÓN Y ESTADÍSTICAS

def estadisticas_ventas_por_mes():
    """Estadísticas de ventas agrupadas por mes"""
    try:
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', fecha_pedido) as mes,
                COUNT(*) as total_pedidos,
                SUM(total) as ventas_totales,
                AVG(total) as promedio_venta,
                MIN(total) as venta_minima,
                MAX(total) as venta_maxima
            FROM pedidos
            WHERE estado NOT IN ('cancelado')
            GROUP BY strftime('%Y-%m', fecha_pedido)
            ORDER BY mes DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== ESTADÍSTICAS DE VENTAS POR MES ===")
        for mes in lista_diccionarios:
            print(f"{mes['mes']}: {mes['total_pedidos']} pedidos | "
                  f"Total: €{mes['ventas_totales']:.2f} | Promedio: €{mes['promedio_venta']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en estadísticas de ventas:", e)
        return []

def top_clientes_por_gasto():
    """Top 10 clientes que más han gastado"""
    try:
        cursor.execute("""
            SELECT c.nombre, c.telefono, c.direccion,
                   COUNT(p.id_pedido) as total_pedidos,
                   SUM(p.total) as total_gastado,
                   AVG(p.total) as promedio_pedido
            FROM clientes c
            INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
            WHERE p.estado NOT IN ('cancelado')
            GROUP BY c.id_cliente, c.nombre, c.telefono, c.direccion
            ORDER BY total_gastado DESC
            LIMIT 10
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== TOP 10 CLIENTES POR GASTO ===")
        for i, cliente in enumerate(lista_diccionarios, 1):
            print(f"{i}. {cliente['nombre']} | Pedidos: {cliente['total_pedidos']} | "
                  f"Total: €{cliente['total_gastado']:.2f} | Promedio: €{cliente['promedio_pedido']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en top clientes:", e)
        return []

# 4. CONSULTAS CON UNIONES Y SUBCONSULTAS

def consulta_union_proveedores_clientes():
    """Unión de proveedores y clientes con información común"""
    try:
        cursor.execute("""
            SELECT 'Proveedor' as tipo, nombre, telefono, direccion, CIF
            FROM proveedores
            UNION ALL
            SELECT 'Cliente' as tipo, nombre, telefono, direccion, CIF
            FROM clientes
            ORDER BY nombre
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PROVEEDORES Y CLIENTES (UNIÓN) ===")
        for contacto in lista_diccionarios:
            print(f"{contacto['tipo']}: {contacto['nombre']} | {contacto['telefono']} | "
                  f"{contacto['direccion']} | CIF: {contacto['CIF']}")
        return lista_diccionarios
    except Exception as e:
        print("Error en unión de proveedores y clientes:", e)
        return []

def consulta_subconsulta_piezas_caras():
    """Subconsulta para encontrar piezas más caras que el promedio"""
    try:
        cursor.execute("""
            SELECT pi.nombre, pi.precio, pi.stock, pv.nombre as proveedor,
                   (SELECT AVG(precio) FROM piezas) as precio_promedio_general
            FROM piezas pi
            INNER JOIN proveedores pv ON pi.id_proveedor = pv.id_proveedor
            WHERE pi.precio > (SELECT AVG(precio) FROM piezas)
            ORDER BY pi.precio DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PIEZAS MÁS CARAS QUE EL PROMEDIO ===")
        for pieza in lista_diccionarios:
            print(f"{pieza['nombre']} | €{pieza['precio']:.2f} | "
                  f"Promedio: €{pieza['precio_promedio_general']:.2f} | "
                  f"Proveedor: {pieza['proveedor']}")
        return lista_diccionarios
    except Exception as e:
        print("Error en subconsulta de piezas caras:", e)
        return []




def calcular_total_pedido():
    """Calcula el total de un pedido con IVA"""
    try:
        id_pedido = int(input("ID del pedido para calcular total: "))
        
        cursor.execute("""
            SELECT SUM(cantidad * precio_unitario) as subtotal
            FROM elementos_pedido
            WHERE id_pedido = ?
        """, (id_pedido,))
        
        resultado = cursor.fetchone()
        if resultado and resultado[0]:
            subtotal = resultado[0]
            iva = subtotal * 0.21  # 21% IVA
            total = subtotal + iva
            
            print(f"\n=== CÁLCULO DE TOTAL PARA PEDIDO #{id_pedido} ===")
            print(f"Subtotal: €{subtotal:.2f}")
            print(f"IVA (21%): €{iva:.2f}")
            print(f"Total: €{total:.2f}")
            
            return {'subtotal': subtotal, 'iva': iva, 'total': total}
        else:
            print(f"No se encontraron elementos para el pedido #{id_pedido}")
            return None
    except ValueError:
        print("ID de pedido inválido")
        return None
    except Exception as e:
        print(f"Error calculando total del pedido {id_pedido}:", e)
        return None

def actualizar_stock():
    """Actualiza el stock de una pieza después de una venta"""
    try:
        id_pieza = int(input("ID de la pieza: "))
        cantidad = int(input("Cantidad vendida: "))
        
        # Verificar stock disponible
        cursor.execute("SELECT stock FROM piezas WHERE id_pieza = ?", (id_pieza,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"Pieza con ID {id_pieza} no encontrada")
            return False
            
        stock_actual = resultado[0]
        
        if stock_actual < cantidad:
            print(f"Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}")
            return False
        
        # Actualizar stock
        nuevo_stock = stock_actual - cantidad
        cursor.execute("UPDATE piezas SET stock = ? WHERE id_pieza = ?", (nuevo_stock, id_pieza))
        conn.commit()
        
        print(f"\n=== ACTUALIZACIÓN DE STOCK ===")
        print(f"Pieza ID: {id_pieza}")
        print(f"Stock anterior: {stock_actual}")
        print(f"Cantidad vendida: {cantidad}")
        print(f"Nuevo stock: {nuevo_stock}")
        
        return True
    except ValueError:
        print("Valores inválidos")
        return False
    except Exception as e:
        print(f"Error actualizando stock de pieza {id_pieza}:", e)
        return False

def reporte_proveedor():
    """Genera un reporte de ventas por proveedor"""
    try:
        id_proveedor = int(input("ID del proveedor para reporte: "))
        
        cursor.execute("""
            SELECT pv.nombre as proveedor,
                   COUNT(DISTINCT pi.id_pieza) as piezas_vendidas,
                   SUM(ep.cantidad) as unidades_vendidas,
                   SUM(ep.cantidad * ep.precio_unitario) as ingresos_totales,
                   AVG(ep.precio_unitario) as precio_promedio
            FROM proveedores pv
            INNER JOIN piezas pi ON pv.id_proveedor = pi.id_proveedor
            INNER JOIN elementos_pedido ep ON pi.id_pieza = ep.id_pieza
            INNER JOIN pedidos p ON ep.id_pedido = p.id_pedido
            WHERE pv.id_proveedor = ? AND p.estado NOT IN ('cancelado')
            GROUP BY pv.id_proveedor, pv.nombre
        """, (id_proveedor,))
        
        resultado = cursor.fetchone()
        if resultado:
            print(f"\n=== REPORTE DE VENTAS - PROVEEDOR ===")
            print(f"Proveedor: {resultado[0]}")
            print(f"Piezas vendidas: {resultado[1]}")
            print(f"Unidades vendidas: {resultado[2]}")
            print(f"Ingresos totales: €{resultado[3]:.2f}")
            print(f"Precio promedio: €{resultado[4]:.2f}")
            return resultado
        else:
            print(f"No se encontraron ventas para el proveedor ID {id_proveedor}")
            return None
    except ValueError:
        print("ID de proveedor inválido")
        return None
    except Exception as e:
        print(f"Error generando reporte del proveedor {id_proveedor}:", e)
        return None



def consulta_pedidos_ultimo_mes():
    """Consulta de pedidos del último mes usando funciones de fecha"""
    try:
        cursor.execute("""
            SELECT p.id_pedido, c.nombre as cliente, p.fecha_pedido, p.estado, p.total,
                   julianday('now') - julianday(p.fecha_pedido) as dias_desde_pedido
            FROM pedidos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.fecha_pedido >= date('now', '-1 month')
            ORDER BY p.fecha_pedido DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PEDIDOS DEL ÚLTIMO MES ===")
        for pedido in lista_diccionarios:
            print(f"Pedido #{pedido['id_pedido']} | {pedido['cliente']} | "
                  f"{pedido['fecha_pedido']} | {pedido['estado']} | "
                  f"€{pedido['total']:.2f} | Hace {int(pedido['dias_desde_pedido'])} días")
        return lista_diccionarios
    except Exception as e:
        print("Error en consulta de pedidos del último mes:", e)
        return []

def consulta_clientes_por_ciudad():
    """Consulta que extrae ciudad de la dirección usando funciones de cadena"""
    try:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN direccion LIKE '%,%' THEN trim(substr(direccion, instr(direccion, ',') + 1))
                    ELSE 'Sin ciudad'
                END as ciudad,
                COUNT(*) as total_clientes,
                GROUP_CONCAT(nombre, ' | ') as nombres_clientes
            FROM clientes
            GROUP BY ciudad
            ORDER BY total_clientes DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== CLIENTES POR CIUDAD ===")
        for ciudad in lista_diccionarios:
            print(f"{ciudad['ciudad']}: {ciudad['total_clientes']} clientes")
            print(f"  Clientes: {ciudad['nombres_clientes'][:100]}...")
        return lista_diccionarios
    except Exception as e:
        print("Error en consulta de clientes por ciudad:", e)
        return []



def consulta_estado_pedidos_resumen():
    """Consulta con CASE para resumir estados de pedidos"""
    try:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN estado = 'pendiente' THEN 'Por Procesar'
                    WHEN estado = 'procesando' THEN 'En Proceso'
                    WHEN estado = 'enviado' THEN 'Enviados'
                    WHEN estado = 'entregado' THEN 'Entregados'
                    WHEN estado = 'cancelado' THEN 'Cancelados'
                    ELSE 'Estado Desconocido'
                END as estado_grupo,
                COUNT(*) as cantidad,
                SUM(total) as total_importe,
                AVG(total) as promedio_importe
            FROM pedidos
            GROUP BY estado
            ORDER BY cantidad DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== RESUMEN DE ESTADOS DE PEDIDOS ===")
        for estado in lista_diccionarios:
            print(f"{estado['estado_grupo']}: {estado['cantidad']} pedidos | "
                  f"Total: €{estado['total_importe']:.2f} | "
                  f"Promedio: €{estado['promedio_importe']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en resumen de estados:", e)
        return []

# 8. CONSULTAS COMPLEJAS 

def consulta_ventas_por_mes_con_comparacion():
    """Consulta que muestra ventas por mes y compara con el mes anterior"""
    try:
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', fecha_pedido) as mes,
                COUNT(*) as pedidos_mes,
                SUM(total) as ventas_mes,
                AVG(total) as promedio_mes
            FROM pedidos
            WHERE estado NOT IN ('cancelado')
            GROUP BY strftime('%Y-%m', fecha_pedido)
            ORDER BY mes DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== VENTAS POR MES ===")
        for i, mes in enumerate(lista_diccionarios):
            if i < len(lista_diccionarios) - 1:
                mes_anterior = lista_diccionarios[i + 1]
                diferencia = mes['ventas_mes'] - mes_anterior['ventas_mes']
                print(f"{mes['mes']}: €{mes['ventas_mes']:.2f} | "
                      f"Diferencia: €{diferencia:.2f}")
            else:
                print(f"{mes['mes']}: €{mes['ventas_mes']:.2f} | "
                      f"(Primer mes)")
        return lista_diccionarios
    except Exception as e:
        print("Error en ventas por mes:", e)
        return []

def consulta_clientes_con_mas_pedidos():
    """Consulta que muestra los clientes que más pedidos han hecho"""
    try:
        cursor.execute("""
            SELECT c.nombre, c.telefono, c.direccion,
                   COUNT(p.id_pedido) as total_pedidos,
                   SUM(p.total) as total_gastado,
                   AVG(p.total) as promedio_pedido
            FROM clientes c
            INNER JOIN pedidos p ON c.id_cliente = p.id_cliente
            WHERE p.estado NOT IN ('cancelado')
            GROUP BY c.id_cliente, c.nombre, c.telefono, c.direccion
            ORDER BY total_pedidos DESC
            LIMIT 10
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== CLIENTES CON MÁS PEDIDOS ===")
        for i, cliente in enumerate(lista_diccionarios, 1):
            print(f"{i}. {cliente['nombre']} | Pedidos: {cliente['total_pedidos']} | "
                  f"Total: €{cliente['total_gastado']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en clientes con más pedidos:", e)
        return []

def consulta_piezas_mas_vendidas():
    """Consulta que muestra las piezas más vendidas"""
    try:
        cursor.execute("""
            SELECT pi.nombre, pi.precio, pi.stock, pv.nombre as proveedor,
                   SUM(ep.cantidad) as total_vendido,
                   COUNT(DISTINCT ep.id_pedido) as pedidos_con_pieza
            FROM piezas pi
            INNER JOIN proveedores pv ON pi.id_proveedor = pv.id_proveedor
            INNER JOIN elementos_pedido ep ON pi.id_pieza = ep.id_pieza
            INNER JOIN pedidos p ON ep.id_pedido = p.id_pedido
            WHERE p.estado NOT IN ('cancelado')
            GROUP BY pi.id_pieza, pi.nombre, pi.precio, pi.stock, pv.nombre
            ORDER BY total_vendido DESC
            LIMIT 15
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PIEZAS MÁS VENDIDAS ===")
        for i, pieza in enumerate(lista_diccionarios, 1):
            print(f"{i}. {pieza['nombre']} | Vendidas: {pieza['total_vendido']} | "
                  f"Precio: €{pieza['precio']:.2f} | Proveedor: {pieza['proveedor']}")
        return lista_diccionarios
    except Exception as e:
        print("Error en piezas más vendidas:", e)
        return []

def consulta_proveedores_con_mas_piezas():
    """Consulta que muestra los proveedores con más piezas en stock"""
    try:
        cursor.execute("""
            SELECT pv.nombre as proveedor, pv.telefono, pv.direccion,
                   COUNT(pi.id_pieza) as total_piezas,
                   SUM(pi.stock) as stock_total,
                   AVG(pi.precio) as precio_promedio,
                   MIN(pi.precio) as precio_minimo,
                   MAX(pi.precio) as precio_maximo
            FROM proveedores pv
            INNER JOIN piezas pi ON pv.id_proveedor = pi.id_proveedor
            GROUP BY pv.id_proveedor, pv.nombre, pv.telefono, pv.direccion
            ORDER BY total_piezas DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PROVEEDORES CON MÁS PIEZAS ===")
        for i, proveedor in enumerate(lista_diccionarios, 1):
            print(f"{i}. {proveedor['proveedor']} | Piezas: {proveedor['total_piezas']} | "
                  f"Stock Total: {proveedor['stock_total']} | Precio Promedio: €{proveedor['precio_promedio']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en proveedores con más piezas:", e)
        return []

def consulta_facturas_por_mes():
    """Consulta que muestra las facturas agrupadas por mes"""
    try:
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', fecha_emision) as mes,
                COUNT(*) as total_facturas,
                SUM(total) as total_facturado,
                AVG(total) as promedio_factura,
                SUM(iva) as total_iva,
                SUM(importe_base) as total_base
            FROM facturas
            GROUP BY strftime('%Y-%m', fecha_emision)
            ORDER BY mes DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== FACTURAS POR MES ===")
        for mes in lista_diccionarios:
            print(f"{mes['mes']}: {mes['total_facturas']} facturas | "
                  f"Total: €{mes['total_facturado']:.2f} | IVA: €{mes['total_iva']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en facturas por mes:", e)
        return []

def consulta_pedidos_por_estado():
    """Consulta que muestra los pedidos agrupados por estado"""
    try:
        cursor.execute("""
            SELECT 
                estado,
                COUNT(*) as total_pedidos,
                SUM(total) as total_importe,
                AVG(total) as promedio_pedido,
                MIN(total) as pedido_minimo,
                MAX(total) as pedido_maximo
            FROM pedidos
            GROUP BY estado
            ORDER BY total_pedidos DESC
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        lista_diccionarios = [dict(zip(columnas, fila)) for fila in resultados]
        print("\n=== PEDIDOS POR ESTADO ===")
        for estado in lista_diccionarios:
            print(f"{estado['estado']}: {estado['total_pedidos']} pedidos | "
                  f"Total: €{estado['total_importe']:.2f} | Promedio: €{estado['promedio_pedido']:.2f}")
        return lista_diccionarios
    except Exception as e:
        print("Error en pedidos por estado:", e)
        return []


if __name__ == "__main__":
    menu()

