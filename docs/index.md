---
title: Health Insurance Reserving Handbook
subtitle: Manual técnico sobre IBNR y reservas actuariales en seguros de salud
author: Health Insurance Reserving Handbook
version: 1.0
chapter: Home
part: Repository Navigation
status: Draft
last_updated: 2026-07-14
language: es
jurisdiction: General con aplicaciones a Colombia
tags:
  - ibnr
  - reserving
  - health-insurance
  - loss-development
  - actuarial-science
prerequisites: []
related_chapters:
  - part-01-foundations/01-ibnr-and-reserving.md
  - part-02-classical-reserving/06-chain-ladder-method.md
  - part-07-colombia/29-colombia-health-reserving-methodologies.md
---

# Health Insurance Reserving Handbook

> Una referencia técnica, reproducible y orientada a decisiones sobre IBNR, reservas actuariales y desarrollo de reclamos en seguros de salud.

!!! info "Estado del proyecto"
    El handbook se encuentra en desarrollo activo. El inventario actual registra **24 capítulos con contenido construido**, pero la existencia de un archivo no implica que ya haya superado la revisión actuarial, estadística, editorial, de código y compilación exigida para una versión estable.

## Empiece aquí

El handbook está diseñado para distintos niveles de experiencia:

- **Si es nuevo en reserving**, comience con [IBNR and Reserving](part-01-foundations/01-ibnr-and-reserving.md) y continúe con la construcción de triángulos.
- **Si debe producir o revisar una estimación**, estudie primero [Chain Ladder](part-02-classical-reserving/06-chain-ladder-method.md), sus [diagnósticos](part-02-classical-reserving/07-chain-ladder-diagnostics.md) y los métodos de credibilidad.
- **Si necesita cuantificar incertidumbre**, consulte [Mack Chain Ladder](part-03-stochastic-reserving/08-mack-chain-ladder.md) y [Bootstrap Chain Ladder](part-03-stochastic-reserving/09-bootstrap-chain-ladder.md).
- **Si trabaja con modelos estadísticos o machine learning**, utilice los métodos clásicos como benchmarks antes de avanzar a [GLM](part-04-statistical-models/15-glm-for-loss-reserving.md), [GAM](part-04-statistical-models/16-gam-for-loss-reserving.md), Bayes o modelos basados en árboles.
- **Si trabaja en el sistema de salud colombiano**, comience por [Colombia Health Reserving Methodologies](part-07-colombia/29-colombia-health-reserving-methodologies.md), después de revisar los fundamentos.

## Propósito

Una reserva actuarial convierte información incompleta sobre reclamos observados en una estimación de obligaciones o costos que todavía no se han reconocido plenamente. En su forma más simple, para el periodo de origen (i):

\[
R_i = U_i - C_{i,k_i},
\]

donde (U_i) es el costo *ultimate* estimado y (C_{i,k_i}) es el importe acumulado observado a la madurez disponible (k_i).

La fórmula es sencilla; estimar sus componentes no lo es. En salud intervienen, entre otros factores:

- fecha de servicio, presentación, adjudicación y pago;
- elegibilidad y exposición de la población;
- comportamiento de proveedores y terceros administradores;
- autorizaciones, denegaciones, ajustes y reversos;
- cambios en beneficios, redes, contratos y prácticas de pago;
- tendencia médica, estacionalidad y efectos calendario;
- reclamos de alto costo y tratamientos prolongados;
- glosas, controversias y conciliaciones;
- incertidumbre de datos, parámetros, proceso y modelo.

El handbook conecta esos fenómenos operativos con la teoría actuarial, la inferencia estadística y la implementación reproducible.

```mermaid
flowchart LR
    A["Reclamos y exposición"] --> B["Triángulos y rezagos"]
    B --> C["Modelo actuarial"]
    C --> D["Reserva e incertidumbre"]
    D --> E["Validación y gobierno"]
```

## Alcance del handbook

El contenido integra cuatro perspectivas complementarias:

| Perspectiva | Preguntas principales |
|---|---|
| Actuarial | ¿Cuál es el *ultimate* esperado? ¿Qué parte permanece no reportada, no pagada o insuficientemente reservada? |
| Estadística | ¿Qué supuestos identifican el modelo? ¿Cómo se cuantifican la variabilidad y la incertidumbre predictiva? |
| Ciencia de datos | ¿Cómo se construyen, validan, comparan, explican y monitorean los modelos de forma reproducible? |
| Operación y regulación | ¿Qué significan los datos, contratos y procesos? ¿Qué debe documentarse y qué requisitos aplican al propósito de la estimación? |

Se cubren métodos determinísticos, estocásticos, estadísticos y de machine learning. Los modelos avanzados no se presentan como sustitutos automáticos del juicio actuarial: deben competir contra benchmarks transparentes y demostrar mejoras relevantes fuera de muestra.

## Navegación por partes

| Parte | Contenido | Punto de entrada | Estado actual |
|---:|---|---|---|
| I | Fundamentos, triángulos, rezagos y factores | [01 — IBNR and Reserving](part-01-foundations/01-ibnr-and-reserving.md) | Completed — content |
| II | Métodos clásicos y credibilidad | [06 — Chain Ladder](part-02-classical-reserving/06-chain-ladder-method.md) | Completed — content |
| III | Reserving estocástico e incertidumbre | [08 — Mack Chain Ladder](part-03-stochastic-reserving/08-mack-chain-ladder.md) | Completed — content |
| IV | GLM, GAM y modelos bayesianos | [15 — GLM for Loss Reserving](part-04-statistical-models/15-glm-for-loss-reserving.md) | Completed — content |
| V | Machine learning y modelos basados en árboles | [18 — Machine Learning for Loss Reserving](part-05-machine-learning/18-machine-learning-for-loss-reserving.md) | Completed — content |
| VI | Particularidades de seguros de salud | `part-06-health-specific/` | Planned |
| VII | Aplicaciones al sistema de salud colombiano | [21 — Colombia Health Reserving Methodologies](part-07-colombia/29-colombia-health-reserving-methodologies.md) | Completed — content |
| VIII | ASOP, validación y gobierno | `part-08-governance/` | Planned |
| IX | Implementaciones, pipelines y pruebas | `part-09-implementation/` | Planned |
| X | Casos de estudio integrales | `part-10-case-studies/` | Planned |

!!! warning "Numeración provisional"
    Los capítulos 08–14 conservan por ahora la numeración histórica del repositorio, aunque estén distribuidos entre las partes II y III. No deben renombrarse de forma aislada. La numeración global se estabilizará antes de la versión 1.0 para evitar romper navegación, referencias cruzadas e historial de Git.

## Rutas de aprendizaje

### Ruta 1 — Fundamentos de IBNR y triángulos

Recomendada para construir una base conceptual y operativa:

1. [IBNR and Reserving](part-01-foundations/01-ibnr-and-reserving.md)
2. [Triangle Construction](part-01-foundations/02-triangle-construction.md)
3. [Development Lags and Triangle Transformations](part-01-foundations/03-development-lags-and-triangle-transformations.md)
4. [Incremental vs. Cumulative Triangles](part-01-foundations/04-incremental-vs-cumulative-triangles.md)
5. [Age-to-Age Development Factors](part-01-foundations/05-age-to-age-development-factors.md)
6. [Chain Ladder Method](part-02-classical-reserving/06-chain-ladder-method.md)
7. [Chain Ladder Diagnostics](part-02-classical-reserving/07-chain-ladder-diagnostics.md)

### Ruta 2 — Selección de estimadores y credibilidad

Recomendada cuando los datos maduros, la expectativa inicial y la exposición contienen información distinta:

1. [Chain Ladder Method](part-02-classical-reserving/06-chain-ladder-method.md)
2. [Bornhuetter-Ferguson](part-02-classical-reserving/11-bornhuetter-ferguson.md)
3. [Benktander Method](part-02-classical-reserving/12-benktander-method.md)
4. [Cape Cod Method](part-02-classical-reserving/13-cape-cod-method.md)
5. [Classical Reserving Methods Comparison](part-02-classical-reserving/14-classical-reserving-methods-comparison.md)

### Ruta 3 — Incertidumbre predictiva

Recomendada cuando la decisión requiere error estándar, intervalos o distribución completa de resultados:

1. [Chain Ladder Diagnostics](part-02-classical-reserving/07-chain-ladder-diagnostics.md)
2. [Mack Chain Ladder](part-03-stochastic-reserving/08-mack-chain-ladder.md)
3. [Bootstrap Chain Ladder](part-03-stochastic-reserving/09-bootstrap-chain-ladder.md)
4. [Comparing Mack vs. Bootstrap](part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md)
5. [Bayesian Loss Reserving](part-04-statistical-models/17-bayesian-loss-reserving.md)

### Ruta 4 — Modelación estadística y machine learning

Recomendada para modelar no linealidades, efectos calendario o información granular:

1. [GLM for Loss Reserving](part-04-statistical-models/15-glm-for-loss-reserving.md)
2. [GAM for Loss Reserving](part-04-statistical-models/16-gam-for-loss-reserving.md)
3. [Bayesian Loss Reserving](part-04-statistical-models/17-bayesian-loss-reserving.md)
4. [Machine Learning for Loss Reserving](part-05-machine-learning/18-machine-learning-for-loss-reserving.md)
5. [Tree-Based Models for Loss Reserving](part-05-machine-learning/19-tree-based-models-for-loss-reserving.md)

Antes de seguir esta ruta, revise al menos los capítulos 01–07. Un modelo más complejo no es necesariamente más preciso, estable, explicable ni adecuado para la decisión.

### Ruta 5 — Reservas en el sistema de salud colombiano

Recomendada para EPS, IPS, medicina prepagada, supervisión, auditoría y consultoría:

1. [IBNR and Reserving](part-01-foundations/01-ibnr-and-reserving.md)
2. [Triangle Construction](part-01-foundations/02-triangle-construction.md)
3. [Colombia Health Reserving Methodologies](part-07-colombia/29-colombia-health-reserving-methodologies.md)
4. [Colombia Paid vs. Incurred Triangles](part-07-colombia/30-colombia-paid-vs-incurred-triangles.md)
5. [Colombia Data and Multistate Models](part-07-colombia/31-colombia-data-and-multistate-models.md)
6. [Colombia Glosas and Disputes](part-07-colombia/32-colombia-glosas-and-disputes.md)
7. [Colombia Capitation and Prospective Payments](part-07-colombia/33-colombia-capitation-and-prospective-payments.md)

Esta ruta distingue entre EPS, IPS, medicina prepagada, ARL y aseguradoras. También separa la mejor estimación actuarial, el mínimo regulatorio, la provisión contable, el margen prudencial, el costo médico y la obligación contractual.

## Orientación inicial para seleccionar una metodología

No existe un método universalmente superior. La selección depende del propósito, la madurez, la calidad de los datos, los cambios estructurales y la información externa disponible.

| Situación dominante | Punto de partida | Evidencia o diagnóstico requerido |
|---|---|---|
| Desarrollo relativamente estable y suficiente historia | Chain Ladder | Estabilidad de factores, calendario, mezcla, *outliers* y madurez |
| Periodos inmaduros y expectativa externa defendible | Bornhuetter-Ferguson | Calidad del *prior*, exposición, ELR y sensibilidad |
| Actualización gradual entre expectativa y experiencia | Benktander | Credibilidad, convergencia y coherencia con Chain Ladder |
| Exposición comparable entre periodos | Cape Cod | Homogeneidad de exposición y estabilidad del ELR implícito |
| Necesidad de error estándar bajo supuestos de Mack | Mack Chain Ladder | Supuestos condicionales, independencia y estructura de varianza |
| Necesidad de distribución predictiva simulada | Bootstrap | Residuos, proceso generador, cola, negativos y calibración |
| Efectos origen, desarrollo o calendario explícitos | GLM o GAM | Distribución, enlace, residuos, suavización y validación temporal |
| Información previa y jerarquías relevantes | Modelos bayesianos | Priors, convergencia, calibración posterior y sensibilidad |
| Datos granulares con relaciones complejas | Machine learning | Benchmark actuarial, *leakage*, validación temporal, explicabilidad y estabilidad |

La futura `methodology-selection-guide.md` ampliará esta tabla con árboles de decisión, criterios de materialidad y evidencia mínima por método.

## Cómo usar el repositorio en una valoración

Una aplicación profesional debería seguir, como mínimo, este ciclo:

1. **Definir el propósito:** mejor estimación, reporte financiero, solvencia, pricing, planeación, auditoría u otro uso.
2. **Delimitar la obligación:** población, cobertura, contrato, periodo de servicio, moneda y fecha de valoración.
3. **Entender los datos:** fuentes, fechas, estados del reclamo, exposición, transformaciones y reconciliación financiera.
4. **Construir un benchmark:** Chain Ladder, Bornhuetter-Ferguson, PMPM u otro método simple y defendible.
5. **Ejecutar diagnósticos:** estabilidad, madurez, cambios de mezcla, tendencia, calendario, extremos y calidad.
6. **Ajustar o segmentar:** solo cuando exista una razón económica, operativa o estadística verificable.
7. **Cuantificar incertidumbre:** distinguir riesgo de proceso, parámetros, modelo, datos y eventos no capturados.
8. **Comparar métodos:** explicar diferencias y evitar promedios mecánicos sin fundamento.
9. **Validar:** realizar *backtesting*, análisis de sensibilidad, revisión independiente y conciliaciones.
10. **Documentar y monitorear:** registrar decisiones, excepciones, versiones, limitaciones y señales de deterioro.

## Supuestos que no deben permanecer ocultos

La mayoría de los modelos de reserving depende, explícita o implícitamente, de que:

- los periodos históricos sean comparables con los periodos proyectados;
- la definición de reclamo y las reglas de adjudicación sean consistentes;
- los cambios de población, cobertura, red y contratos estén medidos o sean inmateriales;
- la inflación médica y la estacionalidad estén separadas de los rezagos de reporte o pago;
- los datos observados representen adecuadamente la obligación;
- los reclamos de alto costo no distorsionen indebidamente los patrones;
- la cola no observada pueda estimarse con evidencia suficiente;
- la incertidumbre comunicada sea coherente con la decisión.

Cuando esos supuestos no son defendibles, cambiar de algoritmo puede ser menos efectivo que corregir la segmentación, el modelo de datos, el periodo de experiencia o el diseño de la estimación.

## Calidad y reproducibilidad

Cada capítulo aspira a cumplir los siguientes criterios antes de considerarse terminado:

- front matter, nomenclatura y referencias cruzadas consistentes;
- teoría, intuición, supuestos y notación explícitos;
- ejemplo numérico reproducible;
- código con validaciones y manejo de errores cuando corresponda;
- diagnósticos, sensibilidad y limitaciones;
- checklist práctico y bibliografía comentada;
- revisión actuarial, estadística, editorial y de software;
- compilación con `mkdocs build --strict` sin errores ni enlaces rotos.

Los ejemplos deben usar datos sintéticos o datos públicos con autorización y trazabilidad. Ningún ejemplo constituye por sí mismo una nota técnica aprobada ni evidencia de idoneidad para otra entidad.

## Recursos editoriales en preparación

Los siguientes archivos forman parte de la infraestructura inmediata, pero todavía no se presentan como enlaces:

- `roadmap.md`: versiones, backlog, dependencias y criterios de completitud;
- `methodology-selection-guide.md`: selección de métodos y evidencia mínima;
- `glossary.md`: terminología actuarial, estadística y operativa;
- `bibliography.md`: bibliografía central comentada.

El inventario completo y la estructura objetivo del repositorio están disponibles en `README.md`, ubicado en la raíz del proyecto.

## Advertencia profesional

!!! danger "Uso responsable"
    Este material es educativo y técnico. No reemplaza el juicio profesional de un actuario calificado ni constituye asesoría jurídica, contable, regulatoria, financiera o de inversión. Las metodologías deben adaptarse al propósito, los datos, los contratos, la materialidad y la regulación aplicable. Toda afirmación regulatoria debe verificarse contra fuentes oficiales vigentes para la jurisdicción y fecha de valoración.

Un resultado puede ser matemáticamente correcto y aun así ser inadecuado si la obligación está mal definida, los datos no representan el riesgo, los supuestos dejaron de cumplirse o la incertidumbre relevante no fue comunicada.

## Checklist para comenzar

- [ ] Identifiqué el propósito y la fecha de valoración.
- [ ] Sé qué obligación, cobertura y población estoy estimando.
- [ ] Comprendo las fechas y estados disponibles en los reclamos.
- [ ] Puedo reconciliar los datos con una fuente financiera u operativa autorizada.
- [ ] Revisé los fundamentos antes de seleccionar un modelo avanzado.
- [ ] Definí un benchmark actuarial transparente.
- [ ] Documenté cambios de mezcla, tendencia, procesos y contratos.
- [ ] Separé estimación central, incertidumbre y margen prudencial.
- [ ] Planeé validación, revisión independiente y monitoreo.
- [ ] Verifiqué los requerimientos profesionales y regulatorios aplicables.

---

**Estado:** Draft  
**Versión de la página:** 1.0  
**Próximo archivo del plan:** `docs/roadmap.md`
