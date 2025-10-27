import libsql
import envyte

print("¿Dónde quieres trabajar?")
print("1. Local")
print("2. Turso")
opcion = input("Selecciona una opción (1-2): ").strip()

if opcion == "1":
    # Local
    conn = libsql.connect("proyectoaad")
    print("Conectado a base de datos LOCAL")
elif opcion == "2":
    # Turso
    db_url = envyte.get("DB_URL")
    api_token = envyte.get("API_TOKEN")
    conn = libsql.connect("proyectoaad", sync_url=db_url, auth_token=api_token)
    print("Conectado a base de datos TURSO")
else:
    print("Opción no válida")
    exit()

cursor = conn.cursor()

def sync():
    if opcion == "2":
        conn.sync()


# Eliminar tablas existentes
cursor.execute("DROP TABLE IF EXISTS facturas")
cursor.execute("DROP TABLE IF EXISTS elementos_pedido")
cursor.execute("DROP TABLE IF EXISTS pedidos")
cursor.execute("DROP TABLE IF EXISTS piezas")
cursor.execute("DROP TABLE IF EXISTS proveedores")
cursor.execute("DROP TABLE IF EXISTS clientes")
print("Tablas eliminadas")

cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                CIF TEXT UNIQUE NOT NULL
                )   
                ''')
cursor.execute("""
                CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                CIF TEXT UNIQUE NOT NULL
                )
                """)
cursor.execute("""
                CREATE TABLE IF NOT EXISTS piezas (
                id_pieza INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL CHECK(precio >= 0),
                stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
                id_proveedor INTEGER NOT NULL,
                FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE CASCADE ON UPDATE CASCADE
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
                ON DELETE CASCADE ON UPDATE CASCADE
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
                ON DELETE CASCADE ON UPDATE CASCADE
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
sync()
print("Tablas creadas localmente")
print("Insertando datos iniciales espere...")
# INSERTS PROVEEDORES
proveedores_inserts = [
    ('Suministros Hernández S.A.', '+34 645641431', 'Avenida del Sol 178, Sevilla', 'U66163695'),
    ('Repuestos Andalucía S.L.', '+34 667207586', 'Avenida del Sol 161, Bilbao', 'P13555435'),
    ('Talleres García S.A.', '+34 601047959', 'Calle de la Paz 181, Valencia', 'W94635537'),
    ('Repuestos Cantabria S.L.', '+34 665020350', 'Avenida del Sol 100, Barcelona', 'C65098238'),
    ('Distribuciones Valencia S.L.U.', '+34 653844252', 'Camino del Prado 1, Sevilla', 'K92485285'),
    ('Autopartes Cantabria S.L.', '+34 670305031', 'Calle Real 11, Barcelona', 'J86534480'),
    ('Talleres Valencia S.L.', '+34 681387554', 'Camino del Prado 99, Bilbao', 'M48922408'),
    ('Motores Andalucía S.L.U.', '+34 687736284', 'Camino del Prado 137, Barcelona', 'E68258985'),
    ('Distribuciones Valencia S.L.', '+34 630829914', 'Paseo de la Castellana 22, Bilbao', 'A32507628'),
    ('Motores García S.L.', '+34 667643993', 'Calle Mayor 192, Bilbao', 'Y43643016')
]

cursor.executemany('INSERT INTO proveedores (nombre, telefono, direccion, CIF) VALUES (?, ?, ?, ?)', proveedores_inserts)
conn.commit()
sync()

# INSERTS PIEZAS (con id_proveedor distribuido entre 1-10)
piezas_inserts = [
    ('Pastillas de freno Mann Filter', 148.9, 156, 1),
    ('Turbo NGK', 60.4, 208, 2),
    ('Lámpara H7 Philips', 469.09, 161, 3),
    ('Compresor de aire Hella', 438.95, 121, 4),
    ('Inyector Bosch', 191.5, 50, 5),
    ('Pastillas de freno Bosch', 172.39, 48, 5),
    ('Limpiaparabrisas Mann Filter', 199.28, 49, 1),
    ('Filtro de aire Hella', 171.66, 42, 4),
    ('Sensor de oxígeno Denso', 228.99, 84, 6),
    ('Espejo retrovisor Denso', 31.29, 292, 6),
    ('Filtro de aire Mahle', 150.07, 287, 7),
    ('Turbo Bosch', 496.56, 197, 5),
    ('Correa de distribución NGK', 203.14, 151, 2),
    ('Sensor de oxígeno NGK', 422.38, 291, 2),
    ('Batería Mahle', 13.48, 158, 7),
    ('Embrague Philips', 138.65, 269, 3),
    ('Motor de arranque Mahle', 398.81, 96, 7),
    ('Amortiguador delantero Monroe', 375.28, 15, 8),
    ('Disco de freno NGK', 144.95, 257, 2),
    ('Correa de distribución Denso', 59.05, 190, 6),
    ('Motor de arranque Philips', 407.13, 248, 3),
    ('Lámpara H7 NGK', 486.29, 162, 2),
    ('Amortiguador trasero NGK', 70.03, 54, 2),
    ('Inyector Hella', 140.39, 203, 4),
    ('Pastillas de freno Mahle', 165.11, 285, 7),
    ('Pastillas de freno Valeo', 11.82, 236, 9),
    ('Amortiguador trasero Valeo', 443.94, 213, 9),
    ('Inyector Brembo', 455.51, 18, 10),
    ('Pastillas de freno Philips', 423.85, 81, 3),
    ('Sensor de oxígeno Philips', 135.5, 221, 3),
    ('Amortiguador delantero Hella', 301.81, 288, 4),
    ('Compresor de aire Denso', 71.81, 104, 6),
    ('Correa de distribución Hella', 53.4, 127, 4),
    ('Embrague Brembo', 103.18, 143, 10),
    ('Filtro de aire Monroe', 73.59, 233, 8),
    ('Lámpara H7 Hella', 446.41, 243, 4),
    ('Inyector Philips', 77.72, 20, 3),
    ('Amortiguador trasero Hella', 119.97, 266, 4),
    ('Lámpara H7 Bosch', 332.39, 261, 5),
    ('Motor de arranque Monroe', 152.23, 137, 8),
    ('Compresor de aire Valeo', 9.9, 179, 9),
    ('Alternador NGK', 312.9, 161, 2),
    ('Amortiguador delantero Bosch', 113.19, 229, 5),
    ('Filtro de aceite Mahle', 100.89, 32, 7),
    ('Embrague Bosch', 48.69, 202, 5),
    ('Motor de arranque Mann Filter', 72.68, 135, 1),
    ('Amortiguador trasero Mahle', 485.47, 249, 7),
    ('Filtro de aire NGK', 256.3, 140, 2),
    ('Alternador Bosch', 38.88, 212, 5),
    ('Motor de arranque NGK', 126.76, 135, 2),
    ('Filtro de aceite Denso', 406.59, 267, 6),
    ('Bujía Denso', 440.31, 86, 6),
    ('Compresor de aire Monroe', 144.21, 55, 8),
    ('Compresor de aire NGK', 273.15, 115, 2),
    ('Filtro de aire Mann Filter', 429.22, 24, 1),
    ('Motor de arranque Denso', 401.21, 242, 6),
    ('Compresor de aire Mann Filter', 421.17, 224, 1),
    ('Turbo Brembo', 235.83, 235, 10),
    ('Alternador Mann Filter', 221.2, 278, 1),
    ('Turbo Mann Filter', 343.93, 123, 1),
    ('Espejo retrovisor Brembo', 102.11, 93, 10),
    ('Amortiguador trasero Denso', 472.98, 232, 6),
    ('Batería Hella', 344.11, 245, 4),
    ('Radiador Mann Filter', 143.48, 60, 1),
    ('Espejo retrovisor Philips', 185.05, 54, 3),
    ('Alternador Philips', 381.88, 233, 3),
    ('Turbo Valeo', 342.44, 284, 9),
    ('Motor de arranque Valeo', 260.86, 53, 9),
    ('Bujía Mann Filter', 44.89, 21, 1),
    ('Inyector NGK', 96.02, 237, 2),
    ('Bujía Philips', 132.33, 100, 3),
    ('Inyector Valeo', 425.05, 184, 9),
    ('Disco de freno Hella', 327.99, 223, 4),
    ('Filtro de aceite Hella', 296.65, 161, 4),
    ('Batería Monroe', 252.77, 63, 8),
    ('Limpiaparabrisas Denso', 457.8, 299, 6),
    ('Disco de freno Monroe', 189.12, 204, 8),
    ('Pastillas de freno Denso', 274.85, 100, 6),
    ('Batería Valeo', 139.19, 17, 9),
    ('Limpiaparabrisas NGK', 78.88, 187, 2),
    ('Alternador Brembo', 36.83, 281, 10),
    ('Filtro de aceite NGK', 153.86, 291, 2),
    ('Radiador Hella', 257.96, 42, 4),
    ('Disco de freno Denso', 21.77, 257, 6),
    ('Amortiguador trasero Bosch', 27.28, 275, 5),
    ('Pastillas de freno Brembo', 302.44, 172, 10),
    ('Sensor de oxígeno Monroe', 176.5, 88, 8),
    ('Amortiguador trasero Brembo', 66.82, 226, 10),
    ('Correa de distribución Brembo', 210.32, 104, 10),
    ('Amortiguador trasero Monroe', 99.94, 48, 8),
    ('Disco de freno Philips', 428.32, 134, 3),
    ('Disco de freno Valeo', 6.18, 11, 9),
    ('Filtro de aire Bosch', 116.77, 91, 5),
    ('Filtro de aceite Valeo', 80.41, 69, 9),
    ('Radiador Denso', 273.14, 196, 6),
    ('Amortiguador delantero NGK', 194.08, 218, 2),
    ('Lámpara H7 Valeo', 434.83, 57, 9),
    ('Batería Mann Filter', 481.16, 174, 1),
    ('Correa de distribución Philips', 63.22, 149, 3),
    ('Limpiaparabrisas Brembo', 83.51, 108, 10)
]

cursor.executemany('INSERT INTO piezas (nombre, precio, stock, id_proveedor) VALUES (?, ?, ?, ?)', piezas_inserts)
conn.commit()
sync()

# INSERTS CLIENTES
clientes_inserts = [
    ('Repuestos Castilla S.A.', '+34 683843941', 'Avenida del Sol 164, Sevilla', 'F22000417'),
    ('Suministros Andalucía S.A.', '+34 605681565', 'Calle Mayor 91, Barcelona', 'T46760834'),
    ('Distribuciones López S.A.', '+34 692267866', 'Camino del Prado 150, Sevilla', 'W51998001'),
    ('Talleres Madrid S.A.', '+34 613570494', 'Paseo de la Castellana 24, Madrid', 'Y58337454'),
    ('Talleres Ibéricos S.A.', '+34 679772409', 'Calle Mayor 144, Sevilla', 'T86745543'),
    ('Suministros Andalucía S.L.U.', '+34 610608518', 'Calle Mayor 185, Bilbao', 'M89538558'),
    ('Talleres Ibéricos S.L.', '+34 630380708', 'Calle de la Paz 57, Sevilla', 'Q91786580'),
    ('Talleres López S.L.U.', '+34 699869252', 'Camino del Prado 97, Bilbao', 'F69935209'),
    ('Talleres Andalucía S.L.', '+34 647176963', 'Paseo de la Castellana 181, Barcelona', 'H15616370'),
    ('Distribuciones Hernández S.L.U.', '+34 670270377', 'Paseo de la Castellana 173, Sevilla', 'S12003363'),
    ('Repuestos García S.L.U.', '+34 698097723', 'Camino del Prado 5, Sevilla', 'K64524577'),
    ('Talleres García S.L.', '+34 677648324', 'Paseo de la Castellana 181, Madrid', 'E30818602'),
    ('Distribuciones Hernández S.L.', '+34 669849026', 'Calle Real 9, Valencia', 'K46130918'),
    ('Distribuciones Castilla S.L.U.', '+34 687574481', 'Avenida del Sol 167, Valencia', 'H30586117'),
    ('Repuestos Ibéricos S.L.U.', '+34 658449728', 'Paseo de la Castellana 46, Madrid', 'G72845859'),
    ('Suministros García S.A.', '+34 696499778', 'Calle Mayor 93, Zaragoza', 'W59103016'),
    ('Autopartes Madrid S.A.', '+34 697512478', 'Calle Mayor 84, Sevilla', 'Z89697132'),
    ('Repuestos Valencia S.L.', '+34 669018815', 'Avenida del Sol 111, Bilbao', 'X93269893'),
    ('Suministros Madrid S.L.U.', '+34 660281145', 'Camino del Prado 130, Valencia', 'Z92618796'),
    ('Repuestos Cantabria S.L.U.', '+34 664773938', 'Calle Real 4, Valencia', 'C25444069'),
    ('Autopartes Hernández S.L.', '+34 655163598', 'Calle Mayor 5, Bilbao', 'V58254898'),
    ('Talleres Castilla S.L.', '+34 613187983', 'Paseo de la Castellana 76, Madrid', 'S21027682'),
    ('Talleres Castilla S.L.', '+34 692440848', 'Avenida del Sol 31, Bilbao', 'C67184405'),
    ('Autopartes Ibéricos S.L.U.', '+34 677294436', 'Calle Mayor 154, Sevilla', 'R68866183'),
    ('Talleres Castilla S.L.U.', '+34 661912137', 'Calle Mayor 54, Zaragoza', 'P90962511'),
    ('Autopartes Madrid S.L.', '+34 643341081', 'Camino del Prado 37, Bilbao', 'C26230746'),
    ('Distribuciones Andalucía S.A.', '+34 666344472', 'Calle de la Paz 143, Sevilla', 'N32260215'),
    ('Talleres Castilla S.A.', '+34 622049284', 'Calle Mayor 125, Zaragoza', 'J81934549'),
    ('Distribuciones Ibéricos S.L.', '+34 618736497', 'Camino del Prado 139, Sevilla', 'R69474389'),
    ('Suministros Hernández S.L.U.', '+34 627436445', 'Avenida del Sol 6, Barcelona', 'Q14209630'),
    ('Motores Castilla S.L.', '+34 659994668', 'Paseo de la Castellana 157, Bilbao', 'N52051060'),
    ('Distribuciones Castilla S.L.', '+34 605732713', 'Avenida del Sol 57, Zaragoza', 'L18130361'),
    ('Motores García S.A.', '+34 631678635', 'Calle Real 167, Barcelona', 'E24223521'),
    ('Talleres Andalucía S.L.U.', '+34 612686907', 'Camino del Prado 84, Valencia', 'C87376265'),
    ('Suministros Castilla S.L.U.', '+34 677379138', 'Paseo de la Castellana 69, Bilbao', 'Y51760142'),
    ('Distribuciones Hernández S.A.', '+34 672723776', 'Avenida del Sol 175, Madrid', 'U19750559'),
    ('Autopartes López S.A.', '+34 602450819', 'Calle Real 22, Bilbao', 'A41740893'),
    ('Talleres García S.L.U.', '+34 698165599', 'Calle de la Paz 39, Zaragoza', 'X24530787'),
    ('Motores Madrid S.L.', '+34 604544779', 'Camino del Prado 191, Zaragoza', 'N89884494'),
    ('Repuestos Valencia S.A.', '+34 638524937', 'Paseo de la Castellana 47, Valencia', 'T97995658'),
    ('Distribuciones Castilla S.A.', '+34 687478657', 'Paseo de la Castellana 37, Bilbao', 'A29313888'),
    ('Repuestos Valencia S.L.U.', '+34 699529244', 'Calle Real 104, Sevilla', 'B19746294'),
    ('Repuestos López S.L.', '+34 646114432', 'Camino del Prado 29, Bilbao', 'U85896407'),
    ('Distribuciones García S.L.U.', '+34 645635633', 'Calle Real 38, Valencia', 'P29168564'),
    ('Motores Hernández S.A.', '+34 621204168', 'Calle Mayor 70, Sevilla', 'E48977304'),
    ('Repuestos López S.L.U.', '+34 613394122', 'Avenida del Sol 162, Zaragoza', 'J84137983'),
    ('Repuestos López S.L.U.', '+34 632283574', 'Calle de la Paz 134, Valencia', 'X67057078'),
    ('Autopartes Cantabria S.L.U.', '+34 680519869', 'Paseo de la Castellana 107, Sevilla', 'C18437522'),
    ('Talleres López S.L.', '+34 611780463', 'Avenida del Sol 140, Madrid', 'D70632363'),
    ('Talleres Castilla S.L.U.', '+34 659313766', 'Camino del Prado 20, Madrid', 'G11635296'),
    ('Talleres García S.L.', '+34 618231771', 'Camino del Prado 179, Valencia', 'E13793694'),
    ('Distribuciones Cantabria S.A.', '+34 658439587', 'Calle de la Paz 128, Zaragoza', 'H83511320'),
    ('Repuestos Cantabria S.L.U.', '+34 649010478', 'Calle Real 192, Madrid', 'B73022724'),
    ('Suministros Valencia S.L.', '+34 686781960', 'Calle Real 82, Zaragoza', 'X57265444'),
    ('Autopartes Madrid S.L.U.', '+34 670630195', 'Avenida del Sol 144, Madrid', 'X70119689'),
    ('Talleres Valencia S.A.', '+34 639333756', 'Avenida del Sol 68, Zaragoza', 'S39415696'),
    ('Suministros Andalucía S.L.', '+34 666779172', 'Calle Real 105, Barcelona', 'A77289056'),
    ('Autopartes Madrid S.L.U.', '+34 640557154', 'Paseo de la Castellana 173, Madrid', 'M23458967'),
    ('Repuestos Hernández S.L.', '+34 633125888', 'Avenida del Sol 125, Bilbao', 'G17889097'),
    ('Repuestos López S.L.', '+34 660273982', 'Camino del Prado 16, Bilbao', 'Z94810019'),
    ('Autopartes Andalucía S.L.U.', '+34 623346713', 'Avenida del Sol 88, Bilbao', 'P74406681'),
    ('Suministros Andalucía S.A.', '+34 646784632', 'Avenida del Sol 61, Valencia', 'Y74654271'),
    ('Repuestos Castilla S.A.', '+34 631769668', 'Camino del Prado 98, Madrid', 'S20871128'),
    ('Motores Valencia S.L.U.', '+34 637592876', 'Paseo de la Castellana 167, Barcelona', 'Z46699640'),
    ('Motores Hernández S.A.', '+34 627905411', 'Calle Mayor 140, Barcelona', 'D62090022'),
    ('Repuestos Hernández S.A.', '+34 657545204', 'Camino del Prado 128, Valencia', 'M41493023'),
    ('Talleres Andalucía S.L.U.', '+34 676652393', 'Calle Real 103, Zaragoza', 'L69721019'),
    ('Repuestos Valencia S.L.U.', '+34 617214199', 'Calle Mayor 37, Valencia', 'R36516841'),
    ('Repuestos Andalucía S.A.', '+34 641374254', 'Paseo de la Castellana 81, Bilbao', 'F13786537'),
    ('Distribuciones Hernández S.L.', '+34 680228848', 'Calle Mayor 101, Sevilla', 'W27563408'),
    ('Autopartes Cantabria S.L.U.', '+34 648050123', 'Paseo de la Castellana 2, Zaragoza', 'T34369671'),
    ('Repuestos Cantabria S.L.U.', '+34 614788467', 'Calle de la Paz 181, Bilbao', 'K65854488'),
    ('Autopartes Cantabria S.L.U.', '+34 686887986', 'Avenida del Sol 75, Bilbao', 'K69811126'),
    ('Suministros Valencia S.A.', '+34 695031547', 'Calle de la Paz 196, Zaragoza', 'S14691074'),
    ('Talleres Castilla S.A.', '+34 631090157', 'Camino del Prado 188, Valencia', 'X13965522'),
    ('Talleres López S.L.', '+34 647640169', 'Calle Mayor 20, Madrid', 'G39252916'),
    ('Motores López S.L.', '+34 601437792', 'Calle Real 147, Sevilla', 'Y63864205'),
    ('Distribuciones Hernández S.L.U.', '+34 619370327', 'Calle Mayor 181, Valencia', 'X34397799'),
    ('Motores Andalucía S.L.', '+34 666472096', 'Calle Real 165, Barcelona', 'D11671514'),
    ('Talleres Valencia S.L.U.', '+34 678593413', 'Camino del Prado 14, Madrid', 'Y93969940'),
    ('Motores Madrid S.L.', '+34 671768379', 'Avenida del Sol 16, Zaragoza', 'L17741841'),
    ('Autopartes Hernández S.A.', '+34 699525292', 'Camino del Prado 148, Zaragoza', 'B50851562'),
    ('Autopartes López S.A.', '+34 680972108', 'Camino del Prado 54, Madrid', 'V61425768'),
    ('Repuestos López S.L.U.', '+34 695414736', 'Paseo de la Castellana 195, Bilbao', 'C56969588'),
    ('Suministros Hernández S.L.', '+34 648423075', 'Calle de la Paz 118, Barcelona', 'P26521790'),
    ('Distribuciones García S.A.', '+34 636217812', 'Camino del Prado 12, Barcelona', 'P85353521'),
    ('Autopartes Castilla S.A.', '+34 633891924', 'Paseo de la Castellana 150, Bilbao', 'A62675260'),
    ('Suministros Andalucía S.A.', '+34 622856078', 'Avenida del Sol 5, Valencia', 'C59878009'),
    ('Autopartes Ibéricos S.L.', '+34 649760908', 'Calle de la Paz 144, Madrid', 'Z78411197'),
    ('Motores Valencia S.L.U.', '+34 669150866', 'Calle Real 37, Zaragoza', 'E26987067'),
    ('Motores Valencia S.L.U.', '+34 668384272', 'Calle Real 132, Valencia', 'Q31052123'),
    ('Suministros Madrid S.L.U.', '+34 665777228', 'Calle Real 70, Valencia', 'Y19667566'),
    ('Suministros Cantabria S.L.', '+34 680265441', 'Avenida del Sol 141, Sevilla', 'U26412631'),
    ('Talleres Castilla S.L.', '+34 677787517', 'Avenida del Sol 109, Sevilla', 'Z38830711'),
    ('Autopartes Valencia S.L.U.', '+34 622814368', 'Avenida del Sol 199, Sevilla', 'A23168876'),
    ('Motores Valencia S.A.', '+34 650620131', 'Calle de la Paz 85, Barcelona', 'C88089417'),
    ('Suministros Valencia S.A.', '+34 666057871', 'Calle Mayor 138, Valencia', 'Z85205114'),
    ('Distribuciones López S.L.U.', '+34 677334704', 'Calle Real 147, Madrid', 'P65208367'),
    ('Autopartes Andalucía S.L.U.', '+34 649973659', 'Calle de la Paz 138, Barcelona', 'D33899649'),
    ('Repuestos Madrid S.L.', '+34 624726033', 'Calle de la Paz 85, Madrid', 'V71638848')
]

cursor.executemany('INSERT INTO clientes (nombre, telefono, direccion, CIF) VALUES (?, ?, ?, ?)', clientes_inserts)
conn.commit()
sync()

# INSERTS PEDIDOS (con id_cliente distribuido entre 1-100 y fechas coherentes)
pedidos_inserts = [
    (1, '2025-07-15', 'cancelado', 4922.12),
    (5, '2025-09-23', 'procesando', 1199.7),
    (12, '2025-10-20', 'procesando', 864.26),
    (8, '2024-10-25', 'procesando', 1440.42),
    (23, '2025-03-12', 'enviado', 4842.11),
    (15, '2025-01-15', 'procesando', 3312.22),
    (34, '2025-08-18', 'enviado', 1273.0),
    (7, '2025-08-18', 'entregado', 1847.0),
    (45, '2025-02-10', 'procesando', 2339.23),
    (19, '2025-05-11', 'entregado', 432.12),
    (28, '2025-01-20', 'pendiente', 3070.19),
    (56, '2025-05-14', 'entregado', 1028.14),
    (41, '2025-03-24', 'enviado', 973.84),
    (67, '2025-08-12', 'enviado', 2554.05),
    (3, '2025-09-11', 'cancelado', 53.31),
    (72, '2024-11-09', 'cancelado', 2296.48),
    (88, '2025-08-08', 'procesando', 925.7),
    (14, '2025-10-14', 'entregado', 2472.92),
    (92, '2025-06-08', 'procesando', 1029.23),
    (26, '2025-06-29', 'entregado', 2625.88),
    (37, '2025-07-04', 'enviado', 1990.66),
    (51, '2025-01-13', 'enviado', 4994.58),
    (9, '2025-02-16', 'cancelado', 4408.97),
    (64, '2024-10-26', 'entregado', 2679.67),
    (78, '2025-05-12', 'cancelado', 940.42),
    (31, '2025-07-18', 'entregado', 2095.58),
    (43, '2025-03-26', 'enviado', 3883.43),
    (55, '2025-01-17', 'procesando', 679.26),
    (2, '2025-06-18', 'cancelado', 4163.27),
    (89, '2025-06-12', 'enviado', 4057.52),
    (16, '2025-04-17', 'procesando', 1949.06),
    (74, '2025-10-16', 'entregado', 185.12),
    (21, '2025-03-01', 'enviado', 1017.93),
    (38, '2025-04-17', 'procesando', 3794.42),
    (49, '2025-05-28', 'enviado', 3333.7),
    (61, '2025-01-08', 'entregado', 4221.48),
    (85, '2025-09-16', 'entregado', 1152.19),
    (11, '2025-05-13', 'enviado', 623.54),
    (94, '2025-09-29', 'enviado', 4152.14),
    (27, '2025-05-18', 'procesando', 4775.62),
    (42, '2025-10-13', 'enviado', 2867.96),
    (58, '2025-08-15', 'procesando', 4556.83),
    (6, '2025-01-19', 'enviado', 3160.6),
    (73, '2024-10-26', 'pendiente', 4863.24),
    (18, '2025-01-16', 'cancelado', 153.06),
    (90, '2025-07-12', 'procesando', 2756.3),
    (33, '2025-09-17', 'cancelado', 485.47),
    (47, '2025-02-15', 'enviado', 4977.81),
    (60, '2025-09-18', 'enviado', 446.97),
    (4, '2024-12-08', 'pendiente', 1578.2),
    (81, '2025-07-12', 'entregado', 4442.1),
    (24, '2025-10-02', 'pendiente', 2977.15),
    (96, '2025-08-23', 'cancelado', 3369.54),
    (13, '2025-09-14', 'enviado', 1640.77),
    (70, '2024-11-11', 'pendiente', 1485.73),
    (35, '2025-08-05', 'cancelado', 986.74),
    (53, '2025-05-09', 'procesando', 2423.88),
    (66, '2025-09-19', 'procesando', 1264.72),
    (79, '2024-12-05', 'cancelado', 1834.63),
    (10, '2025-02-10', 'procesando', 1146.85),
    (87, '2025-06-09', 'enviado', 4352.39),
    (22, '2025-09-07', 'pendiente', 3412.99),
    (44, '2025-10-02', 'entregado', 3312.19),
    (57, '2025-09-18', 'pendiente', 3084.24),
    (30, '2025-03-01', 'cancelado', 1068.3),
    (98, '2025-05-01', 'entregado', 3914.27),
    (17, '2025-01-19', 'enviado', 1652.41),
    (75, '2025-05-01', 'enviado', 147.07),
    (39, '2025-10-04', 'enviado', 2979.99),
    (52, '2025-09-07', 'procesando', 1522.56),
    (63, '2025-05-30', 'enviado', 1851.36),
    (82, '2025-08-21', 'entregado', 671.52),
    (20, '2024-12-01', 'entregado', 3498.72),
    (95, '2025-01-24', 'entregado', 2545.24),
    (29, '2025-09-30', 'enviado', 1892.29),
    (46, '2024-11-01', 'enviado', 125.19),
    (68, '2024-11-15', 'procesando', 2173.67),
    (84, '2025-07-21', 'enviado', 4422.45),
    (25, '2025-05-06', 'entregado', 1685.97),
    (91, '2025-02-03', 'procesando', 3389.39),
    (36, '2024-12-29', 'enviado', 2815.8),
    (50, '2025-01-30', 'entregado', 2024.79),
    (62, '2025-05-20', 'cancelado', 2673.86),
    (77, '2024-12-17', 'pendiente', 695.43),
    (32, '2024-11-20', 'procesando', 2015.66),
    (99, '2025-03-31', 'pendiente', 3953.45),
    (48, '2024-11-04', 'enviado', 3651.27),
    (65, '2024-12-17', 'enviado', 3769.05),
    (86, '2025-08-05', 'cancelado', 3088.25),
    (40, '2025-06-27', 'cancelado', 2563.07),
    (54, '2025-09-07', 'procesando', 3502.77),
    (71, '2025-04-09', 'procesando', 3796.08),
    (93, '2025-05-10', 'pendiente', 3497.13),
    (80, '2024-12-28', 'entregado', 1712.0),
    (59, '2025-01-24', 'entregado', 2751.92),
    (97, '2025-08-15', 'cancelado', 749.58),
    (69, '2025-10-10', 'pendiente', 4111.48),
    (83, '2025-04-11', 'enviado', 3079.57),
    (100, '2025-03-05', 'procesando', 440.39),
    (76, '2025-06-29', 'pendiente', 455.56)
]

cursor.executemany('INSERT INTO pedidos (id_cliente, fecha_pedido, estado, total) VALUES (?, ?, ?, ?)', pedidos_inserts)
conn.commit()
sync()

# INSERTS ELEMENTOS_PEDIDO (con id_pedido de 1-100 y id_pieza de 1-100, distribución variada)
elementos_pedido_inserts = [
    (1, 12, 10, 193.46),
    (1, 45, 3, 384.26),
    (2, 23, 10, 370.3),
    (2, 67, 10, 30.9),
    (3, 8, 1, 429.76),
    (4, 34, 6, 269.73),
    (5, 91, 6, 165.68),
    (5, 5, 3, 392.57),
    (6, 78, 9, 250.06),
    (7, 19, 6, 450.59),
    (8, 56, 2, 105.67),
    (9, 41, 7, 160.48),
    (10, 88, 8, 36.57),
    (10, 14, 3, 225.2),
    (11, 72, 5, 16.99),
    (12, 3, 4, 188.68),
    (13, 92, 9, 110.34),
    (14, 26, 8, 261.65),
    (15, 37, 2, 205.94),
    (16, 51, 1, 282.32),
    (17, 9, 8, 349.66),
    (18, 64, 2, 184.31),
    (19, 78, 1, 104.55),
    (20, 31, 10, 203.8),
    (21, 43, 6, 103.99),
    (22, 55, 4, 478.47),
    (22, 2, 6, 224.09),
    (23, 89, 5, 412.25),
    (24, 16, 5, 58.56),
    (25, 74, 1, 35.45),
    (26, 21, 2, 63.63),
    (27, 38, 8, 495.5),
    (28, 49, 7, 424.91),
    (29, 61, 3, 79.52),
    (30, 85, 6, 8.67),
    (31, 11, 3, 32.05),
    (32, 94, 10, 10.3),
    (33, 27, 2, 112.63),
    (34, 42, 4, 382.24),
    (35, 58, 6, 9.13),
    (36, 6, 5, 401.66),
    (37, 73, 2, 329.53),
    (38, 18, 10, 35.3),
    (39, 90, 10, 140.25),
    (40, 33, 1, 243.24),
    (41, 47, 6, 34.87),
    (42, 60, 8, 37.17),
    (43, 4, 4, 174.38),
    (44, 81, 7, 486.72),
    (45, 24, 9, 291.79),
    (46, 96, 10, 378.96),
    (47, 13, 9, 165.01),
    (48, 70, 9, 234.77),
    (49, 35, 7, 348.41),
    (50, 53, 4, 351.96),
    (51, 66, 9, 272.55),
    (52, 79, 3, 375.99),
    (53, 10, 2, 344.04),
    (54, 87, 1, 484.46),
    (55, 22, 8, 354.88),
    (56, 44, 4, 470.33),
    (57, 57, 8, 457.69),
    (58, 30, 9, 84.14),
    (59, 98, 7, 142.04),
    (60, 17, 6, 386.81),
    (61, 75, 4, 203.12),
    (62, 39, 3, 489.97),
    (63, 52, 1, 497.7),
    (64, 63, 6, 65.46),
    (65, 82, 1, 54.46),
    (66, 20, 1, 367.22),
    (67, 95, 6, 173.79),
    (68, 29, 3, 353.76),
    (69, 46, 5, 379.84),
    (70, 68, 10, 310.29),
    (71, 84, 4, 262.43),
    (72, 25, 5, 137.51),
    (73, 91, 7, 275.02),
    (74, 36, 5, 241.4),
    (75, 50, 1, 465.22),
    (76, 62, 9, 378.2),
    (77, 77, 5, 27.73),
    (78, 32, 1, 97.86),
    (79, 99, 5, 138.28),
    (80, 48, 6, 261.73),
    (81, 65, 3, 227.17),
    (82, 86, 8, 105.85),
    (83, 40, 2, 188.02),
    (84, 54, 8, 35.68),
    (85, 71, 5, 79.54),
    (86, 93, 2, 469.74),
    (87, 80, 4, 292.58),
    (88, 59, 7, 482.91),
    (89, 97, 8, 424.75),
    (90, 69, 7, 486.96),
    (91, 83, 2, 100.01),
    (92, 100, 9, 272.12),
    (93, 76, 8, 232.73),
    (94, 15, 10, 109.77),
    (95, 28, 8, 164.68),
    (96, 7, 5, 298.45),
    (97, 89, 3, 412.89),
    (98, 1, 7, 148.9),
    (99, 50, 4, 465.22),
    (100, 99, 2, 138.28)
]

cursor.executemany('INSERT INTO elementos_pedido (id_pedido, id_pieza, cantidad, precio_unitario) VALUES (?, ?, ?, ?)', elementos_pedido_inserts)
conn.commit()
sync()

# INSERTS FACTURAS (con id_pedido de 1-100, variando las fechas coherentemente después del pedido)
facturas_inserts = [
    (1, '2025-07-05', 774.09, 21.0, 936.65),
    (2, '2025-01-04', 1094.51, 21.0, 1324.36),
    (3, '2025-06-14', 2223.84, 21.0, 2690.85),
    (4, '2025-09-23', 3621.47, 21.0, 4381.98),
    (5, '2025-02-23', 2919.87, 21.0, 3533.04),
    (6, '2024-11-20', 337.34, 21.0, 408.18),
    (7, '2025-07-31', 1969.13, 21.0, 2382.65),
    (8, '2025-06-09', 1083.15, 21.0, 1310.61),
    (9, '2025-01-26', 3032.36, 21.0, 3669.16),
    (10, '2025-07-04', 667.24, 21.0, 807.36),
    (11, '2025-01-27', 2820.15, 21.0, 3412.38),
    (12, '2025-05-22', 2601.95, 21.0, 3148.36),
    (13, '2025-01-04', 1244.35, 21.0, 1505.66),
    (14, '2024-12-28', 1929.09, 21.0, 2334.2),
    (15, '2025-02-28', 1808.87, 21.0, 2188.73),
    (16, '2025-07-23', 1930.35, 21.0, 2335.72),
    (17, '2024-12-25', 3144.79, 21.0, 3805.2),
    (18, '2024-10-28', 1058.91, 21.0, 1281.28),
    (19, '2025-03-19', 926.56, 21.0, 1121.14),
    (20, '2025-08-29', 2305.32, 21.0, 2789.44),
    (21, '2024-11-25', 364.61, 21.0, 441.18),
    (22, '2025-10-11', 3113.39, 21.0, 3767.2),
    (23, '2025-06-15', 2910.99, 21.0, 3522.3),
    (24, '2025-02-25', 2408.7, 21.0, 2914.53),
    (25, '2025-05-03', 1556.62, 21.0, 1883.51),
    (26, '2025-03-15', 2490.76, 21.0, 3013.82),
    (27, '2025-10-18', 1223.09, 21.0, 1479.94),
    (28, '2025-05-27', 1785.61, 21.0, 2160.59),
    (29, '2025-05-31', 3889.19, 21.0, 4705.92),
    (30, '2025-07-07', 2495.84, 21.0, 3019.97),
    (31, '2025-08-21', 1261.29, 21.0, 1526.16),
    (32, '2024-11-19', 3568.66, 21.0, 4318.08),
    (33, '2025-01-03', 3778.76, 21.0, 4572.3),
    (34, '2025-02-23', 2910.69, 21.0, 3521.93),
    (35, '2025-07-27', 2836.21, 21.0, 3431.81),
    (36, '2025-06-08', 3974.0, 21.0, 4808.54),
    (37, '2025-09-04', 3324.62, 21.0, 4022.79),
    (38, '2025-01-28', 2555.33, 21.0, 3091.95),
    (39, '2025-06-21', 2689.15, 21.0, 3253.87),
    (40, '2025-02-19', 2409.46, 21.0, 2915.45),
    (41, '2025-05-30', 2027.48, 21.0, 2453.25),
    (42, '2025-03-09', 648.53, 21.0, 784.72),
    (43, '2025-08-03', 206.66, 21.0, 250.06),
    (44, '2025-02-28', 3344.58, 21.0, 4046.94),
    (45, '2025-08-15', 2111.79, 21.0, 2555.27),
    (46, '2025-04-17', 423.39, 21.0, 512.3),
    (47, '2025-09-04', 2579.56, 21.0, 3121.27),
    (48, '2025-04-19', 1443.45, 21.0, 1746.57),
    (49, '2025-06-03', 1232.49, 21.0, 1491.31),
    (50, '2025-07-11', 1934.54, 21.0, 2340.79),
    (51, '2025-03-22', 372.25, 21.0, 450.42),
    (52, '2025-08-20', 259.72, 21.0, 314.26),
    (53, '2024-11-24', 1280.72, 21.0, 1549.67),
    (54, '2024-10-24', 2960.93, 21.0, 3582.73),
    (55, '2025-05-03', 2592.98, 21.0, 3137.51),
    (56, '2025-04-14', 2827.99, 21.0, 3421.87),
    (57, '2025-07-26', 740.16, 21.0, 895.59),
    (58, '2024-11-19', 1031.83, 21.0, 1248.51),
    (59, '2025-09-21', 2716.59, 21.0, 3287.07),
    (60, '2024-10-27', 986.57, 21.0, 1193.75),
    (61, '2024-12-20', 840.02, 21.0, 1016.42),
    (62, '2025-01-27', 1428.14, 21.0, 1728.05),
    (63, '2024-12-09', 3103.99, 21.0, 3755.83),
    (64, '2025-03-10', 3130.84, 21.0, 3788.32),
    (65, '2025-02-02', 2108.51, 21.0, 2551.3),
    (66, '2024-12-19', 133.37, 21.0, 161.38),
    (67, '2025-02-24', 2130.17, 21.0, 2577.51),
    (68, '2025-08-01', 3679.65, 21.0, 4452.38),
    (69, '2025-09-08', 2486.77, 21.0, 3008.99),
    (70, '2024-12-22', 1095.31, 21.0, 1325.33),
    (71, '2025-06-07', 1877.69, 21.0, 2272.0),
    (72, '2024-11-21', 3434.45, 21.0, 4155.68),
    (73, '2025-01-08', 3838.38, 21.0, 4644.44),
    (74, '2024-11-17', 2640.76, 21.0, 3195.32),
    (75, '2024-12-26', 2606.54, 21.0, 3153.91),
    (76, '2025-05-13', 1989.72, 21.0, 2407.56),
    (77, '2025-05-01', 1705.02, 21.0, 2063.07),
    (78, '2025-07-22', 661.38, 21.0, 800.27),
    (79, '2025-02-04', 3256.73, 21.0, 3940.64),
    (80, '2025-07-19', 3586.96, 21.0, 4340.22),
    (81, '2025-05-26', 2519.34, 21.0, 3048.4),
    (82, '2024-11-29', 1606.49, 21.0, 1943.85),
    (83, '2024-12-12', 3687.4, 21.0, 4461.75),
    (84, '2025-03-31', 1679.36, 21.0, 2032.03),
    (85, '2025-04-09', 3319.35, 21.0, 4016.41),
    (86, '2025-05-28', 3730.22, 21.0, 4513.57),
    (87, '2024-11-11', 1894.01, 21.0, 2291.75),
    (88, '2025-10-10', 3951.78, 21.0, 4781.65),
    (89, '2025-01-22', 1134.57, 21.0, 1372.83),
    (90, '2024-11-09', 3803.75, 21.0, 4602.54),
    (91, '2025-09-18', 2409.55, 21.0, 2915.56),
    (92, '2025-07-02', 1740.03, 21.0, 2105.44),
    (93, '2025-04-04', 1489.49, 21.0, 1802.28),
    (94, '2025-09-10', 2899.86, 21.0, 3508.83),
    (95, '2024-11-02', 704.57, 21.0, 852.53),
    (96, '2025-04-13', 3213.67, 21.0, 3888.54),
    (97, '2025-08-21', 629.31, 21.0, 761.47),
    (98, '2025-06-09', 585.95, 21.0, 709.0),
    (99, '2024-11-13', 2309.38, 21.0, 2794.35),
    (100, '2025-01-18', 1025.68, 21.0, 1241.07)
]

cursor.executemany('INSERT INTO facturas (id_pedido, fecha_emision, importe_base, iva, total) VALUES (?, ?, ?, ?, ?)', facturas_inserts)

print("Datos iniciales insertados correctamente.")

# Confirmar los cambios
conn.commit()

sync()
print("Sincronizado con la base de datos")

conn.close()