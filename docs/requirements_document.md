# Requerimientos de Datos - Plataforma de Análisis Financiero

## 1. Fuentes de Datos

### 1.1 Transacciones Bancarias

**Descripción**: Sistema Core Bancario que provee información de transacciones financieras de clientes.

| Atributo | Valor |
|----------|-------|
| Tipo | Base de datos transaccional PostgreSQL |
| Volumen estimado | 50 millones de registros/día |
| Frecuencia de actualización | Tiempo real (streaming) |
| Formato | JSON via CDC (Debezium) |
| Latencia objetivo | < 5 segundos |
| Retención | 7 años |

**Campos principales**:
- `transaction_id`: Identificador único de transacción
- `account_id`: Identificador de cuenta origen
- `recipient_account`: Identificador de cuenta destino
- `amount`: Monto de la transacción
- `currency`: Moneda (ISO 4217)
- `transaction_type`: Tipo de transacción (transferencia, pago, retiro, depósito)
- `timestamp`: Fecha y hora de la transacción
- `status`: Estado (completada, pendiente, fallida)
- `merchant_category`: Categoría del comercio
- `location`: Ubicación geográfica

### 1.2 Datos de Mercado

**Descripción**: Proveedor de datos bursátiles y de mercados financieros en tiempo real.

| Atributo | Valor |
|----------|-------|
| Tipo | API REST + WebSocket |
| Volumen estimado | 2 millones de registros/día |
| Frecuencia de actualización | Tiempo real (tick-by-tick) |
| Formato | JSON |
| Latencia objetivo | < 1 segundo |
| Retención | 5 años |

**Campos principales**:
- `symbol`: Símbolo del instrumento financiero
- `price`: Precio actual
- `bid`: Precio de compra
- `ask`: Precio de venta
- `volume`: Volumen de operaciones
- `timestamp`: Timestamp de la cotización
- `exchange`: Bolsa de valores
- `market_cap`: Capitalización de mercado
- `pe_ratio`: Relación precio/ganancias

### 1.3 Noticias Financieras

**Descripción**: Agregador de noticias financieras de múltiples fuentes.

| Atributo | Valor |
|----------|-------|
| Tipo | API REST + Webhooks |
| Volumen estimado | 100,000 artículos/día |
| Frecuencia de actualización | Cada 5 minutos |
| Formato | JSON |
| Latencia objetivo | < 30 segundos |
| Retención | 3 años |

**Campos principales**:
- `news_id`: Identificador único de noticia
- `title`: Título de la noticia
- `content`: Contenido completo
- `summary`: Resumen ejecutivo
- `source`: Fuente de la noticia
- `author`: Autor
- `published_at`: Fecha de publicación
- `sentiment`: Análisis de sentimiento (-1 a 1)
- `entities`: Entidades mencionadas (tickers, empresas)
- `categories`: Categorías temáticas

## 2. Requerimientos Funcionales

### 2.1 Ingesta de Datos

- **R1.1**: El sistema debe poder ingestar datos de las tres fuentes simultáneamente sin bloqueos.
- **R1.2**: La ingesta debe tolerar fallos temporales de las fuentes con reintento automático.
- **R1.3**: El sistema debe manejar picos de volumen de hasta 10x el volumen normal.
- **R1.4**: Cada registro ingestado debe recibir un identificador único de correlación.

### 2.2 Transformación de Datos

- **R2.1**: Las transformaciones deben normalizar formatos de fecha, moneda y números.
- **R2.2**: El sistema debe enriquecer datos de transacciones con información de mercado.
- **R2.3**: Las transformaciones deben preservar la trazabilidad completa del dato original.
- **R2.4**: El pipeline debe soportar transformación de esquemas (schema evolution).

### 2.3 Calidad de Datos

- **R3.1**: Cada registro debe pasar por validación de esquema antes de procesarse.
- **R3.2**: El sistema debe detectar y quarantenar registros con valores fuera de umbrales.
- **R3.3**: Se deben registrar métricas de calidad por fuente y por período.
- **R3.4**: Los datos duplicados deben identificarse y manejarse según reglas de idempotencia.

### 2.4 Almacenamiento

- **R4.1**: Los datos crudos deben almacenarse en formato columnar (Parquet/Delta).
- **R4.2**: El particionamiento debe realizarse por fecha y tipo de fuente.
- **R4.3**: Los datos deben cifrarse en reposo usando KMS.
- **R4.4**: El sistema debe mantener versionado de datos para auditoría.

### 2.5 Disponibilidad y Escalabilidad

- **R5.1**: El sistema debe mantener disponibilidad del 99.9%.
- **R5.2**: La arquitectura debe escalar horizontalmente para manejar crecimiento.
- **R5.3**: El tiempo de recuperación ante fallos debe ser menor a 15 minutos.
- **R5.4**: El sistema debe soportar reprocesamiento de datos históricos.

### 2.6 Seguridad

- **R6.1**: Todos los datos en tránsito deben usar TLS 1.3.
- **R6.2**: El acceso a datos sensibles debe controlarse por IAM con principio de mínimo privilegio.
- **R6.3**: Los logs de acceso deben preservarse por 1 año.
- **R6.4**: El sistema debe cumplir con PCI-DSS para datos de tarjetas.

## 3. Requerimientos No Funcionales

### 3.1 Rendimiento

- Latencia end-to-end: < 30 segundos para datos de transacciones
- Throughput mínimo: 10,000 transacciones/segundo
- Tiempo de consulta en Curated Zone: < 5 segundos para queries analíticos

### 3.2 Observabilidad

- Métricas de pipeline disponibles en CloudWatch
- Logs estructurados con correlación de request
- Alertas automáticas ante fallos de calidad o disponibilidad

### 3.3 Costo

- Costo de almacenamiento objetivo: < $0.023/GB/mes
- Costo de procesamiento objetivo: < $0.000014/registro