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
        """, (nombre, apellidos, telefono, email, direccion,cif))
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
        print("17. Salir")

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
            print("Saliendo del programa...")
            break
        else:
            print("Opcion no valida.")

if __name__ == "__main__":
    menu()

