# Prompt para Mejorar el Codigo Base

Copia y pega el contenido del bloque de abajo en un asistente de IA (Claude, ChatGPT)
para obtener un ZIP con el proyecto completo y arrancable.

Si preferis trabajar en tu editor con un agente local (Claude Code, Cursor, Copilot), usa `AGENTS.md` en vez de este archivo: dice lo mismo pero para que escriba los archivos en disco.

## Las dos reglas que no se negocian

1. **Completa el boilerplate.** Todo lo que el proyecto necesita para compilar y arrancar: manifiesto de dependencias, punto de entrada, configuracion, capa de interfaz, y las capas del patron arquitectonico declarado. Eso es andamiaje y es tu trabajo.
2. **NO resuelvas el reto.** Los entregables de las fases son el trabajo de la persona. El hueco pedagogico se deja como esta: el proyecto arranca, pero lo que el reto pide implementar NO esta implementado.

Dicho de otra forma: si algo impide compilar, arreglalo. Si algo es logica de negocio incompleta, validaciones ausentes, un secreto hardcodeado o un patron mejorable, dejalo exactamente como esta — es lo que la persona tiene que encontrar.

## Superficie de practica — NO resuelvas

Estos archivos SON el ejercicio de la persona. No los implementes; deja stubs.

- `src/utils/security_utils.py` — El topic pide autenticacion/seguridad: este archivo es el ejercicio.

## Lo que le falta a este proyecto

Esto NO lo tenes que adivinar: salio de comparar el proyecto contra la arquitectura declarada del reto y de un analisis estatico del codigo. Completalo TODO.

### Archivos que la arquitectura del reto declara y no estan

Creálos con implementacion real, en la capa que les corresponde:

- `src/utils/security_utils.py`
- `tests/test_transformations.py`
- `tests/test_idempotency.py`

### Referencias colgando en el codigo que si esta

Cada una rompe la compilacion:

- `dags/financial_analysis_pipeline.py` — `DataWriter.get`: Se invoca `get` sobre `DataWriter`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `requirements.txt` — `aws-encryption-sdk@3.1.2`: aws-encryption-sdk declara la version 3.1.2, pero PyPI respondio que esa version no existe. Es una version inventada: reemplazala por una version publicada real, o si no se conoce con certeza, usa el mecanismo centralizado del ecosistema (BOM/parent/platform/version catalog) y no declares una version individual.
- `requirements.txt` — `delta-rs@0.17.0`: delta-rs declara la version 0.17.0, pero PyPI respondio que esa version no existe. Es una version inventada: reemplazala por una version publicada real, o si no se conoce con certeza, usa el mecanismo centralizado del ecosistema (BOM/parent/platform/version catalog) y no declares una version individual.

## Como saber que terminaste

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando corriendo sin errores es la definicion de "listo".

---

```
## Briefing del reto (autoridad)
Este bloque manda sobre los archivos adjuntos. El stack y el rol salen de AQUÍ, no de un topic genérico ni de markdown placeholder.

### Perfil
Chapter Ciencia de Datos, Especialidad Ingeniero de Datos, Seniority Master

### Brecha de conocimiento
Ha hecho el levantamiento de los requerimientos técnicos y funcionales de un proyecto de datos. Además, diseña la solución acorde a la necesidad.

### Misión / candidato
Candidato con experiencia senior en ingeniería de datos

### Reto
- Tema: Levantamiento de requerimientos de Arquitectura de Datos
- Seniority: master-l3
- Tipo: mixed
- Título: Diseño de Arquitectura de Datos para una Plataforma de Análisis Financiero
- Tiempo estimado: 10 horas

### Fases (trabajo del HUMANO — PROHIBIDO completarlas)
No implementes estos entregables. Dejalos como hueco pedagógico. El asistente solo materializa el proyecto arrancable para que el participante pueda trabajar.
- Fase 1: Identificación de Fuentes de Datos y Requerimientos Funcionales — objetivo: Enumerar y describir todas las fuentes de datos que la plataforma debe integrar y los requerimientos funcionales que deben ser satisfechos. — entregable (NO resolver): Documento que lista todas las fuentes de datos y sus requerimientos funcionales.
- Fase 2: Definición de la Arquitectura de Datos — objetivo: Diseñar la arquitectura de datos que soporte los requerimientos identificados en la fase anterior. — entregable (NO resolver): Diagrama de la arquitectura de datos y documento descriptivo.
- Fase 3: Integración con Sistemas de Terceros — objetivo: Describir cómo la plataforma se integrará con sistemas de terceros para obtener datos adicionales. — entregable (NO resolver): Documento que describe la integración con sistemas de terceros.
- Fase 4: Revisión y Optimización de la Arquitectura — objetivo: Revisar y optimizar la arquitectura de datos diseñada para asegurar que cumple con todos los requerimientos y es eficiente. — entregable (NO resolver): Documento que describe las mejoras realizadas y su impacto en la arquitectura.

Eres un asistente experto en análisis, corrección y generación de archivos de cualquier tipo:
código fuente, documentación, hojas de cálculo, documentos Word, configuraciones, entre otros.
Voy a enviarte una cadena de texto que contiene uno o más archivos. Cada archivo está delimitado por un marcador con el siguiente formato:
// === ARCHIVO: ruta/del/archivo.extension ===
o también puede aparecer como:
## === ARCHIVO: ruta/del/archivo.extension ===
Lo que sigue al marcador puede ser:

El contenido real del archivo (código, texto, YAML, etc.)
Una descripción en lenguaje natural de lo que debe contener el archivo


TU TAREA
PASO 0 — ¿Esto es un proyecto o una carcasa?
Antes de extraer archivos, leé el Briefing (si está) y diagnosticá el adjunto.

Es CARCASA si ocurre CUALQUIERA de estas:
- No hay manifiesto de dependencias del stack del briefing (manifest.json de VTEX IO / package.json / pom.xml / build.gradle / requirements.txt / go.mod / *.tf / *.csproj, según corresponda)
- Hay un "binario" que en realidad es un comentario ("no puede ser mostrado como texto plano", placeholder .fig/.docx vacío)
- Los markdowns ya completan entregables de fases posteriores ("se implementó fade-in", lista de áreas ya resuelta)

Si es CARCASA:
- MATERIALIZÁ un proyecto que arranca en el stack del briefing (VTEX IO Store Framework, Angular, Terraform, pytest, Nest, etc.). Incluí manifiesto, punto de entrada y capa de interfaz reales.
- NO copies los markdowns de "solución" como si fueran el producto. Son ruido de generación.
- NO resuelvas las fases del briefing (están marcadas PROHIBIDO). Dejá el hueco pedagógico: el flujo existe, las microinteracciones/calidad/infra que el reto pide NO están hechas.
- Después seguí al PASO 5 (ZIP).

Si es un proyecto REAL (manifiesto + código que compila o arranca):
- Seguí PASO 1 en adelante. 🔴 compilación sí. 🟡 pedagógico no.

PASO 1 — Detección y extracción
Identifica todos los archivos presentes en la cadena. Para cada archivo extrae:

Su ruta completa (ej: src/main/java/com/pragma/Service.java)
Su contenido o descripción

PASO 2 — Clasificación por tipo
Clasifica cada archivo en una de estas categorías:
A) Código fuente (Java, Python, TypeScript, JavaScript, Kotlin, etc.)
B) Configuración / documentación (YAML, properties, Markdown, JSON, txt, etc.)
C) Excel (.xlsx, .xls, .csv)
D) Word (.docx, .doc)
E) Otro tipo de archivo binario o especial
PASO 3 — Clasificación de errores en código fuente

Objetivo prioritario: que el proyecto compile. No corrijas flujo de negocio ni lógica funcional.

Antes de modificar cualquier archivo de código fuente, clasifica cada problema encontrado en una de estas dos categorías:
🔴 ERROR DE COMPILACIÓN — corregir siempre
Son errores que impiden que el proyecto arranque, sin valor pedagógico:

Import faltante o incorrecto
Clase, método o variable referenciada que no existe en ningún archivo del proyecto
Error de sintaxis
Anotación con atributos inválidos
Dependencia ausente en pom.xml, package.json, etc.
Archivo referenciado que no existe y debe ser creado con implementación mínima

→ CORREGIR estos errores.
🟡 PROBLEMA FUNCIONAL O DE CALIDAD — preservar siempre
Son problemas que no impiden compilar. Pueden ser intencionales para el aprendizaje:

Clave secreta hardcodeada ("secret", "password123")
API deprecada que funciona pero tiene reemplazo moderno
Lógica de negocio incorrecta o incompleta
Código redundante o de baja legibilidad
Falta de validaciones en flujo de negocio
Patrones de diseño incorrectos pero funcionales
Concurrencia no segura
Configuración funcional pero no óptima

→ PRESERVAR tal cual. No corregir, no mejorar, no comentar.
PASO 4 — Procesamiento según tipo de archivo
Tipo A — Código fuente
Aplica únicamente las correcciones clasificadas como 🔴 ERROR DE COMPILACIÓN.
No alteres ningún elemento clasificado como 🟡 PROBLEMA FUNCIONAL O DE CALIDAD.
Si falta un archivo referenciado, créalo con la implementación mínima necesaria para compilar.
Tipo B — Configuración / documentación
Extrae el contenido tal cual, sin modificaciones salvo errores evidentes de sintaxis
(ej: YAML mal indentado).
Tipo C — Excel (.xlsx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un archivo Excel funcional con:

Fila de encabezados en negrita con color de fondo distintivo
Columnas con ancho ajustado al contenido
Tipos de dato correctos por columna
Validaciones si la descripción lo indica
Hojas nombradas descriptivamente si hay más de una
Filas de ejemplo si no hay datos reales

Tipo D — Word (.docx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un documento Word funcional con:

Estilos de título (Título 1, Título 2) para jerarquía de secciones
Fuente legible (Calibri o equivalente), tamaño 11-12pt para cuerpo
Márgenes estándar
Tabla de contenido si tiene múltiples secciones
Tablas con encabezados en negrita si aplica

Tipo E — Otro
Genera el archivo con el contenido o estructura más apropiada según la descripción.
PASO 5 — Exportación en ZIP
Empaqueta todos los archivos en un único archivo ZIP descargable respetando exactamente
la estructura de rutas indicada por los marcadores.
El ZIP debe incluir:

Archivos de código con únicamente los errores de compilación corregidos
Archivos de configuración y documentación sin cambios
Archivos nuevos creados para resolver dependencias de compilación faltantes
Archivos Excel y Word generados desde descripción

IMPORTANTE: El ZIP debe estar listo para descargar al finalizar. No preguntes si el usuario
quiere generarlo. Simplemente genera el archivo y proporciona el enlace de descarga; No debes desplegar en el chat el resumen de lo que arreglaste al Zip, solo entregalo.

REGLAS IMPORTANTES

No omitas ningún archivo aunque no tenga errores ni modificaciones
Respeta los nombres y rutas exactas indicadas por los marcadores
Si un archivo no tiene marcador claro, infiere el nombre desde su contenido
Si la cadena contiene solo documentación, placeholders o binarios fake, NO la reproduzcas:
aplicá PASO 0 (materializar el proyecto del briefing). Reproducir la carcasa es un fallo.
No agregues texto después del enlace de descarga del ZIP
No preguntes si el usuario quiere el ZIP: simplemente generalo siempre
Si detectas que falta un archivo de configuración necesario para compilar
(pom.xml, package.json, requirements.txt, build.gradle, etc.), créalo e inclúyelo
inferiendo su contenido desde los imports y frameworks detectados en el código
Nunca corrijas problemas 🟡 aunque parezcan obvios o fáciles de mejorar.
El participante que recibirá este proyecto los debe encontrar y resolver él mismo.


INPUT
Aquí está la cadena con los archivos:

// === ARCHIVO: requirements.txt ===
apache-airflow==2.9.3
pandas==2.2.2
pyspark==3.5.1
boto3==1.34.120
pyarrow==16.1.0
pytest==8.2.0
jsonschema==4.22.0
cryptography==42.0.8
python-dotenv==1.0.1

# Dependencias adicionales para manejo de esquemas y validación
fastjsonschema==2.19.1
python-dateutil==2.9.0.post0
pytz==2024.1

# Dependencias para manejo de datos sensibles y seguridad
aws-encryption-sdk==3.1.2
pyjwt==2.8.0

# Dependencias para logging y monitoreo
structlog==24.1.0
colorama==0.4.6

# Dependencias para manejo de particionamiento y formatos columnares
delta-rs==0.17.0
s3fs==2024.3.1

# Dependencias para orquestación avanzada
apache-airflow-providers-amazon==8.19.0
apache-airflow-providers-apache-spark==4.7.0

// === ARCHIVO: src/schemas/transaction_schema.json ===
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Esquema de Transacciones Bancarias",
  "description": "Esquema para validar la estructura de datos de transacciones bancarias.",
  "type": "object",
  "properties": {
    "transaction_id": {
      "description": "Identificador único de la transacción.",
      "type": "string",
      "format": "uuid",
      "minLength": 36,
      "maxLength": 36
    },
    "account_id": {
      "description": "Identificador de la cuenta bancaria.",
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    },
    "transaction_date": {
      "description": "Fecha y hora de la transacción en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    },
    "amount": {
      "description": "Monto de la transacción.",
      "type": "number",
      "minimum": -1000000,
      "maximum": 1000000
    },
    "currency": {
      "description": "Moneda de la transacción.",
      "type": "string",
      "enum": ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "MXN", "BRL"]
    },
    "transaction_type": {
      "description": "Tipo de transacción.",
      "type": "string",
      "enum": ["DEPOSIT", "WITHDRAWAL", "TRANSFER", "PAYMENT", "FEE", "INTEREST"]
    },
    "description": {
      "description": "Descripción de la transacción.",
      "type": "string",
      "maxLength": 200
    },
    "merchant": {
      "description": "Información del comercio asociado a la transacción.",
      "type": "object",
      "properties": {
        "merchant_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 50
        },
        "merchant_name": {
          "type": "string",
          "maxLength": 100
        },
        "merchant_category": {
          "type": "string",
          "enum": ["RETAIL", "GROCERY", "TRAVEL", "ENTERTAINMENT", "HEALTH", "UTILITIES", "OTHER"]
        }
      },
      "required": ["merchant_id", "merchant_name"]
    },
    "location": {
      "description": "Ubicación geográfica de la transacción.",
      "type": "object",
      "properties": {
        "latitude": {
          "type": "number",
          "minimum": -90,
          "maximum": 90
        },
        "longitude": {
          "type": "number",
          "minimum": -180,
          "maximum": 180
        },
        "country": {
          "type": "string",
          "minLength": 2,
          "maxLength": 2
        },
        "city": {
          "type": "string",
          "maxLength": 100
        }
      },
      "required": ["latitude", "longitude"]
    },
    "status": {
      "description": "Estado de la transacción.",
      "type": "string",
      "enum": ["PENDING", "COMPLETED", "FAILED", "REVERSED"]
    },
    "metadata": {
      "description": "Metadatos adicionales de la transacción.",
      "type": "object",
      "additionalProperties": {
        "type": "string"
      }
    },
    "created_at": {
      "description": "Fecha y hora de creación del registro en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "description": "Fecha y hora de última actualización del registro en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "transaction_id",
    "account_id",
    "transaction_date",
    "amount",
    "currency",
    "transaction_type",
    "status",
    "created_at"
  ],
  "additionalProperties": false
}

// === ARCHIVO: src/schemas/market_data_schema.json ===
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Esquema de Datos de Mercado",
  "description": "Esquema para validar la estructura de datos de mercado financiero.",
  "type": "object",
  "properties": {
    "symbol": {
      "description": "Símbolo del instrumento financiero.",
      "type": "string",
      "minLength": 1,
      "maxLength": 20
    },
    "timestamp": {
      "description": "Fecha y hora del dato en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    },
    "open": {
      "description": "Precio de apertura.",
      "type": "number",
      "minimum": 0
    },
    "high": {
      "description": "Precio máximo.",
      "type": "number",
      "minimum": 0
    },
    "low": {
      "description": "Precio mínimo.",
      "type": "number",
      "minimum": 0
    },
    "close": {
      "description": "Precio de cierre.",
      "type": "number",
      "minimum": 0
    },
    "volume": {
      "description": "Volumen negociado.",
      "type": "integer",
      "minimum": 0
    },
    "adjusted_close": {
      "description": "Precio de cierre ajustado.",
      "type": "number",
      "minimum": 0
    },
    "dividend_amount": {
      "description": "Monto de dividendo.",
      "type": "number",
      "minimum": 0
    },
    "split_coefficient": {
      "description": "Coeficiente de split.",
      "type": "number",
      "minimum": 0
    },
    "exchange": {
      "description": "Mercado de negociación.",
      "type": "string",
      "enum": ["NYSE", "NASDAQ", "LSE", "TSE", "HKEX", "EURONEXT", "BM&FBOVESPA", "OTHER"]
    },
    "currency": {
      "description": "Moneda del instrumento.",
      "type": "string",
      "enum": ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "BRL", "MXN"]
    },
    "metadata": {
      "description": "Metadatos adicionales del instrumento.",
      "type": "object",
      "properties": {
        "sector": {
          "type": "string",
          "enum": ["TECHNOLOGY", "FINANCE", "HEALTHCARE", "ENERGY", "UTILITIES", "CONSUMER", "INDUSTRIALS", "OTHER"]
        },
        "industry": {
          "type": "string"
        },
        "market_cap": {
          "type": "number",
          "minimum": 0
        }
      },
      "additionalProperties": true
    },
    "created_at": {
      "description": "Fecha y hora de creación del registro en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "description": "Fecha y hora de última actualización del registro en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "symbol",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "created_at"
  ],
  "additionalProperties": false
}

// === ARCHIVO: src/schemas/news_schema.json ===
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Esquema de Noticias Financieras",
  "description": "Esquema para validar la estructura de datos de noticias financieras.",
  "type": "object",
  "properties": {
    "news_id": {
      "description": "Identificador único de la noticia.",
      "type": "string",
      "format": "uuid",
      "minLength": 36,
      "maxLength": 36
    },
    "title": {
      "description": "Título de la noticia.",
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "content": {
      "description": "Contenido de la noticia.",
      "type": "string",
      "minLength": 1
    },
    "source": {
      "description": "Fuente de la noticia.",
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "author": {
      "description": "Autor de la noticia.",
      "type": "string",
      "maxLength": 100
    },
    "published_date": {
      "description": "Fecha y hora de publicación en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    },
    "url": {
      "description": "URL de la noticia.",
      "type": "string",
      "format": "uri",
      "maxLength": 500
    },
    "symbols": {
      "description": "Símbolos financieros mencionados en la noticia.",
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 20
      },
      "minItems": 0,
      "uniqueItems": true
    },
    "sentiment": {
      "description": "Sentimiento asociado a la noticia.",
      "type": "string",
      "enum": ["POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED"]
    },
    "sentiment_score": {
      "description": "Puntuación de sentimiento.",
      "type": "number",
      "minimum": -1,
      "maximum": 1
    },
    "metadata": {
      "description": "Metadatos adicionales de la noticia.",
      "type": "object",
      "properties": {
        "categories": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["MARKET", "ECONOMY", "POLITICS", "TECHNOLOGY", "ENERGY", "HEALTHCARE", "OTHER"]
          },
          "minItems": 0,
          "uniqueItems": true
        },
        "entities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "type": {
                "type": "string",
                "enum": ["PERSON", "ORGANIZATION", "LOCATION", "EVENT"]
              }
            },
            "required": ["name", "type"]
          }
        }
      },
      "additionalProperties": true
    },
    "created_at": {
      "description": "Fecha y hora de creación del registro en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "description": "Fecha y hora de última actualización del registro en formato ISO 8601.",
      "type": "string",
      "format": "date-time"
    }
  },
  "required": [
    "news_id",
    "title",
    "content",
    "source",
    "published_date",
    "created_at"
  ],
  "additionalProperties": false
}

// === ARCHIVO: dags/financial_analysis_pipeline.py ===
"""
DAG principal para el pipeline de análisis financiero.
Orquesta las etapas de extracción, transformación y carga de datos
provenientes de múltiples fuentes: transacciones bancarias, datos de mercado y noticias financieras.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor

import pandas as pd
import boto3
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
}

ENVIRONMENT = Variable.get('environment', default_var='dev')
EXECUTION_DATE = '{{ ds }}'


def load_config() -> Dict[str, Any]:
    """Carga la configuración del pipeline según el ambiente."""
    config_path = f'conf/{ENVIRONMENT}_config.json'
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config {config_path} no encontrada, usando defaults")
        return {
            's3_bucket': 'financial-data-platform',
            'data_lake_path': 's3://financial-data-platform/data-lake/',
            'output_path': 's3://financial-data-platform/output/',
            'quality_threshold': 0.95,
            'batch_size': 10000
        }


def extract_bank_transactions(**context) -> str:
    """Extrae datos de transacciones bancarias desde la fuente origen."""
    from src.extract.bank_transactions_reader import BankTransactionsReader
    
    config = load_config()
    execution_date = context['ds']
    
    logger.info(f"Iniciando extracción de transacciones bancarias para {execution_date}")
    
    reader = BankTransactionsReader(
        s3_bucket=config.get('s3_bucket'),
        region_name=config.get('aws_region', 'us-east-1')
    )
    
    transactions = reader.read(
        start_date=execution_date,
        end_date=execution_date,
        account_ids=config.get('account_ids', [])
    )
    
    output_key = f"raw/bank_transactions/{execution_date}/transactions.parquet"
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    df = pd.DataFrame(transactions)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    logger.info(f"Extraídas {len(transactions)} transacciones bancarias")
    return output_key


def extract_market_data(**context) -> str:
    """Extrae datos de mercado financiero desde APIs externas."""
    from src.extract.market_data_reader import MarketDataReader
    
    config = load_config()
    execution_date = context['ds']
    
    logger.info(f"Iniciando extracción de datos de mercado para {execution_date}")
    
    reader = MarketDataReader(
        api_key=config.get('market_api_key'),
        region=config.get('aws_region', 'us-east-1')
    )
    
    market_data = reader.read(
        symbols=config.get('market_symbols', ['AAPL', 'GOOGL', 'MSFT']),
        date=execution_date
    )
    
    output_key = f"raw/market_data/{execution_date}/market_data.parquet"
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    df = pd.DataFrame(market_data)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    logger.info(f"Extraídos {len(market_data)} registros de mercado")
    return output_key


def extract_financial_news(**context) -> str:
    """Extrae noticias financieras desde fuentes de terceros."""
    from src.extract.financial_news_reader import FinancialNewsReader
    
    config = load_config()
    execution_date = context['ds']
    
    logger.info(f"Iniciando extracción de noticias financieras para {execution_date}")
    
    reader = FinancialNewsReader(
        api_key=config.get('news_api_key'),
        region=config.get('aws_region', 'us-east-1')
    )
    
    news = reader.read(
        keywords=config.get('news_keywords', ['finance', 'stock', 'market']),
        date=execution_date
    )
    
    output_key = f"raw/financial_news/{execution_date}/news.parquet"
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    df = pd.DataFrame(news)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    logger.info(f"Extraídas {len(news)} noticias financieras")
    return output_key


def validate_data_quality(**context) -> Dict[str, Any]:
    """Aplica reglas de calidad de datos a los datos extraídos."""
    from src.transform.data_quality_rules import DataQualityRules
    
    config = load_config()
    ti = context['ti']
    
    bank_transactions_key = ti.xcom_pull(task_ids='extract_bank_transactions')
    market_data_key = ti.xcom_pull(task_ids='extract_market_data')
    financial_news_key = ti.xcom_pull(task_ids='extract_financial_news')
    
    logger.info("Iniciando validación de calidad de datos")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket = config.get('s3_bucket')
    
    quality_rules = DataQualityRules(threshold=config.get('quality_threshold', 0.95))
    
    quality_results = {}
    
    for source, key in [
        ('bank_transactions', bank_transactions_key),
        ('market_data', market_data_key),
        ('financial_news', financial_news_key)
    ]:
        if key:
            obj = s3_hook.get_key(key, bucket)
            df = pd.read_parquet(f"s3://{bucket}/{key}")
            
            quality_result = quality_rules.validate(df, source)
            quality_results[source] = quality_result
            
            logger.info(f"Calidad {source}: {quality_result['score']:.2%}")
            
            if quality_result['score'] < config.get('quality_threshold', 0.95):
                quarantine_key = f"quarantine/{source}/{context['ds']}/data.parquet"
                buffer = df.to_parquet(engine='pyarrow', compression='snappy')
                s3_hook.load_bytes(
                    buffer.getvalue(),
                    key=quarantine_key,
                    bucket_name=bucket,
                    replace=True
                )
                logger.warning(f"Datos de {source} en cuarentena: score={quality_result['score']:.2%}")
    
    return json.dumps(quality_results)


def transform_financial_data(**context) -> str:
    """Aplica transformaciones financieras a los datos validados."""
    from src.transform.financial_data_transformer import FinancialDataTransformer
    
    config = load_config()
    ti = context['ti']
    
    bank_transactions_key = ti.xcom_pull(task_ids='extract_bank_transactions')
    market_data_key = ti.xcom_pull(task_ids='extract_market_data')
    financial_news_key = ti.xcom_pull(task_ids='extract_financial_news')
    
    logger.info("Iniciando transformación de datos financieros")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket = config.get('s3_bucket')
    
    transformer = FinancialDataTransformer(config)
    
    dfs = {}
    for source, key in [
        ('transactions', bank_transactions_key),
        ('market', market_data_key),
        ('news', financial_news_key)
    ]:
        if key:
            obj = s3_hook.get_key(key, bucket)
            dfs[source] = pd.read_parquet(f"s3://{bucket}/{key}")
    
    transformed_data = transformer.transform(dfs)
    
    output_key = f"transformed/financial_analysis/{context['ds']}/data.parquet"
    
    df = pd.DataFrame(transformed_data)
    buffer = df.to_parquet(engine='pyarrow', compression='snappy')
    
    s3_hook.load_bytes(
        buffer.getvalue(),
        key=output_key,
        bucket_name=bucket,
        replace=True
    )
    
    logger.info(f"Transformados {len(transformed_data)} registros")
    return output_key


def load_to_destination(**context) -> str:
    """Carga los datos transformados al destino final."""
    from src.load.data_writer import DataWriter
    
    config = load_config()
    ti = context['ti']
    
    transformed_key = ti.xcom_pull(task_ids='transform_financial_data')
    quality_results = ti.xcom_pull(task_ids='validate_data_quality')
    
    logger.info("Iniciando carga de datos al destino")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    bucket = config.get('s3_bucket')
    
    obj = s3_hook.get_key(transformed_key, bucket)
    df = pd.read_parquet(f"s3://{bucket}/{transformed_key}")
    
    writer = DataWriter(
        output_path=config.get('output_path'),
        partition_by=['date', 'source'],
        format='delta'
    )
    
    result = writer.write(
        df=df,
        table_name='financial_analysis',
        mode='merge',
        partition_date=context['ds']
    )
    
    logger.info(f"Cargados {result['records_written']} registros a destino")
    return json.dumps(result)


def generate_analysis_report(**context):
    """Genera reporte de análisis y métricas del pipeline."""
    config = load_config()
    ti = context['ti']
    
    load_result = json.loads(ti.xcom_pull(task_ids='load_to_destination'))
    quality_results = json.loads(ti.xcom_pull(task_ids='validate_data_quality'))
    
    report = {
        'execution_date': context['ds'],
        'records_processed': load_result.get('records_written', 0),
        'quality_scores': quality_results,
        'status': 'SUCCESS' if load_result.get('records_written', 0) > 0 else 'FAILED',
        'environment': ENVIRONMENT
    }
    
    logger.info(f"Reporte de análisis: {json.dumps(report, indent=2)}")
    
    s3_hook = S3Hook(aws_conn_id='aws_default')
    report_key = f"reports/{context['ds']}/analysis_report.json"
    
    s3_hook.load_string(
        json.dumps(report, indent=2),
        key=report_key,
        bucket_name=config.get('s3_bucket'),
        replace=True
    )
    
    return report_key


with DAG(
    dag_id='financial_analysis_pipeline',
    default_args=DEFAULT_ARGS,
    description='Pipeline ETL para análisis financiero con datos de múltiples fuentes',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'financial', 'analysis', 'data-lake'],
    doc_md="""
# Pipeline de Análisis Financiero

Este DAG orquesta el flujo completo de extracción, transformación y carga de datos
provenientes de tres fuentes principales:
- Transacciones bancarias
- Datos de mercado financiero
- Noticias financieras

## Flujo de Ejecución

1. **Extracción**: Los datos se extraen de sus fuentes originales y se almacenan en formato Parquet.
2. **Validación**: Se aplican reglas de calidad para verificar integridad de los datos.
3. **Transformación**: Transformaciones financieras específicas se aplican a los datos validados.
4. **Carga**: Los datos transformados se cargan al destino final en formato Delta.
5. **Reporte**: Se genera un reporte de análisis del pipeline.

## Configuración

- **Programación**: Diario a las 6:00 AM
- **Retries**: 3 intentos con backoff exponencial
- **Particionamiento**: Por fecha y fuente de datos
"""
) as dag:
    
    start = EmptyOperator(task_id='start', doc_md='Inicio del pipeline de análisis financiero')
    
    extract_bank = PythonOperator(
        task_id='extract_bank_transactions',
        python_callable=extract_bank_transactions,
        provide_context=True,
        doc_md='Extrae transacciones bancarias desde la fuente origen'
    )
    
    extract_market = PythonOperator(
        task_id='extract_market_data',
        python_callable=extract_market_data,
        provide_context=True,
        doc_md='Extrae datos de mercado desde APIs externas'
    )
    
    extract_news = PythonOperator(
        task_id='extract_financial_news',
        python_callable=extract_financial_news,
        provide_context=True,
        doc_md='Extrae noticias financieras desde fuentes de terceros'
    )
    
    extraction_complete = EmptyOperator(
        task_id='extraction_complete',
        doc_md='Todas las fuentes de datos extraídas'
    )
    
    validate_quality = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        provide_context=True,
        doc_md='Aplica reglas de calidad a los datos extraídos',
        trigger_rule='all_done'
    )
    
    transform_data = PythonOperator(
        task_id='transform_financial_data',
        python_callable=transform_financial_data,
        provide_context=True,
        doc_md='Aplica transformaciones financieras a los datos validados',
        trigger_rule='all_done'
    )
    
    load_data = PythonOperator(
        task_id='load_to_destination',
        python_callable=load_to_destination,
        provide_context=True,
        doc_md='Carga los datos transformados al destino final',
        trigger_rule='all_done'
    )
    
    generate_report = PythonOperator(
        task_id='generate_analysis_report',
        python_callable=generate_analysis_report,
        provide_context=True,
        doc_md='Genera reporte de análisis y métricas del pipeline',
        trigger_rule='all_done'
    )
    
    end = EmptyOperator(task_id='end', doc_md='Fin del pipeline de análisis financiero')
    
    start >> [extract_bank, extract_market, extract_news] >> extraction_complete
    extraction_complete >> validate_quality >> transform_data >> load_data >> generate_report >> end

// === ARCHIVO: src/extract/bank_transactions_reader.py ===
"""
Lector de transacciones bancarias para el pipeline de análisis financiero.
Se conecta a la fuente de datos bancarios y extrae transacciones en bruto.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional
from dataclasses import dataclass, field

import pandas as pd
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class TransactionRecord:
    """Representa una transacción bancaria individual."""
    transaction_id: str
    account_id: str
    timestamp: datetime
    amount: float
    currency: str
    transaction_type: str
    description: str
    merchant_id: Optional[str] = None
    merchant_category: Optional[str] = None
    status: str = "completed"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "timestamp": self.timestamp.isoformat(),
            "amount": self.amount,
            "currency": self.currency,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "merchant_id": self.merchant_id,
            "merchant_category": self.merchant_category,
            "status": self.status,
            "metadata": self.metadata
        }


class BankTransactionsReader:
    """
    Clase principal para leer transacciones bancarias de múltiples fuentes.
    Soporta conexión a APIs de bancos, bases de datos y archivos en S3.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config.get("source_type", "api")
        self.source_credentials = config.get("credentials", {})
        self.batch_size = config.get("batch_size", 1000)
        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay", 5)
        self._s3_client = None
        self._db_connection = None
        self._api_session = None

    def _get_s3_client(self):
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self.source_credentials.get("aws_access_key"),
                aws_secret_access_key=self.source_credentials.get("aws_secret_key"),
                region_name=self.source_credentials.get("region", "us-east-1")
            )
        return self._s3_client

    def _get_db_connection(self):
        if self._db_connection is None:
            import psycopg2
            self._db_connection = psycopg2.connect(
                host=self.source_credentials.get("db_host"),
                port=self.source_credentials.get("db_port", 5432),
                database=self.source_credentials.get("db_name"),
                user=self.source_credentials.get("db_user"),
                password=self.source_credentials.get("db_password")
            )
        return self._db_connection

    def _retry_with_backoff(self, func, *args, **kwargs):
        import time
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (ClientError, BotoCoreError, Exception) as e:
                last_exception = e
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
        raise last_exception

    def read_from_api(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> Iterator[TransactionRecord]:
        """
        Lee transacciones desde API bancaria con paginación.
        """
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        api_url = self.source_credentials.get("api_url")
        api_key = self.source_credentials.get("api_key")

        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Request-ID": f"bankReader-{datetime.now().timestamp()}"
        }

        page = 1
        has_more = True

        while has_more:
            params = {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "page": page,
                "page_size": self.batch_size
            }
            if account_ids:
                params["account_ids"] = ",".join(account_ids)

            try:
                response = session.get(
                    f"{api_url}/transactions",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                for txn_data in data.get("transactions", []):
                    yield self._parse_transaction(txn_data)

                has_more = data.get("has_more", False)
                page += 1

            except requests.RequestException as e:
                logger.error(f"API request failed: {str(e)}")
                raise

    def read_from_s3(
        self,
        bucket: str,
        prefix: str,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[TransactionRecord]:
        """
        Lee transacciones desde archivos en S3 con partición por fecha.
        """
        s3_client = self._get_s3_client()

        date_format = "%Y-%m-%d"
        date_range = pd.date_range(start_date, end_date, freq='D')

        for date_obj in date_range:
            date_str = date_obj.strftime(date_format)
            object_key = f"{prefix}/date={date_str}/transactions.parquet"

            try:
                response = s3_client.get_object(Bucket=bucket, Key=object_key)
                data = response['Body'].read()

                df = pd.read_parquet(pd.io.common.BytesIO(data))

                for _, row in df.iterrows():
                    yield self._row_to_transaction_record(row)

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code == 'NoSuchKey':
                    logger.info(f"No transactions file for date {date_str}")
                    continue
                logger.error(f"S3 error reading {object_key}: {str(e)}")
                raise

    def read_from_database(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> Iterator[TransactionRecord]:
        """
        Lee transacciones desde base de datos PostgreSQL.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                transaction_id, account_id, timestamp, amount,
                currency, transaction_type, description,
                merchant_id, merchant_category, status, metadata
            FROM bank_transactions
            WHERE timestamp >= %s AND timestamp < %s
        """
        params = [start_date, end_date]

        if account_ids:
            query += " AND account_id = ANY(%s)"
            params.append(account_ids)

        query += " ORDER BY timestamp LIMIT %s OFFSET %s"

        offset = 0
        while True:
            cursor.execute(query, params + [self.batch_size, offset])
            rows = cursor.fetchall()

            if not rows:
                break

            for row in rows:
                yield TransactionRecord(
                    transaction_id=row[0],
                    account_id=row[1],
                    timestamp=row[2],
                    amount=float(row[3]),
                    currency=row[4],
                    transaction_type=row[5],
                    description=row[6],
                    merchant_id=row[7],
                    merchant_category=row[8],
                    status=row[9],
                    metadata=row[10] if isinstance(row[10], dict) else {}
                )

            offset += self.batch_size

        cursor.close()

    def _parse_transaction(self, data: Dict[str, Any]) -> TransactionRecord:
        """Convierte diccionario de API a TransactionRecord."""
        return TransactionRecord(
            transaction_id=data["id"],
            account_id=data["account_id"],
            timestamp=datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00')),
            amount=float(data["amount"]),
            currency=data.get("currency", "USD"),
            transaction_type=data["type"],
            description=data.get("description", ""),
            merchant_id=data.get("merchant_id"),
            merchant_category=data.get("merchant_category"),
            status=data.get("status", "completed"),
            metadata=data.get("metadata", {})
        )

    def _row_to_transaction_record(self, row: pd.Series) -> TransactionRecord:
        """Convierte fila de DataFrame a TransactionRecord."""
        return TransactionRecord(
            transaction_id=str(row['transaction_id']),
            account_id=str(row['account_id']),
            timestamp=pd.to_datetime(row['timestamp']),
            amount=float(row['amount']),
            currency=str(row.get('currency', 'USD')),
            transaction_type=str(row['transaction_type']),
            description=str(row.get('description', '')),
            merchant_id=str(row['merchant_id']) if pd.notna(row.get('merchant_id')) else None,
            merchant_category=str(row['merchant_category']) if pd.notna(row.get('merchant_category')) else None,
            status=str(row.get('status', 'completed')),
            metadata=dict(row['metadata']) if 'metadata' in row and pd.notna(row.get('metadata')) else {}
        )

    def read(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> Iterator[TransactionRecord]:
        """
        Método principal que delega según la configuración de fuente.
        """
        logger.info(
            f"Reading bank transactions from {start_date} to {end_date}"
        )

        if self.source_type == "api":
            yield from self.read_from_api(start_date, end_date, account_ids)
        elif self.source_type == "s3":
            bucket = self.source_credentials.get("s3_bucket")
            prefix = self.source_credentials.get("s3_prefix", "transactions")
            yield from self.read_from_s3(bucket, prefix, start_date, end_date)
        elif self.source_type == "database":
            yield from self.read_from_database(start_date, end_date, account_ids)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def read_as_dataframe(
        self,
        start_date: datetime,
        end_date: datetime,
        account_ids: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Retorna los datos como DataFrame de pandas para integración con el pipeline.
        """
        records = list(self.read(start_date, end_date, account_ids))
        if not records:
            return pd.DataFrame()

        data = [record.to_dict() for record in records]
        df = pd.DataFrame(data)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        logger.info(f"Loaded {len(df)} transactions")

        return df

    def close(self):
        """Cleanup de recursos."""
        if self._db_connection:
            self._db_connection.close()
            self._db_connection = None
        logger.info("Bank transactions reader closed")


def create_reader(config_path: str = "conf/dev_config.json") -> BankTransactionsReader:
    """Factory para crear reader desde archivo de configuración."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return BankTransactionsReader(config.get("bank_transactions", {}))

// === ARCHIVO: src/extract/market_data_reader.py ===
"""
Lector de datos de mercado para el pipeline de análisis financiero.
Extrae precios de acciones, divisas, commodities y otros instrumentos financieros.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional
from dataclasses import dataclass, field
from enum import Enum

import pandas as pd
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class MarketDataType(Enum):
    """Tipos de datos de mercado soportados."""
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"
    CRYPTO = "crypto"
    INDEX = "index"
    BOND = "bond"


@dataclass
class MarketDataRecord:
    """Representa un registro de datos de mercado."""
    symbol: str
    timestamp: datetime
    data_type: MarketDataType
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    currency: str = "USD"
    exchange: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "data_type": self.data_type.value,
            "open": self.open_price,
            "high": self.high_price,
            "low": self.low_price,
            "close": self.close_price,
            "volume": self.volume,
            "currency": self.currency,
            "exchange": self.exchange,
            "metadata": self.metadata
        }


class MarketDataReader:
    """
    Clase principal para leer datos de mercado de múltiples fuentes.
    Soporta APIs de mercado, archivos históricos y streaming en tiempo real.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config.get("source_type", "api")
        self.source_credentials = config.get("credentials", {})
        self.batch_size = config.get("batch_size", 500)
        self.max_retries = config.get("max_retries", 3)
        self._s3_client = None
        self._api_session = None

    def _get_s3_client(self):
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self.source_credentials.get("aws_access_key"),
                aws_secret_access_key=self.source_credentials.get("aws_secret_key"),
                region_name=self.source_credentials.get("region", "us-east-1")
            )
        return self._s3_client

    def _retry_with_backoff(self, func, *args, **kwargs):
        import time
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                wait_time = 2 * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
        raise last_exception

    def read_from_api(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        data_type: MarketDataType = MarketDataType.STOCK
    ) -> Iterator[MarketDataRecord]:
        """
        Lee datos de mercado desde API financiera (Bloomberg, Reuters, Alpha Vantage, etc.)
        """
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        api_url = self.source_credentials.get("api_url")
        api_key = self.source_credentials.get("api_key")

        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        for symbol in symbols:
            params = {
                "symbol": symbol,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d"),
                "adjusted": "true",
                "outputsize": "full"
            }

            try:
                response = session.get(
                    f"{api_url}/time_series",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                for item in data.get("time_series", []):
                    yield self._parse_market_data(item, symbol, data_type)

            except requests.RequestException as e:
                logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
                continue

    def read_from_s3(
        self,
        bucket: str,
        prefix: str,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[MarketDataRecord]:
        """
        Lee datos de mercado desde S3 con partición por símbolo y fecha.
        """
        s3_client = self._get_s3_client()

        for symbol in symbols:
            date_format = "%Y-%m-%d"
            date_range = pd.date_range(start_date, end_date, freq='D')

            for date_obj in date_range:
                date_str = date_obj.strftime(date_format)
                object_key = f"{prefix}/symbol={symbol}/date={date_str}/market_data.parquet"

                try:
                    response = s3_client.get_object(Bucket=bucket, Key=object_key)
                    data = response['Body'].read()

                    df = pd.read_parquet(pd.io.common.BytesIO(data))

                    for _, row in df.iterrows():
                        yield self._row_to_market_record(row, symbol)

                except ClientError as e:
                    error_code = e.response.get('Error', {}).get('Code')
                    if error_code == 'NoSuchKey':
                        continue
                    logger.error(f"S3 error reading {object_key}: {str(e)}")
                    raise

    def read_historical_files(
        self,
        directory: str,
        symbols: Optional[List[str]] = None
    ) -> Iterator[MarketDataRecord]:
        """
        Lee archivos históricos locales o desde sistema de archivos mounting.
        """
        import os
        from pathlib import Path

        base_path = Path(directory)

        if not base_path.exists():
            logger.warning(f"Directory {directory} does not exist")
            return

        for file_path in base_path.rglob("*.parquet"):
            try:
                df = pd.read_parquet(file_path)

                for _, row in df.iterrows():
                    symbol = row.get('symbol', file_path.stem)
                    if symbols and symbol not in symbols:
                        continue
                    yield self._row_to_market_record(row, symbol)

            except Exception as e:
                logger.error(f"Error reading {file_path}: {str(e)}")
                continue

    def _parse_market_data(
        self,
        data: Dict[str, Any],
        symbol: str,
        data_type: MarketDataType
    ) -> MarketDataRecord:
        """Convierte respuesta de API a MarketDataRecord."""
        return MarketDataRecord(
            symbol=symbol,
            timestamp=datetime.fromisoformat(data["datetime"]),
            data_type=data_type,
            open_price=float(data["open"]),
            high_price=float(data["high"]),
            low_price=float(data["low"]),
            close_price=float(data["close"]),
            volume=float(data.get("volume", 0)),
            currency=data.get("currency", "USD"),
            exchange=data.get("exchange"),
            metadata=data.get("metadata", {})
        )

    def _row_to_market_record(self, row: pd.Series, symbol: str) -> MarketDataRecord:
        """Convierte fila de DataFrame a MarketDataRecord."""
        data_type_str = row.get('data_type', 'stock')
        try:
            data_type = MarketDataType(data_type_str)
        except ValueError:
            data_type = MarketDataType.STOCK

        return MarketDataRecord(
            symbol=symbol,
            timestamp=pd.to_datetime(row['timestamp']),
            data_type=data_type,
            open_price=float(row['open']),
            high_price=float(row['high']),
            low_price=float(row['low']),
            close_price=float(row['close']),
            volume=float(row.get('volume', 0)),
            currency=str(row.get('currency', 'USD')),
            exchange=str(row['exchange']) if pd.notna(row.get('exchange')) else None,
            metadata=dict(row['metadata']) if 'metadata' in row and pd.notna(row.get('metadata')) else {}
        )

    def read(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        data_type: MarketDataType = MarketDataType.STOCK
    ) -> Iterator[MarketDataRecord]:
        """
        Método principal que delega según la configuración de fuente.
        """
        logger.info(
            f"Reading market data for {symbols} from {start_date} to {end_date}"
        )

        if self.source_type == "api":
            yield from self.read_from_api(symbols, start_date, end_date, data_type)
        elif self.source_type == "s3":
            bucket = self.source_credentials.get("s3_bucket")
            prefix = self.source_credentials.get("s3_prefix", "market_data")
            yield from self.read_from_s3(bucket, prefix, symbols, start_date, end_date)
        elif self.source_type == "files":
            directory = self.source_credentials.get("data_directory")
            yield from self.read_historical_files(directory, symbols)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def read_as_dataframe(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        data_type: MarketDataType = MarketDataType.STOCK
    ) -> pd.DataFrame:
        """
        Retorna los datos como DataFrame de pandas.
        """
        records = list(self.read(symbols, start_date, end_date, data_type))
        if not records:
            return pd.DataFrame()

        data = [record.to_dict() for record in records]
        df = pd.DataFrame(data)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        logger.info(f"Loaded {len(df)} market data records")

        return df

    def close(self):
        """Cleanup de recursos."""
        logger.info("Market data reader closed")


def create_reader(config_path: str = "conf/dev_config.json") -> MarketDataReader:
    """Factory para crear reader desde archivo de configuración."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return MarketDataReader(config.get("market_data", {}))

// === ARCHIVO: src/extract/financial_news_reader.py ===
"""
Lector de noticias financieras para el pipeline de análisis financiero.
Se conecta a APIs de noticias (Bloomberg, Reuters, etc.) y extrae artículos relevantes.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional, Set
from dataclasses import dataclass, field
from urllib.parse import quote_plus

import pandas as pd
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class NewsArticle:
    """Representa un artículo de noticia financiera."""
    article_id: str
    headline: str
    summary: str
    content: str
    source: str
    url: str
    published_at: datetime
    authors: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None
    relevance_score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "article_id": self.article_id,
            "headline": self.headline,
            "summary": self.summary,
            "content": self.content,
            "source": self.source,
            "url": self.url,
            "published_at": self.published_at.isoformat(),
            "authors": self.authors,
            "tags": self.tags,
            "sentiment_score": self.sentiment_score,
            "relevance_score": self.relevance_score,
            "metadata": self.metadata
        }


class FinancialNewsReader:
    """
    Clase principal para leer noticias financieras de múltiples fuentes.
    Soporta APIs de noticias, RSS feeds y archivos procesados.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config.get("source_type", "api")
        self.source_credentials = config.get("credentials", {})
        self.batch_size = config.get("batch_size", 100)
        self.max_retries = config.get("max_retries", 3)
        self.keywords = config.get("keywords", [])
        self.categories = config.get("categories", [])
        self._s3_client = None
        self._api_session = None

    def _get_s3_client(self):
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self.source_credentials.get("aws_access_key"),
                aws_secret_access_key=self.source_credentials.get("aws_secret_key"),
                region_name=self.source_credentials.get("region", "us-east-1")
            )
        return self._s3_client

    def _retry_with_backoff(self, func, *args, **kwargs):
        import time
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                wait_time = 2 * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. "
                    f"Retrying in {wait_time}s..."
                )
                time.sleep(wait_time)
        raise last_exception

    def _build_query_params(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Construye parámetros de query para la API de noticias."""
        params = {
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "language": "en",
            "sortby": "publishedAt",
            "pageSize": self.batch_size
        }

        if self.keywords:
            params["q"] = " OR ".join(self.keywords)

        if self.categories:
            params["categories"] = ",".join(self.categories)

        return params

    def read_from_api(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Lee noticias desde API de noticias financieras (NewsAPI, Bloomberg, etc.)
        """
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        api_url = self.source_credentials.get("api_url")
        api_key = self.source_credentials.get("api_key")

        session = requests.Session()
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

        params = self._build_query_params(start_date, end_date)
        page = 1

        while True:
            params["page"] = page

            try:
                response = session.get(
                    f"{api_url}/articles",
                    headers=headers,
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                articles = data.get("articles", [])
                if not articles:
                    break

                for article_data in articles:
                    yield self._parse_article(article_data)

                if page >= data.get("totalPages", 1):
                    break

                page += 1

            except requests.RequestException as e:
                logger.error(f"News API request failed: {str(e)}")
                break

    def read_from_s3(
        self,
        bucket: str,
        prefix: str,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Lee noticias procesadas previamente desde S3.
        """
        s3_client = self._get_s3_client()

        date_format = "%Y-%m-%d"
        date_range = pd.date_range(start_date, end_date, freq='D')

        for date_obj in date_range:
            date_str = date_obj.strftime(date_format)
            object_key = f"{prefix}/date={date_str}/news.parquet"

            try:
                response = s3_client.get_object(Bucket=bucket, Key=object_key)
                data = response['Body'].read()

                df = pd.read_parquet(pd.io.common.BytesIO(data))

                for _, row in df.iterrows():
                    yield self._row_to_news_article(row)

            except ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code == 'NoSuchKey':
                    logger.info(f"No news file for date {date_str}")
                    continue
                logger.error(f"S3 error reading {object_key}: {str(e)}")
                raise

    def read_from_rss(
        self,
        feed_urls: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Lee noticias desde RSS feeds de fuentes financieras.
        """
        import feedparser

        for feed_url in feed_urls:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries:
                    published = self._parse_rss_date(entry.get("published", ""))

                    if published < start_date or published > end_date:
                        continue

                    yield NewsArticle(
                        article_id=entry.get("id", entry.link),
                        headline=entry.get("title", ""),
                        summary=entry.get("summary", ""),
                        content=entry.get("content", [{}])[0].get("value", ""),
                        source=feed.feed.get("title", "Unknown"),
                        url=entry.link,
                        published_at=published,
                        authors=[author.get("name", "") for author in entry.get("authors", [])],
                        tags=[tag.get("term", "") for tag in entry.get("tags", [])],
                        metadata={"feed": feed_url}
                    )

            except Exception as e:
                logger.error(f"Error parsing RSS feed {feed_url}: {str(e)}")
                continue

    def _parse_rss_date(self, date_str: str) -> datetime:
        """Parsea fecha de RSS feed."""
        from email.utils import parsedate_to_datetime
        try:
            return parsedate_to_datetime(date_str)
        except Exception:
            try:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except Exception:
                return datetime.now()

    def _parse_article(self, data: Dict[str, Any]) -> NewsArticle:
        """Convierte respuesta de API a NewsArticle."""
        published_str = data.get("publishedAt", data.get("published_at", ""))
        try:
            published_at = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        except Exception:
            published_at = datetime.now()

        return NewsArticle(
            article_id=data.get("url", data.get("id", "")),
            headline=data.get("title", ""),
            summary=data.get("description", data.get("summary", "")),
            content=data.get("content", data.get("body", "")),
            source=data.get("source", {}).get("name", "Unknown"),
            url=data.get("url", ""),
            published_at=published_at,
            authors=data.get("author", "").split(", ") if data.get("author") else [],
            tags=data.get("keywords", "").split(", ") if data.get("keywords") else [],
            sentiment_score=data.get("sentiment_score"),
            relevance_score=data.get("relevance_score"),
            metadata=data.get("metadata", {})
        )

    def _row_to_news_article(self, row: pd.Series) -> NewsArticle:
        """Convierte fila de DataFrame a NewsArticle."""
        return NewsArticle(
            article_id=str(row['article_id']),
            headline=str(row['headline']),
            summary=str(row['summary']),
            content=str(row['content']),
            source=str(row['source']),
            url=str(row['url']),
            published_at=pd.to_datetime(row['published_at']),
            authors=list(row['authors']) if 'authors' in row else [],
            tags=list(row['tags']) if 'tags' in row else [],
            sentiment_score=float(row['sentiment_score']) if pd.notna(row.get('sentiment_score')) else None,
            relevance_score=float(row['relevance_score']) if pd.notna(row.get('relevance_score')) else None,
            metadata=dict(row['metadata']) if 'metadata' in row and pd.notna(row.get('metadata')) else {}
        )

    def read(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Iterator[NewsArticle]:
        """
        Método principal que delega según la configuración de fuente.
        """
        logger.info(
            f"Reading financial news from {start_date} to {end_date}"
        )

        if self.source_type == "api":
            yield from self.read_from_api(start_date, end_date)
        elif self.source_type == "s3":
            bucket = self.source_credentials.get("s3_bucket")
            prefix = self.source_credentials.get("s3_prefix", "news")
            yield from self.read_from_s3(bucket, prefix, start_date, end_date)
        elif self.source_type == "rss":
            feed_urls = self.source_credentials.get("rss_feeds", [])
            yield from self.read_from_rss(feed_urls, start_date, end_date)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def read_as_dataframe(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        Retorna los datos como DataFrame de pandas.
        """
        records = list(self.read(start_date, end_date))
        if not records:
            return pd.DataFrame()

        data = [record.to_dict() for record in records]
        df = pd.DataFrame(data)

        df['published_at'] = pd.to_datetime(df['published_at'])
        logger.info(f"Loaded {len(df)} news articles")

        return df

    def filter_by_keywords(
        self,
        articles: Iterator[NewsArticle],
        keywords: List[str]
    ) -> Iterator[NewsArticle]:
        """
        Filtra artículos por palabras clave en headline o contenido.
        """
        keywords_lower = [k.lower() for k in keywords]

        for article in articles:
            text = f"{article.headline} {article.summary} {article.content}".lower()
            if any(kw in text for kw in keywords_lower):
                yield article

    def close(self):
        """Cleanup de recursos."""
        logger.info("Financial news reader closed")


def create_reader(config_path: str = "conf/dev_config.json") -> FinancialNewsReader:
    """Factory para crear reader desde archivo de configuración."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return FinancialNewsReader(config.get("financial_news", {}))

// === ARCHIVO: src/transform/data_quality_rules.py ===
"""Data quality rules and thresholds for financial data validation."""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class QualityThreshold:
    """Threshold configuration for a quality rule."""
    
    name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    null_percentage_allowed: float = 0.0
    unique_values_required: bool = False
    custom_validator: Optional[Callable[[Any], bool]] = None
    severity: str = "ERROR"  # ERROR, WARNING, INFO
    description: str = ""
    
    def validate(self, series: pd.Series) -> dict:
        """Validate a pandas Series against this threshold."""
        result = {
            "rule": self.name,
            "passed": True,
            "severity": self.severity,
            "details": {}
        }
        
        total_count = len(series)
        if total_count == 0:
            result["passed"] = False
            result["details"]["error"] = "Empty series"
            return result
        
        null_count = series.isnull().sum()
        null_percentage = (null_count / total_count) * 100
        
        if null_percentage > self.null_percentage_allowed:
            result["passed"] = False
            result["details"]["null_percentage"] = null_percentage
            result["details"]["null_threshold"] = self.null_percentage_allowed
        
        if self.min_value is not None:
            numeric_series = pd.to_numeric(series, errors='coerce')
            below_min = (numeric_series < self.min_value).sum()
            if below_min > 0:
                result["passed"] = False
                result["details"]["below_min_count"] = int(below_min)
                result["details"]["min_value"] = self.min_value
        
        if self.max_value is not None:
            numeric_series = pd.to_numeric(series, errors='coerce')
            above_max = (numeric_series > self.max_value).sum()
            if above_max > 0:
                result["passed"] = False
                result["details"]["above_max_count"] = int(above_max)
                result["details"]["max_value"] = self.max_value
        
        if self.unique_values_required:
            unique_count = series.nunique()
            if unique_count < total_count:
                result["passed"] = False
                result["details"]["unique_violations"] = int(total_count - unique_count)
        
        if self.custom_validator is not None:
            try:
                invalid_count = series.apply(lambda x: not self.custom_validator(x) if pd.notna(x) else False).sum()
                if invalid_count > 0:
                    result["passed"] = False
                    result["details"]["custom_validation_failures"] = int(invalid_count)
            except Exception as e:
                result["passed"] = False
                result["details"]["custom_validation_error"] = str(e)
        
        return result


@dataclass
class DataQualityRuleSet:
    """Collection of quality rules for a data source."""
    
    source_name: str
    rules: list[QualityThreshold] = field(default_factory=list)
    quarantine_threshold: float = 0.05  # 5% failure rate triggers quarantine
    
    def add_rule(self, rule: QualityThreshold) -> None:
        """Add a quality rule to the set."""
        self.rules.append(rule)
        logger.debug(f"Added rule '{rule.name}' to {self.source_name}")
    
    def validate_dataframe(self, df: pd.DataFrame) -> dict:
        """Validate a DataFrame against all rules in the set."""
        validation_results = {
            "source": self.source_name,
            "timestamp": datetime.utcnow().isoformat(),
            "total_rows": len(df),
            "rules_checked": len(self.rules),
            "passed": True,
            "results": [],
            "quarantine_required": False
        }
        
        failed_rules = 0
        
        for rule in self.rules:
            if rule.name not in df.columns:
                logger.warning(f"Column '{rule.name}' not found in DataFrame for source '{self.source_name}'")
                validation_results["results"].append({
                    "rule": rule.name,
                    "passed": False,
                    "severity": "ERROR",
                    "details": {"error": "Column not found"}
                })
                failed_rules += 1
                continue
            
            result = rule.validate(df[rule.name])
            validation_results["results"].append(result)
            
            if not result["passed"]:
                failed_rules += 1
                logger.warning(f"Quality rule '{rule.name}' failed for {self.source_name}: {result['details']}")
        
        failure_rate = failed_rules / len(self.rules) if self.rules else 0
        validation_results["failure_rate"] = failure_rate
        validation_results["failed_rules"] = failed_rules
        
        if failure_rate >= self.quarantine_threshold:
            validation_results["quarantine_required"] = True
            validation_results["passed"] = False
            logger.error(f"Quarantine required for {self.source_name}: {failure_rate*100:.2f}% failure rate")
        
        return validation_results


class FinancialDataQualityRules:
    """Predefined quality rules for financial data sources."""
    
    @staticmethod
    def get_transaction_rules() -> DataQualityRuleSet:
        """Get quality rules for bank transaction data."""
        rules = DataQualityRuleSet(source_name="bank_transactions")
        
        rules.add_rule(QualityThreshold(
            name="transaction_id",
            unique_values_required=True,
            severity="ERROR",
            description="Transaction ID must be unique"
        ))
        
        rules.add_rule(QualityThreshold(
            name="amount",
            min_value=-1000000,
            max_value=1000000,
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Transaction amount must be within reasonable bounds"
        ))
        
        rules.add_rule(QualityThreshold(
            name="timestamp",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Timestamp cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="currency",
            null_percentage_allowed=0.0,
            custom_validator=lambda x: x in ["USD", "EUR", "GBP", "JPY", "CHF"],
            severity="WARNING",
            description="Currency must be a supported code"
        ))
        
        rules.add_rule(QualityThreshold(
            name="account_id",
            null_percentage_allowed=0.0,
            unique_values_required=False,
            severity="ERROR",
            description="Account ID cannot be null"
        ))
        
        return rules
    
    @staticmethod
    def get_market_data_rules() -> DataQualityRuleSet:
        """Get quality rules for market data."""
        rules = DataQualityRuleSet(source_name="market_data")
        
        rules.add_rule(QualityThreshold(
            name="symbol",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Market symbol cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="price",
            min_value=0.01,
            max_value=1000000,
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Price must be positive and within bounds"
        ))
        
        rules.add_rule(QualityThreshold(
            name="volume",
            min_value=0,
            null_percentage_allowed=0.0,
            severity="WARNING",
            description="Volume cannot be negative"
        ))
        
        rules.add_rule(QualityThreshold(
            name="timestamp",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Timestamp cannot be null"
        ))
        
        return rules
    
    @staticmethod
    def get_news_rules() -> DataQualityRuleSet:
        """Get quality rules for financial news data."""
        rules = DataQualityRuleSet(source_name="financial_news")
        
        rules.add_rule(QualityThreshold(
            name="headline",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Headline cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="published_at",
            null_percentage_allowed=0.0,
            severity="ERROR",
            description="Publication date cannot be null"
        ))
        
        rules.add_rule(QualityThreshold(
            name="source",
            null_percentage_allowed=5.0,
            severity="WARNING",
            description="Source is optional but recommended"
        ))
        
        rules.add_rule(QualityThreshold(
            name="sentiment_score",
            min_value=-1.0,
            max_value=1.0,
            null_percentage_allowed=10.0,
            severity="WARNING",
            description="Sentiment score must be between -1 and 1"
        ))
        
        return rules


class QualityRuleEngine:
    """Engine to execute quality rules and manage quarantine logic."""
    
    def __init__(self):
        self.rule_sets: dict[str, DataQualityRuleSet] = {}
        self.quarantine_path = "s3://data-lake/quarantine/"
    
    def register_rule_set(self, rule_set: DataQualityRuleSet) -> None:
        """Register a rule set for a data source."""
        self.rule_sets[rule_set.source_name] = rule_set
        logger.info(f"Registered quality rules for source: {rule_set.source_name}")
    
    def validate(self, source_name: str, df: pd.DataFrame) -> dict:
        """Validate data against registered rules."""
        if source_name not in self.rule_sets:
            logger.warning(f"No rules registered for source: {source_name}")
            return {
                "source": source_name,
                "passed": True,
                "warning": "No validation rules applied"
            }
        
        rule_set = self.rule_sets[source_name]
        return rule_set.validate_dataframe(df)
    
    def get_quarantine_path(self, source_name: str, execution_date: datetime) -> str:
        """Generate quarantine path for failed records."""
        date_str = execution_date.strftime("%Y%m%d")
        return f"{self.quarantine_path}{source_name}/{date_str}/"

// === ARCHIVO: src/transform/financial_data_transformer.py ===
"""Financial data transformation module for normalizing and enriching data."""

import logging
from typing import Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path

from src.transform.data_quality_rules import (
    FinancialDataQualityRules,
    QualityRuleEngine,
    DataQualityRuleSet
)

logger = logging.getLogger(__name__)


class SchemaNormalizer:
    """Normalizes data schemas across different financial data sources."""
    
    def __init__(self, schema_path: str = "src/schemas"):
        self.schema_path = Path(schema_path)
        self.schemas: dict[str, dict] = {}
        self._load_schemas()
    
    def _load_schemas(self) -> None:
        """Load JSON schemas from the schema directory."""
        schema_files = ["transaction_schema.json", "market_data_schema.json", "news_schema.json"]
        
        for schema_file in schema_files:
            schema_file_path = self.schema_path / schema_file
            if schema_file_path.exists():
                with open(schema_file_path, 'r') as f:
                    schema_name = schema_file.replace("_schema.json", "")
                    self.schemas[schema_name] = json.load(f)
                    logger.info(f"Loaded schema: {schema_name}")
    
    def normalize_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize transaction data to standard schema."""
        normalized = df.copy()
        
        if "transaction_id" in normalized.columns and "id" in normalized.columns:
            normalized = normalized.drop(columns=["id"])
        
        if "txn_amount" in normalized.columns and "amount" not in normalized.columns:
            normalized.rename(columns={"txn_amount": "amount"}, inplace=True)
        
        if "txn_date" in normalized.columns and "timestamp" not in normalized.columns:
            normalized.rename(columns={"txn_date": "timestamp"}, inplace=True)
        
        if "txn_type" in normalized.columns and "transaction_type" not in normalized.columns:
            normalized.rename(columns={"txn_type": "transaction_type"}, inplace=True)
        
        required_columns = ["transaction_id", "amount", "timestamp", "currency", "account_id"]
        for col in required_columns:
            if col not in normalized.columns:
                normalized[col] = None
        
        normalized["ingestion_timestamp"] = datetime.utcnow()
        normalized["data_source"] = "bank_transactions"
        
        return normalized[required_columns + ["transaction_type", "ingestion_timestamp", "data_source"]]
    
    def normalize_market_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize market data to standard schema."""
        normalized = df.copy()
        
        if "ticker" in normalized.columns and "symbol" not in normalized.columns:
            normalized.rename(columns={"ticker": "symbol"}, inplace=True)
        
        if "close_price" in normalized.columns and "price" not in normalized.columns:
            normalized.rename(columns={"close_price": "price"}, inplace=True)
        
        if "trade_date" in normalized.columns and "timestamp" not in normalized.columns:
            normalized.rename(columns={"trade_date": "timestamp"}, inplace=True)
        
        required_columns = ["symbol", "price", "timestamp"]
        for col in required_columns:
            if col not in normalized.columns:
                normalized[col] = None
        
        if "volume" not in normalized.columns:
            normalized["volume"] = 0
        
        normalized["ingestion_timestamp"] = datetime.utcnow()
        normalized["data_source"] = "market_data"
        
        return normalized[required_columns + ["volume", "ingestion_timestamp", "data_source"]]
    
    def normalize_news(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize financial news to standard schema."""
        normalized = df.copy()
        
        if "title" in normalized.columns and "headline" not in normalized.columns:
            normalized.rename(columns={"title": "headline"}, inplace=True)
        
        if "pub_date" in normalized.columns and "published_at" not in normalized.columns:
            normalized.rename(columns={"pub_date": "published_at"}, inplace=True)
        
        if "news_source" in normalized.columns and "source" not in normalized.columns:
            normalized.rename(columns={"news_source": "source"}, inplace=True)
        
        required_columns = ["headline", "published_at"]
        for col in required_columns:
            if col not in normalized.columns:
                normalized[col] = None
        
        if "source" not in normalized.columns:
            normalized["source"] = "unknown"
        
        if "sentiment_score" not in normalized.columns:
            normalized["sentiment_score"] = None
        
        normalized["ingestion_timestamp"] = datetime.utcnow()
        normalized["data_source"] = "financial_news"
        
        return normalized[required_columns + ["source", "sentiment_score", "ingestion_timestamp", "data_source"]]


class FinancialMetricsCalculator:
    """Calculate derived financial metrics from normalized data."""
    
    @staticmethod
    def calculate_transaction_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for transaction data."""
        result = df.copy()
        
        result["abs_amount"] = result["amount"].abs()
        
        result["is_credit"] = result["amount"] > 0
        result["is_debit"] = result["amount"] < 0
        
        result["day_of_week"] = pd.to_datetime(result["timestamp"]).dt.dayofweek
        result["month"] = pd.to_datetime(result["timestamp"]).dt.month
        result["year"] = pd.to_datetime(result["timestamp"]).dt.year
        
        result["amount_bucket"] = pd.cut(
            result["abs_amount"],
            bins=[0, 100, 1000, 10000, 100000, float('inf')],
            labels=["micro", "small", "medium", "large", "xlarge"]
        )
        
        return result
    
    @staticmethod
    def calculate_market_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for market data."""
        result = df.copy()
        
        result = result.sort_values(["symbol", "timestamp"])
        
        result["price_change"] = result.groupby("symbol")["price"].diff()
        result["price_change_pct"] = result.groupby("symbol")["price"].pct_change() * 100
        
        result["moving_avg_5d"] = result.groupby("symbol")["price"].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
        
        result["volatility_5d"] = result.groupby("symbol")["price"].transform(
            lambda x: x.rolling(window=5, min_periods=1).std()
        )
        
        result["volume_ma_5d"] = result.groupby("symbol")["volume"].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
        
        return result
    
    @staticmethod
    def calculate_news_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for news data."""
        result = df.copy()
        
        result["headline_length"] = result["headline"].str.len()
        
        result["published_hour"] = pd.to_datetime(result["published_at"]).dt.hour
        result["published_day_of_week"] = pd.to_datetime(result["published_at"]).dt.dayofweek
        
        result["sentiment_category"] = pd.cut(
            result["sentiment_score"],
            bins=[-1.0, -0.3, 0.3, 1.0],
            labels=["negative", "neutral", "positive"]
        )
        
        return result


class DataTransformer:
    """Main transformer orchestrating normalization and metric calculation."""
    
    def __init__(self, schema_path: str = "src/schemas"):
        self.normalizer = SchemaNormalizer(schema_path)
        self.metrics_calculator = FinancialMetricsCalculator()
        self.quality_engine = QualityRuleEngine()
        
        self.quality_engine.register_rule_set(FinancialDataQualityRules.get_transaction_rules())
        self.quality_engine.register_rule_set(FinancialDataQualityRules.get_market_data_rules())
        self.quality_engine.register_rule_set(FinancialDataQualityRules.get_news_rules())
    
    def transform_transactions(self, df: pd.DataFrame, execution_date: datetime) -> dict:
        """Transform transaction data through the full pipeline."""
        logger.info(f"Transforming {len(df)} transactions")
        
        normalized = self.normalizer.normalize_transactions(df)
        logger.info(f"Normalized transactions schema: {list(normalized.columns)}")
        
        enriched = self.metrics_calculator.calculate_transaction_metrics(normalized)
        logger.info(f"Enriched with {len(enriched.columns) - len(normalized.columns)} derived metrics")
        
        quality_result = self.quality_engine.validate("bank_transactions", enriched)
        
        validated = enriched[quality_result["passed"]] if quality_result["passed"] else enriched.head(0)
        quarantined = enriched[~quality_result["passed"]] if not quality_result["passed"] else pd.DataFrame()
        
        return {
            "validated_data": validated,
            "quarantined_data": quarantined,
            "quality_report": quality_result,
            "record_count": len(df),
            "execution_date": execution_date.isoformat()
        }
    
    def transform_market_data(self, df: pd.DataFrame, execution_date: datetime) -> dict:
        """Transform market data through the full pipeline."""
        logger.info(f"Transforming {len(df)} market data records")
        
        normalized = self.normalizer.normalize_market_data(df)
        logger.info(f"Normalized market data schema: {list(normalized.columns)}")
        
        enriched = self.metrics_calculator.calculate_market_metrics(normalized)
        logger.info(f"Enriched with {len(enriched.columns) - len(normalized.columns)} derived metrics")
        
        quality_result = self.quality_engine.validate("market_data", enriched)
        
        validated = enriched[quality_result["passed"]] if quality_result["passed"] else enriched.head(0)
        quarantined = enriched[~quality_result["passed"]] if not quality_result["passed"] else pd.DataFrame()
        
        return {
            "validated_data": validated,
            "quarantined_data": quarantined,
            "quality_report": quality_result,
            "record_count": len(df),
            "execution_date": execution_date.isoformat()
        }
    
    def transform_news(self, df: pd.DataFrame, execution_date: datetime) -> dict:
        """Transform financial news through the full pipeline."""
        logger.info(f"Transforming {len(df)} news articles")
        
        normalized = self.normalizer.normalize_news(df)
        logger.info(f"Normalized news schema: {list(normalized.columns)}")
        
        enriched = self.metrics_calculator.calculate_news_metrics(normalized)
        logger.info(f"Enriched with {len(enriched.columns) - len(normalized.columns)} derived metrics")
        
        quality_result = self.quality_engine.validate("financial_news", enriched)
        
        validated = enriched[quality_result["passed"]] if quality_result["passed"] else enriched.head(0)
        quarantined = enriched[~quality_result["passed"]] if not quality_result["passed"] else pd.DataFrame()
        
        return {
            "validated_data": validated,
            "quarantined_data": quarantined,
            "quality_report": quality_result,
            "record_count": len(df),
            "execution_date": execution_date.isoformat()
        }

// === ARCHIVO: src/load/data_writer.py ===
"""Data writer module for loading transformed data to destinations."""

import logging
from typing import Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
import hashlib
import time

import boto3
from botocore.exceptions import ClientError, BotoCoreError
import pyarrow as pa
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)


class S3Writer:
    """Writer for storing data in Amazon S3 with columnar format support."""
    
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.partition_keys = ["year", "month", "day", "data_source"]
    
    def _generate_partition_path(self, execution_date: datetime, data_source: str) -> str:
        """Generate partition path based on execution date and data source."""
        year = execution_date.strftime("%Y")
        month = execution_date.strftime("%m")
        day = execution_date.strftime("%d")
        
        return f"data/{data_source}/year={year}/month={month}/day={day}"
    
    def _generate_file_name(self, data_source: str, execution_date: datetime, file_format: str = "parquet") -> str:
        """Generate unique filename based on execution context."""
        timestamp = execution_date.strftime("%Y%m%d_%H%M%S")
        hash_suffix = hashlib.md5(f"{data_source}_{timestamp}".encode()).hexdigest()[:8]
        return f"{data_source}_{timestamp}_{hash_suffix}.{file_format}"
    
    def write_parquet(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        data_source: str,
        enable_partitioning: bool = True
    ) -> dict:
        """Write DataFrame to S3 in Parquet format with optional partitioning."""
        if df.empty:
            logger.warning(f"Empty DataFrame for {data_source}, skipping write")
            return {"status": "skipped", "reason": "empty_dataframe"}
        
        try:
            if enable_partitioning:
                if "year" not in df.columns:
                    df["year"] = execution_date.year
                if "month" not in df.columns:
                    df["month"] = execution_date.month
                if "day" not in df.columns:
                    df["day"] = execution_date.day
                if "data_source" not in df.columns:
                    df["data_source"] = data_source
            
            table = pa.Table.from_pandas(df)
            
            buffer = pa.BufferOutputStream()
            pq.write_table(table, buffer)
            buffer_data = buffer.getvalue()
            
            partition_path = self._generate_partition_path(execution_date, data_source)
            file_name = self._generate_file_name(data_source, execution_date)
            s3_key = f"{partition_path}/{file_name}"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=buffer_data.to_pybytes(),
                ContentType='application/parquet',
                Metadata={
                    "data_source": data_source,
                    "record_count": str(len(df)),
                    "execution_date": execution_date.isoformat()
                }
            )
            
            logger.info(f"Successfully wrote {len(df)} records to s3://{self.bucket_name}/{s3_key}")
            
            return {
                "status": "success",
                "s3_path": f"s3://{self.bucket_name}/{s3_key}",
                "record_count": len(df),
                "partition_path": partition_path
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"S3 write failed for {data_source}: {str(e)}")
            raise
    
    def write_json(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        data_source: str
    ) -> dict:
        """Write DataFrame to S3 in JSON format."""
        if df.empty:
            logger.warning(f"Empty DataFrame for {data_source}, skipping write")
            return {"status": "skipped", "reason": "empty_dataframe"}
        
        try:
            partition_path = self._generate_partition_path(execution_date, data_source)
            file_name = self._generate_file_name(data_source, execution_date, "json")
            s3_key = f"{partition_path}/{file_name}"
            
            json_data = df.to_json(orient='records', lines=True)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json',
                Metadata={
                    "data_source": data_source,
                    "record_count": str(len(df))
                }
            )
            
            logger.info(f"Successfully wrote {len(df)} records to s3://{self.bucket_name}/{s3_key}")
            
            return {
                "status": "success",
                "s3_path": f"s3://{self.bucket_name}/{s3_key}",
                "record_count": len(df)
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"S3 JSON write failed: {str(e)}")
            raise


class RedshiftWriter:
    """Writer for loading data into Amazon Redshift."""
    
    def __init__(self, cluster_identifier: str, database: str, table_name: str):
        self.cluster_identifier = cluster_identifier
        self.database = database
        self.table_name = table_name
        self.redshift_client = boto3.client('redshift-data')
    
    def write(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        mode: str = "append"  # append, upsert
    ) -> dict:
        """Write DataFrame to Redshift using COPY command."""
        if df.empty:
            logger.warning(f"Empty DataFrame, skipping Redshift write")
            return {"status": "skipped", "reason": "empty_dataframe"}
        
        try:
            s3_writer = S3Writer(bucket_name="staging-bucket-temp")
            staging_result = s3_writer.write_parquet(
                df,
                execution_date,
                f"staging_{self.table_name}",
                enable_partitioning=False
            )
            
            if staging_result["status"] != "success":
                raise RuntimeError(f"Staging write failed: {staging_result}")
            
            s3_path = staging_result["s3_path"]
            
            copy_sql = f"""
            COPY {self.table_name}
            FROM '{s3_path}'
            IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftCopyRole'
            FORMAT AS PARQUET
            """
            
            if mode == "upsert":
                logger.info("Upsert mode requires primary key handling - using staging table approach")
            
            logger.info(f"Executing COPY to {self.table_name} from {s3_path}")
            
            return {
                "status": "success",
                "records_loaded": len(df),
                "staging_s3_path": s3_path
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Redshift write failed: {str(e)}")
            raise


class IdempotentWriter:
    """Writer with idempotency guarantees for pipeline reprocessing."""
    
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.s3_writer = S3Writer(bucket_name, region_name)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)
        self.idempotency_table = "pipeline_idempotency"
    
    def _check_idempotency(self, execution_id: str) -> bool:
        """Check if this execution has already been processed."""
        try:
            response = self.dynamodb_client.get_item(
                TableName=self.idempotency_table,
                Key={'execution_id': {'S': execution_id}}
            )
            return 'Item' in response
        except ClientError:
            return False
    
    def _record_execution(self, execution_id: str, record_count: int, s3_path: str) -> None:
        """Record successful execution for idempotency tracking."""
        try:
            self.dynamodb_client.put_item(
                TableName=self.idempotency_table,
                Item={
                    'execution_id': {'S': execution_id},
                    'record_count': {'N': str(record_count)},
                    's3_path': {'S': s3_path},
                    'timestamp': {'S': datetime.utcnow().isoformat()},
                    'status': {'S': 'COMPLETED'}
                }
            )
        except ClientError as e:
            logger.warning(f"Failed to record idempotency: {e}")
    
    def write_with_idempotency(
        self,
        df: pd.DataFrame,
        execution_date: datetime,
        data_source: str,
        execution_id: str
    ) -> dict:
        """Write data with idempotency guarantee."""
        if self._check_idempotency(execution_id):
            logger.info(f"Execution {execution_id} already processed, skipping")
            return {
                "status": "skipped",
                "reason": "already_processed",
                "execution_id": execution_id
            }
        
        result = self.s3_writer.write_parquet(df, execution_date, data_source)
        
        if result["status"] == "success":
            self._record_execution(execution_id, len(df), result["s3_path"])
        
        result["execution_id"] = execution_id
        return result


class DataWriter:
    """Main writer orchestrating data loading to multiple destinations."""
    
    def __init__(self, config: dict):
        self.config = config
        
        self.s3_bucket = config.get("s3_bucket", "data-lake-bucket")
        self.region = config.get("region", "us-east-1")
        
        self.s3_writer = S3Writer(self.s3_bucket, self.region)
        self.idempotent_writer = IdempotentWriter(self.s3_bucket, self.region)
        
        self.redshift_config = config.get("redshift")
        if self.redshift_config:
            self.redshift_writer = RedshiftWriter(
                cluster_identifier=self.redshift_config.get("cluster_identifier"),
                database=self.redshift_config.get("database"),
                table_name=self.redshift_config.get("table_name")
            )
    
    def write_validated_data(
        self,
        validated_df: pd.DataFrame,
        quarantined_df: pd.DataFrame,
        execution_date: datetime,
        data_source: str,
        enable_idempotency: bool = True
    ) -> dict:
        """Write validated and quarantined data to appropriate destinations."""
        results = {
            "validated": None,
            "quarantined": None,
            "execution_date": execution_date.isoformat(),
            "data_source": data_source
        }
        
        execution_id = f"{data_source}_{execution_date.strftime('%Y%m%d_%H%M%S')}"
        
        if not validated_df.empty:
            if enable_idempotency:
                validated_result = self.idempotent_writer.write_with_idempotency(
                    validated_df,
                    execution_date,
                    data_source,
                    execution_id
                )
            else:
                validated_result = self.s3_writer.write_parquet(
                    validated_df,
                    execution_date,
                    data_source
                )
            results["validated"] = validated_result
            
            if self.redshift_config and validated_result.get("status") == "success":
                try:
                    redshift_result = self.redshift_writer.write(
                        validated_df,
                        execution_date,
                        mode="append"
                    )
                    results["validated"]["redshift_loaded"] = True
                except Exception as e:
                    logger.error(f"Redshift load failed: {e}")
                    results["validated"]["redshift_loaded"] = False
                    results["validated"]["redshift_error"] = str(e)
        
        if not quarantined_df.empty:
            quarantine_result = self.s3_writer.write_parquet(
                quarantined_df,
                execution_date,
                f"quarantine_{data_source}"
            )
            results["quarantined"] = quarantine_result
            logger.warning(f"Quarantined {len(quarantined_df)} records for {data_source}")
        
        logger.info(f"Data write completed for {data_source}: validated={len(validated_df)}, quarantined={len(quarantined_df)}")
        
        return results

// === ARCHIVO: src/utils/idempotency_utils.py ===
"""Utilidades para garantizar idempotencia en operaciones de carga de datos.

Este módulo proporciona mecanismos para evitar duplicados y asegurar que las operaciones
de escritura sean idempotentes mediante estrategias de reintento y claves únicas.
"""

import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar
from dataclasses import dataclass, field
import pandas as pd

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class IdempotencyRecord:
    """Registro de una operación idempotente en el sistema."""
    key: str
    status: str  # 'pending', 'completed', 'failed'
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    retry_count: int = 0

    def mark_completed(self, result: Dict[str, Any]) -> None:
        """Marca el registro como completado exitosamente."""
        self.status = 'completed'
        self.result = result
        self.completed_at = datetime.now(timezone.utc)

    def mark_failed(self, error: str) -> None:
        """Marca el registro como fallido."""
        self.status = 'failed'
        self.error = error
        self.completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el registro a diccionario para serialización."""
        return {
            'key': self.key,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'retry_count': self.retry_count
        }


class IdempotencyStore:
    """Almacén de registros de idempotencia con soporte para múltiples backends."""

    def __init__(self, backend: str = 'memory', **kwargs):
        """Inicializa el almacén de idempotencia.

        Args:
            backend: Tipo de backend ('memory', 's3', 'dynamodb')
            **kwargs: Configuración específica del backend
        """
        self.backend = backend
        self._store: Dict[str, IdempotencyRecord] = {}
        self._s3_bucket = kwargs.get('s3_bucket')
        self._dynamodb_table = kwargs.get('dynamodb_table')

        if backend == 's3' and not self._s3_bucket:
            raise ValueError("S3 bucket requerido para backend 's3'")
        if backend == 'dynamodb' and not self._dynamodb_table:
            raise ValueError("DynamoDB table requerido para backend 'dynamodb'")

        logger.info(f"IdempotencyStore inicializado con backend: {backend}")

    def get(self, key: str) -> Optional[IdempotencyRecord]:
        """Recupera un registro de idempotencia por su clave."""
        if self.backend == 'memory':
            return self._store.get(key)
        elif self.backend == 's3':
            return self._get_from_s3(key)
        elif self.backend == 'dynamodb':
            return self._get_from_dynamodb(key)
        return None

    def save(self, record: IdempotencyRecord) -> None:
        """Guarda un registro de idempotencia."""
        if self.backend == 'memory':
            self._store[record.key] = record
        elif self.backend == 's3':
            self._save_to_s3(record)
        elif self.backend == 'dynamodb':
            self._save_to_dynamodb(record)

    def _get_from_s3(self, key: str) -> Optional[IdempotencyRecord]:
        """Recupera registro desde S3."""
        try:
            import boto3
            s3_client = boto3.client('s3')
            response = s3_client.get_object(Bucket=self._s3_bucket, Key=f"idempotency/{key}.json")
            data = json.loads(response['Body'].read().decode('utf-8'))
            return self._dict_to_record(data)
        except Exception as e:
            logger.debug(f"No se encontró registro en S3: {key} - {e}")
            return None

    def _save_to_s3(self, record: IdempotencyRecord) -> None:
        """Guarda registro en S3."""
        import boto3
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=self._s3_bucket,
            Key=f"idempotency/{record.key}.json",
            Body=json.dumps(record.to_dict()).encode('utf-8')
        )

    def _get_from_dynamodb(self, key: str) -> Optional[IdempotencyRecord]:
        """Recupera registro desde DynamoDB."""
        try:
            import boto3
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(self._dynamodb_table)
            response = table.get_item(Key={'idempotency_key': key})
            if 'Item' in response:
                return self._dict_to_record(response['Item'])
            return None
        except Exception as e:
            logger.debug(f"No se encontró registro en DynamoDB: {key} - {e}")
            return None

    def _save_to_dynamodb(self, record: IdempotencyRecord) -> None:
        """Guarda registro en DynamoDB."""
        import boto3
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self._dynamodb_table)
        table.put_item(Item=record.to_dict())

    @staticmethod
    def _dict_to_record(data: Dict[str, Any]) -> IdempotencyRecord:
        """Convierte diccionario a IdempotencyRecord."""
        record = IdempotencyRecord(
            key=data['key'],
            status=data['status'],
            result=data.get('result'),
            error=data.get('error'),
            retry_count=data.get('retry_count', 0)
        )
        if 'created_at' in data:
            record.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('completed_at'):
            record.completed_at = datetime.fromisoformat(data['completed_at'])
        return record


def generate_idempotency_key(*args, **kwargs) -> str:
    """Genera una clave de idempotencia única basada en los argumentos.

    Args:
        *args: Argumentos posicionales de la operación
        **kwargs: Argumentos nominales de la operación

    Returns:
        Clave de idempotencia única como string hexadecimal
    """
    canonical_repr = json.dumps(
        {'args': args, 'kwargs': kwargs},
        sort_keys=True,
        default=str
    )
    return hashlib.sha256(canonical_repr.encode('utf-8')).hexdigest()


def generate_batch_idempotency_key(
    source: str,
    batch_date: datetime,
    batch_sequence: int,
    content_hash: str
) -> str:
    """Genera clave de idempotencia para operaciones de carga por lotes.

    Args:
        source: Identificador de la fuente de datos
        batch_date: Fecha del lote
        batch_sequence: Número de secuencia del lote
        content_hash: Hash del contenido del lote

    Returns:
        Clave de idempotencia formateada
    """
    key_data = f"{source}:{batch_date.isoformat()}:{batch_sequence}:{content_hash}"
    return f"batch_{hashlib.sha256(key_data.encode('utf-8')).hexdigest()[:32]}"


class RetryStrategy:
    """Estrategia de reintento con backoff exponencial."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        """Configura la estrategia de reintento.

        Args:
            max_retries: Número máximo de reintentos
            base_delay: Delay base en segundos
            max_delay: Delay máximo en segundos
            exponential_base: Base del exponente para backoff
            jitter: Añadir aleatoriedad al delay
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """Calcula el delay para un intento específico."""
        import random
        delay = min(self.base_delay * (self.exponential_base ** attempt), self.max_delay)
        if self.jitter:
            delay *= (0.5 + random.random())
        return delay


def idempotent_operation(
    store: IdempotencyStore,
    retry_strategy: Optional[RetryStrategy] = None,
    operation_name: str = "operation"
):
    """Decorador para hacer una función idempotente.

    Args:
        store: Almacén de idempotencia
        retry_strategy: Estrategia de reintento
        operation_name: Nombre de la operación para logs
    """
    if retry_strategy is None:
        retry_strategy = RetryStrategy()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            idempotency_key = generate_idempotency_key(operation_name, *args, **kwargs)

            existing = store.get(idempotency_key)
            if existing and existing.status == 'completed':
                logger.info(f"Operación idempotente completada previamente: {idempotency_key}")
                return existing.result

            if existing and existing.status == 'pending':
                logger.warning(f"Operación ya en progreso: {idempotency_key}")
                raise IdempotencyConflictError(
                    f"Operación {idempotency_key} ya está en progreso"
                )

            record = IdempotencyRecord(key=idempotency_key, status='pending')
            store.save(record)

            last_error = None
            for attempt in range(retry_strategy.max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    record.mark_completed(result if isinstance(result, dict) else {'result': result})
                    store.save(record)
                    logger.info(f"Operación idempotente completada: {idempotency_key}")
                    return result
                except Exception as e:
                    last_error = e
                    record.retry_count = attempt + 1

                    if attempt < retry_strategy.max_retries:
                        delay = retry_strategy.get_delay(attempt)
                        logger.warning(
                            f"Reintento {attempt + 1}/{retry_strategy.max_retries} "
                            f"para {idempotency_key} tras {delay:.2f}s: {str(e)}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"Operación idempotente fallida después de {attempt + 1} intentos: {idempotency_key}")

            record.mark_failed(str(last_error))
            store.save(record)
            raise last_error

        return wrapper
    return decorator


class IdempotencyConflictError(Exception):
    """Excepción lanzada cuando se detecta un conflicto de idempotencia."""
    pass


def check_duplicate_records(
    df: pd.DataFrame,
    unique_columns: list,
    source_identifier: str
) -> pd.DataFrame:
    """Identifica registros duplicados en un DataFrame.

    Args:
        df: DataFrame con los datos a verificar
        unique_columns: Columnas que definen unicidad
        source_identifier: Identificador de la fuente para logging

    Returns:
        DataFrame con los registros duplicados
    """
    if df.empty:
        return df

    duplicates = df[df.duplicated(subset=unique_columns, keep=False)]

    if not duplicates.empty:
        logger.warning(
            f"Se detectaron {len(duplicates)} registros duplicados "
            f"en fuente {source_identifier} por columnas: {unique_columns}"
        )

    return duplicates


def merge_idempotent(
    existing_df: pd.DataFrame,
    new_df: pd.DataFrame,
    key_columns: list,
    conflict_resolution: str = 'prefer_new'
) -> pd.DataFrame:
    """Fusiona dos DataFrames de manera idempotente.

    Args:
        existing_df: DataFrame con datos existentes
        new_df: DataFrame con nuevos datos
        key_columns: Columnas que definen la clave de fusión
        conflict_resolution: Estrategia de resolución de conflictos
                           ('prefer_new', 'prefer_old', 'max_timestamp')

    Returns:
        DataFrame fusionado de manera idempotente
    """
    if existing_df.empty:
        return new_df.copy()

    if new_df.empty:
        return existing_df.copy()

    combined = pd.concat([existing_df, new_df], ignore_index=True)
    merged = combined.drop_duplicates(subset=key_columns, keep='last')

    logger.info(
        f"Fusión idempotente: {len(existing_df)} existentes + {len(new_df)} nuevos "
        f"= {len(merged)} únicos"
    )

    return merged


class BatchIdempotencyManager:
    """Gestor de idempotencia especializado para cargas por lotes."""

    def __init__(self, store: IdempotencyStore):
        self.store = store

    def register_batch(
        self,
        source: str,
        batch_date: datetime,
        batch_sequence: int,
        record_count: int,
        content_hash: str
    ) -> str:
        """Registra un nuevo lote para procesamiento idempotente."""
        idempotency_key = generate_batch_idempotency_key(
            source, batch_date, batch_sequence, content_hash
        )

        existing = self.store.get(idempotency_key)
        if existing and existing.status == 'completed':
            logger.info(f"Lote ya procesado: {idempotency_key} ({record_count} registros)")
            return idempotency_key

        record = IdempotencyRecord(
            key=idempotency_key,
            status='pending',
            result={'source': source, 'batch_date': batch_date.isoformat(),
                    'record_count': record_count}
        )
        self.store.save(record)

        logger.info(f"Lote registrado: {idempotency_key} ({record_count} registros)")
        return idempotency_key

    def complete_batch(self, key: str, result: Dict[str, Any]) -> None:
        """Marca un lote como completado."""
        record = self.store.get(key)
        if record:
            record.mark_completed(result)
            self.store.save(record)
            logger.info(f"Lote completado: {key}")

    def fail_batch(self, key: str, error: str) -> None:
        """Marca un lote como fallido."""
        record = self.store.get(key)
        if record:
            record.mark_failed(error)
            self.store.save(record)
            logger.error(f"Lote fallido: {key} - {error}")

// === ARCHIVO: tests/test_data_quality.py ===
import pytest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.transform.data_quality_rules import (
    DataQualityValidator,
    QualityThreshold,
    QualityRule,
    ValidationResult
)


class TestDataQualityValidator:
    """Casos de prueba para validar las reglas de calidad de datos."""

    @pytest.fixture
    def sample_transactions_df(self):
        """DataFrame de transacciones bancarias de ejemplo."""
        data = {
            'transaction_id': ['TX001', 'TX002', 'TX003', 'TX004', 'TX005'],
            'account_id': ['ACC001', 'ACC002', 'ACC003', 'ACC004', 'ACC005'],
            'amount': [100.50, 250.00, -50.00, 1000.00, 75.25],
            'currency': ['USD', 'USD', 'EUR', 'USD', 'USD'],
            'transaction_date': [
                datetime(2024, 1, 15),
                datetime(2024, 1, 16),
                datetime(2024, 1, 17),
                datetime(2024, 1, 18),
                datetime(2024, 1, 19)
            ],
            'transaction_type': ['credit', 'debit', 'credit', 'credit', 'debit'],
            'status': ['completed', 'pending', 'completed', 'completed', 'failed']
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def quality_validator(self):
        """Instancia del validador con umbrales por defecto."""
        thresholds = {
            'null_percentage': 0.05,
            'duplicate_percentage': 0.02,
            'min_records': 10,
            'max_amount': 1000000.0,
            'min_amount': 0.01
        }
        return DataQualityValidator(thresholds)

    def test_validate_null_values_below_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que registros con valores nulos por debajo del umbral pasan la validación."""
        df = sample_transactions_df.copy()
        df.loc[0, 'amount'] = np.nan
        
        result = quality_validator.validate_null_values(df, 'amount')
        
        assert result.is_valid is True
        assert result.null_count == 1
        assert result.null_percentage < 0.05

    def test_validate_null_values_above_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que registros con valores nulos por encima del umbral fallan la validación."""
        df = sample_transactions_df.copy()
        df.loc[0:2, 'amount'] = np.nan
        
        result = quality_validator.validate_null_values(df, 'amount')
        
        assert result.is_valid is False
        assert result.null_count == 3
        assert result.null_percentage >= 0.05

    def test_validate_duplicates_below_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que duplicados por debajo del umbral pasan la validación."""
        df = pd.concat([sample_transactions_df, sample_transactions_df.iloc[[0]]], ignore_index=True)
        
        result = quality_validator.validate_duplicates(df, 'transaction_id')
        
        assert result.is_valid is True
        assert result.duplicate_count == 1

    def test_validate_duplicates_above_threshold(self, quality_validator, sample_transactions_df):
        """Verifica que duplicados por encima del umbral fallan la validación."""
        df = pd.concat([sample_transactions_df, sample_transactions_df], ignore_index=True)
        
        result = quality_validator.validate_duplicates(df, 'transaction_id')
        
        assert result.is_valid is False
        assert result.duplicate_count == 5

    def test_validate_amount_range_valid(self, quality_validator, sample_transactions_df):
        """Verifica que montos dentro del rango válido pasan la validación."""
        result = quality_validator.validate_amount_range(sample_transactions_df, 'amount')
        
        assert result.is_valid is True
        assert result.invalid_count == 0

    def test_validate_amount_range_with_outliers(self, quality_validator, sample_transactions_df):
        """Verifica que montos fuera del rango fallan la validación."""
        df = sample_transactions_df.copy()
        df.loc[0, 'amount'] = 5000000.0
        df.loc[1, 'amount'] = -100.0
        
        result = quality_validator.validate_amount_range(df, 'amount')
        
        assert result.is_valid is False
        assert result.invalid_count == 2

    def test_validate_minimum_records(self, quality_validator, sample_transactions_df):
        """Verifica que se cumple el mínimo de registros requeridos."""
        result = quality_validator.validate_minimum_records(sample_transactions_df)
        
        assert result.is_valid is True

    def test_validate_minimum_records_below_minimum(self, quality_validator):
        """Verifica que se detecta cuando hay menos registros que el mínimo."""
        df = pd.DataFrame({'a': [1, 2, 3]})
        
        result = quality_validator.validate_minimum_records(df)
        
        assert result.is_valid is False

    def test_quarantine_invalid_records(self, quality_validator, sample_transactions_df):
        """Verifica que los registros inválidos se aíslan correctamente en cuarentena."""
        df = sample_transactions_df.copy()
        df.loc[0, 'amount'] = np.nan
        df.loc[1, 'amount'] = -50.00
        df.loc[2, 'transaction_id'] = 'TX001'
        
        valid_df, quarantine_df = quality_validator.quarantine_invalid_records(df)
        
        assert len(quarantine_df) >= 3
        assert len(valid_df) <= 2

    def test_validate_currency_format(self, quality_validator):
        """Verifica la validación del formato de moneda."""
        data = {
            'currency': ['USD', 'EUR', 'GBP', 'INVALID', 'JPY']
        }
        df = pd.DataFrame(data)
        valid_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF']
        
        result = quality_validator.validate_currency_format(df, 'currency', valid_currencies)
        
        assert result.is_valid is False
        assert result.invalid_count == 1

    def test_validate_date_range(self, quality_validator, sample_transactions_df):
        """Verifica que las fechas estén dentro del rango válido."""
        df = sample_transactions_df.copy()
        df.loc[0, 'transaction_date'] = datetime(2020, 1, 1)
        
        min_date = datetime(2023, 1, 1)
        max_date = datetime(2025, 12, 31)
        
        result = quality_validator.validate_date_range(df, 'transaction_date', min_date, max_date)
        
        assert result.is_valid is False
        assert result.invalid_count == 1

    def test_comprehensive_quality_check(self, quality_validator, sample_transactions_df):
        """Verifica la ejecución de un chequeo completo de calidad."""
        results = quality_validator.run_comprehensive_check(sample_transactions_df)
        
        assert isinstance(results, dict)
        assert 'null_validation' in results
        assert 'duplicate_validation' in results
        assert 'amount_range_validation' in results
        assert 'min_records_validation' in results
        
        for key, result in results.items():
            assert isinstance(result, ValidationResult)


class TestQualityThreshold:
    """Casos de prueba para los umbrales de calidad."""

    def test_threshold_creation(self):
        """Verifica la correcta creación de un umbral."""
        threshold = QualityThreshold(
            name='null_percentage',
            value=0.05,
            operator='less_than'
        )
        
        assert threshold.name == 'null_percentage'
        assert threshold.value == 0.05
        assert threshold.operator == 'less_than'

    def test_threshold_evaluation_less_than(self):
        """Verifica la evaluación de umbral con operador less_than."""
        threshold = QualityThreshold('test', 0.1, 'less_than')
        
        assert threshold.evaluate(0.05) is True
        assert threshold.evaluate(0.15) is False

    def test_threshold_evaluation_greater_than(self):
        """Verifica la evaluación de umbral con operador greater_than."""
        threshold = QualityThreshold('test', 10, 'greater_than')
        
        assert threshold.evaluate(15) is True
        assert threshold.evaluate(5) is False

    def test_threshold_evaluation_equals(self):
        """Verifica la evaluación de umbral con operador equals."""
        threshold = QualityThreshold('test', 100, 'equals')
        
        assert threshold.evaluate(100) is True
        assert threshold.evaluate(50) is False


class TestQualityRule:
    """Casos de prueba para las reglas de calidad."""

    def test_rule_creation(self):
        """Verifica la correcta creación de una regla de calidad."""
        rule = QualityRule(
            name='no_null_transactions',
            description='No debe haber valores nulos en transaction_id',
            column='transaction_id',
            validation_type='not_null'
        )
        
        assert rule.name == 'no_null_transactions'
        assert rule.column == 'transaction_id'
        assert rule.validation_type == 'not_null'

    def test_custom_rule_execution(self):
        """Verifica la ejecución de una regla personalizada."""
        df = pd.DataFrame({'amount': [100, 200, -50, 300]})
        
        def negative_check(df, column):
            return df[column].min() >= 0
        
        rule = QualityRule(
            name='no_negative_amounts',
            description='Los montos no pueden ser negativos',
            column='amount',
            validation_type='custom',
            custom_validation=negative_check
        )
        
        result = rule.execute(df)
        
        assert result is False


class TestValidationResult:
    """Casos de prueba para el resultado de validación."""

    def test_validation_result_success(self):
        """Verifica la creación de un resultado exitoso."""
        result = ValidationResult(
            rule_name='test_rule',
            is_valid=True,
            message='Validación exitosa'
        )
        
        assert result.is_valid is True
        assert result.rule_name == 'test_rule'

    def test_validation_result_failure(self):
        """Verifica la creación de un resultado fallido."""
        result = ValidationResult(
            rule_name='test_rule',
            is_valid=False,
            message='Validación fallida',
            details={'failed_count': 5}
        )
        
        assert result.is_valid is False
        assert result.details['failed_count'] == 5

// === ARCHIVO: conf/dev_config.json ===
{
  "environment": "development",
  "pipeline": {
    "name": "financial_analysis_pipeline",
    "version": "1.0.0",
    "enabled": true,
    "max_retries": 3,
    "retry_delay_seconds": 30,
    "retry_backoff_multiplier": 2,
    "timeout_seconds": 3600
  },
  "sources": {
    "bank_transactions": {
      "type": "api",
      "url": "http://localhost:8080/api/v1/transactions",
      "auth": {
        "type": "bearer",
        "token": "dev_token_abc123xyz789"
      },
      "pagination": {
        "enabled": true,
        "page_size": 1000,
        "max_pages": 50
      },
      "timeout_seconds": 60,
      "rate_limit": {
        "requests_per_minute": 120,
        "burst_size": 20
      }
    },
    "market_data": {
      "type": "api",
      "url": "http://localhost:8081/api/v1/market",
      "auth": {
        "type": "api_key",
        "key": "dev_market_key_xyz456",
        "header": "X-API-Key"
      },
      "endpoints": {
        "stocks": "/stocks",
        "indices": "/indices",
        "forex": "/forex",
        "commodities": "/commodities"
      },
      "timeout_seconds": 45,
      "retry_on_failure": true
    },
    "financial_news": {
      "type": "api",
      "url": "http://localhost:8082/api/v1/news",
      "auth": {
        "type": "basic",
        "username": "dev_news_user",
        "password": "dev_news_pass_encrypted"
      },
      "filters": {
        "categories": ["markets", "economy", "banking", "crypto"],
        "language": "en",
        "sentiment_analysis_enabled": true
      },
      "timeout_seconds": 30,
      "max_results_per_query": 500
    }
  },
  "storage": {
    "raw_zone": {
      "type": "s3",
      "bucket": "fin-analytics-dev-raw",
      "path_prefix": "raw/",
      "format": "parquet",
      "partitioning": {
        "enabled": true,
        "fields": ["source", "year", "month", "day"]
      },
      "compression": "snappy"
    },
    "processed_zone": {
      "type": "s3",
      "bucket": "fin-analytics-dev-processed",
      "path_prefix": "processed/",
      "format": "parquet",
      "partitioning": {
        "enabled": true,
        "fields": ["data_type", "year", "month", "day", "hour"]
      },
      "compression": "zstd"
    },
    "curated_zone": {
      "type": "s3",
      "bucket": "fin-analytics-dev-curated",
      "path_prefix": "curated/",
      "format": "delta",
      "partitioning": {
        "enabled": true,
        "fields": ["entity_type", "year", "month", "day"]
      },
      "optimize_on_write": true,
      "schema_enforcement": "strict"
    }
  },
  "data_quality": {
    "enabled": true,
    "rules": {
      "transaction_rules": {
        "min_amount": -1000000,
        "max_amount": 1000000,
        "required_fields": ["transaction_id", "timestamp", "amount", "currency", "account_id"],
        "allowed_currencies": ["USD", "EUR", "GBP", "JPY", "CHF"],
        "null_tolerance": {
          "transaction_id": 0,
          "amount": 0,
          "timestamp": 0
        },
        "duplication_check": {
          "enabled": true,
          "key_fields": ["transaction_id"],
          "action": "quarantine"
        }
      },
      "market_data_rules": {
        "price_range": {
          "min": 0.01,
          "max": 1000000
        },
        "volume_min": 0,
        "required_fields": ["symbol", "timestamp", "close_price", "volume"],
        "outlier_detection": {
          "enabled": true,
          "method": "iqr",
          "threshold": 3.0
        },
        "freshness_seconds": 300
      },
      "news_rules": {
        "required_fields": ["article_id", "published_at", "title", "source"],
        "min_title_length": 10,
        "max_title_length": 500,
        "language_filter": ["en", "es", "fr", "de"],
        "sentiment_range": {
          "min": -1.0,
          "max": 1.0
        }
      }
    },
    "thresholds": {
      "min_success_rate": 0.95,
      "max_null_rate": 0.05,
      "max_duplicate_rate": 0.01,
      "alert_on_failure": true
    },
    "quarantine": {
      "enabled": true,
      "bucket": "fin-analytics-dev-quarantine",
      "retention_days": 30
    }
  },
  "security": {
    "encryption": {
      "at_rest": {
        "enabled": true,
        "algorithm": "AES-256-GCM",
        "kms_key_id": "arn:aws:kms:us-east-1:123456789012:key/dev-key-001"
      },
      "in_transit": {
        "enabled": true,
        "tls_version": "1.2",
        "verify_certificates": false
      }
    },
    "token_expiry_seconds": 3600,
    "max_failed_auth_attempts": 5,
    "audit_logging": {
      "enabled": true,
      "bucket": "fin-analytics-dev-audit",
      "retention_days": 90
    }
  },
  "orchestration": {
    "airflow": {
      "dag_schedule": "0 */6 * * *",
      "max_active_runs": 1,
      "catchup": false,
      "concurrency": 4,
      "pool": "default_pool"
    },
    "dependencies": {
      "bank_transactions": [],
      "market_data": ["bank_transactions"],
      "financial_news": ["market_data"]
    },
    "windowing": {
      "type": "sliding",
      "size_hours": 6,
      "step_hours": 1
    }
  },
  "monitoring": {
    "logging": {
      "level": "DEBUG",
      "format": "json",
      "destination": "cloudwatch",
      "log_group": "/aws/fin-analytics/dev"
    },
    "metrics": {
      "enabled": true,
      "destination": "cloudwatch",
      "namespace": "FinAnalytics/Dev",
      "dimensions": ["Environment", "Pipeline", "Source"]
    },
    "alerts": {
      "enabled": false,
      "sns_topic": "arn:aws:sns:us-east-1:123456789012:dev-alerts-topic"
    },
    "tracing": {
      "enabled": true,
      "service_name": "financial-analysis-pipeline-dev",
      "sample_rate": 1.0
    }
  },
  "processing": {
    "spark": {
      "master": "local[*]",
      "app_name": "financial_analysis_dev",
      "executor": {
        "instances": 2,
        "cores": 2,
        "memory": "2g"
      },
      "shuffle_partitions": 8,
      "max_result_size": "1g"
    },
    "batch": {
      "size": 10000,
      "parallelism": 4
    }
  }
}

// === ARCHIVO: conf/prod_config.json ===
{
  "environment": "production",
  "pipeline": {
    "name": "financial_analysis_pipeline",
    "version": "1.0.0",
    "enabled": true,
    "max_retries": 5,
    "retry_delay_seconds": 60,
    "retry_backoff_multiplier": 2,
    "timeout_seconds": 7200
  },
  "sources": {
    "bank_transactions": {
      "type": "api",
      "url": "https://api.bankcorp.com/v1/transactions",
      "auth": {
        "type": "bearer",
        "token": "${BANK_API_TOKEN}"
      },
      "pagination": {
        "enabled": true,
        "page_size": 5000,
        "max_pages": 200
      },
      "timeout_seconds": 120,
      "rate_limit": {
        "requests_per_minute": 60,
        "burst_size": 10
      },
      "circuit_breaker": {
        "enabled": true,
        "failure_threshold": 5,
        "recovery_timeout_seconds": 300
      }
    },
    "market_data": {
      "type": "api",
      "url": "https://api.marketdata.com/v2",
      "auth": {
        "type": "api_key",
        "key": "${MARKET_API_KEY}",
        "header": "X-API-Key"
      },
      "endpoints": {
        "stocks": "/stocks/realtime",
        "indices": "/indices",
        "forex": "/forex",
        "commodities": "/commodities",
        "derivatives": "/derivatives"
      },
      "timeout_seconds": 90,
      "retry_on_failure": true,
      "retry_count": 3
    },
    "financial_news": {
      "type": "api",
      "url": "https://api.financialnews.com/v3",
      "auth": {
        "type": "oauth2",
        "client_id": "${NEWS_CLIENT_ID}",
        "client_secret": "${NEWS_CLIENT_SECRET}",
        "token_url": "https://auth.financialnews.com/oauth/token"
      },
      "filters": {
        "categories": ["markets", "economy", "banking", "crypto", " Commodities", "forex"],
        "language": "en",
        "sentiment_analysis_enabled": true,
        "relevance_score_min": 0.7
      },
      "timeout_seconds": 60,
      "max_results_per_query": 1000
    }
  },
  "storage": {
    "raw_zone": {
      "type": "s3",
      "bucket": "fin-analytics-prod-raw",
      "path_prefix": "raw/",
      "format": "parquet",
      "partitioning": {
        "enabled": true,
        "fields": ["source", "year", "month", "day", "hour"]
      },
      "compression": "zstd",
      "buffering": {
        "enabled": true,
        "size_mb": 128,
        "flush_interval_seconds": 300
      }
    },
    "processed_zone": {
      "type": "s3",
      "bucket": "fin-analytics-prod-processed",
      "path_prefix": "processed/",
      "format": "parquet",
      "partitioning": {
        "enabled": true,
        "fields": ["data_type", "year", "month", "day", "hour", "source"]
      },
      "compression": "zstd",
      "row_group_size_mb": 128
    },
    "curated_zone": {
      "type": "delta",
      "bucket": "fin-analytics-prod-curated",
      "path_prefix": "curated/",
      "format": "delta",
      "partitioning": {
        "enabled": true,
        "fields": ["entity_type", "year", "month", "day"]
      },
      "optimize_on_write": true,
      "optimize_on_read": true,
      "schema_enforcement": "strict",
      "vacuum": {
        "enabled": true,
        "retention_days": 7,
        "dry_run": false
      },
      "cdf": {
        "enabled": true,
        "change_data_feed": true
      }
    }
  },
  "data_quality": {
    "enabled": true,
    "strict_mode": true,
    "rules": {
      "transaction_rules": {
        "min_amount": -5000000,
        "max_amount": 5000000,
        "required_fields": ["transaction_id", "timestamp", "amount", "currency", "account_id", "merchant_id"],
        "allowed_currencies": ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD"],
        "null_tolerance": {
          "transaction_id": 0,
          "amount": 0,
          "timestamp": 0,
          "merchant_id": 0.01
        },
        "duplication_check": {
          "enabled": true,
          "key_fields": ["transaction_id", "account_id"],
          "action": "quarantine"
        },
        "anomaly_detection": {
          "enabled": true,
          "method": "isolation_forest",
          "contamination": 0.01
        }
      },
      "market_data_rules": {
        "price_range": {
          "min": 0.01,
          "max": 5000000
        },
        "volume_min": 0,
        "required_fields": ["symbol", "timestamp", "open_price", "high_price", "low_price", "close_price", "volume"],
        "outlier_detection": {
          "enabled": true,
          "method": "zscore",
          "threshold": 4.0
        },
        "freshness_seconds": 60,
        "gap_detection": {
          "enabled": true,
          "max_gap_minutes": 15
        }
      },
      "news_rules": {
        "required_fields": ["article_id", "published_at", "title", "source", "url", "authors"],
        "min_title_length": 15,
        "max_title_length": 300,
        "language_filter": ["en", "es", "fr", "de", "ja", "zh"],
        "sentiment_range": {
          "min": -1.0,
          "max": 1.0
        },
        "duplicate_detection": {
          "enabled": true,
          "similarity_threshold": 0.9
        }
      }
    },
    "thresholds": {
      "min_success_rate": 0.99,
      "max_null_rate": 0.02,
      "max_duplicate_rate": 0.005,
      "max_error_rate": 0.01,
      "alert_on_failure": true,
      "stop_pipeline_on_critical_failure": true
    },
    "quarantine": {
      "enabled": true,
      "bucket": "fin-analytics-prod-quarantine",
      "retention_days": 90,
      "auto_cleanup_enabled": true
    }
  },
  "security": {
    "encryption": {
      "at_rest": {
        "enabled": true,
        "algorithm": "AES-256-GCM",
        "kms_key_id": "arn:aws:kms:us-east-1:123456789012:key/prod-key-001",
        "key_rotation_days": 90
      },
      "in_transit": {
        "enabled": true,
        "tls_version": "1.3",
        "verify_certificates": true
      },
      "column_level": {
        "enabled": true,
        "encrypted_columns": ["account_number", "amount", "transaction_details"]
      }
    },
    "token_expiry_seconds": 1800,
    "max_failed_auth_attempts": 3,
    "ip_whitelist": {
      "enabled": true,
      "allowed_ips": ["10.0.0.0/8", "172.16.0.0/12"]
    },
    "audit_logging": {
      "enabled": true,
      "bucket": "fin-analytics-prod-audit",
      "retention_days": 365,
      "immutable": true
    },
    "pii_handling": {
      "masking_enabled": true,
      "pii_fields": ["account_number", "ssn", "email", "phone"],
      "masking_algorithm": "SHA-256"
    }
  },
  "orchestration": {
    "airflow": {
      "dag_schedule": "0 */3 * * *",
      "max_active_runs": 2,
      "catchup": false,
      "concurrency": 8,
      "pool": "production_pool",
      "priority_weight": 10,
      "sla_minutes": 120
    },
    "dependencies": {
      "bank_transactions": [],
      "market_data": ["bank_transactions"],
      "financial_news": ["market_data"]
    },
    "windowing": {
      "type": "tumbling",
      "size_hours": 3,
      "offset_hours": 0
    },
    "backfill": {
      "enabled": true,
      "max_days": 30,
      "parallel_tasks": 4
    }
  },
  "monitoring": {
    "logging": {
      "level": "INFO",
      "format": "json",
      "destination": "cloudwatch",
      "log_group": "/aws/fin-analytics/prod",
      "retention_days": 30
    },
    "metrics": {
      "enabled": true,
      "destination": "cloudwatch",
      "namespace": "FinAnalytics/Prod",
      "dimensions": ["Environment", "Pipeline", "Source", "Stage"],
      "detailed_metrics": true
    },
    "alerts": {
      "enabled": true,
      "sns_topic": "arn:aws:sns:us-east-1:123456789012:prod-alerts-topic",
      "pagerduty_integration": true,
      "escalation_policy": "prod_escalation"
    },
    "tracing": {
      "enabled": true,
      "service_name": "financial-analysis-pipeline-prod",
      "sample_rate": 0.1,
      "xray_enabled": true
    },
    "dashboards": {
      "enabled": true,
      "grafana_url": "https://grafana.fin-analytics.com",
      "refresh_interval_seconds": 30
    }
  },
  "processing": {
    "spark": {
      "master": "spark://prod-master:7077",
      "app_name": "financial_analysis_prod",
      "executor": {
        "instances": 10,
        "cores": 4,
        "memory": "8g"
      },
      "dynamic_allocation": {
        "enabled": true,
        "min_executors": 5,
        "max_executors": 20
      },
      "shuffle_partitions": 200,
      "max_result_size": "4g",
      "speculation": {
        "enabled": true,
        "multiplier": 1.5
      }
    },
    "batch": {
      "size": 50000,
      "parallelism": 16
    },
    "streaming": {
      "enabled": true,
      "checkpoint_location": "s3://fin-analytics-prod-checkpoints/",
      "trigger_interval_seconds": 60
    }
  },
  "cost_optimization": {
    "s3": {
      "lifecycle_policies": {
        "raw_to_glacier_days": 90,
        "processed_delete_days": 365
      },
      "intelligent_tiering": true
    },
    "compute": {
      "spot_instances": true,
      "auto_scaling": true,
      "downscale_after_minutes": 30
    },
    "data_transfer": {
      "optimize_cross_zone": true,
      "use_accelerate_endpoint": true
    }
  }
}

// === ARCHIVO: docs/architecture_diagram.puml ===
@startuml FinancialDataPlatformArchitecture
!theme plain

skinparam componentStyle uml2

package "Fuentes de Datos" {
    component "Transacciones Bancarias" as BankDB #LightBlue
    component "Datos de Mercado" as MarketAPI #LightGreen
    component "Noticias Financieras" as NewsAPI #LightYellow
    component "Sistemas de Terceros" as ThirdParty #LightGray
}

package "Capa de Ingesta (Extract)" {
    component "Bank Transactions Reader" as BankReader #LightBlue
    component "Market Data Reader" as MarketReader #LightGreen
    component "Financial News Reader" as NewsReader #LightYellow
    component "Third Party Integrator" as ThirdPartyReader #LightGray
}

package "Capa de Transformación (Transform)" {
    component "Data Quality Rules" as QualityRules #Orange
    component "Financial Data Transformer" as Transformer #Gold
    component "Data Validation Engine" as Validation #Red
}

package "Capa de Carga (Load)" {
    component "Data Writer" as Writer #LightGreen
    component "Partition Manager" as Partitioner #Purple
    component "Encryption Handler" as Encryptor #DarkBlue
}

package "Almacenamiento" {
    component "Raw Zone (S3)" as RawZone #Gray
    component "Processed Zone (S3)" as ProcessedZone #Silver
    component "Curated Zone (Redshift)" as CuratedZone #Gold
    database "Data Catalog" as Catalog #White
}

package "Orquestación" {
    component "Airflow DAG" as Orchestrator #LightBlue
    component "Step Functions" as StepFunctions #LightGreen
}

package "Seguridad" {
    component "KMS Encryption" as KMS #DarkBlue
    component "IAM Roles" as IAM #DarkGray
    component "VPC Endpoints" as VPC #DarkGreen
}

package "Monitoreo" {
    component "CloudWatch" as Monitoring #LightYellow
    component "Data Quality Dashboard" as QualityDash #Orange
}

BankDB -down-> BankReader : JDBC
MarketAPI -down-> MarketReader : REST API
NewsAPI -down-> NewsReader : REST API
ThirdParty -down-> ThirdPartyReader : Webhook

BankReader -down-> QualityRules : Raw Data
MarketReader -down-> QualityRules
NewsReader -down-> QualityRules
ThirdPartyReader -down-> QualityRules

QualityRules -down-> Transformer : Validated Data
Transformer -down-> Validation : Transformed Data
Validation -down-> Writer : Quality Passed

Writer -down-> Partitioner : Partitioned Data
Partitioner -down-> Encryptor : Encrypted Data

Encryptor -up-> RawZone : Write Raw
Encryptor -up-> ProcessedZone : Write Processed
Encryptor -up-> CuratedZone : Write Curated

Orchestrator -up-> BankReader : Trigger
Orchestrator -up-> MarketReader : Trigger
Orchestrator -up-> NewsReader : Trigger
Orchestrator -up-> ThirdPartyReader : Trigger
Orchestrator -up-> QualityRules : Trigger
Orchestrator -up-> Transformer : Trigger
Orchestrator -up-> Writer : Trigger

KMS -up-> Encryptor : Encrypt/Decrypt
IAM -up-> RawZone : Access Control
IAM -up-> ProcessedZone : Access Control
IAM -up-> CuratedZone : Access Control
VPC -up-> BankDB : Secure Connection

Monitoring -up-> Orchestrator : Monitor
Monitoring -up-> Writer : Monitor
QualityDash -up-> Validation : Quality Metrics

RawZone -right-> Catalog : Metadata
ProcessedZone -right-> Catalog : Metadata
CuratedZone -right-> Catalog : Metadata

@enduml

// === ARCHIVO: docs/requirements_document.md ===
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

// === ARCHIVO: docs/integration_document.md ===
# Documento de Integración con Sistemas de Terceros

## 1. Visión General de Integraciones

La Plataforma de Análisis Financiero se integra con sistemas externos para enriquecer los datos internos con información de mercado, noticias, y servicios especializados. Esta sección documenta los mecanismos de integración, protocolos, y criterios de aceptación.

## 2. Integraciones de Datos de Mercado

### 2.1 Bloomberg Terminal API

**Tipo de integración**: REST API con autenticación OAuth 2.0

**Descripción**: Integración con Bloomberg para obtener cotizaciones en tiempo real, datos históricos, y información corporativa de instrumentos financieros.

**Endpoint principal**:
```
GET https://api.bloomberg.com/v1/market/{symbol}
GET https://api.bloomberg.com/v1/historical/{symbol}
```

**Mecanismo de autenticación**:
- OAuth 2.0 con JWT bearer token
- Token de acceso con validez de 1 hora
- Refresh token para renovación automática
- Certificadosmutuos (mTLS) para entorno de producción

**Criterios de aceptación**:
- Latencia de respuesta < 500ms para consultas individuales
- Soporte parabatch de hasta 100 símbolos por request
- Disponibilidad del 99.95% según SLA de Bloomberg
- Datos de precios con timestamp de milisegundos

**Manejo de errores**:
- Retry exponencial con backoff máximo de 5 minutos
- Circuit breaker tras 10 fallos consecutivos
- Cache local de 30 segundos para evitar llamadas redundantes

### 2.2 Reuters Data Platform

**Tipo de integración**: WebSocket para streaming + REST para consultas históricas

**Descripción**: Proveedor alternativo de datos de mercado con enfoque en mercados internacionales y materias primas.

**Endpoint principal**:
```
WSS wss://stream.reuters.com/market/v1
GET https://api.reuters.com/historical/v1/{symbol}
```

**Mecanismo de autenticación**:
- API Key + Signature HMAC-SHA256
- Rotación de claves cada 90 días
- IP whitelist para acceso restrictivo

**Criterios de aceptación**:
- Streaming sin reconexión manual por 24 horas
- Reconexión automática en < 5 segundos ante desconexión
- Formato de respuesta compatible con esquema JSON definido

## 3. Integraciones de Noticias Financieras

### 3.1 NewsAPI.org

**Tipo de integración**: REST API con polling

**Descripción**: Agregador de noticias de múltiples fuentes con búsqueda y filtrado por categoría, idioma, y fecha.

**Endpoint principal**:
```
GET https://newsapi.org/v2/everything?q=finance
GET https://newsapi.org/v2/top-headlines?category=business
```

**Mecanismo de autenticación**:
- API Key en header de autorización
- Rate limiting: 100 requests/minuto en plan profesional

**Criterios de aceptación**:
- Cobertura de fuentes financieras >= 50 publicaciones
- Retrieval de artículos publicados en los últimos 30 días
- Metadata completa (título, descripción, contenido, imagen, autor)

### 3.2 Webhook de Alertas de Mercado

**Tipo de integración**: Webhook entrante

**Descripción**: Receptor de alertas automáticas de eventos de mercado (movimientos significativos, noticias de última hora, cambios en ratings).

**Configuración del endpoint**:
```
POST https://platform.internal.webhook/v1/market-alerts
```

**Mecanismo de seguridad**:
- HMAC-SHA256 signature en header X-Signature
- IP allowlist de sistemas emisores conocidos
- Validación de payload contra JSON Schema

**Criterios de aceptación**:
- Procesamiento de webhook en < 1 segundo
- Acknowledge de receipt en < 200ms
- Idempotencia mediante deduplicación por message_id

## 4. Integraciones de Servicios Auxiliares

### 4.1 Serviciode Análisis de Sentimiento

**Tipo de integración**: REST API asíncrona

**Descripción**: Servicio externo de NLP para análisis de sentimiento de noticias y redes sociales.

**Endpoint principal**:
```
POST https://ml-service.internal.ai/v1/sentiment/analyze
```

**Payload de request**:
```json
{
  "text": "string",
  "language": "string",
  "entities": ["string"]
}
```

**Criterios de aceptación**:
- Scoring de sentimiento en escala -1 a 1
- Identificación de entidades mencionadas
- Latencia < 3 segundos por documento
- Throughput: 1000 documentos/minuto

### 4.2 Servicio de Validación de Identidades

**Tipo de integración**: REST API sincrónica

**Descripción**: Verificación de identidades para cumplimiento KYC/AML en transacciones.

**Endpoint principal**:
```
POST https://kyc-service.internal.com/v2/verify
```

**Mecanismo de seguridad**:
- mTLS con certificados de cliente
- OAuth 2.0 con scope específico
- Logging de auditoría para regulatoría

**Criterios de aceptación**:
- Respuesta de verificación en < 2 segundos
- Tasa de falsos positivos < 1%
- Disponibilidad 99.99%

## 5. Patrones de Integración

### 5.1 Patrón de Retry

Todas las integraciones implementan retry con:
- Backoff exponencial: 1s, 2s, 4s, 8s, 16s, máximo 5 minutos
- Jitter aleatorio ±20% para evitar thundering herd
- Máximo 5 reintentos para APIs sincrónicas
- Máximo 3 reintentos para webhooks

### 5.2 Patrón de Circuit Breaker

- Umbral de apertura: 50% de fallos en ventana de 30 segundos
- Timeout de medio circuito: 60 segundos
- Recupero gradual: 10% de requests de prueba cada 30 segundos

### 5.3 Patrón de Rate Limiting

- Client-side: tracking de requests por ventana de tiempo
- Server-side: respuesta 429 con header Retry-After
- Backoff adaptativo basado en límites detectados

## 6. Monitoreo de Integraciones

### 6.1 Métricas Obligatorias

| Métrica | Descripción | Umbral de alerta |
|---------|-------------|------------------|
| integration_latency_ms | Latencia de respuesta | > 5000ms |
| integration_error_rate | Tasa de errores | > 5% |
| integration_availability | Disponibilidad | < 99.5% |
| integration_timeout_rate | Tasa de timeouts | > 2% |

### 6.2 Logs Estructurados

Cada integración emite logs con:
- Correlation ID para trazabilidad end-to-end
- Timestamp ISO 8601
- Request/response size
- HTTP status code
- Latencia total
- Tipo de error si aplica

## 7. Plan de Contingencia

### 7.1 Fallo de Proveedor de Datos de Mercado

- Activar proveedor alternativo (failover automático)
- Usar datos en cache con indicador de staleness
- Notificación a equipo de operaciones

### 7.2 Fallo de Webhook de Alertas
n- Queue local con persistencia de 24 horas
- Reprocesamiento programado cada 15 minutos
- Alerta crítica si queue excede 1000 mensajes

### 7.3 Fallo de Servicio de Análisis

- Modo degraded: procesar sin análisis de sentimiento
- Batch offline para procesamiento diferido
- Notificación a equipo de ML para investigación

// === ARCHIVO: docs/optimization_document.md ===
# Documento de Optimización de Arquitectura

## Resumen Ejecutivo

Este documento presenta las áreas de mejora identificadas en la arquitectura de datos para la plataforma de análisis financiero, junto con las optimizaciones implementadas y su impacto esperado en rendimiento, escalabilidad y mantenibilidad del sistema.

---

## 1. Áreas de Identificación y Mejora

### 1.1 Optimización de Pipelines ETL

**Problema Identificado:**
Los pipelines ETL originales presentaban cuellos de botella en la etapa de transformación debido a procesamiento secuencial de registros y falta de paralelismo en la carga de datos desde múltiples fuentes.

**Optimización Implementada:**
- Implementación de procesamiento paralelo mediante PySpark Distributed Computing
- Particionamiento de datos por fecha y tipo de fuente para optimizar consultas
- Uso de formatos columnares (Parquet) para reducir tiempo de lectura/escritura
- Implementación de checkpointing para recuperación ante fallos

**Impacto:**
- Reducción del tiempo de procesamiento total en un 65%
- Mejora en el throughput de procesamiento de 1,200 a 4,500 registros/segundo
- Disminución del uso de memoria en un 40% mediante particionamiento efectivo

### 1.2 Estrategia de Calidad de Datos

**Problema Identificado:**
La validación de datos se realizaba al final del pipeline, causando reprocesamiento completo cuando se detectaban registros inválidos.

**Optimización Implementada:**
- Implementación de reglas de calidad en cada etapa del pipeline
- Sistema de cuarentena automática para registros con problemas
- Validación de esquemas en tiempo de extracción mediante JSON Schema
- Métricas de calidad en tiempo real con umbrales configurables

**Impacto:**
- Reducción del 85% en registros rechazados por validación tardía
- Tiempo de detección de problemas reducido de horas a minutos
- Trazabilidad completa de linaje de datos

### 1.3 Arquitectura de Almacenamiento

**Problema Identificado:**
Almacenamiento plano sin estrategia de optimización查询 y costos elevados en transferencia de datos.

**Optimización Implementada:**
- Migración a Delta Lake para gestión de versiones y transacciones ACID
- Particionamiento jerárquico por fecha, fuente y tipo de activo
- Implementación de compaction automática y optimización de archivos pequeños
- Capa de metastore para catálogo centralizado de datos

**Impacto:**
- Reducción del 55% en costos de almacenamiento S3
- Mejora del 70% en tiempo de consulta para análisis históricos
- Habilitación de time travel para recuperación de datos

### 1.4 Seguridad y Cumplimiento

**Problema Identificado:**
Falta de cifrado en reposo y controles de acceso granulares para datos sensibles.

**Optimización Implementada:**
- Cifrado de datos en reposo mediante AWS KMS con claves segregadas por sensibilidad
- Implementación de tokenización para datos PII
- Control de acceso basado en roles con integración IAM
- Auditoría completa de accesos mediante CloudTrail

**Impacto:**
- Cumplimiento de PCI-DSS y GDPR para datos financieros
- Cero incidentes de fuga de información en pruebas de penetración
- Reducción del 30% en tiempo de auditoría de cumplimiento

### 1.5 Orquestación y Resiliencia

**Problema Identificado:**
Falta de manejo robusto de fallos y reprocesamiento manual necesario.

**Optimización Implementada:**
- Implementación de idempotencia mediante claves únicas de procesamiento
- Retry automático con backoff exponencial (configurable por etapa)
- Dead letter queues para mensajes que fallan repetidamente
- Monitorización continua con alertas proactivas

**Impacto:**
- Reducción del 92% en intervención manual para recuperación
- Tiempo medio de recuperación (MTTR) reducido de 4 horas a 15 minutos
- Disponibilidad del sistema incrementada al 99.95%

---

## 2. Métricas de Optimización

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo de procesamiento E2E | 45 min | 18 min | 60% |
| Throughput | 1,200 reg/s | 4,500 reg/s | 275% |
| Costo por millón de registros | $12.50 | $5.20 | 58% |
| Disponibilidad | 99.2% | 99.95% | 0.75% |
| Tiempo de recuperación | 4 horas | 15 min | 93.75% |
| Registros válidos finales | 94.5% | 99.7% | 5.2% |

---

## 3. Recomendaciones Futuras

### 3.1 Corto Plazo (0-3 meses)
- Implementar caching en tiempo real para consultas frecuentes
- Optimizar índices en columnas de alta cardinalidad
- Automatizar detección de skew en joins

### 3.2 Mediano Plazo (3-6 meses)
- Migrar a Iceberg para mayor flexibilidad de esquemas
- Implementar streaming en tiempo real con Kafka Connect
- Habilitar ML ops para detección de anomalías

### 3.3 Largo Plazo (6-12 meses)
- Implementar data mesh arquitectura
- Descentralizar dominios de datos por área de negocio
- Habilitar compute separation para workloads mixtos

---

## 4. Conclusión

Las optimizaciones implementadas demuestran que la arquitectura original, si bien funcional, presentaba oportunidades significativas de mejora en rendimiento, costo y mantenibilidad. La inversión en estas optimizaciones posiciona la plataforma para escalar horizontalmente mientras mantiene los estándares de calidad y seguridad requeridos para datos financieros sensibles.

La arquitectura resultante cumple con los siguientes objetivos estratégicos:
- Escalabilidad lineal mediante particionamiento efectivo
- Confiabilidad mediante idempotencia y recuperación automática
- Seguridad mediante cifrado y control de acceso granular
- Observabilidad mediante métricas y trazabilidad completa

---

*Documento generado como parte del proceso de revisión y optimización de la arquitectura de datos para la plataforma de análisis financiero.*
```
