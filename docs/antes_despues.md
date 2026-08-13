# Impacto del Proyecto: Automatización de Reportes Inmobiliarios

## El Problema: Proceso Manual ("El Antes")
En muchas agencias inmobiliarias, el proceso de consolidación de datos y generación de reportes es altamente ineficiente:
1. **Extracción de datos**: Exportar CSVs desde el CRM (ventas, leads, inventario).
2. **Limpieza y Cruce**: Usar Excel para cruzar datos y eliminar duplicados.
3. **Cálculos manuales**: Crear tablas dinámicas para calcular leads por origen, ventas por asesor, etc.
4. **Diseño visual**: Copiar los gráficos de Excel y pegarlos en una presentación de PowerPoint o Canva.
5. **Distribución**: Exportar a PDF y enviar manualmente por correo a los stakeholders.

**Tiempo estimado**: ~2 a 3 horas semanales por analista/asistente.
**Tasa de error**: Alta (errores de copiar/pegar, fórmulas rotas).

---

## La Solución: Sistema Automatizado ("El Después")
Al implementar este proyecto con Python, SQL y n8n, el proceso cambia radicalmente:
1. **Disparador programado**: n8n inicia el flujo automáticamente cada lunes a las 8:00 AM.
2. **Ejecución del script**: Python se conecta a la base de datos (PostgreSQL/Supabase) y ejecuta una consulta SQL optimizada para obtener los datos en tiempo real.
3. **Generación automática**: Pandas procesa las métricas y Matplotlib genera el reporte en formato PDF de manera instantánea.
4. **Distribución automática**: n8n envía el PDF generado directamente a la bandeja de entrada del gerente.

**Tiempo estimado**: ~3 minutos (completamente desatendido).
**Tasa de error**: Prácticamente 0% (basado en código y consultas estructuradas).

### Métricas de Éxito
- **Ahorro de Tiempo**: 80-90% de reducción en horas operativas semanales.
- **Eficiencia**: La gerencia recibe la información de manera puntual al iniciar la semana.
- **Escalabilidad**: El mismo script puede generar reportes individuales por asesor o por sucursal sin costo adicional de tiempo humano.
