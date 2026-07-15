---
title: "Roadmap del Health Insurance Reserving Handbook"
description: "Estado vigente, próximos hitos, criterios de salida y riesgos para desarrollar el handbook desde v0.1.3 hacia v1.0.0."
chapter: "roadmap"
part: "repository"
language: "es"
status: "draft"
version: "0.1.13"
last_updated: "2026-07-14"
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

La versión pública más reciente es `v0.1.3`. La rama `main` contiene mejoras posteriores que se agruparán en un release futuro.

| Componente | Estado actual |
|---|---|
| Capítulos | 40 capítulos en español |
| Partes | 7 partes temáticas |
| Demos | 2 demos bilingües reproducibles |
| Datos | Conjuntos sintéticos pagados e incurridos |
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

## 3. Trabajo completado después de v0.1.3

- incorporación del demo pagado vs. incurrido;
- traducción y normalización de las Partes 1–7;
- corrección del renderizado matemático en GitHub;
- consolidación de front matter, H1 y navegación;
- actualización editorial de portada, roadmap, changelog y citación.

Estas mejoras permanecen bajo `Unreleased` hasta que se cree un nuevo tag público.

## 4. Próximo hito: v0.2.0

`v0.2.0` debe representar una mejora funcional verificable, no solo una acumulación de correcciones editoriales.

### 4.1 Auditoría matemática preventiva

**Entregables**

- script que detecte delimitadores incompatibles con GitHub;
- validación de bloques matemáticos balanceados;
- detección de signos aislados o fórmulas interpretables como encabezados Markdown;
- ejecución automática en GitHub Actions.

**Criterio de salida**

- cero problemas en los 49 documentos bajo `docs/`;
- resultado reproducible localmente y en CI.

### 4.2 Pruebas para demos reproducibles

**Entregables**

- pruebas de reconciliación entre datos largos y triángulos;
- validación incremental-acumulado;
- comprobación de factores, ultimate e IBNR;
- ejecución determinística por semilla;
- verificación de que regenerar salidas no produce diferencias no explicadas.

**Criterio de salida**

- todos los generadores terminan correctamente en una instalación limpia;
- las pruebas se ejecutan en CI.

### 4.3 Demo 3 · Comparación de métodos clásicos

Comparará:

- Chain Ladder;
- Bornhuetter-Ferguson;
- Benktander;
- Cape Cod.

El demo debe incluir exposición, expectativa previa defendible, ultimate, IBNR, sensibilidad y visualizaciones por año de origen. Tendrá documentación y salidas en español e inglés.

**Criterio de salida**

- resultados conciliados y reproducibles;
- explicación clara de por qué los métodos divergen;
- referencias cruzadas con los capítulos 6 y 11–14.

### 4.4 Cierre de v0.2.0

- auditoría documental limpia;
- build estricto exitoso;
- CI en verde;
- changelog y citación actualizados;
- release notes con alcance, limitaciones y comandos de reproducción;
- verificación del sitio publicado.

## 5. Hito posterior: v0.3.0

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

1. consolidación editorial v0.1.13;
2. auditoría matemática automatizada;
3. pruebas de reproducibilidad de los demos;
4. Demo 3 de métodos clásicos;
5. cierre y publicación de v0.2.0;
6. Demo 4 de incertidumbre para v0.3.0.

No se asignan fechas hasta conocer capacidad de revisión y profundidad requerida. Cada hito debe cerrarse por evidencia.
