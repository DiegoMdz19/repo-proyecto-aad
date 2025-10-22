import libsql
import envyte

db_url = envyte.get("DB_URL")
api_token = envyte.get("API_TOKEN")

conn = libsql.connect("proyectoaad", sync_url = db_url, auth_token = api_token)
cursor = conn.cursor()

cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                CIF TEXT NOT NULL
                )   
                ''')
cursor.execute("""
                CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                CIF TEXT NOT NULL
                )
                """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS piezas (
                id_pieza INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL CHECK(precio >= 0),
                stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
                id_proveedor INTEGER NOT NULL,
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE RESTRICT ON UPDATE CASCADE
                )
                """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                fecha_pedido TEXT NOT NULL DEFAULT (datetime('now')),
                estado TEXT NOT NULL DEFAULT 'pendiente' CHECK(estado IN ('pendiente','procesando', 'enviado', 'entregado', 'cancelado')),
                total REAL NOT NULL DEFAULT 0 CHECK(total >= 0),
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                ON DELETE RESTRICT ON UPDATE CASCADE
                )
                """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS elementos_pedido (
                id_elemento INTEGER PRIMARY KEY,
                id_pedido INTEGER NOT NULL,
                id_pieza INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
                FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
                ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (id_pieza) REFERENCES piezas(id_pieza)
                ON DELETE RESTRICT ON UPDATE CASCADE
                )
               """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS facturas (
                id_factura INTEGER PRIMARY KEY,
                id_pedido INTEGER UNIQUE NOT NULL,
                fecha_emision TEXT NOT NULL DEFAULT (datetime('now')),
                importe_base REAL NOT NULL CHECK(importe_base >= 0),
                iva REAL NOT NULL DEFAULT 21.0 CHECK(iva >= 0),
                total REAL NOT NULL CHECK(total >= 0),
                FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
                ON DELETE CASCADE ON UPDATE CASCADE
                )
                """)

conn.commit()
conn.sync()
conn.close()