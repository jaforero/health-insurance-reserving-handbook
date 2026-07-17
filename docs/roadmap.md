---
title: "Roadmap del Health Insurance Reserving Handbook"
description: "Estado vigente, próximos hitos, criterios de salida y riesgos para desarrollar el handbook desde v0.4.0 hacia v1.0.0."
chapter: "roadmap"
part: "repository"
language: "es"
status: "draft"
version: "0.4.0"
last_updated: "2026-07-17"
---

# Roadmap del Health Insurance Reserving Handbook

> El avance se gobierna mediante entregables verificables y criterios de salida, no únicamente por cantidad de archivos.

## 1. Visión

El objetivo es consolidar una referencia profesional, abierta y reproducible sobre reservas en seguros de salud que combine:

- fundamentos y métodos actuariales;
- incertidumbre y modelación estadística;
- machine learning con benchmarks transparentes;
- operación de reclamaciones médicas;
- aplicaciones al sistema de salud colombiano;
- datos sintéticos, código, pruebas y visualizaciones;
- documentación, validación y gobierno de modelos.

## 2. Línea base actual

La versión pública más reciente es `v0.4.0`. Incorpora el flujo local de datos propios a triángulos
actuariales mediante Demo 5 y Chain Ladder determinístico como primer incremento de Demo 6.

| Componente | Estado actual |
|---|---|
| Capítulos | 40 capítulos en español |
| Partes | 7 partes temáticas |
| Demos | 6 demos reproducibles: tres bilingües y tres en español |
| Datos | Conjuntos sintéticos y diccionario canónico de reserving |
| Visualizaciones | Triángulos actuariales y comparaciones en SVG |
| Publicación | MkDocs Material y GitHub Pages |
| Calidad documental | Auditoría estructural, preflight y build estricto |
| CI | Validación y despliegue desde `main` |

### Distribución de capítulos

| Parte | Tema | Cantidad |
|---:|---|---:|
| 1 | Fundamentos | 5 |
| 2 | Reservas clásicas | 6 |
| 3 | Reservas estocásticas | 3 |
| 4 | Modelos estadísticos | 3 |
| 5 | Machine Learning | 3 |
| 6 | Especificidades de salud | 8 |
| 7 | Colombia | 12 |
|  | **Total** | **40** |

## 3. Alcance cerrado hasta v0.4.0

- incorporación del demo pagado vs. incurrido;
- traducción y normalización de las Partes 1–7;
- corrección del renderizado matemático en GitHub;
- consolidación de front matter, H1 y navegación;
- actualización editorial de portada, roadmap, changelog y citación.
- marco de preparación de datos publicado en dos partes;
- matriz de requisitos y elegibilidad por metodología;
- diccionario canónico con nombres principales en español;
- Demo 4 de preparación y evaluación de datasets.
- Demo 5 local para construir triángulos con datos propios mediante Streamlit;
- Demo 6 local para seleccionar factores, proyectar el triángulo y estimar ultimate e IBNR;
- sistema visual corporativo compartido con IgraSans local y componentes responsivos;
- suite automatizada para preparación, Chain Ladder, Bornhuetter-Ferguson, exportación e
  interfaces.

## 4. Próximo hito: v0.5.0

`v0.5.0` ampliará Demo 6 para comparar métodos clásicos bajo supuestos y fuentes de información
explícitos.

### 4.1 Exposición y expectativa previa

**Entregables**

- carga y validación de exposición por periodo de origen;
- selección documentada de una razón de pérdida o frecuencia-severidad esperada;
- reconciliación entre exposición, prima, expectativa previa y triángulo observado.

### 4.2 Bornhuetter-Ferguson

**Entregables**

- ultimate e IBNR por periodo de origen;
- sensibilidad a la expectativa previa y a los patrones de desarrollo;
- comparación directa con Chain Ladder.

**Sprint 1 del núcleo — implementado**

- motor Python independiente de Streamlit;
- prior directo o reconciliado como exposición por tasa esperada;
- sensibilidad configurable del prior y diagnósticos por periodo;
- pruebas numéricas antes de integrar carga de archivos, interfaz y exportación.

**Sprint 2 de integración — implementado y pendiente de aceptación final**

- carga local de priors en CSV, TXT delimitado, XLSX o Parquet;
- mapeo de periodo de origen y prior directo o exposición por tasa;
- prior sintético reproducible, independiente del desarrollo observado;
- comparación visual Chain Ladder vs. BF por origen y total;
- sensibilidad configurable, diagnósticos y exportación conjunta auditable;
- pruebas del recorrido completo en Streamlit y de privacidad de la exportación.

### 4.3 Benktander y Cape Cod

**Entregables**

- iteraciones Benktander configurables;
- estimación Cape Cod con exposición;
- supuestos, diagnósticos y exportación reproducible.

### 4.4 Comparación de métodos clásicos

El demo deberá explicar por qué los métodos divergen, mostrar sensibilidad por periodo de origen y
mantener referencias cruzadas con los capítulos 6 y 11–14.

**Criterio de salida**

- resultados conciliados y reproducibles;
- priors y exposición trazables;
- comparación visual y tabular de ultimate e IBNR;
- salidas y documentación en español, con expansión bilingüe planificada.

### 4.5 Cierre de v0.5.0

- auditoría documental limpia;
- build estricto exitoso;
- CI en verde;
- changelog y citación actualizados;
- release notes con alcance, limitaciones y comandos de reproducción;
- verificación del sitio publicado.

## 5. Hito posterior: v0.6.0

El foco propuesto es incertidumbre y distribución predictiva:

- demo comparativo Mack vs. Bootstrap;
- error de predicción por año de origen y total;
- intervalos, cuantiles, VaR y TVaR;
- sensibilidad a residuos, cola y supuestos de proceso;
- backtesting y calibración.

## 6. Camino hacia v1.0.0

La versión estable requerirá, como mínimo:

1. revisión técnica transversal de los 40 capítulos;
2. política bibliográfica y regulatoria uniforme;
3. notación consistente entre capítulos y demos;
4. código reproducible con pruebas automatizadas;
5. datos sintéticos documentados mediante diccionarios y esquemas;
6. validación de enlaces, matemáticas, navegación y accesibilidad;
7. revisión independiente de afirmaciones colombianas sensibles a vigencia;
8. política de versiones, deprecaciones y migraciones;
9. evidencia de que una instalación limpia reproduce el sitio y los demos.

## 7. Definición de terminado

Un capítulo o demo puede considerarse validado cuando:

- tiene propósito, alcance y supuestos explícitos;
- utiliza notación coherente con el resto del handbook;
- sus cálculos se pueden reproducir;
- sus resultados se reconcilian;
- incluye limitaciones y riesgos de uso;
- tiene referencias cruzadas y enlaces válidos;
- supera las auditorías automatizadas;
- ha recibido revisión técnica o independiente proporcional a su materialidad.

La existencia de un archivo o su inclusión en la navegación solo indica disponibilidad, no validación completa.

## 8. Riesgos del proyecto

| Riesgo | Respuesta prevista |
|---|---|
| Afirmaciones regulatorias desactualizadas | Fecha de corte, fuentes oficiales y revisión periódica |
| Fórmulas que compilan en MkDocs pero fallan en GitHub | Auditoría matemática en CI |
| Demos que dejan de reproducirse | Semillas, pruebas y verificación de artefactos |
| Divergencia entre portada y contenido real | Inventario automatizado y consolidación por release |
| Métodos avanzados sin benchmark | Comparación obligatoria con referencias actuariales |
| Renombramientos que rompen URLs | Mantener rutas estables y planificar migraciones |
| Datos interpretados como experiencia real | Etiquetado explícito de datos sintéticos |
| Crecimiento sin revisión | Criterios de salida por hito |

## 9. Orden recomendado de ejecución

1. publicación y verificación de `v0.4.0`;
2. prueba de aceptación de Demo 5 con datos anonimizados;
3. aceptación del Sprint 2 de Bornhuetter-Ferguson con priors controlados;
4. incorporación de Benktander y Cape Cod;
5. comparación reproducible de métodos clásicos;
6. cierre y publicación de `v0.5.0`;
7. Demo 7 de incertidumbre para `v0.6.0`.

No se asignan fechas hasta conocer capacidad de revisión y profundidad requerida. Cada hito debe cerrarse por evidencia.
