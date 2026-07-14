# Health Insurance Reserving Handbook

> Manual técnico, reproducible y orientado a la práctica sobre IBNR, reservas actuariales y desarrollo de siniestros en seguros de salud.

[![Project status: active development](https://img.shields.io/badge/status-active%20development-7b61ff)](#estado-del-proyecto)
[![Documentation: MkDocs Material](https://img.shields.io/badge/docs-MkDocs%20Material-526cfe)](#documentación-local-con-mkdocs)
[![Language: Spanish](https://img.shields.io/badge/language-español-2f855a)](#idioma-y-convenciones)

## Descripción

**Health Insurance Reserving Handbook** es un repositorio técnico sobre estimación de reservas en seguros de salud. Integra fundamentos actuariales, métodos determinísticos y estocásticos, modelos estadísticos y de machine learning, particularidades operativas de los reclamos médicos, aplicaciones al sistema de salud colombiano y prácticas de gobierno e implementación.

El objetivo es construir una referencia que pueda utilizarse simultáneamente como:

- libro técnico de nivel avanzado;
- manual de consulta para actuarios y analistas;
- guía práctica para construir y validar modelos de reservas;
- curso autocontenido sobre IBNR y *loss development*;
- repositorio reproducible de código, datos sintéticos y casos de estudio;
- marco de documentación, validación y gobierno de modelos.

El proyecto se encuentra en desarrollo activo. Los capítulos ya disponibles contienen el cuerpo metodológico inicial; la infraestructura de publicación, el bloque específico de salud, el gobierno actuarial, las implementaciones productivas y los casos integrales forman parte del trabajo pendiente.

## Objetivos

El handbook busca:

1. Explicar con rigor la naturaleza económica y actuarial de las reservas, incluidos IBNR, RBNS, IBNER y gastos de ajuste.
2. Desarrollar la teoría matemática, los supuestos y los diagnósticos de los principales métodos de *reserving*.
3. Conectar los modelos agregados de triángulos con datos transaccionales de reclamos, elegibilidad y exposición.
4. Adaptar los métodos generales a las particularidades de seguros de salud: alta frecuencia, rezagos cortos pero heterogéneos, adjudicación, reversos, farmacia, capitación, estacionalidad y reclamos de alto costo.
5. Tratar explícitamente la incertidumbre de proceso, de parámetros, de modelo y de datos.
6. Proporcionar implementaciones reproducibles en Python, R y SQL, acompañadas de validaciones y pruebas.
7. Establecer criterios de selección metodológica, documentación, revisión independiente y gobierno.
8. Desarrollar aplicaciones relevantes para el Sistema General de Seguridad Social en Salud de Colombia sin confundir metodología actuarial, requerimientos regulatorios, provisiones contables y obligaciones contractuales.

## Audiencia

El contenido está dirigido principalmente a:

- actuarios de salud, vida y seguros generales;
- analistas de IBNR, reservas técnicas, costos médicos y suficiencia de primas;
- científicos de datos y estadísticos que trabajan con reclamos de salud;
- profesionales de aseguradoras, EPS, IPS, medicina prepagada, ARL, reaseguradores y entidades supervisoras;
- auditores, validadores de modelos y responsables de riesgo;
- investigadores, docentes y estudiantes de posgrado;
- ingenieros de datos y desarrolladores de plataformas actuariales.

Se asume familiaridad básica con probabilidad, estadística, álgebra y programación. Los capítulos avanzados indican sus prerrequisitos y remiten a los fundamentos necesarios.

## Alcance

### Incluido

- construcción y transformación de triángulos;
- factores de desarrollo y métodos Chain Ladder;
- Bornhuetter-Ferguson, Benktander y Cape Cod;
- Mack y Bootstrap Chain Ladder;
- GLM, GAM y modelos bayesianos;
- machine learning con benchmarks actuariales;
- triángulos pagados e incurridos;
- exposición, PMPM, factores de completitud y curvas de *runout*;
- tendencia médica, estacionalidad y efectos calendario;
- frecuencia-severidad, supervivencia y modelos multiestado;
- glosas, disputas, capitación y pagos prospectivos;
- calidad de datos, validación, documentación y gobierno;
- implementaciones y casos de estudio con datos sintéticos.

### Fuera de alcance

El repositorio no pretende:

- producir una única metodología válida para todas las entidades y propósitos;
- sustituir el juicio de un actuario calificado;
- interpretar de manera definitiva contratos, normas o estándares contables;
- publicar datos personales, clínicos o financieros reales;
- presentar modelos de machine learning como sustitutos automáticos de métodos actuariales transparentes;
- afirmar cumplimiento regulatorio sin una revisión específica de jurisdicción, fecha, entidad y propósito.

## Principios editoriales y técnicos

Cada capítulo busca ser original, autocontenido, auditable y compatible con GitHub y MkDocs Material. Según la naturaleza del tema, debe contener:

- objetivos de aprendizaje;
- definiciones, intuición y notación;
- supuestos y fundamento matemático;
- derivaciones y ejemplos numéricos completos;
- implementaciones en Python, R o SQL cuando correspondan;
- diagnósticos, validación y análisis de sensibilidad;
- limitaciones y riesgos de uso;
- implicaciones prácticas y de gobierno;
- checklist de aplicación;
- bibliografía comentada y referencias cruzadas.

Los ejemplos utilizan datos sintéticos. Todo modelo avanzado debe compararse con un benchmark actuarial apropiado. La mejor estimación actuarial, el mínimo regulatorio, la provisión contable y el margen prudencial se tratan como conceptos relacionados, pero no intercambiables.

## Estado del proyecto

**Etapa actual:** desarrollo previo a la versión `0.1`.

El inventario de transferencia del proyecto registra **24 capítulos con contenido construido**. Antes de considerarlos terminados para una versión estable, deben superar la revisión técnica, editorial, de código, enlaces y compilación definida por el proyecto.

### Leyenda de estado

| Estado | Significado |
|---|---|
| **Completed — content** | El archivo y su contenido base existen según el inventario del proyecto; puede requerir QA final. |
| **In progress** | Es parte de la fase activa de infraestructura o redacción. |
| **Planned** | Está definido en el roadmap, pero todavía no debe asumirse como disponible. |

### Estado por parte

| Parte | Tema | Estado | Archivos con contenido | Próximo foco |
|---:|---|---|---:|---|
| 1 | Foundations | Completed — content | 5 | Revisión cruzada y compilación |
| 2 | Classical Reserving | Completed — content | 6 | Revisión cruzada y pruebas |
| 3 | Stochastic Reserving | Completed — content | 3 | Validación numérica y pruebas |
| 4 | Statistical Models | Completed — content | 3 | Reproducibilidad de código |
| 5 | Machine Learning | Completed — content | 2 | Benchmarks y gobierno |
| 6 | Health-specific | Planned | 0 | Capítulo 20 y factores de completitud |
| 7 | Colombia | Completed — content | 5 | Ampliación y verificación regulatoria |
| 8 | Governance | Planned | 0 | ASOP y gobierno de modelos |
| 9 | Implementation | Planned | 0 | SQL, Python, R, pipelines y tests |
| 10 | Case Studies | Planned | 0 | Casos sintéticos end-to-end |

## Contenido disponible

### Parte 1 — Foundations

| Capítulo | Archivo | Temas principales |
|---:|---|---|
| 01 | [IBNR and Reserving](docs/part-01-foundations/01-ibnr-and-reserving.md) | IBNR, RBNS, IBNER, ALAE, ULAE y marco de reservas |
| 02 | [Triangle Construction](docs/part-01-foundations/02-triangle-construction.md) | Construcción desde reclamos, fechas, rezagos y validaciones |
| 03 | [Development Lags and Triangle Transformations](docs/part-01-foundations/03-development-lags-and-triangle-transformations.md) | Tiempo de origen, desarrollo, calendario y transformaciones |
| 04 | [Incremental vs. Cumulative Triangles](docs/part-01-foundations/04-incremental-vs-cumulative-triangles.md) | Operadores de acumulación, diferencias e implicaciones estadísticas |
| 05 | [Age-to-Age Development Factors](docs/part-01-foundations/05-age-to-age-development-factors.md) | *Link ratios*, selección de factores, CDF y cola |

### Parte 2 — Classical Reserving

| Capítulo | Archivo | Temas principales |
|---:|---|---|
| 06 | [Chain Ladder Method](docs/part-02-classical-reserving/06-chain-ladder-method.md) | Supuestos, factores, *ultimate*, IBNR e implementación |
| 07 | [Chain Ladder Diagnostics](docs/part-02-classical-reserving/07-chain-ladder-diagnostics.md) | Estabilidad, madurez, calendario, *outliers* y sensibilidad |
| 11 | [Bornhuetter-Ferguson](docs/part-02-classical-reserving/11-bornhuetter-ferguson.md) | *Prior*, ELR, proporción no reportada y credibilidad |
| 12 | [Benktander Method](docs/part-02-classical-reserving/12-benktander-method.md) | Actualización iterativa, forma cerrada y convergencia |
| 13 | [Cape Cod Method](docs/part-02-classical-reserving/13-cape-cod-method.md) | Exposición, ELR estimado, *ultimate* e IBNR |
| 14 | [Classical Reserving Methods Comparison](docs/part-02-classical-reserving/14-classical-reserving-methods-comparison.md) | Comparación, credibilidad y matriz de selección |

### Parte 3 — Stochastic Reserving

| Capítulo | Archivo | Temas principales |
|---:|---|---|
| 08 | [Mack Chain Ladder](docs/part-03-stochastic-reserving/08-mack-chain-ladder.md) | MSEP, varianza de proceso, parámetros e intervalos |
| 09 | [Bootstrap Chain Ladder](docs/part-03-stochastic-reserving/09-bootstrap-chain-ladder.md) | ODP, residuos, simulación, VaR, TVaR y *backtesting* |
| 10 | [Comparing Mack vs. Bootstrap](docs/part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md) | Supuestos, distribuciones, incertidumbre y selección |

> **Nota sobre numeración:** la ubicación actual de los capítulos 08–14 refleja la evolución histórica del repositorio. La numeración definitiva se revisará antes de la versión 1.0. No se deben renombrar archivos de forma aislada, porque hacerlo rompería referencias cruzadas y navegación.

### Parte 4 — Statistical Models

| Capítulo | Archivo | Temas principales |
|---:|---|---|
| 15 | [GLM for Loss Reserving](docs/part-04-statistical-models/15-glm-for-loss-reserving.md) | Familia exponencial, Poisson, Gamma, Tweedie, MLE e IRLS |
| 16 | [GAM for Loss Reserving](docs/part-04-statistical-models/16-gam-for-loss-reserving.md) | *Splines*, penalización, EDF, REML, GCV y *concurvity* |
| 17 | [Bayesian Loss Reserving](docs/part-04-statistical-models/17-bayesian-loss-reserving.md) | Priors, posterior predictivo, MCMC, HMC y jerarquías |

### Parte 5 — Machine Learning

| Capítulo | Archivo | Temas principales |
|---:|---|---|
| 18 | [Machine Learning for Loss Reserving](docs/part-05-machine-learning/18-machine-learning-for-loss-reserving.md) | Features, validación temporal, métricas, XAI y gobierno |
| 19 | [Tree-Based Models for Loss Reserving](docs/part-05-machine-learning/19-tree-based-models-for-loss-reserving.md) | Árboles, Random Forest, boosting, XGBoost, LightGBM, CatBoost y SHAP |

### Parte 7 — Colombia

| Capítulo | Archivo | Temas principales |
|---:|---|---|
| 21 | [Colombia Health Reserving Methodologies](docs/part-07-colombia/29-colombia-health-reserving-methodologies.md) | EPS, IPS, reservas, contratos, datos y workflow mensual |
| 22 | [Colombia Paid vs. Incurred Triangles](docs/part-07-colombia/30-colombia-paid-vs-incurred-triangles.md) | Pagado, incurrido, glosas, Munich Chain Ladder y reconciliación |
| 23 | [Colombia Data and Multistate Models](docs/part-07-colombia/31-colombia-data-and-multistate-models.md) | Modelo de datos, eventos, supervivencia y estados |
| 24 | [Colombia Glosas and Disputes](docs/part-07-colombia/32-colombia-glosas-and-disputes.md) | Devoluciones, glosas, conciliación, reaperturas y pisos regulatorios |
| 25 | [Colombia Capitation and Prospective Payments](docs/part-07-colombia/33-colombia-capitation-and-prospective-payments.md) | Capitación, PGP, riesgo compartido, liquidación y giro directo |

## Estructura del repositorio

La estructura objetivo separa documentación, código, datos sintéticos, pruebas y recursos de publicación:

```text
.
├── README.md
├── mkdocs.yml                         # In progress
├── LICENSE                            # Planned; pendiente de decisión
├── CONTRIBUTING.md                    # Planned
├── CHANGELOG.md                       # Planned
├── CITATION.cff                       # Planned
├── requirements-docs.txt              # Planned
├── docs/
│   ├── index.md                       # In progress
│   ├── roadmap.md                     # In progress
│   ├── methodology-selection-guide.md # Planned
│   ├── glossary.md                    # Planned
│   ├── bibliography.md                # Planned
│   ├── part-01-foundations/
│   ├── part-02-classical-reserving/
│   ├── part-03-stochastic-reserving/
│   ├── part-04-statistical-models/
│   ├── part-05-machine-learning/
│   ├── part-06-health-specific/
│   ├── part-07-colombia/
│   ├── part-08-governance/
│   ├── part-09-implementation/
│   ├── part-10-case-studies/
│   └── appendices/
├── python/                             # Planned
├── R/                                  # Planned
├── sql/                                # Planned
├── notebooks/                          # Planned
├── data/
│   ├── raw/                            # Datos sintéticos o públicos autorizados
│   ├── processed/
│   └── synthetic/
├── figures/                            # Planned
├── tests/                              # Planned
├── schemas/                            # Planned
├── bibliography/                      # Planned
└── .github/
    ├── workflows/                      # Planned
    └── ISSUE_TEMPLATE/                 # Planned
```

La estructura objetivo no implica que todos los archivos o directorios estén disponibles en la versión actual.

## Rutas de aprendizaje

### Ruta 1 — Fundamentos de IBNR

Recomendada para lectores que comienzan en reserving:

1. [IBNR and Reserving](docs/part-01-foundations/01-ibnr-and-reserving.md)
2. [Triangle Construction](docs/part-01-foundations/02-triangle-construction.md)
3. [Development Lags and Triangle Transformations](docs/part-01-foundations/03-development-lags-and-triangle-transformations.md)
4. [Incremental vs. Cumulative Triangles](docs/part-01-foundations/04-incremental-vs-cumulative-triangles.md)
5. [Age-to-Age Development Factors](docs/part-01-foundations/05-age-to-age-development-factors.md)
6. [Chain Ladder Method](docs/part-02-classical-reserving/06-chain-ladder-method.md)
7. [Chain Ladder Diagnostics](docs/part-02-classical-reserving/07-chain-ladder-diagnostics.md)

### Ruta 2 — Selección de métodos y credibilidad

Para actuarios que deben comparar estimaciones y dependencia del *prior*:

1. [Chain Ladder Method](docs/part-02-classical-reserving/06-chain-ladder-method.md)
2. [Bornhuetter-Ferguson](docs/part-02-classical-reserving/11-bornhuetter-ferguson.md)
3. [Benktander Method](docs/part-02-classical-reserving/12-benktander-method.md)
4. [Cape Cod Method](docs/part-02-classical-reserving/13-cape-cod-method.md)
5. [Classical Reserving Methods Comparison](docs/part-02-classical-reserving/14-classical-reserving-methods-comparison.md)

### Ruta 3 — Incertidumbre y reserving estocástico

Para cuantificar error de predicción y distribuciones de resultados:

1. [Chain Ladder Diagnostics](docs/part-02-classical-reserving/07-chain-ladder-diagnostics.md)
2. [Mack Chain Ladder](docs/part-03-stochastic-reserving/08-mack-chain-ladder.md)
3. [Bootstrap Chain Ladder](docs/part-03-stochastic-reserving/09-bootstrap-chain-ladder.md)
4. [Comparing Mack vs. Bootstrap](docs/part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md)
5. [Bayesian Loss Reserving](docs/part-04-statistical-models/17-bayesian-loss-reserving.md)

### Ruta 4 — Modelos estadísticos y machine learning

Para estadísticos y científicos de datos:

1. [GLM for Loss Reserving](docs/part-04-statistical-models/15-glm-for-loss-reserving.md)
2. [GAM for Loss Reserving](docs/part-04-statistical-models/16-gam-for-loss-reserving.md)
3. [Bayesian Loss Reserving](docs/part-04-statistical-models/17-bayesian-loss-reserving.md)
4. [Machine Learning for Loss Reserving](docs/part-05-machine-learning/18-machine-learning-for-loss-reserving.md)
5. [Tree-Based Models for Loss Reserving](docs/part-05-machine-learning/19-tree-based-models-for-loss-reserving.md)

Esta ruta no elimina la necesidad de dominar los capítulos 01–07. Los modelos avanzados deben evaluarse contra benchmarks actuariales y mediante validación temporal fuera de muestra.

### Ruta 5 — Aplicación al sistema de salud colombiano

Para profesionales de EPS, IPS, supervisión y consultoría:

1. [IBNR and Reserving](docs/part-01-foundations/01-ibnr-and-reserving.md)
2. [Triangle Construction](docs/part-01-foundations/02-triangle-construction.md)
3. [Colombia Health Reserving Methodologies](docs/part-07-colombia/29-colombia-health-reserving-methodologies.md)
4. [Colombia Paid vs. Incurred Triangles](docs/part-07-colombia/30-colombia-paid-vs-incurred-triangles.md)
5. [Colombia Data and Multistate Models](docs/part-07-colombia/31-colombia-data-and-multistate-models.md)
6. [Colombia Glosas and Disputes](docs/part-07-colombia/32-colombia-glosas-and-disputes.md)
7. [Colombia Capitation and Prospective Payments](docs/part-07-colombia/33-colombia-capitation-and-prospective-payments.md)

La regulación colombiana cambia y debe verificarse siempre contra fuentes oficiales vigentes para la fecha de valoración.

## Cómo navegar el contenido actual

1. Seleccione una ruta de aprendizaje o una parte temática.
2. Revise los prerrequisitos declarados en el *front matter* de cada capítulo.
3. Ejecute los ejemplos con datos sintéticos y concilie los resultados con las tablas del texto.
4. Lea las secciones de supuestos, diagnósticos y limitaciones antes de usar una metodología.
5. Utilice los checklists finales como base de revisión, no como certificación automática de idoneidad.
6. Consulte las referencias cruzadas para distinguir conceptos cercanos, como pagado versus incurrido o costo médico versus obligación contractual.

La portada de MkDocs, el roadmap navegable, el glosario, la bibliografía central y la guía de selección metodológica se incorporarán durante las versiones `0.1` y `0.2`. Hasta entonces, este README funciona como índice principal.

## Documentación local con MkDocs

La publicación está diseñada para usar [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). La configuración `mkdocs.yml` y el archivo `requirements-docs.txt` forman parte de la fase de infraestructura `0.1`.

Una vez que esos archivos estén disponibles, el flujo previsto será:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt
mkdocs serve
```

En Windows PowerShell, active el entorno con:

```powershell
.venv\Scripts\Activate.ps1
```

Para generar el sitio estático y tratar advertencias como errores:

```bash
mkdocs build --strict
```

No se debe asumir que la documentación compila hasta que `mkdocs.yml`, las dependencias y todos los enlaces hayan sido validados en el repositorio completo.

## Roadmap resumido

| Versión | Objetivo | Entregables principales | Estado |
|---|---|---|---|
| `0.1` | Repositorio navegable | README, MkDocs, portada, roadmap, navegación y archivos raíz | In progress |
| `0.2` | Bloque health-specific | Especificidades de salud, completion factors, PMPM, tendencia, estacionalidad, alto costo, frecuencia-severidad y supervivencia | Planned |
| `0.3` | Gobierno y estándares | ASOP 5, 23, 41 y 56, validación, documentación y revisión independiente | Planned |
| `0.4` | Implementación reproducible | SQL, Python, R, datos sintéticos, notebooks, tests y CI | Planned |
| `0.5` | Colombia ampliado | Alto costo, incapacidades, ADRES, IPS, medicina prepagada y caso integral | Planned |
| `1.0` | Handbook estable | Contenido completo, código validado, casos end-to-end, publicación, licencia y citación | Planned |

### Prioridad inmediata

El orden de desarrollo vigente es:

1. completar la infraestructura de la versión `0.1`;
2. crear `docs/part-06-health-specific/21-health-insurance-reserving-specificities.md`;
3. completar factores de desarrollo específicos de salud, exposición PMPM, tendencia y estacionalidad;
4. desarrollar gobierno y estándares profesionales;
5. separar y probar las implementaciones de producción;
6. construir casos de estudio integrales.

La numeración global definitiva debe resolverse antes de ampliar simultáneamente las partes 6 y 7, para evitar identificadores duplicados.

## Definición de terminado

Un capítulo solo se considera terminado para una versión estable cuando:

- tiene *front matter* y nombre consistentes;
- declara objetivos, prerrequisitos y notación;
- documenta supuestos y fundamento metodológico;
- incluye ejemplo, validación, limitaciones y checklist;
- contiene referencias y enlaces relativos correctos;
- no contradice otros capítulos;
- el código asociado es reproducible y está probado;
- ha superado revisión actuarial, estadística y editorial;
- compila en MkDocs sin errores ni enlaces rotos.

La existencia de un archivo no implica por sí sola que cumpla esta definición.

## Contribución

El proyecto aún está definiendo su proceso formal de contribución. Mientras se publica `CONTRIBUTING.md`, una propuesta debe:

1. limitarse a un problema, capítulo o cambio claramente identificado;
2. conservar la convención `NN-nombre-descriptivo-en-minusculas.md`;
3. mantener la notación y los términos definidos por el handbook;
4. distinguir evidencia, juicio actuarial y requerimiento regulatorio;
5. incluir fuentes primarias para afirmaciones normativas o profesionales;
6. usar datos sintéticos o datos públicos con licencia compatible;
7. añadir pruebas cuando modifique código o resultados numéricos;
8. ejecutar `mkdocs build --strict` antes de solicitar revisión;
9. documentar supuestos, limitaciones y posibles efectos en otros capítulos;
10. evitar renumeraciones o cambios masivos de rutas sin una decisión de arquitectura.

Las contribuciones metodológicas deben explicar qué información podría refutar o cambiar la recomendación propuesta. La complejidad adicional requiere evidencia de mejora fuera de muestra, estabilidad y utilidad actuarial.

## Citación

`CITATION.cff` está planeado para la versión `0.1`. Mientras se define la autoría y la versión citable, puede utilizarse provisionalmente:

```text
Health Insurance Reserving Handbook Project. (2026).
Health Insurance Reserving Handbook [Repositorio técnico en desarrollo].
Versión consultada y fecha de acceso.
```

No utilice esta referencia provisional como sustituto de las fuentes originales citadas en cada capítulo.

## Licencias

La licencia todavía no ha sido confirmada. La propuesta de trabajo es:

- **código:** MIT License;
- **documentación:** Creative Commons Attribution 4.0 International (CC BY 4.0).

Hasta que los archivos de licencia sean aprobados y publicados, no debe asumirse que el contenido o el código pueden reutilizarse bajo esos términos.

## Idioma y convenciones

El idioma principal actual es español, conservando en inglés los términos actuariales que son estándar en la literatura cuando su traducción pueda introducir ambigüedad. Los nombres de archivo se mantienen en inglés, en minúsculas y separados por guiones.

Convenciones principales:

- origen: \(i\);
- desarrollo: \(j\);
- incremental: \(X_{i,j}\);
- acumulado: \(C_{i,j} = \sum_{h=0}^{j} X_{i,h}\);
- *ultimate*: \(U_i\);
- reserva: \(R_i = U_i - C_{i,k_i}\);
- pagado: \(P_{i,j}\);
- incurrido: \(I_{i,j} = P_{i,j} + O_{i,j}\);
- exposición: \(E_i\);
- meses-miembro: \(MM_i\).

Las ecuaciones se escriben en LaTeX; los diagramas usan Mermaid cuando mejoran la comprensión; el código Python incluye *type hints* y docstrings; R prioriza flujos reproducibles; SQL usa CTE, funciones de ventana y validaciones explícitas.

## Advertencia profesional y regulatoria

> Este material es educativo y técnico. No reemplaza el juicio profesional de un actuario calificado ni constituye asesoría jurídica, contable, regulatoria, financiera o de inversión. Las metodologías deben adaptarse al propósito de la valoración, los datos, los contratos, la materialidad, la regulación y las circunstancias de cada entidad. Toda afirmación regulatoria debe verificarse contra fuentes oficiales vigentes.

Los resultados de un modelo pueden ser matemáticamente correctos y, aun así, no ser adecuados para una decisión. Entre los riesgos relevantes se encuentran errores y cambios en los datos, inestabilidad de patrones de desarrollo, inflación médica, modificaciones de beneficios, cambios operativos, sesgo de selección, litigios, glosas, reclamos de alto costo, dependencia entre periodos y error de modelo.

## Contacto y gobierno del proyecto

Los canales de contacto, responsables de mantenimiento, URL definitiva del repositorio, política de versiones y proceso de revisión se publicarán cuando se complete la infraestructura de gobierno del proyecto.

---

**Estado:** desarrollo activo  
**Última actualización:** 2026-07-14  
**Próximo entregable:** `mkdocs.yml`
