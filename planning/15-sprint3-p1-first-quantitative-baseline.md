# Ask the Handbook · Sprint 3 P1 — Primera línea base cuantitativa

## Proveniencia y límites de interpretación

- **Fecha de observación:** 2026-11-07 (Bogotá); ejecución de GitHub Actions del 2026-11-08 UTC.
- **Ejecución verificable:** [Validate and build · run 42433088246](https://github.com/jaforero/health-insurance-reserving-handbook/actions/runs/42433088246), concluida con éxito.
- **Commit evaluado:** `be2f000eae2543e5a7885c645ab789fe8ab09265`.
- **Motor y corpus:** motor JavaScript y los 58 Markdown indexados para la rama del PR #24; los dos JSON operativos se generaron desde las fuentes versionadas.
- **Matriz:** 65 consultas, 53 formulaciones documentales y 12 pruebas de alcance. Para la medición existen **12 referencias `path#anchor` inspeccionadas**, 6 controles de alcance revisados y 47 casos pendientes.
- **Criterio de métrica:** solo `reviewed_source` entra en Hit@k y MRR documental; solo `reviewed_scope` entra en los controles de alcance. Los 47 casos `pending` no forman parte de ningún denominador.

> **Precaución:** esta primera inspección de pasajes fue realizada mediante revisión técnica asistida, no adjudicada por un segundo actuario independiente. La selección inicial es deliberada y reducida: no representa una estimación de desempeño general del Handbook. Las fuentes alternativas aún no han sido exhaustivamente etiquetadas, por lo que Hit@k de apartado exacto es una medida estricta y potencialmente conservadora.

## 1. Resultados observados

| Métrica | Numerador / denominador | Valor |
|---|---:|---:|
| Sección exacta revisada, Hit@1 | 0 / 12 | **0 %** |
| Sección exacta revisada, Hit@3 | 0 / 12 | **0 %** |
| Sección exacta revisada, Hit@5 | 0 / 12 | **0 %** |
| MRR@5 de sección exacta | 0 / 12 | **0,0000** |
| Documento que contiene la referencia, Hit@1 | 1 / 12 | **8,3 %** |
| Documento que contiene la referencia, Hit@3 | 7 / 12 | **58,3 %** |
| Documento que contiene la referencia, Hit@5 | 7 / 12 | **58,3 %** |
| MRR@5 a nivel documento | 3,6667 / 12 | **0,3056** |
| `insufficient` pese a tener pasaje revisado | 5 / 12 | **41,7 %** |
| Sin respuesta editorial sustantiva en pruebas de alcance | 6 / 6 | **100 %** |
| `corpus_match` en preguntas no respondibles revisadas | 0 / 6 | **0 %** |
| Acierto del ID editorial para la pregunta histórica | 1 / 1 | **100 %** |

**Interpretación estricta:** localizar un documento relacionado no prueba que su apartado concreto esté bien posicionado. Asimismo, el 100 % en seis consultas de alcance solo acredita ausencia de respuesta editorial sustantiva en esos casos, no seguridad o abstención general.

## 2. Fallos y diagnósticos principales

- **Sesgo hacia navegación:** en 10 de 12 consultas documentales revisadas, el primer resultado es una sección de `index.md` y no el pasaje técnico inspeccionado.
- **Falsos negativos:** P1-02, P1-03, P1-08, P1-19 y P1-49 regresaron `insufficient` pese a disponer de un pasaje documental inspeccionado. La recuperación documental no se tradujo en una clase de cobertura adecuada.
- **Sección exacta ausente del top 5:** 12 de 12. No debe concluirse que las cinco recuperadas son irrelevantes sin revisar cada pasaje alternativo; la matriz inicial anota solo un anchor de referencia por pregunta.
- **Documento fuera del top 5:** 5 de 12. Entre los restantes 7, el documento correcto ocupa una de las primeras cinco posiciones, pero no la sección anotada.
- **Salvaguarda editorial conservada:** P1-34, «Para reservas en salud cuál de los métodos es más recomendado?», conserva `verified` y el ID `health-reserving-method-selection`.

## 3. Casos con pasaje documental inspeccionado

| ID | Resultado del motor | Rango de documento revisado | Rango del apartado revisado |
|---|---|---:|---:|
| P1-02 | `insufficient` | — | — |
| P1-03 | `insufficient` | — | — |
| P1-08 | `insufficient` | — | — |
| P1-10 | `corpus_match` | — | — |
| P1-15 | `corpus_match` | 2 | — |
| P1-19 | `insufficient` | — | — |
| P1-26 | `corpus_match` | 2 | — |
| P1-27 | `corpus_match` | 2 | — |
| P1-34 | `verified` | 3 | — |
| P1-40 | `corpus_match` | 3 | — |
| P1-45 | `corpus_match` | 1 | — |
| P1-49 | `insufficient` | 2 | — |

El reporte de CI contiene la **tabla para las 65 preguntas** y el archivo JSON completo con pregunta, estado, fuentes, ranking, puntajes, ruta/anchor, estado de revisión y códigos de error. El artifact de la ejecución se denomina **`ask-handbook-p1-benchmark`**.

## 4. Reproducción y compuertas

```bash
make qa-index
node tests/js/test_handbook_qa_benchmark.js
node scripts/evaluate_handbook_qa_benchmark.js --output-dir artifacts
```

El último comando genera `artifacts/handbook-qa-p1-report.json` y `artifacts/handbook-qa-p1-report.md`. La validación comprueba que las fuentes revisadas existan, sus anchors estén indexados y cada pasaje citado permanezca dentro del Markdown original. El workflow publica ambos artefactos y bloquea fusiones ante fallos de la suite, pero **no** impone aún un umbral numérico de Hit@k sin una matriz editorial suficientemente revisada.

## 5. Siguiente decisión técnica

Prioridad recomendada: **recuperación por pasajes con ranking menos dependiente de las páginas de navegación**, precedida de ampliar el conjunto de referencias relevantes por pregunta (pooling de evidencia). Evaluar un candidato como BM25 frente a este baseline sin cambiar silenciosamente las etiquetas; adoptar el nuevo algoritmo solo si mejora Hit@k/MRR sin empeorar abstención ni trazabilidad.

El siguiente ciclo debe revisar las 47 preguntas pendientes y las fuentes alternativas del top 5 antes de reclamar resultados representativos. La primera línea base es una fotografía diagnóstica, no una certificación final de precisión del Handbook.
