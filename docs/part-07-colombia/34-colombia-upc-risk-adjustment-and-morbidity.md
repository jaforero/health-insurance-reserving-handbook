---
title: "UPC, ajuste de riesgo y morbilidad en Colombia"
description: "Incorporación de morbilidad y ajuste de riesgo en el análisis de suficiencia de la UPC y en la gestión actuarial de salud."
chapter: 34
part: "part-07-colombia"
language: "es"
status: "draft"
version: "0.1.11"
last_updated: "2026-07-14"
jurisdiction: "Colombia"
---

# UPC, ajuste de riesgo y morbilidad en Colombia

Este capítulo desarrolla una propuesta técnica para incorporar morbilidad en el análisis de suficiencia de la Unidad de Pago por Capitación (UPC) y en la gestión actuarial del riesgo en salud en Colombia. El objetivo no es sustituir el marco regulatorio vigente ni proponer una fórmula oficial, sino definir una arquitectura actuarial defendible para medir diferencias de riesgo clínico entre poblaciones, EPS, regiones, cohortes y periodos.

En el SGSSS, una UPC que dependa principalmente de variables demográficas, geográficas o administrativas puede ser insuficiente para poblaciones con mayor carga de enfermedad crónica, multimorbilidad o alto costo. La consecuencia técnica es directa: dos poblaciones con edad y sexo similares pueden tener costos esperados muy distintos si difieren en diabetes, enfermedad renal crónica, cáncer, VIH, salud mental, enfermedades huérfanas, discapacidad, polifarmacia o historia reciente de uso hospitalario.

El ajuste por morbilidad busca corregir esa limitación. Su propósito actuarial es estimar recursos esperados con base en el estado de salud observable, no solamente con base en edad, sexo o zona. Para reserving, este enfoque también mejora la interpretación de desviaciones: permite separar lo que corresponde a desarrollo de siniestros, inflación médica, cambios operativos y deterioro real del perfil clínico.

> Nota técnica: cualquier uso regulatorio de este capítulo debe contrastarse contra la normativa colombiana vigente, los lineamientos de Minsalud, ADRES, Superintendencia Nacional de Salud y las reglas aplicables a RIPS, FEV, PBS, MIPRES, presupuestos máximos y Cuenta de Alto Costo.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Explicar por qué la morbilidad es una variable crítica para la suficiencia de la UPC.
- Diferenciar ajuste demográfico, ajuste clínico, ajuste farmacéutico y compensación ex post.
- Diseñar un modelo mínimo viable de ajuste de riesgo para Colombia.
- Identificar fuentes de datos relevantes: afiliación, RIPS, diagnósticos, procedimientos, medicamentos, MIPRES, PBS, FEV, pagos y Cuenta de Alto Costo.
- Definir controles para evitar incentivos perversos, sobrecodificación y selección de riesgos.
- Conectar el ajuste de riesgo con reservas IBNR, presupuestos prospectivos y monitoreo de suficiencia.

## 1. Problema actuarial

El problema central es que la transferencia capitada debe financiar un gasto esperado que no se distribuye homogéneamente entre afiliados. La prima promedio puede ser suficiente para una población estándar y simultáneamente insuficiente para una EPS con alta concentración de enfermedad crónica o eventos catastróficos.

La forma simplificada del problema es:

$$
E[C_i \mid X_i] \neq E[C_i \mid \text{edad}_i, \text{sexo}_i, \text{zona}_i]
$$

donde:

- $C_i$ es el costo esperado del afiliado $i$;
- $X_i$ incluye edad, sexo, zona, régimen, morbilidad, diagnósticos, medicamentos, uso histórico, prestador, contrato y condiciones de alto costo;
- el modelo demográfico aproxima solo una parte del riesgo;
- el modelo clínico busca capturar diferencias adicionales en necesidad esperada de recursos.

Cuando el pago capitado ignora morbilidad, aparecen tres problemas:

| Problema | Efecto técnico | Efecto operativo |
|---|---|---|
| Subcompensación de poblaciones enfermas | Déficit esperado persistente | Presión de liquidez, glosas, demora en pagos |
| Sobrecompensación de poblaciones sanas | Margen no explicado por eficiencia | Incentivo a selección de riesgos |
| Señales de reserva distorsionadas | IBNR contaminado por insuficiencia tarifaria | Dificultad para separar reserva, tendencia y tarifa |

Un modelo de ajuste de riesgo no elimina la incertidumbre, pero mejora la asignación esperada de recursos y permite interpretar la experiencia con mayor rigor.

## 2. Qué significa ajustar la UPC por morbilidad

Ajustar por morbilidad significa calcular factores relativos de riesgo a partir de información clínica y de utilización. En lugar de tratar a todos los afiliados de un grupo demográfico como equivalentes, el modelo estima un puntaje de riesgo individual o grupal.

Un esquema general puede expresarse como:

$$
\text{UPC ajustada}_{i,t+1} = \text{UPC base}_{g(i),t+1} \times \text{factor de riesgo}_{i,t} \times \text{ajustes técnicos}_{i,t}
$$

donde:

- $\text{UPC base}_{g(i),t+1}$ es la UPC base para el grupo demográfico o normativo;
- $\text{factor de riesgo}_{i,t}$ resume la carga clínica observada en el periodo base;
- $\text{ajustes técnicos}_{i,t}$ pueden incluir región, régimen, dispersión geográfica, redes, alta complejidad, inflación médica esperada o factores de transición.

El ajuste puede ser:

| Tipo de ajuste | Variables típicas | Uso principal |
|---|---|---|
| Demográfico | Edad, sexo, zona | Base mínima de tarifación |
| Clínico diagnóstico | CIE-10, grupos de condición, comorbilidades | Morbilidad prospectiva |
| Farmacéutico | ATC, medicamentos crónicos, terapias de alto costo | Marcadores de enfermedad y adherencia |
| Uso histórico | Hospitalización, urgencias, UCI, alto costo | Severidad y persistencia |
| Socioeconómico o territorial | Ruralidad, dispersión, vulnerabilidad | Acceso y necesidad esperada |
| Ex post | Cuenta de Alto Costo, reaseguro, corredores | Riesgo extremo o parcialmente mutualizado |

El punto crítico es que el modelo debe distinguir necesidad esperada de recursos de ineficiencia, precio, fraude, glosa o diferencias contractuales. Si el ajuste remunera directamente costos observados sin controles, puede premiar ineficiencias.

## 3. Relación con estándares actuariales

ASOP No. 45, sobre metodologías de ajuste de riesgo basadas en estado de salud, establece una idea central: los modelos de ajuste de riesgo se usan para cuantificar diferencias relativas de uso esperado de recursos por diferencias en estado de salud. También enfatiza que el actuario debe considerar uso previsto, versión del modelo, impacto en incentivos, calidad de datos, población, periodo de estimación, recalibración y comunicación de limitaciones.

Aplicado a Colombia, esto implica que un modelo de UPC ajustada por morbilidad no debe evaluarse solo por su $R^2$, AUC o error predictivo. Debe evaluarse por:

- finalidad: suficiencia UPC, compensación entre EPS, monitoreo de riesgo o reserving;
- datos disponibles y su calidad;
- estabilidad interanual;
- susceptibilidad a codificación oportunista;
- equidad entre poblaciones;
- transparencia para auditoría;
- coherencia con incentivos de prevención y gestión clínica;
- capacidad de recalibración periódica.

Un modelo técnicamente preciso pero débil en gobierno puede producir mejores predicciones y peores incentivos. En salud pública, la robustez institucional es parte del diseño actuarial.

## 4. Fuentes de datos para Colombia

Un modelo mínimo viable no requiere empezar con una historia clínica perfecta. Puede iniciar con datos administrativos y clínicos disponibles, siempre que se documenten limitaciones y se construyan controles.

| Fuente | Variables útiles | Riesgos de calidad |
|---|---|---|
| BDUA / afiliación | Edad, sexo, régimen, municipio, permanencia | Traslados, duplicidades, rezagos |
| RIPS | Diagnósticos, procedimientos, fechas, prestador | Codificación inconsistente, subregistro |
| FEV / facturación electrónica | Valor facturado, validación, identificación de evento | Rechazos, cambios de regla, oportunidad |
| Pagos y cuentas médicas | Valor reconocido, pagado, glosado, pendiente | Mezcla de costo médico y proceso operativo |
| PBS / medicamentos UPC | Uso farmacéutico cubierto | Sustitución terapéutica, adherencia no observada |
| MIPRES / No UPC | Tecnologías no financiadas por UPC, alto costo | Alta severidad, baja frecuencia, rezagos |
| Cuenta de Alto Costo | Cohortes de cáncer, VIH, ERC y otras condiciones | Cobertura parcial del espectro clínico |
| Autorizaciones | Servicios esperados aún no facturados | Cancelaciones, autorizaciones no usadas |
| Prestadores y contratos | Modalidad de pago, red, tarifa, capitación | Diferencias de precio vs necesidad |

La prioridad inicial debe ser construir una vista longitudinal por afiliado, con una ventana de observación clínica y una ventana de predicción de costo. Sin esa separación temporal, el modelo puede incurrir en leakage.

## 5. Ventanas temporales

Para un modelo prospectivo, la estructura básica es:

| Elemento | Ejemplo |
|---|---|
| Periodo de observación | Diagnósticos, medicamentos y uso durante 2025 |
| Periodo de predicción | Costo esperado durante 2026 |
| Unidad de análisis | Afiliado-mes o afiliado-año |
| Target | Costo reconocido, permitido, pagado o gasto técnico depurado |
| Exposición | Meses de afiliación, cobertura efectiva, días persona |

Esta separación es esencial. Un diagnóstico registrado en el mismo evento que genera el costo puede ser útil para medir severidad histórica, pero no necesariamente para calcular un pago prospectivo si se observa después de causado el gasto.

Una versión concurrente puede ser útil para auditoría, medición retrospectiva de morbilidad o análisis de suficiencia histórica. Una versión prospectiva es más adecuada para asignación de recursos futuros.

## 6. Variables clínicas y agrupadores

El modelo puede usar variables clínicas de tres formas:

1. Indicadores directos de diagnósticos CIE-10.
2. Agrupadores clínicos: HCC, CRG, ACG, DxCG o agrupadores locales.
3. Marcadores derivados: multimorbilidad, severidad, recurrencia, persistencia y polifarmacia.

Un enfoque pragmático para Colombia puede iniciar con agrupadores propios mientras se evalúa la adopción o adaptación de modelos internacionales.

| Dimensión | Ejemplos |
|---|---|
| Enfermedad crónica | Diabetes, hipertensión, EPOC, falla cardiaca |
| Alto costo | Cáncer, ERC, VIH, trasplantes, enfermedades huérfanas |
| Salud mental | Depresión severa, trastornos por consumo, esquizofrenia |
| Materno perinatal | Gestación de alto riesgo, neonatal intensivo |
| Complejidad hospitalaria | UCI, cirugía mayor, reingreso |
| Farmacia | Insulina, antirretrovirales, biológicos, oncológicos |
| Utilización | Urgencias frecuentes, hospitalizaciones, terapias recurrentes |
| Multimorbilidad | Número y combinación de condiciones |

El diseño debe evitar variables que capturen precios negociados o comportamiento administrativo de una EPS si el objetivo es compensar riesgo de salud. Por ejemplo, usar directamente el costo pagado histórico puede mezclar morbilidad, tarifa, oportunidad de pago, glosa e ineficiencia.

## 7. Target actuarial

La selección del target define el modelo. No es lo mismo predecir:

- costo facturado;
- costo reconocido;
- costo pagado;
- costo incurrido técnico;
- costo cubierto por UPC;
- costo total PBS + No UPC;
- probabilidad de alto costo;
- tasa de uso de servicios;
- reserva esperada por cohorte.

Para suficiencia de UPC, el target debe aproximar el costo técnico esperado de los servicios financiados por UPC, depurado de diferencias puramente administrativas. Para análisis integral del SGSSS, conviene construir targets separados:

| Target | Uso |
|---|---|
| Costo UPC | Suficiencia de prima capitada |
| Costo No UPC / MIPRES | Presupuestos máximos y riesgo extremo |
| Alto costo CAC | Mutualización y compensación ex post |
| Costo total afiliado | Planeación macro y solvencia |
| IBNR por cohorte clínica | Reservas y liquidez |

Separar targets evita que un único modelo trate como homogéneos riesgos con mecanismos de financiación distintos.

## 8. Modelo mínimo viable

Un primer piloto puede implementarse con un GLM de costo anual o mensual por afiliado. El objetivo no es maximizar complejidad, sino crear una línea base transparente.

Forma general:

$$
E[C_i] = \exp( \beta_0 + \beta_1 \text{edad}_i + \beta_2 \text{sexo}_i + \beta_3 \text{zona}_i + \beta_4 \text{régimen}_i + \sum_k \gamma_k \text{condición}_{ik} + \sum_j \delta_j \text{medicamento}_{ij} )
$$

Distribuciones candidatas:

| Distribución | Uso |
|---|---|
| Poisson / Negativa binomial | Frecuencia de servicios |
| Gamma con enlace log | Costo positivo continuo |
| Tweedie | Masa en cero + costo positivo |
| Lognormal | Costos severos con cola derecha |
| Dos partes / hurdle | Probabilidad de uso + severidad condicional |

La línea base recomendada es comparar al menos tres modelos:

| Modelo | Propósito |
|---|---|
| Demográfico puro | Medir el punto de partida |
| Demográfico + diagnósticos | Cuantificar valor incremental de morbilidad |
| Demográfico + diagnósticos + farmacia + uso | Medir mejora con señales clínicas y de utilización |

La evaluación debe mostrar la ganancia incremental por bloque de variables. Si los diagnósticos mejoran desempeño pero introducen inestabilidad o sesgo de codificación, el resultado debe documentarse.

## 9. Métricas de validación

La validación debe combinar desempeño predictivo, estabilidad y equidad.

| Métrica | Pregunta que responde |
|---|---|
| MAE / RMSE | ¿Qué tan grande es el error individual? |
| Error por decil de riesgo | ¿El modelo subestima grupos de alto costo? |
| Ratio observado / esperado | ¿La compensación es suficiente por grupo? |
| Lift top 1%, 5%, 10% | ¿Identifica concentración de gasto? |
| Estabilidad de coeficientes | ¿El modelo cambia demasiado entre años? |
| Calibración por EPS / región | ¿Hay sesgos sistemáticos? |
| Backtesting prospectivo | ¿Funciona en periodos no usados para entrenar? |
| Sensibilidad a codificación | ¿Se puede manipular con más diagnósticos? |

Una regla práctica es que el modelo debe evaluarse a nivel individual y agregado. En ajuste de riesgo, el error individual puede ser alto por naturaleza, pero el modelo debe producir compensaciones razonables para grupos, EPS, cohortes clínicas y regiones.

## 10. De puntaje individual a transferencia poblacional

El modelo produce un puntaje de riesgo individual:

$$
RS_i = \frac{\widehat{C}_i}{\overline{C}}
$$

Luego se agregan los puntajes:

$$
RS_G = \frac{\sum_{i \in G} w_i RS_i}{\sum_{i \in G} w_i}
$$

donde $w_i$ representa exposición, meses afiliado o ponderadores definidos por el esquema.

La transferencia ajustada para una EPS o grupo puede calcularse como:

$$
\text{Transferencia}_G = \text{UPC base}_G \times RS_G \times \text{factor de normalización}
$$

El factor de normalización evita que el ajuste incremente automáticamente el gasto total del sistema si el objetivo es redistribuir recursos dentro de un presupuesto cerrado. Si el objetivo es estimar suficiencia real, el modelo debe permitir detectar déficit agregado.

## 11. Riesgos de incentivos

El ajuste por morbilidad cambia incentivos. Eso es inevitable. El diseño debe anticiparlo.

| Riesgo | Descripción | Control |
|---|---|---|
| Upcoding | Mayor intensidad de codificación sin mayor enfermedad real | Auditoría clínica, reglas de persistencia, validación cruzada |
| Diagnósticos oportunistas | Códigos usados para elevar puntaje | Jerarquías clínicas, exclusión de códigos débiles |
| Selección residual | Preferencia por afiliados subcompensados favorablemente | Monitoreo de traslados y composición |
| Penalización de prevención | Si mejorar salud reduce pagos futuros | Ajustes de transición e indicadores de calidad |
| Doble pago | UPC + compensación ex post para mismo riesgo | Coordinación con CAC, MIPRES y presupuestos máximos |
| Ineficiencia remunerada | Costos altos por mala gestión parecen alto riesgo | Depuración de precio, red y patrón operativo |

Un buen modelo no debe pagar más simplemente porque una entidad factura más. Debe pagar más cuando la población tiene mayor necesidad esperada de recursos, con evidencia clínica verificable.

## 12. Conexión con reserving

El ajuste de riesgo por morbilidad mejora el reserving en cuatro niveles.

Primero, permite segmentar triángulos por carga clínica. Una cohorte con alta morbilidad puede tener patrones de desarrollo distintos, mayor severidad y mayor probabilidad de reclamaciones tardías.

Segundo, permite construir expected loss ratios más defendibles para Bornhuetter-Ferguson. En lugar de usar una razón esperada plana, se puede usar una razón esperada ajustada por perfil clínico.

Tercero, mejora la explicación de desviaciones. Si una EPS muestra incremento de IBNR, el analista puede separar:

- cambio en rezago de radicación;
- cambio en glosas o pagos;
- inflación médica;
- cambio en mezcla de servicios;
- deterioro de morbilidad;
- insuficiencia de UPC.

Cuarto, permite diseñar alertas tempranas. Un aumento de puntaje de riesgo en afiliados activos puede anticipar presión futura en pagos, autorizaciones y reservas.

## 13. Arquitectura analítica recomendada

Una arquitectura mínima para piloto debe tener las siguientes capas:

| Capa | Función |
|---|---|
| Ingesta | Afiliación, RIPS, FEV, pagos, MIPRES, medicamentos |
| Normalización | Identificadores, fechas, codificación, deduplicación |
| Agrupación clínica | Condiciones, jerarquías, severidad, multimorbilidad |
| Feature store | Variables por afiliado-mes o afiliado-año |
| Modelo | GLM/GAM como base, boosting como challenger |
| Validación | Backtesting, calibración, estabilidad, sesgo |
| Reporting | O/E, deciles de riesgo, suficiencia, alertas |
| Gobierno | Versiones, auditoría, documentación, aprobación |

La unidad recomendada para empezar es afiliado-mes. Permite manejar entradas, retiros, traslados, mortalidad, cambios de EPS y exposición parcial.

## 14. Diseño de piloto

Un piloto defendible puede estructurarse así:

| Fase | Actividad | Salida |
|---|---|---|
| 1 | Definir población, periodo y cobertura | Marco de análisis |
| 2 | Reconciliar afiliación, pagos y servicios | Base analítica |
| 3 | Crear agrupadores clínicos iniciales | Matriz de morbilidad |
| 4 | Entrenar modelo demográfico base | Benchmark |
| 5 | Agregar diagnósticos y medicamentos | Modelo clínico |
| 6 | Validar out-of-time | Métricas prospectivas |
| 7 | Calcular O/E por EPS, región y cohorte | Diagnóstico de suficiencia |
| 8 | Simular transferencias | Impacto financiero |
| 9 | Revisar incentivos y controles | Informe de gobierno |
| 10 | Documentar limitaciones | Nota técnica |

El piloto no debe iniciar con transferencia real de recursos. Primero debe operar como shadow model: calcula resultados paralelos sin afectar pagos, mide estabilidad y permite depurar datos.

## 15. Modelo challenger con machine learning

Después del GLM base, puede evaluarse un modelo challenger con GAM, gradient boosting o redes neuronales. El challenger puede capturar interacciones no lineales entre edad, diagnóstico, medicamentos, región y trayectoria de uso.

Sin embargo, para uso regulatorio o cuasi-regulatorio, el challenger debe cumplir requisitos adicionales:

- explicación global y local;
- estabilidad temporal;
- capacidad de documentación;
- ausencia de variables prohibidas o problemáticas;
- sensibilidad controlada a codificación;
- replicabilidad por terceros autorizados;
- comparación transparente contra GLM.

Una práctica razonable es usar ML para detección, segmentación y validación complementaria, mientras el primer esquema de transferencia se basa en un modelo más interpretable.

## 16. Indicadores de tablero

El monitoreo de UPC ajustada por morbilidad debe incluir indicadores ejecutivos y técnicos.

| Indicador | Definición | Uso |
|---|---|---|
| Risk score promedio | Promedio ponderado de puntajes | Perfil de morbilidad |
| O/E total | Costo observado / esperado | Calibración agregada |
| O/E alto riesgo | O/E en deciles superiores | Subestimación de cola |
| Costo por condición | Costo PMPM por grupo clínico | Gestión clínica |
| Prevalencia ajustada | Casos por exposición | Tendencia epidemiológica |
| Persistencia crónica | Condición presente en varios periodos | Riesgo estructural |
| Costo No UPC asociado | Gasto MIPRES por condición | Fragmentación financiera |
| IBNR por score | Reserva por decil de riesgo | Reserving clínico |
| Glosa por condición | Glosa / facturado por grupo | Calidad de cuenta médica |
| Traslados por riesgo | Entradas/salidas por score | Selección residual |

Estos indicadores permiten evaluar simultáneamente suficiencia, morbilidad, operación y riesgo financiero.

## 17. Consideraciones de equidad

El ajuste por morbilidad debe mejorar equidad financiera sin crear discriminación indebida. La pregunta técnica no es solo quién cuesta más, sino por qué y cómo debe financiarse.

Variables como pobreza, ruralidad, etnia, discapacidad o vulnerabilidad territorial pueden capturar necesidades reales de acceso, pero también pueden introducir riesgos éticos y legales si se usan sin diseño cuidadoso. En un sistema público o solidario, estas variables deben tratarse como factores de equidad y acceso, no como mecanismos de exclusión.

Un diseño responsable debe:

- prohibir uso para negar afiliación o restringir acceso;
- usar el score para financiar necesidad, no para seleccionar población;
- auditar impactos por región y grupo vulnerable;
- documentar variables sensibles;
- separar predicción de decisión;
- incluir indicadores de calidad y oportunidad, no solo costo.

## 18. Conexión con Cuenta de Alto Costo y MIPRES

La UPC ajustada por morbilidad no debe confundirse con mecanismos ex post de alto costo. Ambos pueden coexistir.

| Mecanismo | Función |
|---|---|
| UPC ajustada por morbilidad | Financiar riesgo esperado prospectivo |
| Cuenta de Alto Costo | Mutualizar y monitorear condiciones específicas de alta carga |
| MIPRES / presupuestos máximos | Financiar tecnologías y servicios no cubiertos por UPC |
| Reaseguro o corredores | Limitar volatilidad extrema |

El riesgo técnico es el doble conteo. Si una condición ya está compensada vía score prospectivo y también vía mecanismo ex post, el diseño debe definir qué parte se financia por cada canal.

Una alternativa es usar capas:

1. UPC base demográfica.
2. Ajuste prospectivo por morbilidad común y crónica.
3. Compensación específica para alto costo extremo.
4. Corredores de riesgo para eventos excepcionales.

## 19. Limitaciones

Un modelo colombiano de ajuste por morbilidad enfrentará limitaciones iniciales:

- calidad heterogénea de diagnósticos;
- cambios en reglas de reporte;
- rezagos de facturación;
- glosas y disputas que distorsionan costo observado;
- diferencias tarifarias entre redes;
- subregistro de condiciones crónicas;
- selección residual no observable;
- eventos de alto costo con baja frecuencia;
- cambios regulatorios que rompen comparabilidad histórica.

Estas limitaciones no impiden construir el modelo. Exigen que el modelo se implemente gradualmente, con validación continua y con uso inicial analítico antes de uso financiero vinculante.

## 20. Recomendación metodológica

La ruta más defendible para Colombia es progresiva:

1. Mantener el modelo demográfico como benchmark.
2. Construir una matriz longitudinal afiliado-mes.
3. Crear agrupadores clínicos iniciales a partir de RIPS, medicamentos y alto costo.
4. Estimar GLM/GAM prospectivos para costo UPC.
5. Evaluar modelos challenger con boosting para detectar no linealidades.
6. Validar por año, EPS, región, régimen, condición y decil de riesgo.
7. Implementar shadow model sin transferencias reales.
8. Usar resultados para diagnóstico de suficiencia y diseño de pilotos.
9. Incorporar controles de auditoría clínica y codificación.
10. Definir una política explícita para CAC, MIPRES y No UPC.

El objetivo final no es producir un score perfecto. El objetivo es pasar de una compensación parcialmente ciega a la morbilidad hacia una asignación técnicamente trazable, auditable y coherente con la necesidad esperada de recursos.

## 21. Checklist operativo

Antes de usar un modelo de morbilidad para suficiencia UPC o reserving, debe verificarse:

- ¿La población y exposición están reconciliadas?
- ¿El periodo de observación está separado del periodo de predicción?
- ¿El target corresponde al uso financiero previsto?
- ¿Los diagnósticos tienen reglas de persistencia y severidad?
- ¿Los medicamentos se usan como marcadores clínicos y no solo como costo?
- ¿Se controlan tarifas, glosas y diferencias operativas?
- ¿Existe comparación contra modelo demográfico base?
- ¿El modelo fue validado fuera de muestra y fuera de tiempo?
- ¿Hay métricas por EPS, región, régimen y decil de riesgo?
- ¿Se evaluó riesgo de upcoding?
- ¿Se documentaron variables excluidas?
- ¿Hay versión, bitácora y aprobación técnica?
- ¿El resultado se conecta con reservas, presupuesto y solvencia?

## 22. Conclusión

La UPC ajustada por morbilidad es una evolución técnica necesaria para medir suficiencia con mayor precisión en un sistema con envejecimiento, cronicidad, alto costo y fragmentación financiera. Para Colombia, la prioridad no debería ser adoptar de inmediato un modelo internacional sin adaptación, sino construir una arquitectura local con estándares actuariales: datos longitudinales, agrupadores clínicos, modelo base interpretable, validación rigurosa, controles de incentivos y gobierno transparente.

La morbilidad no reemplaza el juicio actuarial. Lo estructura. Permite explicar mejor por qué una población requiere más recursos, dónde se concentra el riesgo y cómo se conectan la UPC, las reservas, la Cuenta de Alto Costo, MIPRES y la sostenibilidad financiera del SGSSS.

## Fuentes de trabajo del proyecto

- ASOP No. 45, *The Use of Health Status Based Risk Adjustment Methodologies*.
- ASOP No. 12, *Risk Classification*, como referencia conceptual asociada.
- `gemini-deep-research-report.md`, secciones sobre UPC, ajuste de riesgo, RIPS-FEV, brechas y recomendaciones para Colombia.
- `chatgpt-deep-research-report.md`, secciones sobre ajuste de riesgo, modelos HCC/ACG/CRG/DxCG, SGSSS, RIPS, MIPRES y recomendaciones.

## Próximo capítulo

➡️ **[Colombia High-Cost Conditions and Risk Pooling](35-colombia-high-cost-conditions-and-risk-pooling.md)**
