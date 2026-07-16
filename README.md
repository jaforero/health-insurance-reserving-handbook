# Health Insurance Reserving Handbook

> Manual técnico, reproducible y orientado a la práctica sobre IBNR, reservas actuariales y desarrollo de reclamaciones en seguros de salud, con aplicaciones al sistema colombiano.

[![Documentation](https://github.com/jaforero/health-insurance-reserving-handbook/actions/workflows/docs.yml/badge.svg)](https://github.com/jaforero/health-insurance-reserving-handbook/actions/workflows/docs.yml)
[![Release](https://img.shields.io/badge/release-v0.4.0-2f855a)](https://github.com/jaforero/health-insurance-reserving-handbook/releases/tag/v0.4.0)
[![Language](https://img.shields.io/badge/contenido-español-526cfe)](#contenido)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Accesos rápidos

- [Sitio publicado](https://actuaria.javierforero.co/)
- [Portada y rutas de aprendizaje](docs/index.md)
- [Guía de selección de metodologías](docs/methodology-selection-guide.md)
- [Marco de preparación de datos — Parte 1](docs/marco-preparacion-datos-metodologias-parte-1.md)
- [Marco de preparación de datos — Parte 2](docs/marco-preparacion-datos-metodologias-parte-2.md)
- [Matriz de preparación por método](docs/matriz-preparacion-datos-metodologias.md)
- [Roadmap](docs/roadmap.md)
- [Glosario](docs/glossary.md)
- [Bibliografía y evidencia](docs/bibliography.md)
- [Demos prácticos](#demos-prácticos)

## Descripción

**Health Insurance Reserving Handbook** es una referencia abierta sobre estimación de reservas en seguros de salud. Integra fundamentos actuariales, métodos determinísticos y estocásticos, modelos estadísticos y de machine learning, particularidades operativas de las reclamaciones médicas y aplicaciones al Sistema General de Seguridad Social en Salud de Colombia.

El repositorio puede utilizarse como:

- libro técnico de nivel intermedio y avanzado;
- manual de consulta para actuarios, analistas y validadores;
- guía para construir, comparar y gobernar modelos de reservas;
- curso autocontenido sobre IBNR y desarrollo de reclamaciones;
- repositorio reproducible de código, datos sintéticos y visualizaciones;
- punto de partida para casos de estudio y procesos actuariales productivos.

## Estado actual

La versión pública más reciente es **v0.4.0**. Incorpora Demo 5 para construir triángulos con
datos propios y Demo 6 para transformar triángulos acumulados reconciliados en estimaciones
determinísticas de ultimate e IBNR mediante Chain Ladder.

El repositorio incluye actualmente:

- **40 capítulos** técnicos en español;
- **7 partes** temáticas;
- **6 demos prácticos**, tres bilingües y tres publicados inicialmente en español;
- datos sintéticos reproducibles;
- visualizaciones SVG de triángulos actuariales;
- construcción y despliegue automático con MkDocs y GitHub Pages;
- auditoría estructural y preflight de publicación.

Los capítulos permanecen en desarrollo y revisión. Un archivo publicado no debe interpretarse automáticamente como metodología prescrita, cumplimiento regulatorio ni recomendación para una entidad concreta.

## Contenido

| Parte | Tema | Capítulos | Cantidad |
|---:|---|---|---:|
| 1 | Fundamentos | 01–05 | 5 |
| 2 | Reservas clásicas | 06, 07 y 11–14 | 6 |
| 3 | Reservas estocásticas | 08–10 | 3 |
| 4 | Modelos estadísticos | 15–17 | 3 |
| 5 | Machine Learning | 18–20 | 3 |
| 6 | Especificidades de salud | 21–28 | 8 |
| 7 | Colombia | 29–40 | 12 |
|  | **Total** |  | **40** |

### Parte 1 · Fundamentos

- [01 · IBNR y reservas](docs/part-01-foundations/01-ibnr-and-reserving.md)
- [02 · Construcción de triángulos](docs/part-01-foundations/02-triangle-construction.md)
- [03 · Rezagos de desarrollo y transformaciones](docs/part-01-foundations/03-development-lags-and-triangle-transformations.md)
- [04 · Triángulos incrementales y acumulados](docs/part-01-foundations/04-incremental-vs-cumulative-triangles.md)
- [05 · Factores edad-a-edad](docs/part-01-foundations/05-age-to-age-development-factors.md)

### Parte 2 · Reservas clásicas

- [06 · Método Chain Ladder](docs/part-02-classical-reserving/06-chain-ladder-method.md)
- [07 · Diagnósticos de Chain Ladder](docs/part-02-classical-reserving/07-chain-ladder-diagnostics.md)
- [11 · Bornhuetter-Ferguson](docs/part-02-classical-reserving/11-bornhuetter-ferguson.md)
- [12 · Método Benktander](docs/part-02-classical-reserving/12-benktander-method.md)
- [13 · Método Cape Cod](docs/part-02-classical-reserving/13-cape-cod-method.md)
- [14 · Comparación de métodos clásicos](docs/part-02-classical-reserving/14-classical-reserving-methods-comparison.md)

### Parte 3 · Reservas estocásticas

- [08 · Chain Ladder de Mack](docs/part-03-stochastic-reserving/08-mack-chain-ladder.md)
- [09 · Bootstrap Chain Ladder](docs/part-03-stochastic-reserving/09-bootstrap-chain-ladder.md)
- [10 · Comparación entre Mack y Bootstrap](docs/part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md)

### Parte 4 · Modelos estadísticos

- [15 · Modelos lineales generalizados](docs/part-04-statistical-models/15-glm-for-loss-reserving.md)
- [16 · Modelos aditivos generalizados](docs/part-04-statistical-models/16-gam-for-loss-reserving.md)
- [17 · Reservas bayesianas](docs/part-04-statistical-models/17-bayesian-loss-reserving.md)

### Parte 5 · Machine Learning

- [18 · Machine Learning para reservas actuariales](docs/part-05-machine-learning/18-machine-learning-for-loss-reserving.md)
- [19 · Modelos basados en árboles](docs/part-05-machine-learning/19-tree-based-models-for-loss-reserving.md)
- [20 · Deep Learning para reservas actuariales](docs/part-05-machine-learning/20-deep-learning-for-loss-reserving.md)

### Parte 6 · Especificidades de salud

- [21 · Particularidades de las reservas en salud](docs/part-06-health-specific/21-health-insurance-reserving-specificities.md)
- [22 · Ciclo de vida y rezagos operativos](docs/part-06-health-specific/22-health-claim-lifecycle-and-operational-lags.md)
- [23 · Exposición, utilización y severidad](docs/part-06-health-specific/23-health-exposure-utilization-and-severity.md)
- [24 · Tendencia médica, estacionalidad y choques](docs/part-06-health-specific/24-health-medical-trend-seasonality-and-shocks.md)
- [25 · Ajuste de riesgo y morbilidad](docs/part-06-health-specific/25-health-risk-adjustment-and-morbidity.md)
- [26 · Contratos con prestadores y modelos de pago](docs/part-06-health-specific/26-health-provider-contracts-and-payment-models.md)
- [27 · Auditoría, denegaciones y controversias](docs/part-06-health-specific/27-health-claims-audit-denials-and-disputes.md)
- [28 · Gobierno, controles y reporte](docs/part-06-health-specific/28-health-reserving-governance-controls-and-reporting.md)

### Parte 7 · Colombia

- [29 · Metodologías de reservas de salud](docs/part-07-colombia/29-colombia-health-reserving-methodologies.md)
- [30 · Triángulos pagados e incurridos](docs/part-07-colombia/30-colombia-paid-vs-incurred-triangles.md)
- [31 · Datos y modelos multiestado](docs/part-07-colombia/31-colombia-data-and-multistate-models.md)
- [32 · Glosas, devoluciones y controversias](docs/part-07-colombia/32-colombia-glosas-and-disputes.md)
- [33 · Capitación y pagos prospectivos](docs/part-07-colombia/33-colombia-capitation-and-prospective-payments.md)
- [34 · UPC, ajuste de riesgo y morbilidad](docs/part-07-colombia/34-colombia-upc-risk-adjustment-and-morbidity.md)
- [35 · Alto costo y mutualización de riesgos](docs/part-07-colombia/35-colombia-high-cost-conditions-and-risk-pooling.md)
- [36 · Calidad y validación de datos RIPS–FEV](docs/part-07-colombia/36-colombia-rips-fev-data-quality-and-validation.md)
- [37 · IBNR, provisiones y reporte regulatorio](docs/part-07-colombia/37-colombia-ibnr-technical-provisions-and-regulatory-reporting.md)
- [38 · Solvencia, liquidez y pruebas de estrés](docs/part-07-colombia/38-colombia-solvency-liquidity-and-stress-testing.md)
- [39 · Escenarios y hoja de ruta de reforma](docs/part-07-colombia/39-colombia-scenario-planning-and-reform-roadmap.md)
- [40 · Playbook de implementación y plantillas](docs/part-07-colombia/40-colombia-implementation-playbook-and-templates.md)

## Demos prácticos

### Demo 1 · Triángulos pagados simulados

Construye datos en formato largo, triángulos incrementales y acumulados, factores edad-a-edad, ultimate e IBNR por Chain Ladder y visualizaciones actuariales tradicionales.

- [Documentación en español](docs/examples/01-demo-triangulos-simulados-salud.md)
- [English documentation](docs/examples/01-simulated-health-triangles-demo.md)
- [Datos en español](data/demo_triangulos/README.md)
- [English data](data/demo_triangles/README.md)

```bash
python scripts/generate_demo_triangles.py
python scripts/generate_demo_triangle_visuals.py
```

### Demo 2 · Pagado vs. incurrido

Compara triángulos pagados e incurridos, reserva caso, factores de desarrollo y estimaciones Chain Ladder en ambas bases.

- [Documentación en español](docs/examples/02-demo-pagado-vs-incurrido-salud.md)
- [English documentation](docs/examples/02-paid-vs-incurred-health-demo.md)
- [Datos en español](data/demo_pagado_incurrido/README.md)
- [English data](data/demo_paid_incurred/README.md)

```bash
python scripts/generate_demo_paid_incurred.py
```

### Demo 3 · Triángulos mensuales pagados

Construye 60 meses de origen y edades mensuales 0–24, con controles de madurez, número de observaciones por factor, ultimate e IBNR.

- [Documentación en español](docs/examples/03-demo-triangulos-mensuales-salud.md)
- [English documentation](docs/examples/03-monthly-health-triangles-demo.md)
- [Datos en español](data/demo_triangulos_mensuales/README.md)
- [English data](data/demo_monthly_triangles/README.md)

```bash
python scripts/generate_demo_monthly_triangles.py
```

### Demo 4 · Preparación de datos para reserving

Mapea campos operativos a un contrato canónico en español, ejecuta controles de integridad, evalúa los gates G0–G9 y determina qué metodologías están listas, limitadas, exploratorias o bloqueadas.

- [Documentación en español](docs/examples/04-demo-preparacion-datos.md)
- [Diccionario canónico](config/diccionario_datos_canonico.yml)

### Demo 5 · De datos propios a triángulos actuariales

Aplicación local en Streamlit para seleccionar un CSV, TXT delimitado, Excel o Parquet, mapear
campos, validar fechas, importes y duplicados, construir triángulos incrementales y acumulados y
exportar resultados sin incorporar el archivo fuente al repositorio.

La interfaz reutiliza localmente IgraSans, el logo actuarial y la identidad visual corporativa del
sitio principal.

- [Documentación en español](docs/examples/05-demo-datos-propios-triangulos-actuariales.md)

```bash
conda env create -f environment.yml
conda activate reserving-handbook
python scripts/iniciar_asistente_triangulos.py
```

### Demo 6 · Chain Ladder con datos propios

Aplicación local en Streamlit para leer el paquete agregado de Demo 5, comparar reglas de
selección de factores, documentar una selección manual y un factor de cola, completar el triángulo
acumulado y estimar ultimate e IBNR por periodo de origen.

- [Documentación en español](docs/examples/06-demo-chain-ladder-datos-propios.md)

```bash
conda activate reserving-handbook
python scripts/iniciar_chain_ladder.py
```

Los datos incluidos en el repositorio son sintéticos y se generan con semillas reproducibles. El
Demo 5 puede procesar archivos locales del usuario y Demo 6 utiliza solamente sus salidas
agregadas, sin incorporar esos archivos al repositorio.

## Instalación y documentación local

Se requiere Python 3.10 o superior.

```bash
git clone https://github.com/jaforero/health-insurance-reserving-handbook.git
cd health-insurance-reserving-handbook
python -m pip install -r requirements.txt
python -m mkdocs serve
```

La documentación local estará disponible normalmente en `http://127.0.0.1:8000/`.

## Validación antes de contribuir

```bash
rm -rf site
python scripts/audit_docs.py
python scripts/preflight_release.py
python -m unittest discover -s tests -p "test_*.py"
python -m mkdocs build --strict
```

El workflow de GitHub Actions ejecuta estos controles y publica el sitio desde `main`.

## Estructura principal

```text
.
├── docs/                         # Capítulos, portada, demos y activos
├── apps/                         # Interfaces educativas locales
├── src/health_reserving/         # Núcleo Python reutilizable
├── config/                       # Diccionarios y configuraciones canónicas
├── data/                         # Datos sintéticos reproducibles
├── scripts/                      # Generadores y auditorías
├── tests/                        # Pruebas de regresión y del núcleo actuarial
├── bibliography/                 # Reportes de investigación de soporte
├── AAA/                          # Fuentes actuariales de referencia
├── .github/workflows/docs.yml    # Validación y GitHub Pages
├── mkdocs.yml
├── README.md
├── CHANGELOG.md
└── CITATION.cff
```

## Principios de uso

- Los resultados deben reconciliarse con contabilidad, exposición y datos operativos.
- Ningún modelo sustituye el juicio actuarial documentado.
- Los métodos avanzados deben compararse con un benchmark transparente.
- Regulación, mejor estimación, provisión contable y margen prudencial son conceptos relacionados, pero no intercambiables.
- Las aplicaciones colombianas deben verificarse contra la normativa vigente y el propósito específico de la valoración.

## Contribuciones

Consulte [CONTRIBUTING.md](CONTRIBUTING.md), el [Código de Conducta](CODE_OF_CONDUCT.md) y la [Política de Seguridad](SECURITY.md) antes de proponer cambios.

## Citación y licencia

La metadata de citación está disponible en [CITATION.cff](CITATION.cff). El código se distribuye bajo los términos descritos en [LICENSE](LICENSE).

## Descargo de responsabilidad

Este repositorio tiene fines educativos, técnicos y de investigación. No constituye asesoría actuarial, contable, jurídica, regulatoria ni financiera para una entidad o situación concreta.
