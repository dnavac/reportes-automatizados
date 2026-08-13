import os
import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
from dotenv import load_dotenv

# Intentar cargar credenciales de Supabase
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

fake = Faker('es_CO')

ZONAS = ['Bocagrande', 'Manga', 'Crespo', 'El Cabrero', 'Castillogrande', 'Centro Histórico']
TIPOS_PROPIEDAD = ['Apartamento', 'Casa', 'Local', 'Oficina']
ESTADOS_PROPIEDAD = ['Disponible', 'Reservada', 'Vendida']
ORIGEN_LEADS = ['Web', 'Referido', 'Facebook Ads', 'Instagram', 'Valla Publicitaria']
ESTADOS_LEAD = ['Nuevo', 'Contactado', 'Cerrado']
ASESORES = ['Carlos Restrepo', 'Maria Lopez', 'Juan Perez', 'Diana Garcia']

def generar_datos_sqlite():
    """Genera datos de prueba en una base de datos SQLite local."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'inmobiliaria.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tablas en SQLite si no existen
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS propiedades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo VARCHAR(50) NOT NULL,
        zona VARCHAR(100) NOT NULL,
        precio NUMERIC(15, 2) NOT NULL,
        estado VARCHAR(20) NOT NULL,
        fecha_publicacion DATE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(150) NOT NULL,
        telefono VARCHAR(20),
        email VARCHAR(100),
        presupuesto_max NUMERIC(15, 2),
        zona_interes VARCHAR(100)
    );
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER REFERENCES clientes(id),
        propiedad_id INTEGER REFERENCES propiedades(id),
        fecha DATE NOT NULL,
        origen VARCHAR(50),
        estado VARCHAR(20)
    );
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        propiedad_id INTEGER REFERENCES propiedades(id),
        cliente_id INTEGER REFERENCES clientes(id),
        fecha_cierre DATE NOT NULL,
        valor_final NUMERIC(15, 2) NOT NULL,
        asesor VARCHAR(100) NOT NULL
    );
    ''')

    print("Generando datos de prueba...")
    
    # Generar Propiedades (50 propiedades)
    for _ in range(50):
        fecha_pub = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute(
            "INSERT INTO propiedades (tipo, zona, precio, estado, fecha_publicacion) VALUES (?, ?, ?, ?, ?)",
            (
                random.choice(TIPOS_PROPIEDAD),
                random.choice(ZONAS),
                random.randint(150000000, 1200000000),
                random.choice(ESTADOS_PROPIEDAD),
                fecha_pub.isoformat()
            )
        )
    
    # Generar Clientes (100 clientes)
    for _ in range(100):
        cursor.execute(
            "INSERT INTO clientes (nombre, telefono, email, presupuesto_max, zona_interes) VALUES (?, ?, ?, ?, ?)",
            (
                fake.name(),
                fake.phone_number()[:20],
                fake.email(),
                random.randint(200000000, 1500000000),
                random.choice(ZONAS)
            )
        )
    
    # Generar Leads (150 leads)
    for _ in range(150):
        fecha_lead = fake.date_between(start_date='-6m', end_date='today')
        cursor.execute(
            "INSERT INTO leads (cliente_id, propiedad_id, fecha, origen, estado) VALUES (?, ?, ?, ?, ?)",
            (
                random.randint(1, 100),
                random.randint(1, 50),
                fecha_lead.isoformat(),
                random.choice(ORIGEN_LEADS),
                random.choice(ESTADOS_LEAD)
            )
        )
    
    # Generar Ventas (20 ventas de las propiedades "Vendidas")
    cursor.execute("SELECT id, precio, fecha_publicacion FROM propiedades WHERE estado = 'Vendida'")
    propiedades_vendidas = cursor.fetchall()
    
    for prop in propiedades_vendidas:
        prop_id, precio, fecha_pub_str = prop
        fecha_pub = datetime.fromisoformat(fecha_pub_str).date()
        # La venta ocurre entre 1 y 6 meses después de la publicación
        dias_para_venta = random.randint(30, 180)
        fecha_cierre = min(fecha_pub + timedelta(days=dias_para_venta), datetime.now().date())
        
        # Precio final puede ser un poco menor al publicado
        valor_final = int(precio * random.uniform(0.9, 1.0))
        
        cursor.execute(
            "INSERT INTO ventas (propiedad_id, cliente_id, fecha_cierre, valor_final, asesor) VALUES (?, ?, ?, ?, ?)",
            (
                prop_id,
                random.randint(1, 100),
                fecha_cierre.isoformat(),
                valor_final,
                random.choice(ASESORES)
            )
        )

    conn.commit()
    conn.close()
    print(f"Datos generados exitosamente en: {db_path}")

def generar_datos_supabase():
    """Genera datos de prueba en Supabase. Requiere SUPABASE_URL y SUPABASE_KEY."""
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Conectando a Supabase para generar datos...")
    
    # Generar Propiedades (50)
    print("Generando Propiedades...")
    propiedades = []
    for _ in range(50):
        fecha_pub = fake.date_between(start_date='-1y', end_date='today')
        propiedades.append({
            "tipo": random.choice(TIPOS_PROPIEDAD),
            "zona": random.choice(ZONAS),
            "precio": random.randint(150000000, 1200000000),
            "estado": random.choice(ESTADOS_PROPIEDAD),
            "fecha_publicacion": fecha_pub.isoformat()
        })
    res_props = supabase.table("propiedades").insert(propiedades).execute()
    
    # Generar Clientes (100)
    print("Generando Clientes...")
    clientes = []
    for _ in range(100):
        clientes.append({
            "nombre": fake.name(),
            "telefono": fake.phone_number()[:20],
            "email": fake.email(),
            "presupuesto_max": random.randint(200000000, 1500000000),
            "zona_interes": random.choice(ZONAS)
        })
    res_clientes = supabase.table("clientes").insert(clientes).execute()
    
    # Generar Leads (150)
    print("Generando Leads...")
    leads = []
    ids_props = [p['id'] for p in res_props.data] if res_props.data else []
    ids_clientes = [c['id'] for c in res_clientes.data] if res_clientes.data else []
    
    if not ids_props or not ids_clientes:
        print("Error: No se pudieron obtener los IDs de Supabase. ¿Ya creaste las tablas con schema.sql?")
        return

    for _ in range(150):
        fecha_lead = fake.date_between(start_date='-6m', end_date='today')
        leads.append({
            "cliente_id": random.choice(ids_clientes),
            "propiedad_id": random.choice(ids_props),
            "fecha": fecha_lead.isoformat(),
            "origen": random.choice(ORIGEN_LEADS),
            "estado": random.choice(ESTADOS_LEAD)
        })
    supabase.table("leads").insert(leads).execute()
    
    # Generar Ventas para propiedades vendidas
    print("Generando Ventas...")
    ventas = []
    props_vendidas = [p for p in res_props.data if p['estado'] == 'Vendida'] if res_props.data else []
    for prop in props_vendidas:
        fecha_pub = datetime.fromisoformat(prop['fecha_publicacion']).date()
        dias_para_venta = random.randint(30, 180)
        fecha_cierre = min(fecha_pub + timedelta(days=dias_para_venta), datetime.now().date())
        valor_final = int(prop['precio'] * random.uniform(0.9, 1.0))
        
        ventas.append({
            "propiedad_id": prop['id'],
            "cliente_id": random.choice(ids_clientes),
            "fecha_cierre": fecha_cierre.isoformat(),
            "valor_final": valor_final,
            "asesor": random.choice(ASESORES)
        })
    if ventas:
        supabase.table("ventas").insert(ventas).execute()
        
    print("Datos generados exitosamente en Supabase.")

if __name__ == "__main__":
    if SUPABASE_URL and SUPABASE_KEY:
        generar_datos_supabase()
    else:
        print("No se encontraron credenciales de Supabase. Usando SQLite local.")
        generar_datos_sqlite()
