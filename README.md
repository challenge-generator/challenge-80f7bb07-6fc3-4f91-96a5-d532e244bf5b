# Diseño de Arquitectura de Datos para una Plataforma de Análisis Financiero

Eres un Ingeniero de Datos Senior encargado de levantar los requerimientos y diseñar la arquitectura de datos para una nueva plataforma de análisis financiero. La plataforma debe integrar datos de múltiples fuentes, incluyendo transacciones bancarias, datos de mercado y fuentes de noticias financieras. Deberás asegurar que la arquitectura soporte alta disponibilidad, escalabilidad y seguridad de los datos. Los datos deben ser consistentes y actualizados en tiempo real para permitir análisis en vivo. La plataforma también debe soportar la integración con sistemas de terceros para la obtención de datos adicionales.

## Informacion General

| Campo | Valor |
|-------|-------|
| **Tema** | Levantamiento de requerimientos de Arquitectura de Datos |
| **Nivel** | master-l3 |
| **Tipo** | mixed |
| **Tiempo estimado** | 10 horas |

## Fases del Reto

### Fase 0: Configuración del Proyecto

**Objetivo:** Obtener el proyecto base funcional enviando el Código Base a un asistente de IA, que lo analizará, corregirá errores y generará un ZIP listo para usar.

**Tiempo estimado:** 15-30 minutos

**Instrucciones:**

- Asegúrate de tener instalado para ejecutar el proyecto: Python 3.10+, pip, VS Code o similar.
- Copia todo el contenido del campo **Código Base** de este reto — incluyendo el texto de instrucciones que aparece al inicio.
- Abre un asistente de IA (Claude en claude.ai, ChatGPT o Gemini — se recomienda Claude), pega el contenido copiado en el chat y envíalo.
- El asistente analizará los archivos, corregirá errores y generará un archivo ZIP descargable. Descárgalo y extráelo en la carpeta donde quieras trabajar.
- Ejecuta `pip install -r requirements.txt` y luego arranca el proyecto. Si no hay errores, estás listo.

**Entregable:** El proyecto compila/arranca sin errores.

<details>
<summary>Pistas de conocimiento</summary>

- Copia el Código Base completo incluyendo el texto de instrucciones al inicio — esas instrucciones le indican al asistente exactamente qué hacer con los archivos.
- Si el asistente no genera el ZIP automáticamente al terminar el análisis, escríbele: "genera el ZIP ahora".
- Si el proyecto tiene errores al arrancar, comparte el mensaje de error con el mismo asistente para que lo corrija.

</details>

### Fase 1: Identificación de Fuentes de Datos y Requerimientos Funcionales

**Objetivo:** Enumerar y describir todas las fuentes de datos que la plataforma debe integrar y los requerimientos funcionales que deben ser satisfechos.

**Tiempo estimado:** 2 horas

**Instrucciones:**

- Identificar al menos tres fuentes de datos diferentes que la plataforma debe integrar.
- Describir los requerimientos funcionales para cada fuente de datos, incluyendo la frecuencia de actualización, volumen de datos y formato de los datos.

**Entregable:** Documento que lista todas las fuentes de datos y sus requerimientos funcionales.

<details>
<summary>Pistas de conocimiento</summary>

- Considera la latencia aceptable para la actualización de datos en tiempo real.
- Piensa en la consistencia de los datos entre diferentes fuentes.

</details>

### Fase 2: Definición de la Arquitectura de Datos

**Objetivo:** Diseñar la arquitectura de datos que soporte los requerimientos identificados en la fase anterior.

**Tiempo estimado:** 4 horas

**Instrucciones:**

- Definir la estructura de la base de datos, incluyendo tablas y relaciones.
- Describir cómo se asegurará la alta disponibilidad y escalabilidad de la arquitectura.
- Identificar los mecanismos de seguridad para proteger los datos.

**Entregable:** Diagrama de la arquitectura de datos y documento descriptivo.

<details>
<summary>Pistas de conocimiento</summary>

- Considera el uso de particionamiento y replicación para mejorar la disponibilidad y escalabilidad.
- Piensa en el cifrado de datos en tránsito y en reposo para la seguridad.

</details>

### Fase 3: Integración con Sistemas de Terceros

**Objetivo:** Describir cómo la plataforma se integrará con sistemas de terceros para obtener datos adicionales.

**Tiempo estimado:** 2 horas

**Instrucciones:**

- Identificar al menos dos sistemas de terceros que la plataforma debe integrar.
- Describir los mecanismos de integración, incluyendo API, webhooks o otros métodos.
- Definir los criterios de aceptación para la integración exitosa.

**Entregable:** Documento que describe la integración con sistemas de terceros.

<details>
<summary>Pistas de conocimiento</summary>

- Considera la latencia y el volumen de datos que cada sistema de terceros puede manejar.
- Piensa en la autenticación y autorización necesarias para la integración.

</details>

### Fase 4: Revisión y Optimización de la Arquitectura

**Objetivo:** Revisar y optimizar la arquitectura de datos diseñada para asegurar que cumple con todos los requerimientos y es eficiente.

**Tiempo estimado:** 2 horas

**Instrucciones:**

- Revisar la arquitectura de datos y hacer las mejoras necesarias para asegurar que cumple con todos los requerimientos.
- Identificar áreas de optimización para mejorar la eficiencia de la arquitectura.
- Describir las mejoras realizadas y su impacto en la arquitectura.

**Entregable:** Documento que describe las mejoras realizadas y su impacto en la arquitectura.

<details>
<summary>Pistas de conocimiento</summary>

- Considera la optimización de consultas y el uso de índices para mejorar la eficiencia.
- Piensa en la implementación de caché para reducir la latencia.

</details>

## Dimensiones Evaluadas

- **queEs**: ¿Qué es una arquitectura de datos y por qué es importante en una plataforma de análisis financiero?
- **paraQueSirve**: ¿Para qué sirve la integración con sistemas de terceros en una plataforma de análisis financiero?
- **comoSeUsa**: ¿Cómo se usa el particionamiento y la replicación para mejorar la disponibilidad y escalabilidad de una arquitectura de datos?
- **erroresComunes**: ¿Cuáles son los errores comunes al diseñar una arquitectura de datos para una plataforma de análisis financiero?
- **queDecisionesImplica**: ¿Qué decisiones implica la elección de mecanismos de integración con sistemas de terceros?

## Criterios de Evaluacion

- Identificación correcta de todas las fuentes de datos y sus requerimientos funcionales.
- Diseño de una arquitectura de datos que soporte alta disponibilidad, escalabilidad y seguridad.
- Descripción clara de la integración con sistemas de terceros y sus mecanismos.
- Revisión y optimización efectiva de la arquitectura de datos.

## Como trabajar con un asistente de IA

Hay dos caminos, elegi uno:

- **AGENTS.md** (recomendado) — instrucciones nativas del repo. Abri esta carpeta con tu agente local (Claude Code, Cursor, Codex, Copilot, Gemini) y las carga solo. Sabe que archivos faltan y con que comando se verifica, y completa el scaffold escribiendo en disco.
- **PROMPT_MEJORA.md** — para copiar y pegar en un chat (claude.ai, ChatGPT). Devuelve un ZIP con el proyecto. Sirve si no tenes un agente en el IDE.

Ninguno de los dos resuelve las fases del reto: eso es tu trabajo.

## Verificacion

El proyecto esta listo para trabajar cuando este comando corre sin errores:

```bash
pip install -r requirements.txt && pytest -q
```

---

*Reto generado automaticamente por Challenge Generator - Pragma*
