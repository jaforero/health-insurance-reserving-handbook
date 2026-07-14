PROJECT-HANDOFF.md
---
title: Health Insurance Reserving Handbook — Estado del proyecto y guía de continuidad
subtitle: Documento de transferencia para continuar el repositorio en un nuevo chat
author: Health Insurance Reserving Handbook Project
version: 1.0
status: Active
last_updated: 2026-07-14
language: es
---

# Health Insurance Reserving Handbook

## Estado del proyecto y guía de continuidad

Este documento resume el trabajo ya construido, la estructura actual del repositorio, las convenciones editoriales adoptadas, los capítulos disponibles, los vacíos identificados y el orden recomendado para continuar el proyecto en una conversación nueva.

Su propósito es funcionar como **documento de transferencia**. Debe proporcionarse al inicio de un nuevo chat para evitar inconsistencias de nomenclatura, alcance, profundidad técnica, estructura editorial y referencias cruzadas.

---

# 1. Nombre del proyecto

## Nombre principal

**Health Insurance Reserving Handbook**

## Descripción

Repositorio técnico sobre:

- IBNR;
- reservas actuariales;
- triángulos de desarrollo;
- métodos determinísticos;
- métodos estocásticos;
- modelos estadísticos;
- machine learning;
- aplicaciones específicas a seguros de salud;
- adaptación al sistema de salud colombiano;
- gobierno, validación e implementación de modelos.

## Objetivo

Construir un repositorio GitHub que pueda funcionar simultáneamente como:

- libro técnico;
- manual actuarial;
- guía práctica;
- curso avanzado;
- referencia matemática;
- repositorio de código;
- marco de validación;
- guía de implementación industrial;
- referencia para reserving en salud en Estados Unidos y Colombia.

---

# 2. Alcance metodológico

El repositorio integra cuatro perspectivas:

1. **Actuarial**
   - IBNR;
   - ultimate losses;
   - reservas pendientes;
   - paid and incurred triangles;
   - completion factors;
   - credibilidad;
   - incertidumbre.

2. **Estadística**
   - GLM;
   - GAM;
   - modelos bayesianos;
   - supervivencia;
   - frecuencia-severidad;
   - modelos multiestado.

3. **Ciencia de datos**
   - machine learning;
   - modelos basados en árboles;
   - explicabilidad;
   - validación temporal;
   - automatización.

4. **Operación y regulación**
   - calidad de datos;
   - documentación;
   - ASOP;
   - regulación colombiana;
   - glosas;
   - capitación;
   - pagos prospectivos;
   - FEV-RIPS;
   - conciliaciones;
   - reservas técnicas.

---

# 3. Estado actual de la estructura

La estructura actual del directorio `docs/` es:

```text
docs/
├── part-01-foundations/
│   ├── 01-ibnr-and-reserving.md
│   ├── 02-triangle-construction.md
│   ├── 03-development-lags-and-triangle-transformations.md
│   ├── 04-incremental-vs-cumulative-triangles.md
│   └── 05-age-to-age-development-factors.md
│
├── part-02-classical-reserving/
│   ├── 06-chain-ladder-method.md
│   ├── 07-chain-ladder-diagnostics.md
│   ├── 11-bornhuetter-ferguson.md
│   ├── 12-benktander-method.md
│   ├── 13-cape-cod-method.md
│   └── 14-classical-reserving-methods-comparison.md
│
├── part-03-stochastic-reserving/
│   ├── 08-mack-chain-ladder.md
│   ├── 09-bootstrap-chain-ladder.md
│   └── 10-comparing-mack-vs-bootstrap.md
│
├── part-04-statistical-models/
│   ├── 15-glm-for-loss-reserving.md
│   ├── 16-gam-for-loss-reserving.md
│   └── 17-bayesian-loss-reserving.md
│
├── part-05-machine-learning/
│   ├── 18-machine-learning-for-loss-reserving.md
│   └── 19-tree-based-models-for-loss-reserving.md
│
├── part-06-health-specific/
│
├── part-07-colombia/
│   ├── 29-colombia-health-reserving-methodologies.md
│   ├── 30-colombia-paid-vs-incurred-triangles.md
│   ├── 31-colombia-data-and-multistate-models.md
│   ├── 32-colombia-glosas-and-disputes.md
│   └── 33-colombia-capitation-and-prospective-payments.md
│
├── part-08-governance/
├── part-09-implementation/
├── part-10-case-studies/
└── appendices/
```

También se propuso la siguiente estructura técnica en la raíz:

```text
python/
R/
sql/
notebooks/
data/
├── raw/
├── processed/
└── synthetic/
figures/
tests/
schemas/
bibliography/
.github/
├── workflows/
└── ISSUE_TEMPLATE/
```

---

# 4. Convención de nombres

Todos los archivos deben cumplir:

```text
NN-nombre-descriptivo-en-minusculas.md
```

## Reglas

- usar dos dígitos para el número;
- usar guiones medios;
- no usar guiones bajos;
- no usar mayúsculas;
- no usar tildes;
- no usar espacios;
- no abreviar excesivamente;
- mantener el nombre razonablemente corto;
- usar el título completo dentro del front matter.

## Ejemplos correctos

```text
01-ibnr-and-reserving.md
09-bootstrap-chain-ladder.md
15-glm-for-loss-reserving.md
32-colombia-glosas-and-disputes.md
```

## Ejemplos incorrectos

```text
01_ibnr.md
10-Comparing-Mack-vs-Bootstrap.md
Capitulo 15.md
21-colombian-health-reserving-methodolog.md
```

---

# 5. Contenido ya construido

## Parte 1 — Foundations

### 01 — IBNR and Reserving

Archivo:

```text
docs/part-01-foundations/01-ibnr-and-reserving.md
```

Contenido:

- definición de reserving;
- definición de IBNR;
- componentes de reservas;
- RBNS;
- IBNER;
- ALAE;
- ULAE;
- marco matemático;
- datos;
- validación;
- gobierno.

---

### 02 — Triangle Construction

Archivo:

```text
docs/part-01-foundations/02-triangle-construction.md
```

Contenido:

- construcción desde claims;
- fechas relevantes;
- accident period;
- service date;
- payment date;
- development lag;
- incremental triangle;
- cumulative triangle;
- tipos de triángulos;
- validaciones;
- ejemplos SQL, Python y R.

---

### 03 — Development Lags and Triangle Transformations

Archivo:

```text
docs/part-01-foundations/03-development-lags-and-triangle-transformations.md
```

Contenido:

- accident time;
- development time;
- calendar time;
- relación APC;
- coordenadas triangulares;
- transformación incremental-acumulado;
- efectos calendario;
- validaciones.

---

### 04 — Incremental vs. Cumulative Triangles

Archivo:

```text
docs/part-01-foundations/04-incremental-vs-cumulative-triangles.md
```

Contenido:

- operadores de acumulación;
- operadores de diferencia;
- representación matricial;
- invertibilidad;
- preservación de información;
- correlación acumulada;
- ventajas de cada representación;
- uso por metodología.

---

### 05 — Age-to-Age Development Factors

Archivo:

```text
docs/part-01-foundations/05-age-to-age-development-factors.md
```

Contenido:

- link ratios;
- volume-weighted factors;
- arithmetic mean;
- geometric mean;
- median;
- trimmed mean;
- selección de factores;
- CDF;
- tail factor;
- validaciones.

---

# 6. Métodos clásicos construidos

## 06 — Chain Ladder

```text
docs/part-02-classical-reserving/06-chain-ladder-method.md
```

Incluye:

- supuestos;
- factores;
- ultimate;
- IBNR;
- interpretación estadística;
- limitaciones;
- aplicaciones en salud;
- Python y R.

---

## 07 — Chain Ladder Diagnostics

```text
docs/part-02-classical-reserving/07-chain-ladder-diagnostics.md
```

Incluye:

- estabilidad de link ratios;
- madurez;
- efectos calendario;
- inflación;
- outliers;
- sensibilidad;
- leave-one-year-out;
- validación operativa.

---

## 11 — Bornhuetter-Ferguson

```text
docs/part-02-classical-reserving/11-bornhuetter-ferguson.md
```

Incluye:

- prior;
- ELR;
- expected ultimate;
- percent reported;
- percent unreported;
- fórmula BF;
- comparación con Chain Ladder;
- aplicaciones en salud.

---

## 12 — Benktander

```text
docs/part-02-classical-reserving/12-benktander-method.md
```

Incluye:

- actualización iterativa;
- credibilidad;
- convergencia a Chain Ladder;
- forma recursiva;
- forma cerrada;
- implementación.

---

## 13 — Cape Cod

```text
docs/part-02-classical-reserving/13-cape-cod-method.md
```

Incluye:

- ELR estimado;
- exposición;
- premium;
- reported percentage;
- ultimate;
- IBNR;
- comparación con BF.

---

## 14 — Comparison of Classical Reserving Methods

```text
docs/part-02-classical-reserving/14-classical-reserving-methods-comparison.md
```

Incluye:

- Chain Ladder;
- BF;
- Benktander;
- Cape Cod;
- Mack;
- Bootstrap;
- matriz de selección;
- continuum de credibilidad;
- workflow.

---

# 7. Métodos estocásticos construidos

## 08 — Mack Chain Ladder

```text
docs/part-03-stochastic-reserving/08-mack-chain-ladder.md
```

Incluye:

- hipótesis de Mack;
- varianza condicional;
- process variance;
- parameter variance;
- MSEP;
- standard error;
- prediction intervals;
- CV;
- implementación.

---

## 09 — Bootstrap Chain Ladder

```text
docs/part-03-stochastic-reserving/09-bootstrap-chain-ladder.md
```

Incluye:

- ODP;
- fitted values;
- Pearson residuals;
- residual adjustment;
- pseudo-triangles;
- parameter risk;
- process risk;
- simulación;
- VaR;
- TVaR;
- tratamiento de negativos;
- tail;
- implementación Python y R;
- backtesting.

---

## 10 — Comparing Mack vs. Bootstrap

```text
docs/part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md
```

Incluye:

- comparación analítica vs. simulación;
- supuestos;
- outputs;
- intervalos;
- distribución;
- VaR;
- TVaR;
- decisión metodológica.

---

# 8. Modelos estadísticos construidos

## 15 — GLM for Loss Reserving

```text
docs/part-04-statistical-models/15-glm-for-loss-reserving.md
```

Incluye:

- exponential family;
- link functions;
- Poisson;
- Gamma;
- Tweedie;
- accident effects;
- development effects;
- calendar effects;
- MLE;
- IRLS;
- diagnósticos;
- Python y R.

---

## 16 — GAM for Loss Reserving

```text
docs/part-04-statistical-models/16-gam-for-loss-reserving.md
```

Incluye:

- smooth functions;
- splines;
- penalización;
- EDF;
- REML;
- GCV;
- concurvity;
- modelación no lineal;
- implementación.

---

## 17 — Bayesian Loss Reserving

```text
docs/part-04-statistical-models/17-bayesian-loss-reserving.md
```

Incluye:

- prior;
- likelihood;
- posterior;
- posterior predictive;
- MCMC;
- HMC;
- NUTS;
- modelos jerárquicos;
- credible intervals;
- PyMC;
- Stan;
- brms.

---

# 9. Machine Learning construido

## 18 — Machine Learning for Loss Reserving

```text
docs/part-05-machine-learning/18-machine-learning-for-loss-reserving.md
```

Incluye:

- supervised learning;
- feature engineering;
- train-test split;
- validación temporal;
- loss functions;
- metrics;
- XAI;
- governance;
- health applications.

---

## 19 — Tree-Based Models

```text
docs/part-05-machine-learning/19-tree-based-models-for-loss-reserving.md
```

Incluye:

- decision trees;
- recursive partitioning;
- random forest;
- bagging;
- gradient boosting;
- XGBoost;
- LightGBM;
- CatBoost;
- SHAP;
- tuning;
- monitoring.

---

# 10. Capítulos Colombia construidos

## 21 — Colombian Health Reserving Methodologies

```text
docs/part-07-colombia/29-colombia-health-reserving-methodologies.md
```

Incluye:

- particularidades del sistema;
- EPS;
- IPS;
- reservas conocidas;
- reservas no conocidas;
- glosas;
- capitación;
- contratos;
- adaptación de métodos clásicos;
- GLM;
- supervivencia;
- modelos multiestado;
- regulación;
- nota técnica;
- workflow mensual.

---

## 22 — Paid vs. Incurred Triangles in Colombia

```text
docs/part-07-colombia/30-colombia-paid-vs-incurred-triangles.md
```

Incluye:

- paid triangles;
- incurred triangles;
- diferencias económicas;
- obligaciones conocidas;
- glosas;
- reservas de caso;
- Munich Chain Ladder;
- Berquist-Sherman;
- reconciliación;
- selección por segmento.

---

## 23 — Data and Multistate Models

```text
docs/part-07-colombia/31-colombia-data-and-multistate-models.md
```

Incluye:

- modelo de datos;
- prestaciones;
- facturas;
- líneas;
- eventos;
- estados;
- supervivencia;
- competing risks;
- modelos multiestado;
- reserva por cuenta;
- SQL;
- Python;
- R.

---

## 24 — Glosas and Disputes

```text
docs/part-07-colombia/32-colombia-glosas-and-disputes.md
```

Incluye:

- devolución;
- glosa;
- respuesta;
- conciliación;
- causal;
- probabilidad de reconocimiento;
- proporción reconocida;
- tiempo hasta resolución;
- pagos parciales;
- reaperturas;
- modelos actuariales;
- pisos regulatorios.

---

## 25 — Capitation and Prospective Payments

```text
docs/part-07-colombia/33-colombia-capitation-and-prospective-payments.md
```

Incluye:

- capitación;
- PGP;
- paquetes;
- pagos por caso;
- riesgo compartido;
- corredores;
- stop-loss;
- población;
- exposición;
- devengo;
- costo médico vs. obligación contractual;
- liquidación;
- giro directo;
- RIPS-FEV.

---

# 11. Vacío de numeración

Actualmente no existe el capítulo 20.

Debe crearse como puente entre modelos generales y Colombia:

```text
docs/part-06-health-specific/21-health-insurance-reserving-specificities.md
```

## Contenido esperado

- diferencias entre health y P&C;
- service date;
- paid date;
- adjudication date;
- medical claims;
- pharmacy;
- dental;
- vision;
- behavioral health;
- provider lag;
- eligibility;
- claim reversals;
- benefit design;
- coordination of benefits;
- medical trend;
- seasonality;
- PMPM;
- completion factors;
- risk adjustment;
- capitation;
- large claims;
- paid vs. incurred;
- short-tail vs. long-tail health liabilities.

Este es el siguiente capítulo prioritario.

---

# 12. Infraestructura todavía no creada

Los siguientes archivos raíz están pendientes:

```text
README.md
mkdocs.yml
LICENSE
CONTRIBUTING.md
CHANGELOG.md
CITATION.cff
.gitignore
.editorconfig
.pre-commit-config.yaml
requirements-docs.txt
```

Los siguientes archivos de documentación están pendientes:

```text
docs/index.md
docs/roadmap.md
docs/methodology-selection-guide.md
docs/glossary.md
docs/bibliography.md
```

---

# 13. Contenido pendiente por parte

## Parte 6 — Health-specific

Carpeta:

```text
docs/part-06-health-specific/
```

Capítulos recomendados:

```text
21-health-insurance-reserving-specificities.md
26-completion-factors-and-runout-curves.md
27-pmpm-exposure-and-membership.md
28-medical-trend.md
29-seasonality-and-calendar-effects.md
30-large-claims-and-high-cost-claimants.md
31-frequency-severity-reserving.md
32-survival-models-for-claim-development.md
```

## Prioridad conceptual

1. capítulo 20;
2. completion factors;
3. PMPM;
4. medical trend;
5. seasonality;
6. large claims;
7. frequency-severity;
8. survival.

---

# 14. Parte de gobierno pendiente

Carpeta:

```text
docs/part-08-governance/
```

Capítulos recomendados:

```text
33-asop-5-incurred-health-and-disability-claims.md
34-asop-23-data-quality.md
35-asop-41-actuarial-communications.md
36-asop-56-modeling.md
37-model-governance-and-validation.md
38-actuarial-documentation-and-peer-review.md
39-regulatory-and-accounting-crosswalk.md
```

## Objetivo

Establecer:

- requisitos de documentación;
- calidad de datos;
- model governance;
- validación;
- comunicación;
- peer review;
- desviaciones;
- disclosure;
- audit trail;
- control de versiones.

---

# 15. Parte de implementación pendiente

Carpeta:

```text
docs/part-09-implementation/
```

Capítulos sugeridos:

```text
40-sql-for-triangle-construction.md
41-python-reserving-implementation.md
42-r-reserving-implementation.md
43-reproducible-reserving-pipelines.md
```

Directorios relacionados:

```text
python/
R/
sql/
notebooks/
tests/
schemas/
```

## Requisitos

Cada implementación debe incluir:

- validaciones;
- type hints;
- manejo de errores;
- tests;
- reproducibilidad;
- semillas;
- configuración;
- reconciliación;
- outputs estandarizados.

---

# 16. Casos de estudio pendientes

Carpeta:

```text
docs/part-10-case-studies/
```

Capítulos recomendados:

```text
44-case-study-chain-ladder.md
45-case-study-stochastic-reserving.md
46-case-study-credibility-reserving.md
47-case-study-health-completion-factors.md
48-case-study-colombia-eps.md
49-case-study-colombia-glosas.md
50-end-to-end-health-reserving.md
```

Cada caso debería incluir:

1. contexto;
2. datos sintéticos;
3. modelo de datos;
4. SQL;
5. Python;
6. R;
7. validación;
8. resultados;
9. sensibilidad;
10. conclusión actuarial.

---

# 17. Capítulos Colombia pendientes

La parte Colombia puede continuar con:

```text
26-colombia-high-cost-and-complex-cases.md
27-colombia-incapacity-reserving.md
28-colombia-direct-payments-and-adres.md
29-colombia-ips-revenue-and-receivables.md
30-colombia-prepaid-medicine-reserving.md
31-colombia-regulatory-crosswalk.md
32-colombia-end-to-end-case-study.md
```

La numeración deberá revisarse para evitar conflicto con la Parte 6.

## Recomendación de numeración

No continuar numerando partes distintas con números repetidos.

Dos alternativas:

### Alternativa A — Numeración global

```text
20–27 Health-specific
28–35 Colombia
36–42 Governance
43–46 Implementation
47–53 Case studies
```

### Alternativa B — Prefijos por parte

```text
06-01-health-specificities.md
07-01-colombia-methodologies.md
```

La alternativa recomendada es **numeración global**, porque ya existe y es más fácil para lectores.

---

# 18. Renumeración recomendada antes de ampliar

Para evitar conflictos futuros, se propone el siguiente mapa:

## Parte 1

```text
01–05
```

## Parte 2

```text
06–11
```

## Parte 3

```text
12–14
```

## Parte 4

```text
15–17
```

## Parte 5

```text
18–19
```

## Parte 6

```text
20–27
```

## Parte 7

```text
28–39
```

## Parte 8

```text
40–46
```

## Parte 9

```text
47–50
```

## Parte 10

```text
51–57
```

Sin embargo, no es obligatorio renumerar inmediatamente. Puede mantenerse la numeración actual y ajustar cuando se estabilice el índice.

---

# 19. Plantilla editorial obligatoria

Cada capítulo debe usar front matter uniforme:

```yaml
---
title:
subtitle:
author: Health Insurance Reserving Handbook
version: 1.0
chapter:
part:
status: Draft
last_updated:
language:
jurisdiction:
tags:
prerequisites:
related_chapters:
---
```

## Estructura mínima

```text
# Título

> Frase introductoria

## Advertencia de alcance

## Objetivos de aprendizaje

## Contenido

# 1. Introducción

# 2. Motivación

# 3. Definiciones

# 4. Fundamento matemático

# 5. Metodología

# 6. Ejemplo

# 7. Implementación

# 8. Diagnósticos

# 9. Validación

# 10. Limitaciones

# 11. Aplicación práctica

# 12. Gobierno

# 13. Checklist

# 14. Conclusiones

# Referencias

# Próximo capítulo
```

No todos los capítulos requieren exactamente los mismos títulos, pero deben conservar:

- objetivos;
- teoría;
- fórmulas;
- supuestos;
- ejemplo;
- implementación;
- validación;
- limitaciones;
- checklist;
- referencias.

---

# 20. Convenciones matemáticas

## Origen

\[
i
\]

## Desarrollo

\[
j
\]

## Incremental

\[
X_{i,j}
\]

## Acumulado

\[
C_{i,j}
=
\sum_{h=0}^{j}X_{i,h}
\]

## Factor de desarrollo

\[
f_j
=
\frac{
\sum_i C_{i,j+1}
}{
\sum_i C_{i,j}
}
\]

## Ultimate

\[
U_i
\]

## Reserva

\[
R_i
=
U_i-C_{i,k_i}
\]

## Pagado

\[
P_{i,j}
\]

## Incurrido

\[
I_{i,j}
=
P_{i,j}+O_{i,j}
\]

## Exposición

\[
E_i
\]

## Member months

\[
MM_i
\]

Debe conservarse esta notación salvo que exista una razón explícita para cambiarla.

---

# 21. Convenciones de código

## Python

- type hints;
- docstrings;
- manejo de errores;
- `random_state`;
- funciones pequeñas;
- reproducibilidad;
- `pandas`;
- `numpy`;
- `statsmodels`;
- `chainladder`;
- `scikit-learn`;
- `PyMC` cuando aplique.

## R

- tidyverse;
- `ChainLadder`;
- `mgcv`;
- `survival`;
- `mstate`;
- `brms`;
- funciones reproducibles;
- semillas.

## SQL

- SQL genérico o indicar dialecto;
- CTE;
- window functions;
- validaciones;
- comentarios;
- evitar consultas no reproducibles.

---

# 22. Reglas de consistencia

El nuevo chat debe respetar:

1. no cambiar nombres de archivos sin justificarlo;
2. no crear capítulos duplicados;
3. no mezclar inglés y español dentro de un mismo capítulo sin razón;
4. conservar fórmulas y notación;
5. mantener referencias cruzadas;
6. usar paths relativos;
7. mantener enfoque en reserving;
8. no introducir ML sin benchmark actuarial;
9. diferenciar regulación de metodología;
10. diferenciar mejor estimación de mínimo regulatorio;
11. diferenciar reserva contractual de costo médico;
12. diferenciar EPS de IPS;
13. usar datos sintéticos;
14. no copiar normas completas;
15. verificar regulación vigente antes de afirmar requisitos normativos.

---

# 23. Infraestructura GitHub recomendada

## README.md

Debe incluir:

- propósito;
- audiencia;
- alcance;
- estructura;
- estado;
- instalación;
- navegación;
- roadmap;
- contribución;
- licencia;
- disclaimer.

## docs/index.md

Debe ser la portada del sitio MkDocs.

## mkdocs.yml

Debe usar MkDocs Material.

## docs/roadmap.md

Debe documentar versiones y backlog.

## docs/methodology-selection-guide.md

Debe incluir árboles de decisión.

## docs/glossary.md

Debe centralizar definiciones.

## docs/bibliography.md

Debe contener bibliografía comentada.

---

# 24. Roadmap recomendado

## Versión 0.1

Objetivo: repositorio navegable.

- normalización de nombres;
- organización por partes;
- README;
- index;
- mkdocs;
- roadmap;
- LICENSE;
- gitignore;
- navegación;
- publicación local.

## Versión 0.2

Objetivo: completar health-specific.

- capítulo 20;
- completion factors;
- PMPM;
- trend;
- seasonality;
- large claims;
- frequency-severity;
- survival.

## Versión 0.3

Objetivo: gobierno y ASOP.

- ASOP 5;
- ASOP 23;
- ASOP 41;
- ASOP 56;
- model governance;
- peer review;
- regulatory crosswalk.

## Versión 0.4

Objetivo: implementación.

- SQL;
- Python;
- R;
- tests;
- datasets;
- notebooks;
- CI.

## Versión 0.5

Objetivo: Colombia completo.

- alto costo;
- incapacidades;
- ADRES;
- IPS;
- medicina prepagada;
- caso integral.

## Versión 1.0

Objetivo: handbook estable.

- todos los capítulos;
- código validado;
- datasets sintéticos;
- casos end-to-end;
- sitio GitHub Pages;
- citación;
- licencia;
- revisión editorial.

---

# 25. Prioridad inmediata

El siguiente trabajo debe ejecutarse en este orden:

## Paso 1

Crear:

```text
README.md
```

## Paso 2

Crear:

```text
mkdocs.yml
```

## Paso 3

Crear:

```text
docs/index.md
```

## Paso 4

Crear:

```text
docs/roadmap.md
```

## Paso 5

Crear:

```text
docs/methodology-selection-guide.md
docs/glossary.md
docs/bibliography.md
```

## Paso 6

Crear:

```text
docs/part-06-health-specific/21-health-insurance-reserving-specificities.md
```

No continuar con más modelos de machine learning antes de completar el bloque health-specific y la infraestructura editorial.

---

# 26. Prompt maestro para un nuevo chat

Copiar el siguiente texto junto con este documento:

```text
Actúa como un comité editorial y técnico compuesto por:

- un actuario de salud con experiencia en IBNR y reserving;
- un Fellow de la Society of Actuaries;
- un Fellow de la Casualty Actuarial Society;
- un estadístico especializado en GLM, GAM, supervivencia y modelos bayesianos;
- un científico de datos experto en Python, R y SQL;
- un arquitecto de documentación técnica para GitHub y MkDocs;
- un especialista en regulación colombiana de salud.

Estamos construyendo el repositorio “Health Insurance Reserving Handbook”.

Usa el documento PROJECT-HANDOFF.md como fuente principal para entender:

- estructura actual;
- archivos existentes;
- capítulos construidos;
- convenciones de nombres;
- plantilla editorial;
- notación;
- backlog;
- prioridades;
- reglas de consistencia.

Reglas obligatorias:

1. No dupliques capítulos existentes.
2. No cambies nombres ni numeración sin explicar el impacto.
3. Respeta la estructura por partes.
4. Cada entrega debe corresponder a un archivo concreto del repositorio.
5. Indica siempre la ruta exacta del archivo.
6. Usa Markdown compatible con GitHub y MkDocs Material.
7. Usa LaTeX para ecuaciones.
8. Usa Mermaid cuando aporte claridad.
9. Incluye teoría, intuición, supuestos, metodología, ejemplo, implementación, validación, limitaciones, gobierno, checklist y referencias cuando corresponda.
10. Para regulación vigente, verifica fuentes oficiales antes de afirmar requisitos.
11. Distingue reserva actuarial, reserva regulatoria, provisión contable y margen prudencial.
12. En Colombia, diferencia EPS, IPS, medicina prepagada, ARL y aseguradoras.
13. No uses machine learning como sustituto automático de métodos actuariales.
14. Mantén benchmarks como Chain Ladder, BF, Mack o PMPM.
15. Conserva la notación matemática del proyecto.
16. Evita copiar extensamente normas o ASOP; produce explicaciones originales.
17. Cuando se solicite un archivo, entrega únicamente el contenido completo listo para guardar.
18. Mantén referencias cruzadas con rutas relativas.
19. Usa datos sintéticos en ejemplos.
20. Prioriza reproducibilidad, auditabilidad y validación.

Prioridad actual:

1. README.md
2. mkdocs.yml
3. docs/index.md
4. docs/roadmap.md
5. docs/methodology-selection-guide.md
6. docs/glossary.md
7. docs/bibliography.md
8. docs/part-06-health-specific/21-health-insurance-reserving-specificities.md

Antes de crear un archivo, revisa su relación con los capítulos existentes y evita inconsistencias editoriales.
```

---

# 27. Prompt para crear README.md

```text
Usando PROJECT-HANDOFF.md, crea el archivo README.md completo para la raíz del repositorio.

Debe incluir:

- nombre y descripción del proyecto;
- objetivos;
- alcance;
- audiencia;
- estado del repositorio;
- tabla de partes y capítulos;
- estructura de carpetas;
- rutas de aprendizaje;
- instrucciones para navegar;
- instrucciones para ejecutar MkDocs;
- roadmap resumido;
- contribución;
- citación;
- licencias;
- disclaimer actuarial y regulatorio;
- enlaces relativos correctos.

No inventes capítulos como si ya estuvieran terminados. Diferencia claramente:

- Completed;
- In progress;
- Planned.

Entrega únicamente el contenido del archivo README.md listo para guardar.
```

---

# 28. Prompt para crear mkdocs.yml

```text
Usando PROJECT-HANDOFF.md y la estructura actual de docs/, crea el archivo mkdocs.yml.

Requisitos:

- MkDocs Material;
- navegación completa de capítulos existentes;
- secciones por parte;
- búsqueda;
- tablas;
- Mermaid;
- MathJax;
- admonitions;
- code copy;
- dark/light mode;
- repo URL como placeholder configurable;
- copyright como placeholder;
- plugins mínimos;
- extensiones Markdown compatibles;
- comentarios explicativos breves.

No incluyas en nav archivos que todavía no existen, salvo que se identifiquen expresamente como roadmap.

Entrega únicamente el contenido de mkdocs.yml.
```

---

# 29. Prompt para crear docs/index.md

```text
Usando PROJECT-HANDOFF.md, crea docs/index.md como página principal de MkDocs.

Debe incluir:

- introducción;
- propósito;
- audiencia;
- alcance;
- partes del handbook;
- estado actual;
- learning paths;
- cómo usar el repositorio;
- advertencia profesional;
- enlaces relativos a capítulos existentes;
- enlace al roadmap;
- enlace al methodology selection guide cuando exista.

Entrega únicamente el contenido completo de docs/index.md.
```

---

# 30. Prompt para crear docs/roadmap.md

```text
Usando PROJECT-HANDOFF.md, crea docs/roadmap.md.

Debe incluir:

- visión;
- estado actual;
- entregables completados;
- backlog por parte;
- versiones 0.1 a 1.0;
- prioridades;
- dependencias;
- criterios de completitud;
- riesgos del proyecto;
- definición de done por capítulo;
- tabla de estado de capítulos;
- orden recomendado de desarrollo.

Entrega únicamente el contenido completo del archivo.
```

---

# 31. Definición de “capítulo terminado”

Un capítulo se considera completo cuando:

- tiene front matter;
- usa nombre correcto;
- tiene objetivos;
- define notación;
- explica supuestos;
- desarrolla el método;
- incluye ejemplo;
- incluye validación;
- incluye limitaciones;
- incluye checklist;
- incluye referencias;
- contiene enlaces relativos correctos;
- no contradice otros capítulos;
- ha sido revisado técnicamente;
- ha sido revisado editorialmente;
- compila en MkDocs;
- no contiene enlaces rotos.

---

# 32. Riesgos actuales del proyecto

## 32.1 Scope creep

El repositorio puede crecer indefinidamente.

Mitigación:

- roadmap;
- versiones;
- definición de done;
- priorización;
- límite por capítulo.

## 32.2 Inconsistencia editorial

Mitigación:

- plantilla;
- front matter;
- glosario;
- notación común;
- revisión.

## 32.3 Numeración

Los capítulos actuales no están agrupados secuencialmente por parte.

Mitigación:

- mantener temporalmente;
- decidir renumeración antes de versión 1.0;
- no crear conflictos nuevos.

## 32.4 Regulación cambiante

Mitigación:

- fuentes oficiales;
- fecha de actualización;
- disclaimer;
- changelog;
- revisión periódica.

## 32.5 Código no probado

Mitigación:

- tests;
- versiones;
- datasets sintéticos;
- CI;
- notebooks reproducibles.

## 32.6 Exceso de modelos avanzados

Mitigación:

- benchmarks;
- health-specific first;
- governance;
- model selection guide.

---

# 33. Decisiones pendientes

Antes de versión 1.0 se debe decidir:

1. licencia del código;
2. licencia de la documentación;
3. usuario y URL de GitHub;
4. nombre final del repositorio;
5. idioma principal;
6. estrategia bilingüe;
7. numeración definitiva;
8. si se publicará PDF;
9. si se usará MkDocs, Quarto o ambos;
10. nivel de profundidad de código;
11. política de referencias;
12. mecanismo de actualización regulatoria.

---

# 34. Recomendación de licencias

Propuesta:

- código: MIT;
- documentación: CC BY 4.0.

Debe confirmarse antes de publicar.

---

# 35. Advertencia profesional

El repositorio debe incluir un disclaimer consistente:

> Este material es educativo y técnico. No reemplaza el juicio profesional de un actuario calificado, asesoría jurídica, contable, regulatoria o financiera. Las metodologías deben adaptarse a los datos, contratos, regulación y propósito específico de cada entidad. La regulación debe verificarse contra fuentes oficiales vigentes.

---

# 36. Acción inmediata para el nuevo chat

El nuevo chat debe comenzar con:

1. este archivo;
2. la estructura `find docs -maxdepth 2 -type f | sort`;
3. la solicitud concreta:

```text
Crea README.md completo y listo para guardar, usando PROJECT-HANDOFF.md como especificación.
```

Después:

```text
Crea mkdocs.yml.
```

Luego:

```text
Crea docs/index.md.
```

Luego:

```text
Crea docs/roadmap.md.
```

No solicitar los cuatro simultáneamente si se desea revisar cada archivo con profundidad antes de continuar.

---

# 37. Resumen ejecutivo

El proyecto ya cuenta con:

- fundamentos;
- triángulos;
- Chain Ladder;
- diagnósticos;
- Mack;
- Bootstrap;
- BF;
- Benktander;
- Cape Cod;
- GLM;
- GAM;
- Bayes;
- ML;
- árboles;
- cinco capítulos específicos para Colombia.

Falta:

- infraestructura GitHub;
- sitio MkDocs;
- bloque health-specific;
- ASOP y governance;
- implementación;
- datasets;
- tests;
- casos end-to-end;
- glosario;
- bibliografía central;
- roadmap formal.

La siguiente fase no debe enfocarse en crear más algoritmos. Debe enfocarse en transformar la colección actual en un repositorio navegable, reproducible y mantenible.

---

# Próximo entregable

```text
README.md
```

Ruta:

```text
./README.md
```

Después:

```text
./mkdocs.yml
./docs/index.md
./docs/roadmap.md
```