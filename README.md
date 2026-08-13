# Inmobiliaria Reportes Automatizados

Este proyecto de portafolio demuestra la creación de un sistema de generación de reportes inmobiliarios totalmente automatizado. 
Combina la generación de datos mock con Python, el almacenamiento en una base de datos relacional (PostgreSQL/Supabase o SQLite), el procesamiento y la generación de gráficos con Pandas/Matplotlib, un microservicio REST con FastAPI y la orquestación del flujo en n8n.

## El Problema
Los equipos de ventas y gerencia inmobiliaria dedican horas cada semana (aprox. 2 horas manuales) extrayendo datos de los sistemas CRM, armando Excels y diseñando PDFs para analizar métricas clave como:
- Propiedades vendidas
- Leads generados por zona
- Tiempo promedio de cierre
- Rendimiento por asesor

## La Solución (Impacto)
Este sistema **reduce el tiempo de generación de reportes de 2 horas a 3 minutos** de manera totalmente automatizada (ej. cada lunes a las 8 AM). Permite escalar el envío de reportes a la gerencia sin intervención humana.

## Arquitectura

1. **Base de Datos**: Esquema relacional en Supabase (PostgreSQL) o SQLite local con tablas `propiedades`, `clientes`, `leads` y `ventas`.
2. **Generación de Datos**: Script en Python usando `Faker` para simular un escenario realista del mercado inmobiliario colombiano.
3. **Servicio Web & Visualización (FastAPI + Pandas/Matplotlib)**: Microservicio en Python que procesa los datos y genera el PDF dinámicamente expuesto en un endpoint REST (`POST /generar-reporte`).
4. **Orquestación (n8n en Easypanel/Docker)**: Flujo programado semanalmente que invoca el microservicio vía HTTP Request, obtiene el PDF y lo distribuye por Email y Slack.

---

## Cómo ejecutarlo localmente

1. **Instalar dependencias**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. **Generar base de datos de prueba**:
   ```bash
   python scripts/generar_datos.py
   ```

3. **Ejecutar API local con FastAPI**:
   ```bash
   python app.py
   ```
   *Accede a la documentación interactiva en `http://localhost:8000/docs`.*

4. **Generar reporte vía CLI o HTTP**:
   - Vía Python directo: `python scripts/generar_reporte.py`
   - Vía API REST: `curl -X POST http://localhost:8000/generar-reporte --output reporte.pdf`

---

## Despliegue en Easypanel (Docker + n8n)

1. **Desplegar la API en Easypanel:**
   - Crea un nuevo servicio desde este repositorio usando el [Dockerfile](file:///c:/Users/diego/OneDrive/Documentos/prueba-inlaze2/proyecto-portafolio/inmobiliaria-reportes-automatizados/Dockerfile).
   - Configura las variables de entorno `SUPABASE_URL` y `SUPABASE_KEY`.

2. **Importar el Workflow en n8n:**
   - Importa el archivo [n8n/workflow.json](file:///c:/Users/diego/OneDrive/Documentos/prueba-inlaze2/proyecto-portafolio/inmobiliaria-reportes-automatizados/n8n/workflow.json).
   - El nodo **HTTP Request** invocará `http://<nombre-servicio-easypanel>:8000/generar-reporte` y enviará el PDF adjunto por correo.
