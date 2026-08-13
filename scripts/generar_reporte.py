import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from dotenv import load_dotenv

# Configuración
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_data_sqlite():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'inmobiliaria.db')
    if not os.path.exists(db_path):
        raise Exception(f"No se encontró la base de datos en {db_path}. Ejecuta generar_datos.py primero.")
    
    conn = sqlite3.connect(db_path)
    
    # Extraer datos
    df_ventas = pd.read_sql_query("""
        SELECT v.id, v.fecha_cierre, v.valor_final, p.zona, v.asesor
        FROM ventas v
        JOIN propiedades p ON v.propiedad_id = p.id
    """, conn)
    
    df_leads = pd.read_sql_query("SELECT * FROM leads", conn)
    df_propiedades = pd.read_sql_query("SELECT * FROM propiedades", conn)
    
    conn.close()
    return df_ventas, df_leads, df_propiedades

def get_data_supabase():
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Extrayendo datos de Supabase...")
    res_ventas = supabase.table('ventas').select('*').execute()
    df_ventas = pd.DataFrame(res_ventas.data)
    
    res_leads = supabase.table('leads').select('*').execute()
    df_leads = pd.DataFrame(res_leads.data)
    
    res_props = supabase.table('propiedades').select('*').execute()
    df_propiedades = pd.DataFrame(res_props.data)
    
    # Hacer el join de ventas con propiedades para obtener la zona
    if not df_ventas.empty and not df_propiedades.empty:
        df_ventas = df_ventas.merge(df_propiedades[['id', 'zona']], left_on='propiedad_id', right_on='id', suffixes=('', '_prop'))
        
    return df_ventas, df_leads, df_propiedades

def generar_reporte():
    print("Extrayendo datos...")
    if SUPABASE_URL and SUPABASE_KEY:
        df_ventas, df_leads, df_propiedades = get_data_supabase()
    else:
        df_ventas, df_leads, df_propiedades = get_data_sqlite()
        
    print("Generando visualizaciones...")
    
    # Preparar el directorio de salida
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples')
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'reporte_ejemplo.pdf')
    
    with PdfPages(pdf_path) as pdf:
        # Figura 1: Ventas Totales por Zona
        plt.figure(figsize=(10, 6))
        ventas_por_zona = df_ventas.groupby('zona')['valor_final'].sum() / 1e6 # en millones
        ventas_por_zona.sort_values(ascending=False).plot(kind='bar', color='skyblue')
        plt.title('Volumen de Ventas por Zona (Millones COP)')
        plt.ylabel('Millones COP')
        plt.xlabel('Zona')
        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
        
        # Figura 2: Leads por Origen
        plt.figure(figsize=(8, 8))
        leads_por_origen = df_leads['origen'].value_counts()
        plt.pie(leads_por_origen, labels=leads_por_origen.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Leads por Origen')
        plt.tight_layout()
        pdf.savefig()
        plt.close()
        
        # Figura 3: Estado de Propiedades
        plt.figure(figsize=(10, 6))
        estado_props = df_propiedades['estado'].value_counts()
        estado_props.plot(kind='bar', color=['green', 'orange', 'red'])
        plt.title('Estado Actual de las Propiedades')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=0)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Reporte generado exitosamente en: {pdf_path}")

if __name__ == "__main__":
    generar_reporte()
