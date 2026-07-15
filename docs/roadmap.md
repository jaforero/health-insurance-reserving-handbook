---
title: "Roadmap del Health Insurance Reserving Handbook"
description: "Estado vigente, próximos hitos, criterios de salida y riesgos para desarrollar el handbook desde v0.2.1 hacia v1.0.0."
chapter: "roadmap"
part: "repository"
language: "es"
status: "draft"
version: "0.2.1"
last_updated: "2026-07-15"
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

La versión pública más reciente es `v0.2.1`, que incorpora el framework de preparación de datos, el diccionario canónico y el Demo 4.

| Componente | Estado actual |
|---|---|
| Capítulos | 40 capítulos en español |
| Partes | 7 partes temáticas |
| Demos | 4 demos reproducibles: tres bilingües y uno en español |
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

## 3. Alcance cerrado en v0.2.0

- incorporación del demo pagado vs. incurrido;
- traducción y normalización de las Partes 1–7;
- corrección del renderizado matemático en GitHub;
- consolidación de front matter, H1 y navegación;
- actualización editorial de portada, roadmap, changelog y citación.
- marco de preparación de datos publicado en dos partes;
- matriz de requisitos y elegibilidad por metodología;
- diccionario canónico con nombres principales en español;
- Demo 4 de preparación y evaluación de datasets.

Estas mejoras constituyen la línea base pública para los desarrollos posteriores.

## 4. Próximo hito: v0.3.0

`v0.3.0` debe profundizar la reproducibilidad y la comparación práctica de metodologías.

### 4.1 Auditoría matemática preventiva

**Entregables**

- script que detecte delimitadores incompatibles con GitHub;
- validación de bloques matemáticos balanceados;
- detección de signos aislados o fórmulas interpretables como encabezados Markdown;
- ejecución automática en GitHub Actions.

**Criterio de salida**

- cero problemas en los 55 documentos bajo `docs/`;
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

### 4.3 Demo 3 · Triángulos mensuales de salud

Incorpora 60 meses de origen, edades de desarrollo 0–24, controles de suficiencia por factor, comparación con la verdad simulada y visualizaciones bilingües. La configuración 60/24 se documenta como punto de partida práctico y no como mínimo actuarial universal.

**Criterio de salida**

- 1.200 celdas observadas conciliadas;
- al menos 36 observaciones en cada factor bajo la configuración predeterminada;
- curva de maduración, triángulo tradicional y diagnóstico reproducibles;
- documentación explícita de cuándo ampliar el horizonte.

### 4.4 Demo 5 · Comparación de métodos clásicos

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

### 4.5 Cierre de v0.3.0

- auditoría documental limpia;
- build estricto exitoso;
- CI en verde;
- changelog y citación actualizados;
- release notes con alcance, limitaciones y comandos de reproducción;
- verificación del sitio publicado.

## 5. Hito posterior: v0.4.0

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

1. publicación y verificación de v0.2.0;
2. auditoría matemática automatizada;
3. pruebas de reproducibilidad de los demos;
4. Demo 3 de triángulos mensuales;
5. Demo 5 de métodos clásicos;
6. cierre y publicación de v0.3.0;
7. Demo 5 de incertidumbre para v0.4.0.

No se asignan fechas hasta conocer capacidad de revisión y profundidad requerida. Cada hito debe cerrarse por evidencia.
