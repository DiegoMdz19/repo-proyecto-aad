import libsql
import envyte

db_url = envyte.get("DB_URL")
api_token = envyte.get("API_TOKEN")

conn = libsql.connect("proyectoaad") #, sync_url = db_url, auth_token = api_token)
cursor = conn.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                CIF INTEGER NOT NULL
               )
               """)
conn.commit()
conn.sync()
conn.close()