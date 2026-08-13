# Inmobiliaria Reportes Automatizados

Este proyecto de portafolio demuestra la creación de un sistema de generación de reportes inmobiliarios totalmente automatizado. 
Combina la generación de datos mock con Python, el almacenamiento en una base de datos relacional (PostgreSQL/Supabase o SQLite), el procesamiento y la generación de gráficos con Pandas/Matplotlib, y la orquestación del flujo.

## El Problema
Los equipos de ventas y gerencia inmobiliaria dedican horas cada semana (aprox. 2 horas manuales) extrayendo datos de los sistemas CRM, armando Excels y diseñando PDFs para analizar métricas clave como:
- Propiedades vendidas
- Leads generados por zona
- Tiempo promedio de cierre
- Rendimiento por asesor

## La Solución (Impacto)
Este sistema **reduce el tiempo de generación de reportes de 2 horas a 3 minutos** de manera totalmente automatizada (ej. cada lunes a las 8 AM). Permite escalar el envío de reportes a la gerencia sin intervención humana.

## Arquitectura

1. **Base de Datos**: Esquema relacional con tablas `propiedades`, `clientes`, `leads` y `ventas`.
2. **Generación de Datos**: Script en Python usando `Faker` para simular un escenario realista del mercado inmobiliario colombiano.
3. **Reporte (ETL y Visualización)**: Script en Python con `pandas` para análisis de datos y `matplotlib` para la generación del PDF.
4. **Automatización (n8n)**: Flujo orquestado con n8n que automatiza la ejecución periódica.

## Cómo ejecutarlo localmente

1. **Instalar dependencias**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. **Generar base de datos de prueba** (por defecto creará un archivo SQLite `inmobiliaria.db`, o puedes configurar tus credenciales de Supabase):
   ```bash
   python scripts/generar_datos.py
   ```

3. **Generar reporte**:
   ```bash
   python scripts/generar_reporte.py
   ```

Esto generará un archivo `reporte_inmobiliario.pdf` con las métricas clave.
