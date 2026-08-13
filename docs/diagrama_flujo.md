# Diagrama de Flujo del Proceso Automatizado

El siguiente diagrama explica cómo interactúan los componentes técnicos de esta solución:

```mermaid
graph TD
    A[n8n Schedule Trigger<br/>Lunes 8:00 AM] --> B[Ejecutar Script Python<br/>generar_reporte.py];
    
    subgraph Data Extraction & Processing
        B --> C{Base de Datos<br/>Supabase / PostgreSQL};
        C -->|SQL Query: Ventas y Leads| B;
        B --> D[Pandas<br/>Cálculo de Métricas];
        D --> E[Matplotlib<br/>Generación Gráficos];
    end
    
    E --> F[Creación PDF<br/>reporte_ejemplo.pdf];
    F --> G[n8n Send Email Node];
    G --> H((Gerencia Inmobiliaria));
```

## Descripción de los Nodos

1. **Schedule Trigger**: Programado usando notación cron para que se ejecute a una hora y día específicos de la semana.
2. **Execute Command (Python)**: Llama al archivo `generar_reporte.py`, el cual carga las variables de entorno de Supabase, ejecuta las consultas SQL consolidadas, realiza agrupación y sumatorias con Pandas, y dibuja en Matplotlib.
3. **Send Email**: Toma el archivo binario PDF generado por el script anterior en la carpeta `examples/` y lo envía como adjunto junto a un template de email.
