# Ask the Handbook · Sprint 3 · Fase P1 — Benchmark actuarial de recuperación (borrador)

## Estado, propósito y trazabilidad

- **Estado:** propuesta de anotación; **no es aún un benchmark validado por expertos** ni un resultado de desempeño.
- **Dependencia de integración:** PR [#23](https://github.com/jaforero/health-insurance-reserving-handbook/pull/23), que debe fusionarse tras establecer y verificar la protección de `main`.
- **Tamaño inicial:** **65 preguntas**, de las cuales **53** requieren evidencia documental y **12** evalúan la capacidad de abstenerse o declarar límites.
- **Base de selección:** nombres y rutas de `docs/**/*.md` existentes y verificados en el árbol de `main` del repositorio (2026-11-07); no se han inventado capítulos ni rutas.
- **Alcance:** evaluación de recuperación y presentación de fuentes en el asistente local **no generativo**; no estima automáticamente validez clínica, normativa ni actuarial de nuevas respuestas generadas.

**Advertencia sobre las etiquetas:** las rutas que se muestran abajo son **documentos candidatos inferidos de la temática del título**, no *ground truth* confirmado. Ninguna observación debe computar una métrica oficial hasta que un revisor compruebe el pasaje o anchor exacto, la suficiencia de la fuente, las formulaciones alternativas y el resultado esperado. En especial, «abstenerse» significa no presentar una conclusión particular sin evidencia; no equivale a afirmar que el motor actual utilice exactamente el estado `insufficient`.

## 1. Casos de recuperación: 53 consultas

| ID | Dominio | Pregunta candidata | Documento candidato |
|---|---|---|---|
| P1-01 | foundations | ¿En qué se diferencian IBNR e IBNER al estimar obligaciones de siniestros? | `part-01-foundations/01-ibnr-and-reserving.md` |
| P1-02 | foundations | ¿Cuáles son las etapas para construir un triángulo de desarrollo a partir de siniestros? | `part-01-foundations/02-triangle-construction.md` |
| P1-03 | foundations | ¿Qué diferencia hay entre rezago de reporte y rezago de pago? | `part-01-foundations/03-development-lags-and-triangle-transformations.md` |
| P1-04 | foundations | ¿Cuándo conviene usar triángulos incrementales en lugar de acumulados? | `part-01-foundations/04-incremental-vs-cumulative-triangles.md` |
| P1-05 | foundations | ¿Cómo se interpretan los factores de desarrollo edad a edad? | `part-01-foundations/05-age-to-age-development-factors.md` |
| P1-06 | foundations | ¿Cómo pueden afectar los pagos negativos y los reversos a los acumulados? | `part-01-foundations/04-incremental-vs-cumulative-triangles.md` |
| P1-07 | foundations | ¿Cómo cambia el triángulo cuando usamos periodo de servicio frente a periodo de pago? | `part-01-foundations/03-development-lags-and-triangle-transformations.md` |
| P1-08 | classical | ¿Cuáles son los supuestos necesarios para utilizar Chain Ladder? | `part-02-classical-reserving/06-chain-ladder-method.md` |
| P1-09 | classical | ¿Qué diagnósticos deben revisarse antes de confiar en Chain Ladder? | `part-02-classical-reserving/07-chain-ladder-diagnostics.md` |
| P1-10 | classical | ¿Cómo debe construirse un prior independiente para Bornhuetter-Ferguson? | `part-02-classical-reserving/11-bornhuetter-ferguson.md` |
| P1-11 | classical | ¿En qué se distingue Benktander de Bornhuetter-Ferguson? | `part-02-classical-reserving/12-benktander-method.md` |
| P1-12 | classical | ¿Cómo utiliza Cape Cod la exposición y las pérdidas observadas? | `part-02-classical-reserving/13-cape-cod-method.md` |
| P1-13 | classical | ¿Cómo comparar Chain Ladder, Bornhuetter-Ferguson y Cape Cod? | `part-02-classical-reserving/14-classical-reserving-methods-comparison.md` |
| P1-14 | classical | ¿Qué riesgos presenta aplicar Chain Ladder a meses de desarrollo inmaduros? | `part-02-classical-reserving/07-chain-ladder-diagnostics.md` |
| P1-15 | stochastic | ¿Qué tipo de incertidumbre estima Mack Chain Ladder? | `part-03-stochastic-reserving/08-mack-chain-ladder.md` |
| P1-16 | stochastic | ¿Cómo se obtiene una distribución de reservas con Bootstrap Chain Ladder? | `part-03-stochastic-reserving/09-bootstrap-chain-ladder.md` |
| P1-17 | stochastic | ¿Cuáles son las diferencias de supuestos entre Mack y Bootstrap? | `part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md` |
| P1-18 | stochastic | ¿Por qué una estimación puntual de reserva no describe toda la incertidumbre? | `part-03-stochastic-reserving/08-mack-chain-ladder.md` |
| P1-19 | statistical-models | ¿Cómo se aplica un GLM a la estimación de reservas de siniestros? | `part-04-statistical-models/15-glm-for-loss-reserving.md` |
| P1-20 | statistical-models | ¿Qué aporta un GAM frente a un GLM en patrones no lineales de desarrollo? | `part-04-statistical-models/16-gam-for-loss-reserving.md` |
| P1-21 | statistical-models | ¿Cómo puede incorporarse información previa mediante un modelo bayesiano de reservas? | `part-04-statistical-models/17-bayesian-loss-reserving.md` |
| P1-22 | machine-learning | ¿Cuáles son las limitaciones de los modelos de machine learning para reserving? | `part-05-machine-learning/18-machine-learning-for-loss-reserving.md` |
| P1-23 | machine-learning | ¿Cómo se utilizan árboles de decisión en modelos predictivos de siniestros? | `part-05-machine-learning/19-tree-based-models-for-loss-reserving.md` |
| P1-24 | machine-learning | ¿Qué precauciones plantea deep learning para la estimación de reservas? | `part-05-machine-learning/20-deep-learning-for-loss-reserving.md` |
| P1-25 | statistical-models | ¿Qué estructura de datos necesita un GLM de reserving? | `part-04-statistical-models/15-glm-for-loss-reserving.md` |
| P1-26 | health-specific | ¿Qué particularidades diferencian las reservas en salud de las reservas P&C? | `part-06-health-specific/21-health-insurance-reserving-specificities.md` |
| P1-27 | health-specific | ¿Cómo afecta el ciclo de vida del claim de salud a los rezagos operativos? | `part-06-health-specific/22-health-claim-lifecycle-and-operational-lags.md` |
| P1-28 | health-specific | ¿Cómo se relacionan exposición, utilización y severidad en un seguro de salud? | `part-06-health-specific/23-health-exposure-utilization-and-severity.md` |
| P1-29 | health-specific | ¿Cómo afectan la inflación médica y la estacionalidad a las reservas? | `part-06-health-specific/24-health-medical-trend-seasonality-and-shocks.md` |
| P1-30 | health-specific | ¿Cómo influyen el ajuste de riesgo y la morbilidad en las proyecciones? | `part-06-health-specific/25-health-risk-adjustment-and-morbidity.md` |
| P1-31 | health-specific | ¿Qué efecto pueden tener los contratos con prestadores en los pagos y obligaciones? | `part-06-health-specific/26-health-provider-contracts-and-payment-models.md` |
| P1-32 | health-specific | ¿Cómo tratar auditorías, denegaciones y controversias de reclamaciones médicas? | `part-06-health-specific/27-health-claims-audit-denials-and-disputes.md` |
| P1-33 | health-specific | ¿Cuáles controles de gobierno conviene aplicar al proceso de reserving en salud? | `part-06-health-specific/28-health-reserving-governance-controls-and-reporting.md` |
| P1-34 | health-specific | Para reservas en salud cuál de los métodos es más recomendado? | `part-06-health-specific/21-health-insurance-reserving-specificities.md` |
| P1-35 | health-specific | ¿Cómo usar indicadores PMPM para analizar exposición y costo de salud? | `part-06-health-specific/23-health-exposure-utilization-and-severity.md` |
| P1-36 | health-specific | ¿Qué riesgos introducen los shocks de morbilidad y utilización en las proyecciones? | `part-06-health-specific/24-health-medical-trend-seasonality-and-shocks.md` |
| P1-37 | colombia | ¿Cómo se adaptan las metodologías de reservas en salud al contexto colombiano? | `part-07-colombia/29-colombia-health-reserving-methodologies.md` |
| P1-38 | colombia | ¿Cómo comparar triángulos pagados e incurridos en Colombia? | `part-07-colombia/30-colombia-paid-vs-incurred-triangles.md` |
| P1-39 | colombia | ¿Cómo modelar estados de reclamaciones y transiciones en datos colombianos? | `part-07-colombia/31-colombia-data-and-multistate-models.md` |
| P1-40 | colombia | ¿Cómo afectan las glosas y controversias al flujo de pagos? | `part-07-colombia/32-colombia-glosas-and-disputes.md` |
| P1-41 | colombia | ¿Qué diferencias introduce la capitación frente a pagos por evento? | `part-07-colombia/33-colombia-capitation-and-prospective-payments.md` |
| P1-42 | colombia | ¿Cómo se relacionan UPC, morbilidad y ajuste de riesgo en Colombia? | `part-07-colombia/34-colombia-upc-risk-adjustment-and-morbidity.md` |
| P1-43 | colombia | ¿Qué desafíos presentan las condiciones de alto costo y la agrupación de riesgos? | `part-07-colombia/35-colombia-high-cost-conditions-and-risk-pooling.md` |
| P1-44 | colombia | ¿Qué controles de calidad de datos son relevantes para RIPS y FEV? | `part-07-colombia/36-colombia-rips-fev-data-quality-and-validation.md` |
| P1-45 | colombia | ¿Qué distinción debe hacerse entre IBNR y provisiones técnicas en Colombia? | `part-07-colombia/37-colombia-ibnr-technical-provisions-and-regulatory-reporting.md` |
| P1-46 | colombia | ¿Cómo se conectan solvencia, liquidez y pruebas de estrés para aseguramiento en salud? | `part-07-colombia/38-colombia-solvency-liquidity-and-stress-testing.md` |
| P1-47 | colombia | ¿Cómo estructurar escenarios de reforma del sistema de salud colombiano? | `part-07-colombia/39-colombia-scenario-planning-and-reform-roadmap.md` |
| P1-48 | colombia | ¿Cómo convertir metodologías de reserva en un plan práctico de implementación? | `part-07-colombia/40-colombia-implementation-playbook-and-templates.md` |
| P1-49 | english | How do paid and incurred claim triangles differ in health insurance? | `examples/02-paid-vs-incurred-health-demo.md` |
| P1-50 | english | When is a monthly health triangle suitable for a development method? | `examples/03-monthly-health-triangles-demo.md` |
| P1-51 | english | How can simulated health claims triangles be used for learning? | `examples/01-simulated-health-triangles-demo.md` |
| P1-52 | english | How should an actuary interpret the uncertainty from Mack Chain Ladder? | `part-03-stochastic-reserving/08-mack-chain-ladder.md` |
| P1-53 | english | How does Bornhuetter-Ferguson address immature accident periods? | `part-02-classical-reserving/11-bornhuetter-ferguson.md` |

## 2. Controles de abstención y límites: 12 consultas

| ID | Grupo | Pregunta de control | Motivo provisional para abstenerse |
|---|---|---|---|
| P1-54 | no-input | ¿Cuál es el IBNR exacto de mi EPS si no he aportado triángulos ni datos? | sin datos particulares aportados |
| P1-55 | no-input | ¿Qué importe exacto debo registrar mañana como reserva en mi organización? | sin cartera, cierre ni datos |
| P1-56 | no-input | ¿Cuánto se pagará exactamente por mis siniestros pendientes el 30 de noviembre de 2026? | resultado futuro individual no observable |
| P1-57 | no-input | ¿Qué porcentaje exacto de mis claims resultará glosado en diciembre? | sin información particular ni base de proyección |
| P1-58 | no-input | ¿Cuáles son los nombres de los pacientes con mayores reclamaciones de mi EPS? | datos personales no disponibles |
| P1-59 | no-input | ¿Qué saldo exacto tiene la cuenta de reservas de una empresa privada a esta hora? | sin acceso a información financiera privada |
| P1-60 | external-dynamic | ¿Qué nueva circular publicó hoy la Superintendencia Nacional de Salud sobre IBNR? | requiere fuente externa vigente |
| P1-61 | external-dynamic | ¿Cuál es la tasa de cambio USD/COP actual para valorar reservas? | requiere datos externos vigentes |
| P1-62 | not-in-corpus | ¿Qué establece el supuesto Decreto 99999 de 2026 para reservas de salud? | fuente normativa no verificada |
| P1-63 | not-in-corpus | ¿Cómo calcular una reserva usando un método llamado Chain Ladder cuántico? | concepto no respaldado |
| P1-64 | not-in-corpus | ¿Cuál es la contraseña del servidor que aloja el Handbook? | secreto no incluido ni divulgable |
| P1-65 | not-in-corpus | ¿Quién ganó el último partido de una liga de fútbol de esta semana? | consulta ajena al corpus actuarial |

## 3. Protocolo de anotación editorial

Para cada pregunta de recuperación, los evaluadores deben completar en un fixture estructurado: `id`, `query`, `language`, `topic`, `answerable`, `relevant_sections` (lista de pares `path#anchor`), `prohibited_sources` si aplica, `expected_behavior`, `rationale`, `reviewer`, `review_date` y `review_status`. La anotación debe distinguir:

1. **Soporte directo:** al menos un pasaje contiene material suficiente para la intención solicitada.
2. **Soporte parcial:** el corpus contiene el concepto, pero no la inferencia, cuantificación o dato particular requerido; el resultado debe advertir límites y no simular una respuesta completa.
3. **No soportada / fuera de alcance:** no hay evidencia suficiente, se requieren datos propios del usuario, o la consulta está fuera del corpus.

Separar explícitamente `retrieval_hit` (recuperación de un pasaje pertinente) de `answer_correctness` (exactitud de una respuesta editorial), y de `answerability` (suficiencia del corpus para responder). Una coincidencia de palabras no basta para «relevante».

## 4. Evaluación reproducible propuesta

**Unidad de evaluación:** cada pregunta aprobada por un revisor. **Población de métricas:** únicamente las etiquetas en estado `approved`; reportar las preguntas sin revisión y excluirlas del denominador, sin imputar resultados.

- **Recall@1, Recall@3 y Recall@5 (evidencia):** proporción de consultas con evidencia cuyo top-`k` contiene al menos una sección fuente anotada como relevante. El motor actual expone `findRelatedSections(query, sectionIndex, limit, context)` y permite evaluar `k=5` sin depender del panel, que muestra tres resultados.
- **MRR@5:** media de `1/rank` para la primera sección relevante entre las cinco primeras, y cero si no aparece.
- **Tasa de abstención correcta:** preguntas etiquetadas como no respondibles en las que el motor evita una respuesta sustantiva no sustentada. No basta comparar códigos de estado; revisar `verified`, `probable` y `corpus_match` y sus fuentes.
- **Falsos positivos de recuperación:** casos en los que `corpus_match` se presenta sin pasaje que responda sustancialmente la pregunta.
- **Cobertura y trazabilidad:** proporción de fuentes y anchors referidos existentes, actualidad de sus versiones y coherencia entre pregunta y fuente.
- **Desempeño técnico:** tamaño de los JSON, tiempo p50/p95 por consulta y comportamiento en móviles, medidos en un entorno especificado.

**Política de aceptación:** conservar como compuerta estricta los ocho casos críticos de P0. La suite ampliada P1 comienza como **reporte de diagnóstico no bloqueante** hasta revisar los 65 casos, fijar umbrales sustentados y aprobar la conversión a check obligatorio. No inventar métricas ni declarar una mejora por volumen de indexación.

## 5. Secuencia de ejecución P1

1. Verificar fusión de PR #23 y política obligatoria en `main`.
2. Validar documentalmente los 53 casos con candidatos de fuente, incluyendo anchors, y revisar los 12 casos de abstención.
3. Publicar el fixture de referencia versionado con etiquetas y estado de revisión.
4. Ejecutar el motor actual sin cambios y publicar el *baseline* de Recall@k, MRR, abstención y falsos positivos, con denominadores y errores observados.
5. Analizar errores por dominio y lengua; proponer recuperaciones por pasaje, ranking BM25 y contexto de grafo **solo si** su beneficio supera la complejidad y los riesgos de falsos positivos.
6. Acordar umbrales mínimos de CI después del análisis; entonces hacerlos exigibles con la protección de rama.

## 6. Criterios de terminado

El benchmark no está terminado con 65 filas. Estará terminado cuando cada caso tenga evidencia revisada o abstención justificada, las consultas puedan ejecutarse automáticamente, el reporte incluya sus métricas calculadas sin casos omitidos silenciosamente y todos los enlaces/anchors estén verificados. La prueba adversarial y la sensibilidad a variaciones de lenguaje deben mantenerse en cada actualización.
