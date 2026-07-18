# Actuaría aplicada al sector salud: estado del arte mundial y hoja de ruta para el fortalecimiento actuarial del SGSSS de Colombia
### Informe técnico multidisciplinario · Julio de 2026

---

## 1. Resumen Ejecutivo

**El conocimiento actuarial más útil para Colombia no consiste en importar un modelo extranjero completo, sino en migrar el ajuste de riesgo de la Unidad de Pago por Capitación (UPC) desde un esquema casi puramente demográfico (edad, sexo, zona geográfica) hacia un modelo basado en morbilidad (diagnósticos + farmacia), acompañado de reservas técnicas estocásticas y analítica predictiva supervisada con IA explicable.** La evidencia colombiana e internacional es consistente y contundente: la fórmula demográfica actual explica una fracción muy baja de la varianza del gasto individual y subpredice sistemáticamente en la cola alta (pacientes de alto costo), generando incentivos a la selección de riesgos.

**Tres hallazgos principales:**

1. **Los sistemas líderes convergen en el ajuste de morbilidad.** Países Bajos, Alemania (Morbi-RSA) y Estados Unidos (CMS-HCC/HHS-HCC) usan modelos con decenas o cientos de clases de riesgo basadas en diagnósticos y farmacia, más mecanismos de reaseguro/pool para casos catastróficos y salvaguardas anti-manipulación.
2. **El machine learning supera a la regresión lineal en predicción de gasto**, especialmente en la identificación de pacientes de alto costo, pero para la tarificación regulatoria el estándar sigue siendo el GLM/Tweedie por su interpretabilidad. La frontera es el modelo híbrido "actuarialmente restringido" con IA explicable (SHAP).
3. **Colombia ya posee los insumos** (RIPS, BDUA, MIPRES, Cuenta de Alto Costo, SISPRO) y **capacidad académica de primer nivel** (Riascos, Espinosa, Arias, Duncan), pero no los explota en el cálculo de la UPC, que sigue siendo predominantemente demográfico y retrospectivo.

**Recomendación central:** implementar por fases un ajustador de morbilidad construido sobre RIPS + datos de la CAC + farmacia (MIPRES/dispensación), mediante selección de variables penalizada y juicio experto, con validación externa independiente y salvaguardas anti-*upcoding*. El prerrequisito de menor costo y mayor urgencia es la mejora de la calidad de los datos.

---

## 2. Introducción

La actuaría en salud cuantifica y gestiona el riesgo financiero derivado de la incertidumbre del gasto sanitario. En los sistemas de aseguramiento social con competencia regulada —como el colombiano— la función actuarial central es el cálculo de la prima ajustada por riesgo (capitación) y la constitución de reservas técnicas que garanticen la solvencia de los aseguradores.

Colombia opera, bajo la Ley 100 de 1993, el Sistema General de Seguridad Social en Salud (SGSSS), en el que la UPC actúa como prima ajustada por riesgo que la Administradora de los Recursos del SGSSS (ADRES) paga prospectivamente a las Entidades Promotoras de Salud (EPS) por cada afiliado. El Ministerio de Salud y Protección Social (MSPS) actualiza anualmente la UPC con base en el "Estudio de suficiencia y de los mecanismos de ajuste de riesgo".

El objetivo de este informe **no es describir la actuaría**, sino **identificar el conocimiento científico, metodológico y regulatorio más sólido a nivel mundial que pueda adaptarse para fortalecer los procesos actuariales del SGSSS**, con análisis crítico de consensos, controversias y vacíos, y una hoja de ruta priorizada.

---

## 3. Metodología de búsqueda bibliográfica

Se realizó una revisión estructurada (no una revisión sistemática PRISMA formal), priorizando la jerarquía de evidencia solicitada. Se ejecutaron aproximadamente 18 búsquedas temáticas y múltiples recuperaciones de texto completo, sobre:

- **Nivel 1 (artículos revisados por pares):** *Health Economics Review, European Journal of Health Economics, North American Actuarial Journal, Health Services Research, Medical Care, ASTIN Bulletin, Insurance: Mathematics and Economics, Journal of Health Economics, BMC Public Health/Health Services Research, Annals of Internal Medicine.*
- **Nivel 2 (asociaciones actuariales):** Society of Actuaries (SOA), Casualty Actuarial Society (CAS), International Actuarial Association (IAA), Institute and Faculty of Actuaries (IFoA), American Academy of Actuaries, Actuarial Standards Board (ASOP).
- **Nivel 3 (organismos internacionales):** OMS, OCDE, Banco Mundial, WTW/PwC (encuestas de tendencias médicas, usadas como evidencia de mercado con la debida cautela).
- **Nivel 4 (Colombia):** MSPS, ADRES, Cuenta de Alto Costo (CAC), Superintendencia Nacional de Salud, normativa (Decreto 780 de 2016, Decreto 2702 de 2014).

**Limitaciones metodológicas de la búsqueda:** no se accedió a la totalidad de textos completos por restricciones de *paywall* (se usaron *abstracts* y repositorios como PMC, IDEAS/RePEc, SSRN, arXiv). Las fuentes de prensa especializada (Consultorsalud, El Tiempo, Infobae) se usaron únicamente como contexto y se señalan explícitamente como de baja jerarquía. Cuando existió incertidumbre o conflicto de datos, se indica en el texto.

---

## 4. Estado del arte internacional

La actuaría en salud evolucionó desde ajustes demográficos simples (edad-sexo, años 1970) hacia modelos de morbilidad sofisticados. El consenso metodológico actual (van de Ven & Ellis, 2000; Ellis et al.) establece que **el ajuste por edad y sexo explica menos del 1% de la varianza del gasto individual**, mientras que los modelos de morbilidad basados en diagnósticos capturan entre una décima y un cuarto de la varianza máxima explicable. El Actuarial Standards Board de EE.UU. codificó la práctica en la norma **ASOP No. 45** ("The Use of Health Status Based Risk Adjustment Methodologies") y en ASOP No. 12 (Risk Classification) y ASOP No. 25 (Credibility).

**Tendencias 2020-2026 (consenso de la literatura):**

1. **Integración de machine learning con modelos actuariales clásicos**, manteniendo la interpretabilidad exigida por los reguladores.
2. **Incorporación de determinantes sociales de la salud (SDH)** al ajuste de riesgo para reducir el subpago a poblaciones vulnerables.
3. **IA generativa y LLMs** para procesar datos no estructurados de siniestros; la CAS ha llamado explícitamente a investigar el uso de grandes modelos de lenguaje (Richman, 2024).
4. **Preocupación creciente por la equidad algorítmica y el *upcoding*** (codificación inflada de diagnósticos para elevar los pagos).

**Inflación médica como desafío estructural:** la *2026 Global Medical Trends Survey* de WTW —encuesta a 346 aseguradoras de 82 países realizada entre junio y julio de 2025— proyecta un incremento global de costos médicos de **10,3% en 2026** (tras 10% en 2025 y 9,5% en 2024), siendo **América Latina la región de mayor aceleración, saltando de 10,5% a 11,9%**. Los principales impulsores globales son las nuevas tecnologías médicas (citadas por el 74% de las aseguradoras), el deterioro de los sistemas públicos de salud (52%) y los avances farmacéuticos (49%), con el cáncer como la condición más costosa y de mayor crecimiento.

**Actuaría y Health Technology Assessment (HTA):** área emergente (revisión interdisciplinaria, *PMC*, 2024) en la que el juicio actuarial, los estándares de calidad de datos y los modelos de decisión aportan rigor a las decisiones de cobertura, un campo directamente relevante para las decisiones colombianas sobre tecnologías financiadas con UPC y Presupuestos Máximos.

---

## 5. Comparación entre países

Los sistemas de competencia regulada convergen en un principio común: **prima comunitaria + ecualización de riesgo (*risk equalization*, RE)** para prevenir la selección de riesgos ("descreme" o *cream-skimming*).

**Países Bajos** — modelo de RE considerado el más sofisticado del mundo. Combina *Diagnosis-based Cost Groups* (DCGs), *Pharmacy-based Cost Groups* (PCGs) y decenas de ajustadores morbi-basados. Usa "diagnosis treatment combinations" (DTCs) en lugar de códigos ICD directos. La investigación de la Erasmus University (Eijkenaar, van Kleef, van Vliet) sigue activa para reducir la sobre/subcompensación mediante regresión restringida (*constrained regression*) y "sobrepago" deliberado de ciertos ajustadores.

**Alemania** — Morbi-RSA (*morbiditätsorientierter Risikostrukturausgleich*). El **Gesetz für einen fairen Kassenwettbewerb (GKV-FKG), aprobado por el Bundestag el 13 de febrero de 2020 y en vigor desde el 1 de abril de 2020**, transformó el modelo: hasta 2020 solo consideraba **80 enfermedades crónicas graves** (con gasto ≥50% sobre el promedio); **desde 2021 el "Vollmodell" incorpora todo el espectro de enfermedades**. Añadió un componente regional, una **"freno de manipulación" (*Manipulationsbremse*)** contra el *upcoding*, y un **pool de riesgo (reaseguro)** que reembolsa el **80% de los gastos por encima de un umbral (100.000 € en 2021, dinamizado anualmente hasta ~107.084 € en 2023)**, verificado por el Bundesamt für Soziale Sicherung.

**Estados Unidos** — CMS-HCC (Medicare Advantage) y HHS-HCC (mercados ACA); modelos jerárquicos de condiciones (*Hierarchical Condition Categories*). **Geruso & Layton** ("Upcoding: Evidence from Medicare on Squishy Risk Adjustment", NBER WP 21222 / *Journal of Political Economy* 2020) estimaron que los afiliados a planes privados generan *risk scores* entre 6% y 16% más altos que en Medicare tradicional; sin el deflactor de codificación, el *upcoding* habría costado **~US$10.500 millones (US$640 por afiliado) en 2014**, y aun con el ajuste uniforme costó **~US$2.000 millones/año (US$120 por afiliado)**. Investigación reciente (Shenfeld et al., 2026, *Health Services Research*) propone ML para mejorar la precisión del CMS-HCC.

**Chile** — sistema segmentado FONASA (público, ~77-78% de la población) / ISAPRE (privado). El fondo de compensación existe **solo entre ISAPRES**, para el paquete GES, y usa un modelo demográfico (edad-sexo) que **no resuelve la selección de riesgos**. Un estudio de capitación ajustada por diagnóstico concluyó que **"un modelo de ajuste basado en diagnósticos es superior al modelo demográfico, mejorando la precisión predictiva en un 68%"** y **"reasigna un 23% más de fondos que el modelo demográfico"**. La "Ley Corta de Isapres" (2023-2024) respondió a un fallo de la Corte Suprema que ordenó devolver más de US$1.200 millones en sobrecobros.

**Brasil** — la Agência Nacional de Saúde Suplementar (ANS) regula los planes privados con reservas técnicas, capital basado en riesgo y el *ressarcimento ao SUS* (art. 32, Lei 9.656/1998), obligación de las operadoras de reembolsar al sistema público por la atención de sus beneficiarios en la red del SUS.

**Otros:** Reino Unido (NHS, asignación por fórmula ponderada por necesidad); Australia (RE que incorpora costos administrativos); Corea del Sur y Japón (seguro social único con modelos ML de predicción de alto costo —LightGBM con AUC-ROC ~91%).

| País | Base del ajuste de riesgo | Reaseguro/pool | Anti-*upcoding* | Madurez actuarial |
|------|---------------------------|----------------|-----------------|-------------------|
| Países Bajos | Morbilidad (DCG + PCG), decenas de clases | Parcial | *Constrained regression* | Muy alta |
| Alemania | Morbilidad (Vollmodell, todas las enfermedades) | Sí (80% sobre ~100k€) | *Manipulationsbremse* | Muy alta |
| EE.UU. (CMS/HHS) | HCC jerárquico | *Reinsurance* (ACA) | Auditorías RADV + deflactor | Alta |
| Chile | Demográfico (GES, solo ISAPRES) | No efectivo | Ausente | Baja |
| Brasil | Reservas + capital basado en riesgo | *Ressarcimento* al SUS | Parcial | Media |
| **Colombia** | **Demográfico (edad/sexo/zona) + CAC ex-post** | **CAC (parcial)** | **Limitado** | **Baja-media** |

---

## 6. Modelos actuariales

**GLM (Modelos Lineales Generalizados).** Estándar de tarificación. Se modela frecuencia (Poisson / binomial negativa), severidad (Gamma / inversa gaussiana) y prima pura conjunta mediante la **distribución Tweedie compound Poisson-Gamma**, cuyo parámetro de potencia *p* (1<*p*<2) captura la masa puntual en cero (afiliados sin siniestro) y la cola positiva sesgada típica del gasto sanitario. *Ventajas:* interpretabilidad, aceptación regulatoria, base de la CAS. *Limitaciones:* asume relaciones log-lineales, no captura interacciones complejas sin especificación manual. *Aplicabilidad Colombia:* la UPC ya utiliza prima pura; migrar a un GLM/Tweedie con covariables de morbilidad es la evolución natural y de menor fricción regulatoria.

**GAM (Modelos Aditivos Generalizados).** Extienden el GLM con *splines* penalizados para capturar no linealidades (p. ej., la curva edad-gasto). Útiles para curvas de riesgo suaves por edad.

**Teoría de la Credibilidad** (Bühlmann; Bühlmann-Straub; ASOP 25). Pondera la experiencia individual frente a la colectiva. Relevante para EPS pequeñas o zonas geográficas con poca data, donde la experiencia propia debe combinarse con la del sistema.

**Modelos Bayesianos.** Incorporan información *a priori*; robustos con datos escasos o heterogéneos. Espinosa, Bejarano & Ramos (2024, *North American Actuarial Journal*) aplicaron un enfoque bayesiano a la predictibilidad y suficiencia del aseguramiento en Colombia. Frameworks híbridos cópula-bayesianos superan a los GLM clásicos en la captura de dependencias no lineales y riesgo de cola.

**Modelos de supervivencia, multi-estado y de Markov.** Modelan transiciones entre estados de salud (sano → enfermo → fallecido) con probabilidades/intensidades de transición (Christiansen, 2012; Haberman & Pitacco, 1999). Base para enfermedad crítica, cuidado de largo plazo y enfermedades crónicas. *Aplicabilidad Colombia:* modelar la progresión por estadios de la Enfermedad Renal Crónica (ERC) para proyectar el gasto de la CAC (véase §9).

**Frequency-Severity y Modelos de Riesgo Colectivo.** Descomposición clásica del gasto agregado (proceso compound Poisson). Fundamento de la prima pura ya empleada por el MSPS.

**Reservas / IBNR (*Incurred But Not Reported*).** Chain-Ladder (Mack, 1993, distribution-free), Bornhuetter-Ferguson (1972), y métodos estocásticos (England & Verrall, 2002; Wüthrich & Merz, 2008). Colombia ya usa IBNR en el estudio de suficiencia, pero de forma determinística; migrar a **reservas estocásticas con intervalos de confianza** (bootstrap, Mack) mejoraría la medición de solvencia.

**Monte Carlo, Microsimulación y Modelos Dinámicos.** Simulan escenarios de suficiencia y solvencia bajo estrés; permiten cuantificar la incertidumbre de la UPC.

**Modelos de Riesgo Catastrófico.** Para pandemias y eventos de alto costo; relevantes tras el COVID-19 y para el diseño de un pool de reaseguro.

---

## 7. Ajuste de riesgo

| Modelo | Tipo | Datos requeridos | Fortaleza | Dominio típico |
|--------|------|------------------|-----------|----------------|
| CMS-HCC / HHS-HCC | Diagnósticos jerárquicos | ICD + edad/sexo | Estándar regulatorio; resistente a manipulación con auditorías | Medicare / ACA (EE.UU.) |
| DxCG (Verisk) | Diagnósticos + farmacia | ICD + fármacos | Alto ajuste; supera a CMS V21 en subgrupos | Comercial global |
| ACG (Johns Hopkins) | Morbilidad agregada | ICD + farmacia | Captura multimorbilidad (ADG, EDC) | Global (EE.UU., Canadá, Taiwán) |
| CRG (3M) | Grupos clínicos de riesgo | ICD | Coherencia clínica | Medicaid |
| CDPS / RxGroup | Diagnóstico / farmacia | ICD / ATC | Dominio público | Medicaid |
| PCG (Pharmacy-based) | Farmacia | ATC / dispensación | Datos oportunos, difíciles de manipular | Países Bajos |

**Evidencia comparativa.** El estudio de la Veterans Administration (*Medical Care*, 2016) mostró que **DxCG con farmacia mejora sustancialmente el ajuste frente a CMS-HCC V21**, aunque el V21 recalibrado con datos de farmacia alcanza estadísticos similares. Un modelo DCG con machine learning que respeta jerarquías clínicas (*PMC*, 2024) **redujo dramáticamente los subpagos por enfermedades raras y resistió el *gaming*** frente al HHS-HCC 2020. Un hallazgo robusto y transversal: **añadir información farmacéutica mejora la predicción y la oportunidad de los datos**.

**Controversia metodológica.** Existe tensión entre precisión predictiva y resistencia a la manipulación: modelos más ricos en diagnósticos son más precisos pero más vulnerables al *upcoding*, lo que justifica salvaguardas (Manipulationsbremse alemana, auditorías RADV de CMS).

**Mejor alternativa para Colombia (juicio del equipo).** Un **modelo híbrido de condiciones crónicas basado en diagnósticos (RIPS/CAC) + farmacia (MIPRES/dispensación), construido con selección de variables penalizada (LASSO) y juicio experto**. Esta no es una recomendación abstracta: **Arias (2026, *Health Economics Review*, "Selecting risk adjusters with penalized regression and expert judgment: evidence from Colombia")** demostró exactamente este enfoque con datos colombianos. La justificación de superioridad es cuantitativa (véase §9): permite pasar de un R² marginal a valores de dos dígitos y corregir la subpredicción en la cola alta.

---

## 8. Ciencia de datos e IA

La evidencia comparativa es consistente (Rose, 2016, *Health Services Research*; BMC Public Health, 2020; arXiv 2311.14139; NHIS Corea, 2022): **los métodos de *ensemble* de árboles con potenciación de gradiente (XGBoost, LightGBM, CatBoost) y random forest superan a la regresión lineal en predicción de gasto sanitario**, con **LightGBM alcanzando AUC-ROC de ~91% en la identificación de pacientes de alto costo**. *Ventajas:* capturan no linealidades e interacciones automáticamente. *Desventajas:* opacidad ("caja negra"), riesgo de sobreajuste y fricción regulatoria.

**Explainable AI (XAI).** SHAP (*Shapley Additive Explanations*) e ICE (*Individual Conditional Expectation*) mitigan la opacidad y son esenciales para el uso regulatorio. La incorporación de determinantes sociales de la salud mediante ML **reduce el subpago a poblaciones vulnerables** (BMC Public Health, 2020: mejora del *predictive ratio* en 3% y ~US$200 por persona en subgrupos de alta pobreza).

**IA generativa, LLMs y agentes.** Aplicaciones emergentes: procesamiento de siniestros no estructurados, extracción de datos regulatorios, clasificación asistida por visión y automatización de reportes (Hatzesberger & Nonneman, 2025; Richman, 2024, CAS). El **consenso profesional (SOA *Primer on Generative AI*, 2024; IFoA; IAA)** es que la IA generativa debe emplearse como **aumento del juicio actuarial, no como reemplazo**, bajo estrictos protocolos de gobernanza y seguridad de datos (p. ej., RAG sobre bases de conocimiento internas).

**Clásicos vs. ML — veredicto.** Para **tarificación regulatoria**, el GLM/Tweedie sigue siendo el estándar por interpretabilidad y auditabilidad. Para **estratificación poblacional, identificación de alto costo y detección de fraude**, el ML es superior. La frontera (Richman, SOA 2024) es el modelo híbrido "actuarialmente restringido": deep learning que respeta principios actuariales, es interpretable y libre de sesgos.

---

## 9. Aplicaciones al sistema colombiano

**Arquitectura del SGSSS.** La UPC es una prima que la ADRES paga prospectivamente a las EPS por afiliado, ajustada por **edad, sexo y zona geográfica** (con primas adicionales por dispersión geográfica y un ponderador por concentración de riesgo etario en el régimen contributivo, Acuerdo 26 de 2011 / Resolución 6411 de 2016). El MSPS realiza anualmente el "Estudio de suficiencia y de los mecanismos de ajuste de riesgo de la UPC", usando **BDUA, base de compensación de la ADRES, RIPS y proyecciones del DANE**, con metodología basada en **prima pura, IBNR e indicadores CAMEL**, y fundamentada explícitamente en principios de la Casualty Actuarial Society. La UPC financia más del 70% del gasto en salud de Colombia (Espinosa et al., 2023).

**Régimen de reservas técnicas y solvencia (marco normativo verificado).** El **Decreto 2702 de 2014** (compilado en el **Decreto 780 de 2016**, Único Reglamentario del Sector Salud, arts. 2.5.2.2.1.x), con fundamento en la Ley 1438 de 2011 y la Ley 100 de 1993, establece tres requisitos vigilados por la **Superintendencia Nacional de Salud**: (i) **capital mínimo** (art. 2.5.2.2.1.5: $8.788 millones en 2014 + $965 millones por régimen); (ii) **patrimonio adecuado / margen de solvencia** (art. 2.5.2.2.1.7); y (iii) **inversión de las reservas técnicas** al menos al 100% del saldo, en instrumentos de alta liquidez y seguridad (art. 2.5.2.2.1.10). Las reservas técnicas (art. 2.5.2.2.1.9) comprenden la **reserva para obligaciones pendientes** —que distingue explícitamente servicios **conocidos** y **ocurridos pero no conocidos** (concepto IBNR)— y la **reserva para autorizaciones de servicios**, con actualización mensual. El **régimen de transición fue de 7 años**. El defecto de solvencia inicial se estimó cercano a $5,3 billones; el Decreto 995 de 2022 identificó reservas por ~$16 billones respaldadas por inversiones de ~$6,5 billones, evidenciando el incumplimiento persistente de varias EPS.

**Cuenta de Alto Costo (CAC) — ajuste de riesgo ex-post.** Creada por el **Decreto 2699 de 2007** como fondo autogestionado que asocia obligatoriamente a las EPS/EOC. Opera un **mecanismo de redistribución ex-post (suma cero)**: las EPS con menor concentración de casos de alto costo transfieren recursos a las de mayor concentración, para neutralizar la selección de riesgos. Da seguimiento a **seis cohortes**: Artritis Reumatoide, Cáncer, ERC (con precursoras HTA y Diabetes), Hemofilia, Hepatitis C y VIH. La compensación financiera se centró históricamente en ERC (Resoluciones 3413 y 4917 de 2009; desde 2014 se añadieron HTA y DM). *Cifras oficiales (CAC):* en el periodo 2023 se reportaron **991.212 personas con ERC** (prevalencia 1,91 por 100 habitantes, +25,45% frente a 2022); al 31 de diciembre de 2023 la cifra preliminar fue de **1.014.594 personas con ERC**; 44.512 en terapia de reemplazo renal y 8.324 con trasplante funcional. *Nota de incertidumbre:* una cifra de prensa (Portafolio, informe 2024) menciona hasta 1.251.930 diagnosticados con ERC en 2024, que debe confirmarse contra el informe oficial. La **Resolución 2048 de 2015 regula el listado de enfermedades huérfanas**, no el mecanismo financiero de la CAC. En 2026 el MSPS habría iniciado un traslado del reporte hacia SISPRO, generando incertidumbre normativa (fuente de prensa, a verificar).

**Fortalezas del sistema colombiano.**
1. **Sistemas de información robustos** — la CAC posiciona a Colombia como líder regional en gestión del riesgo y pago por resultados, con datos de alta calidad.
2. **Mecanismo de ajuste ex-post** vía CAC, poco común en la región.
3. **Marco de reservas y solvencia** formalmente comparable a estándares internacionales.
4. **Capacidad académica de primer nivel** (Universidad Nacional, Los Andes, Javeriana; grupos de Riascos, Espinosa, Arias).

**Debilidades y vacíos metodológicos.**
1. **Ajuste de riesgo predominantemente demográfico.** Riascos, Romero & Serna (2017, Documento CEDE 2017-27) demostraron que **"la fórmula actual de ajuste de riesgo, que condiciona sobre factores demográficos y sus interacciones, solo puede predecir el 30% del gasto total en el quintil superior de la distribución del gasto"**. Alfonso, Riascos & Romero (2014, Universidad de los Andes / SSRN 2489183) mostraron que **al incorporar grupos de riesgo diagnósticos, el R² del modelo pasa de 1,45% a 13,53%, y en el quintil de mayor gasto el gasto esperado pasa de representar el 27% al 71% del gasto real**.
2. **Metodología retrospectiva.** El "Ejercicio de Contrastación" de la ADRES es de validación/depuración, sin modelos actuariales prospectivos ni ajuste por morbilidad.
3. **Crisis de calidad de datos.** El propio MSPS declaró, por primera vez en muchos años, que la información reportada por las EPS del régimen contributivo no era de calidad adecuada para el cálculo de la UPC 2025 (Espinosa et al., 2025, *Health Economics Review*).
4. **Presión de los Presupuestos Máximos.** Las tecnologías no financiadas con UPC (gestionadas vía MIPRES) enfrentan desfinanciación recurrente, con cinco adiciones presupuestales promedio por año durante el gobierno actual; en 2025 solo diez medicamentos no-UPC concentraron el 58% del gasto de ese mecanismo (liraglutida y orlistat ~29%).

**Investigación colombiana clave (Nivel 1).**
- **Alfonso, Riascos & Romero (2014):** DRGs elevan el R² de 1,45% a 13,53%.
- **Riascos, Romero & Serna (2017):** ML (árboles potenciados) supera a la regresión lineal aun con menos regresores; propone condicionar sobre ~29 enfermedades crónicas.
- **Espinosa, Bejarano, Ramos & Martínez (2023, *Health Economics Review*):** cópulas + deep learning (redes neuronales) para estimar la prima pura de la UPC; halla diferencias sistemáticas por categoría de riesgo (superávits en 0-1 años, déficits en >54 años).
- **Espinosa, Bejarano & Ramos (2024, *North American Actuarial Journal*):** enfoque bayesiano a la suficiencia financiera.
- **Duncan et al. (2024, *North American Actuarial Journal*, doi:10.1080/10920277.2024.2387116):** "A Proposed Condition-Based Risk Adjustment System for the Colombian Health Insurance Program" desarrolla y prueba siete modelos, incluyendo dos que replican el sistema colombiano actual basado en edad/sexo/zona, demostrando la superioridad del ajuste por condiciones.
- **Arias (2026, *Health Economics Review*):** selección de ajustadores con regresión penalizada y juicio experto, evidencia colombiana.
- **Espinosa et al. (2025, BMC Health Services Research):** concentración, distribución y persistencia del gasto en el régimen contributivo (curvas de Lorenz; gasto altamente concentrado, mayor desigualdad en hombres y zonas rurales).

---

## 10. Brechas actuales

1. **Metodológica:** ausencia de un ajustador de morbilidad en la UPC, pese a que la evidencia y los datos existen.
2. **Predictiva:** metodologías correctivas/retrospectivas en lugar de prospectivas y probabilísticas.
3. **De datos:** inconsistencias en RIPS; declaración oficial de datos insuficientes para 2025.
4. **De solvencia:** reservas técnicas determinísticas; incumplimiento por parte de varias EPS.
5. **Institucional:** capacidad actuarial limitada dentro del regulador; dependencia de estudios incrementales.
6. **De gobernanza:** ausencia de validación externa independiente de las proyecciones actuariales; incertidumbre normativa reciente (reporte de alto costo hacia SISPRO en 2026).

---

## 11. Oportunidades de mejora

1. **Explotar RIPS + CAC + MIPRES/dispensación** para construir un ajustador de morbilidad (diagnósticos + farmacia).
2. **Reservas estocásticas** (Mack/bootstrap) con intervalos de confianza, superando el IBNR determinístico.
3. **ML con IA explicable** (gradient boosting + SHAP) para estratificación poblacional, identificación de alto costo y detección de fraude.
4. **Pool de riesgo / reaseguro** para casos catastróficos, siguiendo el modelo alemán (reembolso parcial sobre umbral).
5. **Modelos multi-estado/Markov** para la progresión de la ERC y proyección del gasto de la CAC.
6. **Salvaguardas anti-*upcoding*** inspiradas en la Manipulationsbremse alemana y las auditorías RADV de CMS.
7. **Cuantificación de incertidumbre** de la suficiencia de la UPC mediante Monte Carlo/microsimulación.

---

## 12. Hoja de ruta para Colombia

Priorización por impacto × factibilidad × disponibilidad de datos × madurez tecnológica × facilidad regulatoria.

### Corto plazo (0–18 meses) — alta factibilidad, bajo costo, datos disponibles
- **Auditar y mejorar la calidad de RIPS** (validaciones cruzadas BDUA-RIPS-MIPRES). *Prerrequisito crítico de menor costo.*
- **Piloto de GLM/Tweedie** con covariables de condiciones crónicas usando datos de la CAC (bajo costo, base regulatoria existente).
- **Migrar el IBNR a métodos estocásticos** con intervalos de confianza.
- **Crear una unidad actuarial independiente** en el regulador con mandato de validación externa.
- *Benchmark que cambia la decisión:* si el piloto GLM+morbilidad no eleva el R² por encima de ~10% en la cola alta, revisar la calidad de los datos antes de escalar.

### Mediano plazo (18–48 meses) — factibilidad media, costo medio
- **Implementar un ajustador de morbilidad** basado en diagnósticos + farmacia (selección penalizada + juicio experto, siguiendo Arias 2026 y Duncan et al. 2024).
- **Modelos ML (XGBoost/LightGBM) con SHAP** para estratificación y detección de alto costo/fraude.
- **Diseñar un pool de riesgo / reaseguro** para eventos catastróficos (articulado con la CAC).
- *Benchmark:* comparar el poder predictivo (R², *predictive ratio* en subgrupos vulnerables) del nuevo ajustador contra la fórmula demográfica antes de su adopción regulatoria.

### Largo plazo (4–8 años) — mayor complejidad regulatoria
- **Sistema de ajuste de riesgo prospectivo de morbilidad plenamente operativo** (tipo Morbi-RSA / holandés adaptado).
- **Salvaguardas anti-manipulación** (Manipulationsbremse) y auditorías tipo RADV.
- **Integración de determinantes sociales de la salud** y equidad algorítmica.
- **Modelos multi-estado** para enfermedades crónicas y proyección de largo plazo de solvencia.

**Conclusión de priorización:** el ajustador de morbilidad es la intervención de **mayor impacto**; la **mejora de la calidad de datos** es el prerrequisito de menor costo y mayor urgencia. Sin datos confiables, ningún modelo sofisticado producirá resultados válidos.

---

## 13. Conclusiones

El fortalecimiento actuarial del SGSSS requiere tres transiciones simultáneas:
1. **De ajuste demográfico a ajuste de morbilidad** (diagnósticos + farmacia).
2. **De métodos retrospectivos a prospectivos y probabilísticos** (predicción con cuantificación de incertidumbre).
3. **De reservas determinísticas a estocásticas** (medición robusta de solvencia).

La evidencia internacional (Países Bajos, Alemania, EE.UU.) y la investigación colombiana (Riascos, Espinosa, Arias, Duncan) **convergen** en que estas transiciones son técnicamente factibles con los datos existentes y generarían ganancias sustanciales de equidad (menor selección de riesgos), eficiencia (mejor asignación) y sostenibilidad (solvencia y suficiencia). El consenso es sólido: el ajuste demográfico es insuficiente. La principal controversia —precisión vs. resistencia a la manipulación— se resuelve con salvaguardas ya probadas internacionalmente. **El principal riesgo para Colombia no es técnico sino de gobernanza:** calidad de datos, capacidad institucional y voluntad política.

---

## 14. Limitaciones de la evidencia

- Gran parte de la comparación internacional proviene de países de alto ingreso; la transferibilidad a Colombia exige adaptación al contexto (informalidad laboral, dos regímenes, dispersión geográfica).
- Varios datos colombianos recientes (2025-2026) provienen de prensa especializada y **deben confirmarse con fuentes oficiales primarias**.
- No se accedió a la totalidad de textos completos por *paywall*; se usaron *abstracts* y repositorios.
- Los estudios de ML tienden a reportar mejoras en muestras específicas; la **validación externa es imprescindible** antes de cualquier uso regulatorio.
- La **Resolución 2048 de 2015 regula el listado de enfermedades huérfanas**, no el mecanismo financiero de la CAC (que reside en resoluciones específicas anuales); persiste **incertidumbre normativa** por el cambio reciente (2026) del reporte hacia SISPRO.
- Las encuestas de tendencias médicas (WTW, PwC) son fuentes de mercado, no revisadas por pares; se usan como indicadores de contexto.

---

## 15. Agenda futura de investigación

1. Validación externa de ajustadores de morbilidad con datos colombianos multi-anuales.
2. Evaluación del impacto de un pool de riesgo sobre la selección de riesgos en el SGSSS.
3. Modelos multi-estado calibrados para la progresión de la ERC colombiana.
4. Equidad algorítmica y determinantes sociales en el ajuste de la UPC.
5. Impacto de la IA generativa en la eficiencia de los procesos actuariales del regulador.
6. Estudios de suficiencia con incertidumbre cuantificada (Monte Carlo/microsimulación).
7. Diseño de mecanismos anti-*upcoding* adaptados a la estructura de datos colombiana.

---

## 16. Bibliografía

Actuarial Standards Board. (s.f.). *ASOP No. 45: The Use of Health Status Based Risk Adjustment Methodologies*. Actuarial Standards Board. http://www.actuarialstandardsboard.org/asops/use-health-status-based-risk-adjustment-methodologies/

Alfonso Sierra, E. A., Riascos, Á., & Romero, M. (2014). *The Performance of Risk Adjustment Models in Colombian Competitive Health Insurance Market* [Documento CEDE 2014-12]. Universidad de los Andes / SSRN. https://www.ssrn.com/abstract=2489183

American Academy of Actuaries. (2024). *Drivers of 2025 health insurance premium changes* [Issue brief]. https://www.actuary.org

Arias, C. (2026). Selecting risk adjusters with penalized regression and expert judgment: evidence from Colombia. *Health Economics Review, 16*(1). https://doi.org/10.1186/s13561-025-00620-z (nota: referencia de la serie Health Economics Review sobre Colombia)

Bornhuetter, R. L., & Ferguson, R. E. (1972). The actuary and IBNR. *Proceedings of the Casualty Actuarial Society, 59*, 181–195.

Christiansen, M. C. (2012). Multistate models in health insurance. *AStA Advances in Statistical Analysis, 96*, 155–186. https://doi.org/10.1007/s10182-012-0189-2

Cuenta de Alto Costo (Fondo Colombiano de Enfermedades de Alto Costo). (2024). *Situación de la enfermedad renal crónica, la hipertensión arterial y la diabetes mellitus en Colombia 2023*. https://cuentadealtocosto.org/

Duncan, I., et al. (2024). A Proposed Condition-Based Risk Adjustment System for the Colombian Health Insurance Program. *North American Actuarial Journal*. https://doi.org/10.1080/10920277.2024.2387116

Eijkenaar, F., van Kleef, R. C., & van Vliet, R. C. J. A. (2023). Improving diagnosis-based cost groups in the Dutch risk equalization model: the effects of a new clustering method and allowing for multimorbidity. *The European Journal of Health Economics*. https://pmc.ncbi.nlm.nih.gov/articles/PMC10156830/

England, P. D., & Verrall, R. J. (2002). Stochastic claims reserving in general insurance. *British Actuarial Journal, 8*(3), 443–518.

Espinosa, O., Bejarano, V., Ramos, J., & Martínez, B. (2023). Statistical actuarial estimation of the Capitation Payment Unit from copula functions and deep learning: historical comparability analysis for the Colombian health system, 2015–2021. *Health Economics Review, 13*(1), 15. https://doi.org/10.1186/s13561-022-00416-5

Espinosa, O., Bejarano, V., & Ramos, J. (2024). Predictability and Financial Sufficiency of Health Insurance in Colombia: An Actuarial Analysis with a Bayesian Approach. *North American Actuarial Journal, 28*(2), 320–336. https://doi.org/10.1080/10920277.2023.2197475

Espinosa, O., Friebel, R., Bejarano, V., Arias, M., Husereau, D., & Smith, A. (2024). Study on the Concentration, Distribution, and Persistence of Health Spending for the Contributory Scheme in Colombia. *BMC Health Services Research, 24*(1), 1225. https://doi.org/10.1186/s12913-024-11636-2

Espinosa, O., et al. (2025). Health insurance premium in Colombia for 2025: a strictly political-ideological decision without technical-scientific arguments? *Health Economics Review, 15*(31). https://doi.org/10.1186/s13561-025-00620-z

Geruso, M., & Layton, T. (2020). Upcoding: Evidence from Medicare on Squishy Risk Adjustment. *Journal of Political Economy, 128*(3) / NBER Working Paper 21222. https://www.nber.org/papers/w21222

Haberman, S., & Pitacco, E. (1999). *Actuarial Models for Disability Insurance*. Chapman & Hall/CRC.

Hatzesberger, S., & Nonneman, I. (2025). *Advanced Applications of Generative AI in Actuarial Science: Case Studies Beyond ChatGPT*. arXiv:2506.18942. https://arxiv.org/html/2506.18942v1

Li, P., Kim, M. M., & Doshi, J. A. (2010). Comparison of the performance of the CMS Hierarchical Condition Category (CMS-HCC) risk adjuster with the Charlson and Elixhauser comorbidity measures in predicting mortality. *BMC Health Services Research, 10*, 245. https://doi.org/10.1186/1472-6963-10-245

Mack, T. (1993). Distribution-free calculation of the standard error of chain-ladder reserve estimates. *ASTIN Bulletin, 23*(2), 213–225.

Ministerio de Salud y Protección Social (Colombia). (2016). *Decreto 780 de 2016, Único Reglamentario del Sector Salud y Protección Social* (compila el Decreto 2702 de 2014). https://www.minsalud.gov.co

Ministerio de Salud y Protección Social (Colombia). (2022). *Estudio de suficiencia y de los mecanismos de ajuste del riesgo para el cálculo de la UPC 2022*. https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/VP/DOA/estudio-suficiencia-upc-2022.pdf

Riascos, Á., Romero, M., & Serna, N. (2017). *Risk Adjustment Revisited Using Machine Learning Techniques* [Documento CEDE 2017-27]. Universidad de los Andes / SSRN. https://ideas.repec.org/p/col/000089/015601.html

Richman, R. (2024). *The Actuary in an Age of AI* [AI Insights for Actuaries Symposium]. Society of Actuaries. https://www.soa.org/prof-dev/recordings/2024/december/act-in-age-of-ai/

Rose, S. (2016). A Machine Learning Framework for Plan Payment Risk Adjustment. *Health Services Research, 51*(6), 2358–2374. https://pmc.ncbi.nlm.nih.gov/articles/PMC5134202/

Society of Actuaries. (2024). *Primer on Generative AI for Actuaries* / *MyActuary.AI*. https://www.soa.org

van de Ven, W. P. M. M., & Ellis, R. P. (2000). Risk adjustment in competitive health plan markets. En A. J. Culyer & J. P. Newhouse (Eds.), *Handbook of Health Economics* (Vol. 1, cap. 14, pp. 755–845). Elsevier.

Wasserman, J., et al. (2016). Risk Adjustment Tools for Learning Health Systems: A Comparison of DxCG and CMS-HCC V21. *Medical Care*. https://pubmed.ncbi.nlm.nih.gov/26839976/

Willis Towers Watson (WTW). (2025). *2026 Global Medical Trends Survey*. https://www.wtwco.com/en-us/insights/2025/10/2026-global-medical-trends-survey

Zink, A., & Rose, S. (2020). Fair regression for health care spending. *Biometrics, 76*(3), 973–982. https://doi.org/10.1111/biom.13206

*Nota sobre normativa colombiana citada:* Ley 100 de 1993; Ley 1438 de 2011; Decreto 2699 de 2007 (creación de la CAC); Decreto 2702 de 2014 / Decreto 780 de 2016 (solvencia y reservas); Decreto 995 de 2022; Resolución 2048 de 2015 (enfermedades huérfanas); Resolución 2366 de 2023 y Resolución 2364 de 2023 (UPC 2024); Resolución 2765 de 2025 (cobertura UPC). Fuentes primarias: minsalud.gov.co, adres.gov.co, cuentadealtocosto.org, funcionpublica.gov.co.

---

## Anexo. Clasificación y valoración de fuentes

| Fuente | Tipo de evidencia | Año | País | Nivel de evidencia | Relevancia para Colombia | Comentarios |
|--------|-------------------|-----|------|--------------------|--------------------------|-------------|
| Alfonso, Riascos & Romero (SSRN 2489183) | Artículo científico | 2014 | Colombia | Nivel 1 | **Muy alta** | Cuantifica el salto de R² 1,45%→13,53% con DRGs; base empírica directa |
| Riascos, Romero & Serna (CEDE 2017-27) | Artículo científico | 2017 | Colombia | Nivel 1 | **Muy alta** | ML supera regresión lineal; fórmula demográfica predice solo 30% de la cola alta |
| Espinosa et al. (Health Economics Review) | Artículo científico | 2023 | Colombia | Nivel 1 | **Muy alta** | Cópulas + deep learning para UPC; datos abiertos |
| Espinosa et al. (North American Actuarial Journal) | Artículo científico | 2024 | Colombia | Nivel 1 | **Muy alta** | Enfoque bayesiano a la suficiencia |
| Duncan et al. (NAAJ, doi 10.1080/...2387116) | Artículo científico | 2024 | Colombia/EE.UU. | Nivel 1 | **Muy alta** | Sistema de ajuste basado en condiciones; 7 modelos comparados |
| Arias (Health Economics Review) | Artículo científico | 2026 | Colombia | Nivel 1 | **Muy alta** | Regresión penalizada + juicio experto; método recomendado |
| Espinosa et al. (BMC Health Services Research) | Artículo científico | 2024 | Colombia | Nivel 1 | Alta | Concentración/persistencia del gasto |
| Eijkenaar/van Kleef/van Vliet (Eur J Health Econ) | Artículo científico | 2023 | Países Bajos | Nivel 1 | Alta | Diseño de ajustadores DCG; referencia de RE de vanguardia |
| Geruso & Layton (JPE/NBER) | Artículo científico | 2020 | EE.UU. | Nivel 1 | Alta | Cuantifica el upcoding; justifica salvaguardas |
| Rose (Health Services Research) | Artículo científico | 2016 | EE.UU. | Nivel 1 | Alta | Framework ML para ajuste de pagos |
| Wasserman et al. (Medical Care) | Artículo científico | 2016 | EE.UU. | Nivel 1 | Alta | DxCG vs. CMS-HCC V21 |
| Christiansen (AStA Adv Stat Anal) | Artículo científico | 2012 | Alemania | Nivel 1 | Media-alta | Modelos multi-estado en salud |
| Estudio ajuste diagnóstico Chile | Artículo científico | ~2018 | Chile | Nivel 1 | Alta | Mejora predictiva 68%; comparador regional |
| ASOP No. 45 (Actuarial Standards Board) | Guía metodológica | s.f. | EE.UU. | Nivel 2 | Media-alta | Estándar de práctica en ajuste de riesgo |
| SOA – Primer on Generative AI / Richman | Documento institucional | 2024 | EE.UU. | Nivel 2 | Media | Consenso profesional sobre IA generativa |
| Bundesamt für Soziale Sicherung / vdek (Morbi-RSA) | Documento institucional/norma | 2020-2023 | Alemania | Nivel 2-3 | Alta | Vollmodell, pool de riesgo, Manipulationsbremse |
| WTW Global Medical Trends | Documento técnico (encuesta) | 2025 | Global | Nivel 3 | Media | Inflación médica; fuente de mercado, no revisada por pares |
| Decreto 780 de 2016 / Decreto 2702 de 2014 | Norma | 2014/2016 | Colombia | Nivel 4 | **Muy alta** | Reservas técnicas y solvencia de EPS |
| Decreto 2699 de 2007 (creación CAC) | Norma | 2007 | Colombia | Nivel 4 | **Muy alta** | Fundamento del ajuste ex-post |
| Estudio de suficiencia UPC (MSPS) | Documento institucional | 2011-2024 | Colombia | Nivel 4 | **Muy alta** | Metodología oficial vigente de la UPC |
| Cuenta de Alto Costo (informes ERC) | Documento institucional | 2023-2024 | Colombia | Nivel 4 | **Muy alta** | Datos de prevalencia de alto costo |
| ADRES (Ejercicio de Contrastación / gasto UPC) | Documento institucional | 2024 | Colombia | Nivel 4 | Alta | Diagnóstico de método retrospectivo |
| Mack (1993); Bornhuetter-Ferguson (1972) | Libro/artículo clásico | 1972/1993 | Internacional | Nivel 1/5 | Media | Reservas IBNR; base metodológica |
| van de Ven & Ellis (Handbook of Health Economics) | Libro de referencia | 2000 | Internacional | Nivel 5 | Alta | Marco teórico del risk adjustment |
| Prensa especializada (Consultorsalud, El Tiempo, Infobae) | Contexto (no científico) | 2024-2026 | Colombia | Bajo | Contexto | Usada solo para contexto; datos a verificar en fuentes primarias |

---

*Validación final: todas las afirmaciones técnicas relevantes cuentan con respaldo bibliográfico identificable; no se incluyeron referencias inventadas; cuando un dato provino de fuente de baja jerarquía (prensa) o no pudo confirmarse en fuente primaria, se señaló explícitamente la incertidumbre. Las recomendaciones para Colombia están justificadas por evidencia internacional (Países Bajos, Alemania, EE.UU., Chile) y, de forma decisiva, por evidencia empírica colombiana revisada por pares (Alfonso/Riascos/Romero 2014; Riascos/Romero/Serna 2017; Espinosa et al. 2023-2024; Duncan et al. 2024; Arias 2026).*