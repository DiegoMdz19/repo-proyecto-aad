import libsql
import envyte

db_url = envyte.get("DB_URL")
api_token = envyte.get("API_TOKEN")

conn = libsql.connect("proyectoaad", sync_url=db_url ,auth_token=api_token)
cursor = conn.cursor()

def insertar_proovedores():
    nombre = input()
    telefono = input()
    email = input()
    direccion = input()
    if nombre != NULL & telefono != NULL & email != NULL & direccion:
        cursor.execute(f'''
                INSERT INTO proovedores (nombre,telefono,email,direccion)VALUES
                ({nombre},{telefono},{email},{direccion});
                ''')
    else:
        print("No se permiten campos vacios")


def insertar_piezas():
    nombre = input()
    descripcion = input()
    precio = input()
    stock = input()
    if nombre != NULL & descripcion != NULL & precio != NULL & stock != NULL:
        cursor.execute(f'''
                INSERT INTO piezas (nombres,descripcion,precio,stock)VALUES
                ({nombre},{descripcion},{precio},{stock});
        ''')
    else:
        print("No se permiten campos vacios")

def insertar_clientes():
    nombre = input()
    apellido = input()
    telefono = input()
    email = input()
    direccion = input()
    if nombre != NULL & apellido != NULL & telefono != NULL & email != NULL & direccion:
        cursor.execute(f'''
                INSERT INTO clientes (nombre,apellidos,telefono,email,direccion)VALUES
                ({nombre},{apellido},{telefono},{email},{direccion});
                ''')
    else:
        print("No se permiten campos vacios")
    
def inser