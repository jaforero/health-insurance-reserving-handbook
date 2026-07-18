---
title: Bibliografía y registro de evidencia
subtitle: Fuentes verificadas, reglas de citación y control de vigencia para el handbook
author: Health Insurance Reserving Handbook
version: 1.0
chapter: Bibliography
part: Repository Governance
status: Draft
last_updated: 2026-07-14
language: es
jurisdiction: General con aplicaciones a Colombia
tags:
  - bibliography
  - evidence-governance
  - actuarial-standards
  - reserving
  - health-insurance
  - colombia
prerequisites:
  - index.md
  - roadmap.md
  - methodology-selection-guide.md
  - glossary.md
related_chapters:
  - index.md
  - roadmap.md
  - methodology-selection-guide.md
  - glossary.md
  - part-01-foundations/01-ibnr-and-reserving.md
  - part-01-foundations/02-triangle-construction.md
  - part-02-classical-reserving/06-chain-ladder-method.md
  - part-02-classical-reserving/11-bornhuetter-ferguson.md
  - part-03-stochastic-reserving/08-mack-chain-ladder.md
  - part-04-statistical-models/15-glm-for-loss-reserving.md
  - part-05-machine-learning/18-machine-learning-for-loss-reserving.md
  - part-06-health-specific/21-health-insurance-reserving-specificities.md
  - part-07-colombia/29-colombia-health-reserving-methodologies.md
---

# Bibliografía y registro de evidencia

> Este documento define qué fuentes pueden sostener afirmaciones del handbook, cómo deben citarse, qué tan verificadas están y qué limitaciones aplican. Su función principal es gobernar evidencia; la lista bibliográfica es una consecuencia de ese gobierno.

## Advertencia de alcance

Este registro no convierte una fuente extranjera en norma local, no reemplaza asesoría jurídica, contable o actuarial, y no prueba por sí solo la vigencia de una obligación. En especial:

- las Actuarial Standards of Practice (ASOP) son referencias profesionales emitidas en Estados Unidos y deben tratarse como marco técnico, no como regulación colombiana;
- las afirmaciones sobre Colombia requieren fuente oficial vigente, fecha de consulta, texto aplicable y, cuando corresponda, análisis jurídico separado;
- los informes de investigación adjuntos sirven para descubrir fuentes y organizar preguntas, pero no deben citarse como autoridad primaria;
- cada capítulo debe citar la fuente concreta que soporta la afirmación específica, no este documento como sustituto.

## 1. Propósito

La bibliografía del handbook cumple cinco funciones:

1. establecer una jerarquía de evidencia para afirmaciones actuariales, metodológicas, regulatorias, operativas y de implementación;
2. fijar claves de citación estables para que los capítulos sean consistentes;
3. distinguir fuentes verificadas, fuentes candidatas y fuentes de descubrimiento;
4. documentar limitaciones de jurisdicción, vigencia, edición, licencia y alcance;
5. crear una lista de adquisición y mantenimiento de fuentes antes de publicar una versión estable.

Una cita aceptable debe responder estas preguntas mínimas:

- ¿quién emite la fuente?
- ¿qué versión, edición, documento, norma o fecha se está usando?
- ¿qué afirmación del handbook soporta?
- ¿para qué jurisdicción, línea de negocio, propósito y fecha aplica?
- ¿qué parte de la fuente se revisó?
- ¿qué no debe inferirse de esa fuente?

## 2. Jerarquía de evidencia

La regla central es simple: cuanto más normativa, financiera o decisoria sea una afirmación, más primaria debe ser su fuente.

| Nivel | Tipo de evidencia | Uso permitido | Ejemplos |
|---|---|---|---|
| `P1` | Fuente primaria oficial o contractual | Puede sostener obligaciones, definiciones normativas, políticas profesionales y requisitos de divulgación | leyes, decretos, resoluciones, circulares, ASOP oficiales, contratos, estados financieros auditados |
| `P2` | Literatura técnica revisada o publicación profesional reconocida | Puede sostener metodología, supuestos, fórmulas, limitaciones y comparaciones de modelos | artículos ASTIN, CAS monographs, libros técnicos, textos estadísticos |
| `P3` | Evidencia empírica reproducible del proyecto | Puede sostener resultados de ejemplos, benchmarks, pruebas y diagnósticos internos | notebooks, scripts, datos sintéticos, pruebas automatizadas, salidas versionadas |
| `P4` | Documentación de herramientas, vendors o plataformas | Puede sostener instrucciones de uso, APIs, parámetros y comportamiento de software | documentación de Python, R, SQL, librerías actuariales o visualización |
| `D` | Fuente de descubrimiento | Solo puede orientar búsqueda, hipótesis o agenda editorial | informes de investigación, notas de trabajo, conversaciones, resúmenes automáticos |

!!! danger "Regla de autoridad"
    Ninguna fuente `D` puede sostener una afirmación final del handbook. Si un informe de investigación menciona una norma, paper, dataset o entidad, el capítulo debe consultar y citar la fuente original antes de usar la afirmación.

## 3. Estados de verificación

Cada fuente debe tener un estado explícito. La presencia de un PDF o enlace no equivale a fuente verificada.

| Estado | Significado | Puede citarse en capítulos |
|---|---|---:|
| `V-L` | Verificada contra archivo local disponible en el workspace del proyecto | Sí, con sección/página cuando aplique |
| `V-O` | Verificada contra fuente oficial en línea, pero falta incorporar copia local o snapshot | Sí, con fecha de consulta y revisión de vigencia |
| `P` | Pendiente de adquisición, lectura completa o confirmación de versión | No para afirmaciones finales |
| `D` | Fuente secundaria de descubrimiento | No como autoridad |
| `H` | Fuente histórica, comparativa o de jurisdicción limitada | Solo si se declara la limitación |
| `R` | Reemplazada, obsoleta o no vigente para el propósito | No, salvo historia o contraste explícito |

La columna de estado puede combinar etiquetas. Por ejemplo, `V-L/H` significa que el archivo local fue verificado, pero su uso es histórico, comparativo o de alcance limitado.

## 4. Convenciones de citación

### 4.1 Claves canónicas

Las claves se escriben en mayúsculas, sin espacios, y deben ser estables aunque cambie el texto alrededor.

| Tipo de fuente | Formato recomendado | Ejemplo |
|---|---|---|
| ASOP | `ASB-ASOPNN-YYYY` | `ASB-ASOP28-2024` |
| Norma colombiana | `COL-ENTIDAD-YYYY-TIPO-NNNN` | `COL-MINSALUD-2026-RES-XXXX` |
| Dataset oficial | `COL-ENTIDAD-YYYY-DATASET` | `COL-ADRES-2026-UPC` |
| Artículo académico | `AUTOR-YYYY` | `MACK-1993` |
| Libro técnico | `AUTOR-YYYY-BOOK` | `WUTHRICH-MERZ-2008-BOOK` |
| Documento interno reproducible | `HIRH-YYYY-ARTEFACTO` | `HIRH-2026-SYNTHETIC-TRIANGLES` |
| Informe de descubrimiento | `DISC-ORIGEN-YYYY` | `DISC-GEMINI-2026` |

En el texto del capítulo, la clave debe acompañarse de la ubicación revisada cuando la afirmación sea material:

```markdown
La selección del modelo debe documentar propósito, datos, supuestos, limitaciones y validación (`ASB-ASOP56-2019`, secciones 3 y 4).
```

Si el proyecto adopta más adelante un procesador bibliográfico, estas claves pueden migrarse a BibTeX, CSL YAML o `references.yml` sin cambiar el cuerpo conceptual de los capítulos.

### 4.2 Citas en Markdown

Para documentos del repositorio:

- usar enlaces relativos cuando se cite otro capítulo;
- usar claves bibliográficas en backticks para fuentes externas;
- evitar URLs desnudas en el cuerpo del texto;
- incluir fecha de consulta para fuentes oficiales en línea;
- incluir página, sección, tabla, artículo o numeral cuando la afirmación sea sensible.

Ejemplo aceptable:

```markdown
En salud, las definiciones de pagado, reportado e incurrido deben reconciliarse contra el sistema fuente, la obligación contractual y el propósito de la valoración (`ASB-ASOP05-2017`, secciones 3.1-3.3; `ASB-ASOP23-2016`, secciones 3 y 4).
```

Ejemplo no aceptable:

```markdown
Según un informe de investigación, la reserva debe calcularse de cierta manera.
```

## 5. Registro maestro de fuentes profesionales

Esta tabla registra las fuentes profesionales que ya están incorporadas o priorizadas para el handbook. No todas tienen el mismo peso para salud, Colombia o claims reserving.

| Clave | Fuente canónica | Estado | Uso principal en el handbook | Limitaciones |
|---|---|---|---|---|
| `ASB-ASOP01-2013` | Actuarial Standards Board. (2013). *Introductory Actuarial Standard of Practice*. ASOP No. 1, Doc. No. 170. | `V-L` | marco general de propósito, juicio profesional, materialidad, desviaciones y lenguaje profesional | no define metodología específica de reservas |
| `ASB-ASOP05-2017` | Actuarial Standards Board. *Incurred Health and Disability Claims*. ASOP No. 5, Doc. No. 186. | `V-O` | fuente prioritaria para claims incurridos de salud y discapacidad | falta incorporar copia local; verificar versión vigente antes de release |
| `ASB-ASOP19-2005` | Actuarial Standards Board. (2005; deviation language effective 2011). *Appraisals of Casualty, Health, and Life Insurance Businesses*. ASOP No. 19, Doc. No. 137. | `V-L/H` | contexto para valoraciones de negocios de seguros y supuestos de appraisal | no es guía central de IBNR; uso comparativo o de gobierno |
| `ASB-ASOP22-2021` | Actuarial Standards Board. (2021). *Statements of Actuarial Opinion Based on Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities*. ASOP No. 22, Doc. No. 203. | `V-L` | opiniones basadas en asset adequacy analysis cuando involucran reservas de salud | no sustituye ASOP 5 para claims incurridos |
| `ASB-ASOP23-2016` | Actuarial Standards Board. *Data Quality*. ASOP No. 23, Doc. No. 185. | `V-O` | calidad de datos, dependencia de terceros, limitaciones, revisión y divulgaciones | falta incorporar copia local; verificar versión vigente antes de release |
| `ASB-ASOP28-2024` | Actuarial Standards Board. (2024). *Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities*. ASOP No. 28, Doc. No. 214. | `V-L` | opiniones actuariales sobre activos y pasivos de salud; gobierno de comunicación y alcance | no reemplaza la regulación colombiana ni define cálculo operativo de cada reserva |
| `ASB-ASOP38-2021` | Actuarial Standards Board. (2021). *Catastrophe Modeling (for All Practice Areas)*. ASOP No. 38, Doc. No. 201. | `V-L` | escenarios de pandemia, shocks de utilización, eventos extremos y modelos de catástrofe | usar solo cuando el modelo o escenario tenga naturaleza catastrófica o extrema |
| `ASB-ASOP41-2010` | Actuarial Standards Board. *Actuarial Communications*. ASOP No. 41. | `P` | comunicación, divulgaciones, limitaciones y dependencia de terceros | verificar versión vigente y actividad de exposure drafts antes de citar |
| `ASB-ASOP42-2018` | Actuarial Standards Board. *Health and Disability Actuarial Assets and Liabilities Other Than Liabilities for Incurred Claims*. ASOP No. 42. | `V-O` | activos y pasivos de salud distintos de liabilities por incurred claims | falta incorporar copia local; distinguir de ASOP 5 y ASOP 28 |
| `ASB-ASOP43-2007` | Actuarial Standards Board. (2007; deviation language effective 2011). *Property/Casualty Unpaid Claim Estimates*. ASOP No. 43, Doc. No. 159. | `V-L/H` | comparación con reserving P/C, unpaid claim estimates y lenguaje de incertidumbre | no es fuente primaria para salud; evitar trasladar supuestos sin justificación |
| `ASB-ASOP45-2012` | Actuarial Standards Board. (2012). *The Use of Health Status Based Risk Adjustment Methodologies*. ASOP No. 45, Doc. No. 164. | `V-L/H` | ajuste por riesgo, morbilidad, segmentación y comparación de poblaciones | revisar vigencia y aplicabilidad para esquemas colombianos |
| `ASB-ASOP50-2015` | Actuarial Standards Board. (2015). *Determining Minimum Value and Actuarial Value under the Affordable Care Act*. ASOP No. 50, Doc. No. 182. | `V-L/H` | contexto de valor actuarial bajo ACA y diseño de beneficios | jurisdicción estadounidense y alcance ACA; no generalizar a Colombia |
| `ASB-ASOP56-2019` | Actuarial Standards Board. (2019). *Modeling*. ASOP No. 56, Doc. No. 195. | `V-L` | gobierno de modelos, validación, sensibilidad, documentación, dependencia y divulgación | no prescribe un modelo específico ni garantiza suficiencia de datos |
| `ASB-ASOP57-2023` | Actuarial Standards Board. (2023). *Statements of Actuarial Opinion Not Based on an Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Related Actuarial Items*. ASOP No. 57, Doc. No. 208. | `V-L` | opiniones no basadas en asset adequacy analysis para reservas de vida, anualidades o salud | aplicar solo cuando el tipo de opinión corresponda |

### 5.1 Fuentes ASOP disponibles localmente

Las siguientes fuentes fueron verificadas contra los archivos locales adjuntos el 2026-07-14:

| Archivo local | ASOP | Páginas | Título abreviado | Documento |
|---|---:|---:|---|---|
| `project_sources/01-asop038_201.pdf` | 38 | 18 | Catastrophe Modeling | Doc. No. 201 |
| `project_sources/02-asop019_137.pdf` | 19 | 18 | Appraisals of Casualty, Health, and Life Insurance Businesses | Doc. No. 137 |
| `project_sources/03-asop028_214.pdf` | 28 | 26 | Health Insurance Assets and Liabilities | Doc. No. 214 |
| `project_sources/04-asop050_182.pdf` | 50 | 18 | Minimum Value and Actuarial Value under ACA | Doc. No. 182 |
| `project_sources/05-asop022_203.pdf` | 22 | 26 | Asset Adequacy Analysis | Doc. No. 203 |
| `project_sources/06-asop043_159.pdf` | 43 | 31 | Property/Casualty Unpaid Claim Estimates | Doc. No. 159 |
| `project_sources/07-asop056_195-1.pdf` | 56 | 37 | Modeling | Doc. No. 195 |
| `project_sources/08-asop045_164.pdf` | 45 | 19 | Health Status Based Risk Adjustment | Doc. No. 164 |
| `project_sources/09-asop001_170.pdf` | 1 | 23 | Introductory ASOP | Doc. No. 170 |
| `project_sources/10-asop057_208.pdf` | 57 | 14 | Opinions Not Based on Asset Adequacy Analysis | Doc. No. 208 |

## 6. Literatura metodológica central

La literatura metodológica sostiene fórmulas, supuestos, diagnósticos y comparaciones. Debe complementarse con fuentes profesionales cuando la afirmación pase de “método estadístico” a “trabajo actuarial aceptable”.

| Clave | Fuente canónica | Nivel | Estado | Uso principal | Observaciones |
|---|---|---|---|---|---|
| `BORN-FERGUSON-1972` | Bornhuetter, R. L., & Ferguson, R. E. (1972). *The Actuary and IBNR*. Proceedings of the Casualty Actuarial Society, 59. | `P2` | `P` | Bornhuetter-Ferguson, credibilidad implícita, combinación de experiencia y desarrollo | confirmar paginación exacta antes de cita final |
| `MACK-1993` | Mack, T. (1993). *Distribution-Free Calculation of the Standard Error of Chain Ladder Reserve Estimates*. ASTIN Bulletin, 23(2), 213-225. | `P2` | `V-O` | Mack chain ladder, MSEP, supuestos estocásticos, incertidumbre de estimación | fuente central para capítulos estocásticos |
| `ENGLAND-VERRALL-2002` | England, P. D., & Verrall, R. J. (2002). *Stochastic Claims Reserving in General Insurance*. British Actuarial Journal, 8(3), 443-518. | `P2` | `P` | bootstrap, GLM, reserving estocástico, comparación de marcos | distinguir general insurance de salud |
| `WUTHRICH-MERZ-2008-BOOK` | Wüthrich, M. V., & Merz, M. (2008). *Stochastic Claims Reserving Methods in Insurance*. Wiley. | `P2` | `P` | formulación estocástica, distribución predictiva, riesgo de proceso y parámetro | citar capítulo o sección al usar resultados específicos |
| `FRIEDLAND-2010` | Friedland, J. (2010). *Estimating Unpaid Claims Using Basic Techniques*. Casualty Actuarial Society. | `P2` | `P` | técnicas básicas, selección de factores, Bornhuetter-Ferguson, Cape Cod, diagnósticos | útil como puente pedagógico; verificar licencia de reproducción |
| `MCCULLAGH-NELDER-1989-BOOK` | McCullagh, P., & Nelder, J. A. (1989). *Generalized Linear Models* (2nd ed.). Chapman and Hall. | `P2` | `P` | GLM, familias exponenciales, enlace, deviance, IRLS | requiere extracción de capítulos relevantes |
| `WOOD-2017-BOOK` | Wood, S. N. (2017). *Generalized Additive Models: An Introduction with R* (2nd ed.). CRC Press. | `P2` | `P` | GAM, suavización, penalización, diagnóstico de suavizadores | no es fuente actuarial por sí sola |
| `GELMAN-ETAL-2013-BOOK` | Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press. | `P2` | `P` | modelos bayesianos, priors, posterior predictivo, validación | citar junto con literatura actuarial al aplicar a reserving |
| `HASTIE-TIBSHIRANI-FRIEDMAN-2009-BOOK` | Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. | `P2` | `P` | machine learning, regularización, árboles, ensembles, validación | no reemplaza reglas de validación temporal actuarial |
| `JAMES-ETAL-2021-BOOK` | James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning with Applications in R* (2nd ed.). Springer. | `P2` | `P` | explicación pedagógica de ML y validación | fuente de apoyo, no autoridad de reserving |

### 6.1 Regla para métodos clásicos

Los métodos clásicos no deben citarse solo por tradición. Cada capítulo debe identificar:

- fuente metodológica;
- supuesto estadístico o actuarial;
- medida modelada: pagado, incurrido reportado, allowed amount, número de reclamos u otra;
- definición de origen y desarrollo;
- diagnóstico que justificaría o rechazaría el método;
- sensibilidad de tail, factor de desarrollo, prior, exposición o mezcla de negocio;
- relación con ASOP 5, ASOP 23 y ASOP 56 cuando el capítulo hable de práctica profesional.

## 7. Fuentes regulatorias y operativas de Colombia

Las fuentes colombianas todavía requieren un registro primario detallado por norma, artículo, fecha de vigencia y entidad. Hasta completar esa extracción, este documento solo fija la política de admisión.

| Clave raíz | Entidad o fuente | Nivel | Uso previsto | Requisito antes de citar |
|---|---|---|---|---|
| `COL-MINSALUD-*` | Ministerio de Salud y Protección Social | `P1` | regulación sectorial, UPC, PBS, RIPS, operación del sistema, circulares o resoluciones aplicables | citar norma exacta, fecha, artículo y texto vigente |
| `COL-ADRES-*` | Administradora de los Recursos del Sistema General de Seguridad Social en Salud | `P1/P3` | flujos de compensación, pagos, bases o reportes oficiales | documentar dataset, corte, diccionario y limitaciones |
| `COL-SISPRO-*` | SISPRO y fuentes oficiales asociadas | `P1/P3` | datos, catálogos, reportes y definiciones operativas | conservar diccionario, corte, entidad responsable y versión |
| `COL-SUPERSALUD-*` | Superintendencia Nacional de Salud | `P1` | vigilancia, reportes, instrucciones, medidas y estados de entidades | identificar circular, resolución, informe o base oficial |
| `COL-SUIN-*` | SUIN-Juriscol u otro repositorio oficial normativo | `P1` | texto legal consolidado o histórico normativo | verificar que el texto corresponda a la vigencia usada |
| `COL-CAC-*` | Cuenta de Alto Costo | `P1/P2` | reportes técnicos, cohortes de alto costo, indicadores epidemiológicos | distinguir reporte descriptivo de obligación normativa |
| `COL-DANE-*` | DANE | `P1/P3` | inflación, población, demografía, mortalidad, contexto macro | citar serie, frecuencia, corte y método |
| `COL-CONTADURIA-*` | Contaduría General de la Nación | `P1` | criterios contables públicos cuando aplique | separar de regulación de aseguradoras privadas |
| `COL-SFC-*` | Superintendencia Financiera de Colombia | `P1` | aseguradoras vigiladas por SFC, instrucciones contables o financieras aplicables | no extrapolar a EPS sin análisis institucional |
| `COL-DIAN-*` | DIAN | `P1` | factura electrónica, documentos soporte y reglas tributarias relacionadas con datos | no tratar reglas tributarias como definición actuarial de incurred |
| `COL-PROESA-FASECOLDA-PVS-2021` | PROESA, con participación técnica de Fasecolda y ACEMI | `P2` | contexto, utilización, costos y política pública del mercado de planes voluntarios de salud | fuente institucional aplicada, no norma; citar periodo, muestra y página; no extrapolar sus resultados a la situación actual |

### 7.1 Regla para afirmaciones sobre Colombia

Una afirmación colombiana debe clasificarse antes de escribirse:

| Tipo de afirmación | Fuente mínima requerida |
|---|---|
| “La norma exige…” | norma oficial vigente, artículo o numeral, fecha de vigencia |
| “El dato se reporta así…” | manual, resolución, anexo técnico o diccionario oficial |
| “La entidad calcula…” | metodología oficial, acto administrativo o reporte institucional |
| “En la práctica algunas entidades…” | evidencia empírica documentada, muestra, periodo y limitación |
| “Para modelar conviene…” | literatura metodológica más justificación actuarial y validación local |

!!! warning "Separación jurisdiccional"
    ASOP 5, ASOP 23, ASOP 28 y ASOP 56 pueden orientar calidad profesional del trabajo, pero una obligación colombiana debe sostenerse en fuente colombiana. Si hay tensión entre marco profesional extranjero y norma local, el capítulo debe explicarla y escalarla a revisión experta.

### 7.2 Fuente institucional sobre planes voluntarios de salud

El archivo recibido como `SistemaSalud_Facecolda.pdf` corresponde a PROESA (2021),
*Análisis estratégico, rol en el sistema de salud y lineamientos de política pública para el
mercado de planes voluntarios de salud (PVS) en Colombia*. La ficha
`bibliography/COL-PROESA-FASECOLDA-PVS-2021.md` registra alcance, limitaciones y SHA-256.

El PDF no se redistribuye porque incluye una restricción expresa de reproducción. Su contenido
puede sustentar contexto sectorial cuando se cite página, periodo y población; no debe presentarse
como norma vigente, estándar actuarial ni descripción automática del mercado actual.

## 8. Informes de investigación adjuntos

Los tres informes adjuntos se registran como insumos de descubrimiento, no como autoridad final.

| Clave | Archivo | Estado | Uso permitido | Restricción |
|---|---|---|---|---|
| `DISC-GEMINI-2026` | `bibliography/gemini-deep-research-report.md` | `D` | inventario de temas, pistas de fuentes, mapa inicial de preguntas, identificación de posibles normas y datasets | cada cita mencionada debe verificarse contra su fuente original antes de entrar a un capítulo |
| `DISC-CHATGPT-2026` | `bibliography/chatgpt-deep-research-report.md` | `D` | estructura conceptual, comparación internacional, hipótesis y preguntas editoriales | versión actualizada el 2026-07-18; sus referencias y cifras requieren verificación primaria |
| `DISC-CLAUDE-2026` | `bibliography/claude-deep-research-report.md` | `D` | mapa del estado del arte, brechas del SGSSS y fuentes candidatas | no usar sus conclusiones, cifras ni clasificación de evidencia como autoridad sin leer la fuente original |

### 8.1 Cómo convertir una fuente de descubrimiento en fuente admitida

Cuando un informe de investigación mencione una referencia útil, el editor debe:

1. localizar la fuente original;
2. confirmar autor o entidad emisora;
3. confirmar título, fecha, edición, versión y enlace oficial;
4. leer la sección específica que soporta la afirmación;
5. decidir nivel de evidencia y jurisdicción;
6. crear clave bibliográfica;
7. registrar limitaciones;
8. actualizar este archivo antes de citarla en capítulos.

## 9. Mapa de fuentes por bloque del handbook

Este mapa indica qué fuentes deberían revisarse antes de estabilizar cada bloque. No reemplaza las citas internas de cada capítulo.

| Bloque | Capítulos | Fuentes mínimas | Fuentes complementarias |
|---|---|---|---|
| Fundamentos | 01-05 | `ASB-ASOP05-2017`, `ASB-ASOP23-2016`, `FRIEDLAND-2010` | `ASB-ASOP01-2013`, `ASB-ASOP56-2019` |
| Métodos clásicos | 06-07, 11-14 | `FRIEDLAND-2010`, `BORN-FERGUSON-1972`, `ASB-ASOP05-2017` | `ASB-ASOP23-2016`, `ASB-ASOP56-2019` |
| Reserving estocástico | 08-10 | `MACK-1993`, `ENGLAND-VERRALL-2002`, `WUTHRICH-MERZ-2008-BOOK` | `ASB-ASOP56-2019`, `ASB-ASOP23-2016` |
| Modelos estadísticos | 15-17 | `MCCULLAGH-NELDER-1989-BOOK`, `WOOD-2017-BOOK`, `GELMAN-ETAL-2013-BOOK` | `ENGLAND-VERRALL-2002`, `ASB-ASOP56-2019` |
| Machine learning | 18-19 | `HASTIE-TIBSHIRANI-FRIEDMAN-2009-BOOK`, `JAMES-ETAL-2021-BOOK`, `ASB-ASOP56-2019` | `ASB-ASOP23-2016`, fuentes de fairness, drift y validación temporal por incorporar |
| Salud específico | 20 y capítulos health-specific futuros | `ASB-ASOP05-2017`, `ASB-ASOP28-2024`, `ASB-ASOP42-2018`, `ASB-ASOP45-2012` | fuentes clínicas, utilización, network contracting y risk adjustment por incorporar |
| Colombia | 21-25 y migración futura | `COL-MINSALUD-*`, `COL-ADRES-*`, `COL-SISPRO-*`, `COL-SUPERSALUD-*` | `COL-CAC-*`, `COL-DANE-*`, contratos, políticas internas |
| Gobierno y opinión actuarial | capítulos 40-46 futuros | `ASB-ASOP28-2024`, `ASB-ASOP41-2010`, `ASB-ASOP56-2019`, `ASB-ASOP57-2023` | `ASB-ASOP22-2021`, normativa local y requisitos de reporte |
| Implementación y pruebas | capítulos 47-50 futuros | `ASB-ASOP23-2016`, `ASB-ASOP56-2019`, evidencia `P3` del repositorio | documentación de librerías y ambientes reproducibles |

## 10. Plantilla de registro de fuente

Toda fuente nueva debe registrarse con una ficha mínima. La plantilla puede convertirse más adelante en `docs/_data/sources.yml`.

```yaml
id: ASB-ASOP28-2024
title: Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities
authors_or_issuer:
  - Actuarial Standards Board
type: professional_standard
evidence_tier: P1
status: V-L
jurisdiction:
  - United States professional actuarial practice
practice_area:
  - health insurance
  - actuarial opinion
version_or_edition: Revised Edition
document_number: Doc. No. 214
publication_or_adoption_date: 2024-04
retrieved_or_verified_on: 2026-07-14
source_location:
  local_file: project_sources/03-asop028_214.pdf
  official_url: null
chapters:
  - part-06-health-specific/21-health-insurance-reserving-specificities.md
  - part-07-colombia/29-colombia-health-reserving-methodologies.md
  - future-governance-chapters
claim_types_supported:
  - professional-scope
  - actuarial-opinion
  - communication-and-disclosure
limitations:
  - Not Colombian regulation.
  - Does not prescribe a single reserving method.
review_due: before-v1.0-release
```

## 11. Reglas de admisión por tipo de fuente

### 11.1 Estándares profesionales

Un estándar profesional se puede admitir cuando:

- proviene del emisor oficial;
- se conoce número, edición, fecha de adopción o vigencia y documento;
- se revisó si existe una versión más reciente, exposición pública o reemplazo;
- se documenta la jurisdicción profesional;
- se indica si el estándar es central, complementario, histórico o comparativo.

### 11.2 Normativa

Una norma se puede admitir cuando:

- proviene de fuente oficial o repositorio normativo confiable;
- se identifica tipo de norma, número, fecha, entidad emisora y vigencia;
- se registra si el texto está compilado, modificado, derogado o sujeto a transición;
- se cita artículo, numeral, anexo o sección específica;
- se distingue obligación legal de interpretación actuarial.

### 11.3 Literatura académica y profesional

Una fuente metodológica se puede admitir cuando:

- se conoce autor, año, título, publicación, editorial o institución;
- se confirma si es artículo, libro, monografía, paper de trabajo o presentación;
- se registra el resultado que soporta;
- se identifica si aplica a general insurance, health, life, P/C o un contexto más amplio;
- se evitan citas decorativas que no soportan una afirmación concreta.

### 11.4 Datos y artefactos reproducibles

Un dataset, notebook o salida del repositorio se puede citar cuando:

- tiene propietario, fecha de corte, diccionario y reglas de transformación;
- se conoce si es sintético, público, privado, anonimizado o agregado;
- tiene script reproducible o procedimiento de generación;
- pasa controles mínimos de calidad;
- registra semilla, versión, ambiente y checksums cuando aplique.

## 12. Checklist de citación para autores

Antes de cerrar un capítulo, el autor debe confirmar:

- [ ] Todas las afirmaciones regulatorias tienen fuente oficial y fecha de vigencia.
- [ ] Las afirmaciones sobre ASOP citan número, año, documento y sección.
- [ ] Las fuentes de descubrimiento no aparecen como autoridad final.
- [ ] Los métodos tienen fuente metodológica y limitaciones.
- [ ] Las fórmulas copiadas o adaptadas respetan licencia y atribución.
- [ ] Las definiciones coinciden con [glossary.md](glossary.md) o justifican la diferencia.
- [ ] Los enlaces relativos funcionan dentro de MkDocs.
- [ ] Las URLs externas no aparecen desnudas en el cuerpo del texto.
- [ ] Los datasets citados tienen corte, diccionario y proceso de extracción.
- [ ] Las conclusiones diferencian evidencia, juicio actuarial e hipótesis.

## 13. Fuentes pendientes de incorporación prioritaria

Estas fuentes deben incorporarse antes de declarar estable la versión 1.0.

| Prioridad | Fuente | Motivo | Acción requerida |
|---|---|---|---|
| P0 | ASOP 5 | base profesional directa para incurred health and disability claims | incorporar PDF oficial, registrar secciones y mapearlo a capítulos 01, 02, 20 y Colombia |
| P0 | ASOP 23 | calidad de datos transversal | incorporar PDF oficial, extraer checklist de data quality y dependencia de terceros |
| P0 | fuentes colombianas exactas | necesarias para capítulos 21-25 y futura parte health-specific Colombia | construir registro por norma, artículo, vigencia y entidad |
| P1 | ASOP 41 | comunicaciones actuariales | verificar versión vigente y exposure drafts antes de citar |
| P1 | ASOP 42 | activos y pasivos de salud distintos de incurred claims | incorporar PDF oficial y separar de ASOP 5 |
| P1 | Bornhuetter-Ferguson original | fuente histórica del método | confirmar paginación y referencia exacta |
| P1 | CAS/Friedland | técnicas básicas y exposición pedagógica | confirmar licencia, edición y secciones |
| P2 | documentación de librerías | reproducibilidad de código | registrar versiones de Python, R, SQL y paquetes |
| P2 | fuentes de validación ML | leakage, drift, calibration, fairness y explainability | seleccionar literatura y documentación técnica aplicable |

## 14. Política de mantenimiento

La bibliografía debe revisarse:

- antes de cada release;
- cuando se agregue o renombre un capítulo;
- cuando una norma colombiana cambie o sea reemplazada;
- cuando el ASB publique nueva edición, revisión o exposure draft relevante;
- cuando se incorporen datos oficiales nuevos;
- cuando un capítulo cambie de `Draft` a `Technical review`;
- como mínimo cada 90 días para fuentes regulatorias colombianas activas;
- como mínimo una vez al año para literatura metodológica y estándares profesionales.

Todo cambio material debe registrar:

- fuente agregada, reemplazada o retirada;
- motivo del cambio;
- capítulos afectados;
- reclamos o afirmaciones que deben revisarse;
- responsable de revisión técnica;
- fecha de próxima revisión.

## 15. Decisiones editoriales abiertas

| Decisión | Opciones | Recomendación inicial |
|---|---|---|
| Motor de referencias | Markdown manual, BibTeX, CSL YAML, `references.yml` | comenzar manual; migrar a YAML cuando haya más de 50 fuentes admitidas |
| Citas por página o sección | obligatorias siempre, obligatorias solo para claims sensibles | obligatorias para normas, ASOP y afirmaciones cuantitativas |
| Snapshots oficiales | guardar PDFs locales, guardar metadatos y enlaces, ambos | ambos, cuando la licencia lo permita |
| Fuentes de Colombia | por capítulo o registro central | registro central más citas específicas en cada capítulo |
| Informes de investigación | anexos, fuentes `D`, o exclusión | conservar como fuentes `D` para trazabilidad |

## 16. Definición de terminado para este archivo

`docs/bibliography.md` puede pasar de `Draft` a `Technical review` cuando:

- ASOP 5, 23, 41 y 42 estén incorporados o tengan justificación documentada de exclusión temporal;
- exista un registro inicial de fuentes colombianas exactas;
- cada capítulo existente tenga al menos sus fuentes mínimas asignadas;
- el `mkdocs.yml` incluya este archivo en navegación;
- los enlaces internos pasen validación;
- un revisor técnico confirme que los informes de investigación no se usan como autoridad.

Puede pasar a `Validated` cuando:

- todos los capítulos publicados cumplan la checklist de citación;
- las fuentes regulatorias vigentes estén verificadas contra fuente oficial;
- las referencias metodológicas tengan edición, páginas o secciones suficientes;
- las licencias de reproducción de tablas, fórmulas y fragmentos estén documentadas;
- el repositorio pueda reconstruir ejemplos y salidas citadas.

## 17. Referencias registradas

### 17.1 Estándares actuariales

- `ASB-ASOP01-2013`: Actuarial Standards Board. (2013). *Introductory Actuarial Standard of Practice*. ASOP No. 1, Doc. No. 170.
- `ASB-ASOP05-2017`: Actuarial Standards Board. *Incurred Health and Disability Claims*. ASOP No. 5, Doc. No. 186.
- `ASB-ASOP19-2005`: Actuarial Standards Board. (2005; updated for deviation language effective 2011). *Appraisals of Casualty, Health, and Life Insurance Businesses*. ASOP No. 19, Doc. No. 137.
- `ASB-ASOP22-2021`: Actuarial Standards Board. (2021). *Statements of Actuarial Opinion Based on Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities*. ASOP No. 22, Doc. No. 203.
- `ASB-ASOP23-2016`: Actuarial Standards Board. *Data Quality*. ASOP No. 23, Doc. No. 185.
- `ASB-ASOP28-2024`: Actuarial Standards Board. (2024). *Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities*. ASOP No. 28, Doc. No. 214.
- `ASB-ASOP38-2021`: Actuarial Standards Board. (2021). *Catastrophe Modeling (for All Practice Areas)*. ASOP No. 38, Doc. No. 201.
- `ASB-ASOP41-2010`: Actuarial Standards Board. *Actuarial Communications*. ASOP No. 41.
- `ASB-ASOP42-2018`: Actuarial Standards Board. *Health and Disability Actuarial Assets and Liabilities Other Than Liabilities for Incurred Claims*. ASOP No. 42.
- `ASB-ASOP43-2007`: Actuarial Standards Board. (2007; updated for deviation language effective 2011). *Property/Casualty Unpaid Claim Estimates*. ASOP No. 43, Doc. No. 159.
- `ASB-ASOP45-2012`: Actuarial Standards Board. (2012). *The Use of Health Status Based Risk Adjustment Methodologies*. ASOP No. 45, Doc. No. 164.
- `ASB-ASOP50-2015`: Actuarial Standards Board. (2015). *Determining Minimum Value and Actuarial Value under the Affordable Care Act*. ASOP No. 50, Doc. No. 182.
- `ASB-ASOP56-2019`: Actuarial Standards Board. (2019). *Modeling*. ASOP No. 56, Doc. No. 195.
- `ASB-ASOP57-2023`: Actuarial Standards Board. (2023). *Statements of Actuarial Opinion Not Based on an Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Related Actuarial Items*. ASOP No. 57, Doc. No. 208.

### 17.2 Métodos actuariales y estadísticos

- `BORN-FERGUSON-1972`: Bornhuetter, R. L., & Ferguson, R. E. (1972). *The Actuary and IBNR*. Proceedings of the Casualty Actuarial Society, 59.
- `ENGLAND-VERRALL-2002`: England, P. D., & Verrall, R. J. (2002). *Stochastic Claims Reserving in General Insurance*. British Actuarial Journal, 8(3), 443-518.
- `FRIEDLAND-2010`: Friedland, J. (2010). *Estimating Unpaid Claims Using Basic Techniques*. Casualty Actuarial Society.
- `GELMAN-ETAL-2013-BOOK`: Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- `HASTIE-TIBSHIRANI-FRIEDMAN-2009-BOOK`: Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.
- `JAMES-ETAL-2021-BOOK`: James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning with Applications in R* (2nd ed.). Springer.
- `MACK-1993`: Mack, T. (1993). *Distribution-Free Calculation of the Standard Error of Chain Ladder Reserve Estimates*. ASTIN Bulletin, 23(2), 213-225.
- `MCCULLAGH-NELDER-1989-BOOK`: McCullagh, P., & Nelder, J. A. (1989). *Generalized Linear Models* (2nd ed.). Chapman and Hall.
- `WOOD-2017-BOOK`: Wood, S. N. (2017). *Generalized Additive Models: An Introduction with R* (2nd ed.). CRC Press.
- `WUTHRICH-MERZ-2008-BOOK`: Wüthrich, M. V., & Merz, M. (2008). *Stochastic Claims Reserving Methods in Insurance*. Wiley.

### 17.3 Insumos de descubrimiento

- `DISC-GEMINI-2026`: *Deep research report* adjunto al proyecto. Uso permitido: descubrimiento de temas y fuentes candidatas.
- `DISC-CHATGPT-2026`: *Modernizing Health Actuarial Practices: Global Lessons for Colombia*. Informe de investigación actualizado el 2026-07-18. Uso permitido: estructura conceptual, hipótesis y preguntas editoriales.
- `DISC-CLAUDE-2026`: *Actuaría aplicada al sector salud: estado del arte mundial y hoja de ruta para el fortalecimiento actuarial del SGSSS de Colombia*. Informe de investigación de julio de 2026. Uso permitido: descubrimiento y priorización de fuentes originales.

### 17.4 Fuente institucional colombiana

- `COL-PROESA-FASECOLDA-PVS-2021`: PROESA. (2021). *Análisis estratégico, rol en el sistema de salud y lineamientos de política pública para el mercado de planes voluntarios de salud (PVS) en Colombia: informe final de consultoría*. Participación técnica de Fasecolda y ACEMI. Uso admitido: contexto sectorial e investigación aplicada, con cita de página, periodo y muestra.
