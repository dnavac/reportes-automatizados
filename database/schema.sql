-- Tablas para Inmobiliaria Reportes Automatizados
-- Diseñado para PostgreSQL (Supabase) pero compatible en su mayoría con SQLite para pruebas locales.

CREATE TABLE IF NOT EXISTS propiedades (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL, -- Ej: Apartamento, Casa, Local
    zona VARCHAR(100) NOT NULL, -- Ej: Bocagrande, Manga
    precio NUMERIC(15, 2) NOT NULL,
    estado VARCHAR(20) NOT NULL, -- Disponible, Reservada, Vendida
    fecha_publicacion DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    presupuesto_max NUMERIC(15, 2),
    zona_interes VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id),
    propiedad_id INTEGER REFERENCES propiedades(id),
    fecha DATE NOT NULL,
    origen VARCHAR(50), -- Ej: Web, Referido, Facebook Ads
    estado VARCHAR(20) -- Nuevo, Contactado, Cerrado
);

CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    propiedad_id INTEGER REFERENCES propiedades(id),
    cliente_id INTEGER REFERENCES clientes(id),
    fecha_cierre DATE NOT NULL,
    valor_final NUMERIC(15, 2) NOT NULL,
    asesor VARCHAR(100) NOT NULL
);
