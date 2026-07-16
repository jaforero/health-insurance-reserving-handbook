---
title: "Health Insurance Reserving Handbook"
description: "Portada, rutas de aprendizaje y acceso a 40 capítulos y cinco demos reproducibles sobre reservas actuariales en seguros de salud."
chapter: "index"
part: "repository"
language: "es"
status: "draft"
version: "0.2.4"
last_updated: "2026-07-15"
---

<div class="home-hero" markdown>

# Health Insurance Reserving Handbook

Manual técnico y reproducible sobre IBNR, reservas actuariales y desarrollo de reclamaciones en seguros de salud, con aplicaciones al sistema colombiano.

[:material-book-open-page-variant: Comenzar por los fundamentos](part-01-foundations/01-ibnr-and-reserving.md){ .md-button .md-button--primary }
[:material-chart-box: Explorar los demos](examples/01-demo-triangulos-simulados-salud.md){ .md-button }
[:material-source-repository: Ver el repositorio](https://github.com/jaforero/health-insurance-reserving-handbook){ .md-button }

<div class="home-stats">
  <div class="home-stat"><strong>40</strong>capítulos técnicos</div>
  <div class="home-stat"><strong>7</strong>partes temáticas</div>
  <div class="home-stat"><strong>5</strong>demos reproducibles</div>
  <div class="home-stat"><strong>132</strong>campos canónicos</div>
</div>

</div>

## Estado del handbook

El proyecto contiene actualmente:

- **40 capítulos** técnicos en español;
- **7 partes** temáticas;
- **5 demos prácticos**, tres bilingües y dos publicados inicialmente en español;
- generadores reproducibles en Python;
- visualizaciones SVG de triángulos actuariales;
- auditoría estructural, preflight y construcción estricta con MkDocs.

La versión pública más reciente es `v0.2.4`, que incorpora la identidad corporativa, IgraSans, el logo, el favicon, el footer y la analítica de uso.

!!! warning "Uso profesional"
    El handbook es una referencia educativa y técnica. Una aplicación profesional requiere validar datos, obligaciones, contratos, supuestos, regulación vigente y propósito de la estimación.

## Contenido por parte

| Parte | Tema | Capítulos | Enfoque |
|---:|---|---:|---|
| 1 | Fundamentos | 5 | IBNR, construcción y transformación de triángulos |
| 2 | Reservas clásicas | 6 | Chain Ladder, BF, Benktander y Cape Cod |
| 3 | Reservas estocásticas | 3 | Mack, Bootstrap e incertidumbre |
| 4 | Modelos estadísticos | 3 | GLM, GAM y modelos bayesianos |
| 5 | Machine Learning | 3 | Diseño, árboles, deep learning y gobierno |
| 6 | Especificidades de salud | 8 | Exposición, tendencia, contratos, auditoría y gobierno |
| 7 | Colombia | 12 | UPC, RIPS–FEV, glosas, alto costo, provisiones y solvencia |

## Demos prácticos

### 1. Triángulos simulados de reclamaciones pagadas

Desde datos en formato largo hasta triángulos incrementales y acumulados, factores edad-a-edad, ultimate, IBNR y una visualización tradicional.

- [Abrir demo en español](examples/01-demo-triangulos-simulados-salud.md)
- [Open English demo](examples/01-simulated-health-triangles-demo.md)

### 2. Triángulos pagados vs. incurridos

Compara madurez, reserva caso, factores de desarrollo y resultados Chain Ladder sobre bases pagadas e incurridas.

- [Abrir demo en español](examples/02-demo-pagado-vs-incurrido-salud.md)
- [Open English demo](examples/02-paid-vs-incurred-health-demo.md)

### 3. Triángulos mensuales de reclamaciones pagadas

Utiliza 60 meses de origen y desarrollo 0–24, con una visualización actuarial tradicional, curva de maduración y conteo de observaciones por factor.

- [Abrir demo en español](examples/03-demo-triangulos-mensuales-salud.md)
- [Open English demo](examples/03-monthly-health-triangles-demo.md)

### 4. Preparación de datos para metodologías de reserving

Evalúa la semántica, integridad, historia, exposición, priors, snapshots y gobierno del dataset antes de aplicar o comparar metodologías.

- [Abrir demo en español](examples/04-demo-preparacion-datos.md)
- [Marco conceptual — Parte 1](marco-preparacion-datos-metodologias-parte-1.md)
- [Gates y benchmark — Parte 2](marco-preparacion-datos-metodologias-parte-2.md)
- [Matriz de preparación por método](matriz-preparacion-datos-metodologias.md)

### 5. De datos propios a triángulos actuariales

Asistente local en Streamlit para seleccionar un CSV, TXT delimitado, Excel o Parquet, mapear
columnas, ejecutar controles, construir triángulos incrementales y acumulados y descargar
resultados reproducibles.

- [Abrir Demo 5](examples/05-demo-datos-propios-triangulos-actuariales.md)

## Rutas de aprendizaje

### Ruta A · Construir una primera estimación de IBNR

1. [IBNR y reservas](part-01-foundations/01-ibnr-and-reserving.md)
2. [Construcción de triángulos](part-01-foundations/02-triangle-construction.md)
3. [Triángulos incrementales y acumulados](part-01-foundations/04-incremental-vs-cumulative-triangles.md)
4. [Factores edad-a-edad](part-01-foundations/05-age-to-age-development-factors.md)
5. [Método Chain Ladder](part-02-classical-reserving/06-chain-ladder-method.md)
6. [Demo de triángulos simulados](examples/01-demo-triangulos-simulados-salud.md)
7. [Demo de triángulos mensuales](examples/03-demo-triangulos-mensuales-salud.md)

### Ruta B · Comparar métodos y dependencia del prior

1. [Diagnósticos de Chain Ladder](part-02-classical-reserving/07-chain-ladder-diagnostics.md)
2. [Bornhuetter-Ferguson](part-02-classical-reserving/11-bornhuetter-ferguson.md)
3. [Benktander](part-02-classical-reserving/12-benktander-method.md)
4. [Cape Cod](part-02-classical-reserving/13-cape-cod-method.md)
5. [Comparación de métodos clásicos](part-02-classical-reserving/14-classical-reserving-methods-comparison.md)

### Ruta C · Cuantificar incertidumbre

1. [Chain Ladder de Mack](part-03-stochastic-reserving/08-mack-chain-ladder.md)
2. [Bootstrap Chain Ladder](part-03-stochastic-reserving/09-bootstrap-chain-ladder.md)
3. [Comparación entre Mack y Bootstrap](part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md)
4. [Reservas bayesianas](part-04-statistical-models/17-bayesian-loss-reserving.md)

### Ruta D · Reservas de salud en Colombia

1. [Particularidades de las reservas en salud](part-06-health-specific/21-health-insurance-reserving-specificities.md)
2. [Ciclo de vida y rezagos operativos](part-06-health-specific/22-health-claim-lifecycle-and-operational-lags.md)
3. [Metodologías de reservas en Colombia](part-07-colombia/29-colombia-health-reserving-methodologies.md)
4. [Triángulos pagados e incurridos](part-07-colombia/30-colombia-paid-vs-incurred-triangles.md)
5. [Glosas, devoluciones y controversias](part-07-colombia/32-colombia-glosas-and-disputes.md)
6. [IBNR, provisiones y reporte regulatorio](part-07-colombia/37-colombia-ibnr-technical-provisions-and-regulatory-reporting.md)

## Selección metodológica

No existe un método universalmente superior. La selección depende, entre otros elementos, de:

- propósito de la valoración;
- definición de la obligación;
- madurez y estabilidad de los datos;
- disponibilidad y calidad de exposición o priors;
- cambios de población, beneficios, contratos, red y operación;
- tendencia médica, estacionalidad y eventos extraordinarios;
- materialidad, explicabilidad y gobierno requerido.

Consulte la [guía de selección de metodologías](methodology-selection-guide.md) y el [roadmap](roadmap.md) para conocer criterios de evidencia y próximos desarrollos.

## Calidad y reproducibilidad

Antes de publicar cambios se ejecutan:

```bash
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m mkdocs build --strict
```

Los ejemplos utilizan datos sintéticos. Los resultados deben reconciliarse y someterse a validación independiente antes de cualquier uso profesional.
