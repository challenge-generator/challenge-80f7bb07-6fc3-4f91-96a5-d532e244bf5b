# AGENTS.md

Instrucciones para el agente de IA que abra este repositorio (Claude Code, Cursor, Codex, Copilot, Gemini). Se cargan solas: no hay que pegar nada en ningun chat.

## Que es este repositorio

Es el codigo base de un reto de aprendizaje de Pragma: **Diseño de Arquitectura de Datos para una Plataforma de Análisis Financiero**.

| | |
|---|---|
| Tema | Levantamiento de requerimientos de Arquitectura de Datos |
| Nivel | master-l3 |
| Chapter | Ciencia de Datos — Ingeniero de Datos |
| Especialidad | Ingeniero de datos |
| Stack | Python / Apache Airflow |
| Patron arquitectonico | ETL con orquestación en capas y pipelines idempotentes |
| Tiempo estimado | 10 horas |

## Receta del stack

Esqueleto obligatorio:

- `pyproject.toml o requirements.txt en la raiz`
- `dags/ con el DAG de Airflow o el orquestador equivalente`
- `src/extract con los lectores de origen`
- `src/transform con las transformaciones y las reglas de calidad`
- `src/load con los escritores de destino`
- `tests/ con casos de validacion de resultados esperados`
- `conf/ con la configuracion por ambiente`

Dependencias:

- apache-airflow 2.9.3
- pandas 2.2.2
- pyspark 3.5.1
- boto3 1.34.120
- pyarrow 16.1.0
- pytest 8.2.0
- jsonschema 4.22.0
- cryptography 42.0.8
- python-dotenv 1.0.1

## Tu tarea

Dejar este proyecto en estado **verificable**: que el comando de verificacion corra sin errores. Escribi los archivos en disco, en este repositorio. No generes ZIPs ni archivos adjuntos.

En orden:

1. Corre `pip install -r requirements.txt && pytest -q` y mira que falla.
2. Completa lo que falte de la lista de abajo: manifiesto de dependencias, punto de entrada, capa de interfaz y las capas del patron declarado.
3. Arregla SOLO los errores que impiden compilar o arrancar.
4. Volve a correr `pip install -r requirements.txt && pytest -q` hasta que pase.
5. Pará ahí.

## Regla dura: las fases son trabajo del humano

**PROHIBIDO implementar los entregables de las fases.** El valor del reto esta en que la persona los resuelva. Tu trabajo es que tenga un proyecto que arranca; el hueco pedagogico se queda como esta.

No resuelvas nada de esto:

- **Fase 1 — Identificación de Fuentes de Datos y Requerimientos Funcionales**: Documento que lista todas las fuentes de datos y sus requerimientos funcionales.
- **Fase 2 — Definición de la Arquitectura de Datos**: Diagrama de la arquitectura de datos y documento descriptivo.
- **Fase 3 — Integración con Sistemas de Terceros**: Documento que describe la integración con sistemas de terceros.
- **Fase 4 — Revisión y Optimización de la Arquitectura**: Documento que describe las mejoras realizadas y su impacto en la arquitectura.

Distincion operativa:

- **Arreglar** (si): import faltante, tipo que no existe, dependencia sin declarar, error de sintaxis, archivo referenciado que no existe.
- **No tocar** (no): logica de negocio incompleta, validaciones ausentes, secretos hardcodeados, APIs deprecadas que funcionan, concurrencia insegura, patrones mejorables. Eso es lo que la persona tiene que encontrar.

## Superficie de practica (NO completes)

Estos archivos SON el ejercicio de la persona. No los implementes; deja stubs. No toques la logica que el reto pide completar.

- [ ] `src/utils/security_utils.py` — El topic pide autenticacion/seguridad: este archivo es el ejercicio.

## Lo que falta y tenes que completar

### 1. Archivos que la arquitectura declara (3 de 22)

La propuesta arquitectonica del reto los lista y no llegaron al repo. Crealos con implementacion real, respetando la capa en la que viven:

- [ ] `src/utils/security_utils.py`
- [ ] `tests/test_transformations.py`
- [ ] `tests/test_idempotency.py`

### 2. Referencias colgando (3)

Salieron de un analisis estatico del codigo que SI esta en el repo. Cada una rompe la compilacion:

- [ ] `dags/financial_analysis_pipeline.py` — `DataWriter.get`
      Se invoca `get` sobre `DataWriter`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- [ ] `requirements.txt` — `aws-encryption-sdk@3.1.2`
      aws-encryption-sdk declara la version 3.1.2, pero PyPI respondio que esa version no existe. Es una version inventada: reemplazala por una version publicada real, o si no se conoce con certeza, usa el mecanismo centralizado del ecosistema (BOM/parent/platform/version catalog) y no declares una version individual.
- [ ] `requirements.txt` — `delta-rs@0.17.0`
      delta-rs declara la version 0.17.0, pero PyPI respondio que esa version no existe. Es una version inventada: reemplazala por una version publicada real, o si no se conoce con certeza, usa el mecanismo centralizado del ecosistema (BOM/parent/platform/version catalog) y no declares una version individual.

### Presentes (19)

- `requirements.txt`
- `src/schemas/transaction_schema.json`
- `src/schemas/market_data_schema.json`
- `src/schemas/news_schema.json`
- `dags/financial_analysis_pipeline.py`
- `src/extract/bank_transactions_reader.py`
- `src/extract/market_data_reader.py`
- `src/extract/financial_news_reader.py`
- `src/transform/data_quality_rules.py`
- `src/transform/financial_data_transformer.py`
- `src/load/data_writer.py`
- `src/utils/idempotency_utils.py`
- `tests/test_data_quality.py`
- `conf/dev_config.json`
- `conf/prod_config.json`
- `docs/architecture_diagram.puml`
- `docs/requirements_document.md`
- `docs/integration_document.md`
- `docs/optimization_document.md`

### Capas del patron declarado

Cada una tiene que existir como directorio real con al menos un archivo. Codigo plano en la raiz no satisface el patron.

- `dags`
- `src/extract`
- `src/transform`
- `src/load`
- `src/schemas`
- `src/utils`
- `tests`
- `conf`
- `docs`

## Verificacion

```bash
pip install -r requirements.txt && pytest -q
```

El comando tiene que pasar SIN implementar los archivos de la superficie de practica: solo andamiaje.

Ese comando pasando es la definicion de "terminado" para vos.

## Convenciones que tenes que respetar

- Un solo ecosistema: no declares librerias de otro lenguaje ni mezcles gestores de paquetes.
- Toda libreria que uses tiene que estar declarada en el manifiesto de dependencias.
- Todo import declarado tiene que usarse; todo tipo usado tiene que existir o venir de una dependencia declarada.
- El patron es **ETL con orquestación en capas y pipelines idempotentes**: los contratos (interfaces, puertos) los define la capa interna y los implementa la externa, nunca al revés.
- Los archivos que crees llevan implementacion real, no stubs: sin `TODO`, sin cuerpos vacios, sin `// getters y setters`.

## Contexto del candidato

Sirve para calibrar el nivel del codigo, no para resolver las fases.

- Perfil: Chapter Ciencia de Datos, Especialidad Ingeniero de Datos, Seniority Master
- Brecha que el reto ataca: Ha hecho el levantamiento de los requerimientos técnicos y funcionales de un proyecto de datos. Además, diseña la solución acorde a la necesidad.
- Mision: Candidato con experiencia senior en ingeniería de datos

---

*Generado por Challenge Generator — Pragma. `README.md` tiene el enunciado completo del reto para la persona. `PROMPT_MEJORA.md` es la variante para pegar en un chat, si se prefiere ese flujo.*
