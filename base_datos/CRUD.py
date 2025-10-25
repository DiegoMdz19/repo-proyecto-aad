import libsql
import envyte

db_url = envyte.get("DB_URL")
api_token = envyte.get("API_TOKEN")

conn = libsql.connect("proyectoaad", sync_url=db_url ,auth_token=api_token)
cursor = conn.cursor()

def insertar_proovedores():
    nombre = input().strip()
    telefono = input().strip()
    email = input().strip()
    direccion = input().strip()
    if nombre != NULL & telefono != NULL & email != NULL & direccion:
        cursor.execute(f'''
                INSERT INTO proovedores (nombre,telefono,email,direccion)VALUES
                ({nombre},{telefono},{email},{direccion});
                ''')
    else:
        print("No se permiten campos vacios")


def insertar_piezas():
    nombre = input().strip()
    descripcion = input().strip()
    precio = input().strip()
    stock = input().strip()
    if nombre != NULL & descripcion != NULL & precio != NULL & stock != NULL:
        cursor.execute(f'''
                INSERT INTO piezas (nombres,descripcion,precio,stock)VALUES
                ({nombre},{descripcion},{precio},{stock});
        ''')
    else:
        print("No se permiten campos vacios")

def insertar_clientes():
    nombre = input().strip()
    apellido = input().strip()
    telefono = input().strip()
    email = input().strip()
    direccion = input().strip()
    if nombre != NULL & apellido != NULL & telefono != NULL & email != NULL & direccion:
        cursor.execute(f'''
                INSERT INTO clientes (nombre,apellidos,telefono,email,direccion)VALUES
                ({nombre},{apellido},{telefono},{email},{direccion});
                ''')
    else:
        print("No se permiten campos vacios")
    
def insertar_pedidos():
    fecha_pedido = input().strip()
    estado = input().strip()
    total=input().strip()

    if fecha_pedido != NULL & estado != NULL & total != NULL:
        cursor.execute(f'''
                INSERT INTO pedidos(fecha_pedido,estado,total)VALUES
                ("{fecha_pedido}","{estado}","{total}");
                    ''')
    else:
        print("No se permiten campos vacios")

def insertar_elementos_pedido():
    cantidad = input().strip()
    precio_unitario = input().strip()

    if cantidad != NULL & precio_unitario != NULL:
        cursor.execute(f'''
        INSERT INTO elementos_pedido(cantidad,precio_unitario)VALUES
        ("{cantidad}","{precio_unitario}");
                    ''')
    else:
        print("No se pueden poner campos vacios")


def insertar_facturas():
    fecha_emision = input().strip()
    importe = input().strip()
    iva = input().strip()
    total = input().strip()

    if fecha_emision != NULL & importe != NULL & iva != NULL & total != NULL :
        cursor.execute(f'''
                    INSERT INTO facturas(fecha_emision,importe,iva,total)VALUES
                    ("{fecha_emision}","{importe}","{iva}","{total}");
                    ''')
    else:
        print("No pueden estar los campos vacios")
