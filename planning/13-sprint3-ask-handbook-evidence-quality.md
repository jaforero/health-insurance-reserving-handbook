# Ask the Handbook · Sprint 3 — Integridad del motor y compuertas de calidad

## Estado y decisión

- **Iniciativa única:** Ask the Handbook · Evidence-Driven Quality (Sprint 3).
- **Línea base:** Sprint 2 y mejora de indexación del corpus, PR [#22](https://github.com/jaforero/health-insurance-reserving-handbook/pull/22).
- **Fase inicial (P0):** implementación propuesta en un solo PR; no se considera liberada hasta que CI y la revisión editorial sean satisfactorios.
- **Arquitectura preservada:** navegador + MkDocs + GitHub Pages, sin LLM, backend, embeddings externos ni costos variables por pregunta.
- **Propósito:** impedir que una actualización de documentación o del ranking introduzca brechas de cobertura, respuestas sin respaldo o diferencias entre fuente y despliegue.

## 1. Problema verificable

El generador incorporado en el PR #22 indexaba el corpus, pero también modificaba `docs/assets/javascripts/handbook-qa.js` y `docs/assets/stylesheets/handbook-qa.css` por sustitución de texto durante el build. Además, `handbook-qa-catalog.json` y `handbook-section-index.json` se mantenían versionados en estados anteriores a la generación. Esta separación impedía que el repositorio, antes de ejecutar el build, mostrara exactamente la implementación servida.

La corrección de P0 establece **fuentes editables versionadas** frente a **artefactos derivados**:

| Tipo | Fuente única | Regla |
| --- | --- | --- |
| Lógica de consulta y presentación | `docs/assets/javascripts/handbook-qa.js` | Versionada, jamás modificada durante generación |
| Estilos de estados | `docs/assets/stylesheets/handbook-qa.css` | Versionados, jamás modificados durante generación |
| Catálogo editorial base | `config/handbook_qa_base_catalog.json` | Versionado; contiene preguntas existentes |
| Respuestas editoriales prioritarias | `config/handbook_qa_editorial_defaults.json` | Versionadas; se aplican sin duplicar IDs |
| Índice de corpus | `docs/assets/data/handbook-section-index.json` | Derivado de `docs/**/*.md`; se genera antes de probar/servir/publicar |
| Catálogo para navegador | `docs/assets/data/handbook-qa-catalog.json` | Derivado de ambos archivos editoriales; se genera antes de probar/servir/publicar |
| Generador | `scripts/generate_handbook_qa_knowledge.py` | Solo produce o verifica JSON; no reescribe JS/CSS |

Ambos JSON derivados quedan excluidos del control de versiones. Deben existir en el **artefacto publicado** y en el entorno local después de `make qa-index`. No es una decisión de borrar contenido editorial: la fuente base se conserva en `config/`.

## 2. Entrega P0 · Compilación reproducible y quality gate

**Flujo local:** `make qa-index` → `make test` → `make build`. El generador admite `--check` para verificar el contenido de los JSON sin modificarlos.

**Compuertas obligatorias de CI:**

1. Generar el catálogo y el índice a partir de las fuentes versionadas.
2. Ejecutar el generador en modo `--check` para comprobar que el resultado es determinista.
3. Comprobar que el paso de generación no cambia JS ni CSS y que los JSON derivados no están registrados como archivos fuente.
4. Ejecutar la suite Python de estructura, integridad de archivos, fuentes, anchors, presupuesto de tamaño, privacidad y datos del corpus.
5. Ejecutar las regresiones JS existentes y la matriz bloqueante `tests/fixtures/handbook_qa_quality_cases.json` con `tests/js/test_handbook_qa_quality_gate.js`.
6. Mantener la auditoría y construcción `mkdocs build --strict` y las pruebas del Knowledge Graph/Explorer.

### Contratos de calidad de la matriz inicial

Los ocho casos iniciales no constituyen una evaluación estadística representativa: son **regresiones críticas bloqueantes**. Para pasar deben acertar **8/8** en estado, ID editorial cuando aplica, abstención y ruta de evidencia requerida. Incluyen:

- la pregunta histórica «Para reservas en salud cuál de los métodos es más recomendado?» y su primera sugerencia por defecto;
- dos formulaciones equivalentes de selección metodológica;
- una pregunta respaldada por el corpus sobre glosas y controversias en salud;
- dos consultas fuera de alcance, incluida una instrucción que intenta eludir las fuentes;
- una consulta sin soporte para verificar la abstención.

**Regla editorial:** `verified` significa coincidencia con respuesta editorial revisada; `corpus_match` únicamente identifica pasajes fuente y **no** equivale a una respuesta generada o validada clínico-actuarialmente. Nunca optimizar la cobertura sacrificando abstención fundamentada.

## 3. Fase P1 · Benchmark de recuperación y evidencia (posterior a P0)

Ampliar la matriz a 50–100 consultas revisadas por actuarios, con preguntas en español e inglés, sinonimia, consultas transversales, negações, preguntas sin soporte y ambigüedades sobre: pagado/incurrido, IBNR/IBNER, madurez, Chain Ladder, BF, PMPM, GLM, riesgo Colombia, glosas y cambios de calendario. Cada caso llevará intención, fuentes mínimas, fuentes contraindicadas cuando proceda y criterio de abstención. La ampliación debe ser un cambio revisable, no datos generados como verdades sin revisión.

Medidas que se reportarán por versión del índice: **Recall@5** de fuentes, **MRR** o ranking medio de evidencia relevante, tasa de abstención correcta, tasa de falsos positivos de `corpus_match`, validez de anchors, tamaño de los recursos publicados y latencia de consultas en navegador. En la fase no generativa, *faithfulness* de texto generado no aplica; se evalúa **trazabilidad y pertinencia de evidencia**. Los umbrales de producción para esos indicadores deben fijarse después de contar con un conjunto etiquetado suficiente; no se inventan aquí.

## 4. Fase P2 · Recuperación granular y jerarquía del Knowledge Graph

Solo después de medir el baseline se decidirá si incorporar indexación por pasajes completos, BM25, expansión de sinónimos de dominio y señales del Knowledge Graph. Cualquier método nuevo debe superar el benchmark de P1, preservar enlaces válidos y mantener restricciones de costo y privacidad. No mezclar este desarrollo con P0: dificultaría atribuir mejoras o regresiones.

## 5. Criterios para integrar el PR de P0

- El código fuente JS/CSS contiene `corpus_match` sin transformaciones de build.
- El catálogo base y los defaults se pueden regenerar de manera idempotente; no hay JSON derivados obsoletos versionados.
- La consulta original retorna `verified` y el ID `health-reserving-method-selection`; figura primero en sugerencias por defecto.
- La consulta sobre glosas conserva `corpus_match` con enlace a `part-07-colombia/32-colombia-glosas-and-disputes.md`.
- Consultas fuera de alcance y sin evidencia no se convierten en respuestas.
- `make test`, `python scripts/generate_handbook_qa_knowledge.py --check`, `make build` y CI quedan correctos.
- No se alteran los capítulos actuariales ni se modifica el contenido de una respuesta sin revisión.

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
| --- | --- |
| Eliminación accidental de un archivo derivado local | `make qa-index` reconstruye ambos JSON desde `docs/` y `config/` |
| Uso de `mkdocs build` directo sin preprocesamiento | Usar `make build`; CI obliga a generar primero |
| Falsa cobertura por coincidencia léxica | Pruebas negativas bloqueantes y posterior revisión de Recall@5 y falsos positivos |
| Pérdida de enlaces o anchors | Suite Python de fuentes y secciones; build estricto |
| Sobreajuste a una única pregunta | Matriz de dominios/abstenciones y expansión curada en P1 |
| Confundir recuperación con recomendación actuarial | Preservar estados, citas a fuentes y advertencia de alcance |

**Decisión de cierre:** no fusionar el PR cuando alguna compuerta falle; no declarar alcanzadas las métricas de P1/P2 hasta medirlas.
