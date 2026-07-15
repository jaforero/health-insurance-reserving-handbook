---
title: "Planeación de escenarios y hoja de ruta de reforma"
description: "Planeación de escenarios actuariales y hoja de ruta para gestionar cambios regulatorios y reformas del sistema de salud colombiano."
chapter: 39
part: "part-07-colombia"
language: "es"
status: "draft"
version: "0.1.11"
last_updated: "2026-07-14"
jurisdiction: "Colombia"
---

# Planeación de escenarios y hoja de ruta de reforma

Este capítulo cierra el bloque Colombia con una hoja de ruta técnica para planear escenarios, priorizar reformas actuariales y secuenciar capacidades de reserving, datos, ajuste de riesgo, alto costo, solvencia y reporting. No es una propuesta legal ni una predicción política. Es un marco de implementación para transformar un sistema de estimación reactivo en una arquitectura actuarial prospectiva, trazable y gobernable.

La idea central es pragmática: ningún sistema de salud cambia de una vez. La reforma técnica debe avanzar por capas. Primero se estabilizan datos y reservas. Luego se construyen modelos de morbilidad y alto costo. Después se integran escenarios de solvencia, liquidez y presupuestos. Finalmente se institucionaliza un ciclo continuo de monitoreo, recalibración y mejora.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Diseñar escenarios actuariales para el SGSSS o una EPS.
- Priorizar iniciativas de corto, mediano y largo plazo.
- Traducir brechas de datos, modelos y regulación en una hoja de ruta ejecutable.
- Definir dependencias entre RIPS-FEV, IBNR, UPC, morbilidad, MIPRES, alto costo y solvencia.
- Establecer indicadores de avance y criterios de éxito.
- Diferenciar pilotos analíticos, shadow models, modelos financieros vinculantes y reporting regulatorio.
- Construir un plan de gobierno para implementación gradual.

## 1. Por qué hacer planeación de escenarios

La planeación de escenarios es necesaria porque el sistema de salud enfrenta incertidumbre simultánea:

- demográfica;
- epidemiológica;
- tecnológica;
- regulatoria;
- financiera;
- operativa;
- política;
- judicial;
- climática;
- de datos.

Un forecast único tiende a ocultar riesgos. Un escenario bien diseñado permite responder preguntas como:

- ¿Qué pasa si la morbilidad crónica aumenta más rápido que la UPC?
- ¿Qué pasa si los datos RIPS-FEV mejoran y revelan pasivos antes no observados?
- ¿Qué pasa si alto costo crece por nuevas tecnologías?
- ¿Qué pasa si se acumulan glosas o cuentas por pagar?
- ¿Qué pasa si la liquidez se deteriora antes de que la solvencia contable lo muestre?
- ¿Qué capacidades técnicas deben construirse primero?

El objetivo no es adivinar el futuro. Es preparar decisiones robustas bajo varios futuros plausibles.

## 2. Principios de la hoja de ruta

La hoja de ruta debe seguir principios explícitos.

| Principio | Implicación |
|---|---|
| Secuencialidad | No se implementa ajuste de riesgo robusto sin datos confiables |
| Trazabilidad | Cada resultado debe poder reconstruirse |
| Proporcionalidad | La complejidad crece según calidad de datos y materialidad |
| Transparencia | Supuestos y limitaciones se documentan |
| Separación de capas | UPC, alto costo, MIPRES, reservas y liquidez se modelan con lógica propia |
| Validación antes de uso financiero | Primero shadow model, luego uso gradual |
| Gobierno | Cambios de modelo y supuestos requieren aprobación |
| Equidad | El score de riesgo financia necesidad, no selección |
| Monitoreo | La reforma técnica se recalibra con experiencia |

Sin estos principios, la modernización actuarial puede convertirse en una colección de modelos desconectados.

## 3. Brechas principales

Las brechas identificadas en el proyecto pueden agruparse así:

| Brecha | Manifestación | Riesgo |
|---|---|---|
| Datos | RIPS, FEV, pagos, glosas y afiliación no siempre reconciliados | Modelos no confiables |
| Reservas | IBNR y obligaciones pendientes con métodos heterogéneos | Pasivo subestimado |
| Morbilidad | UPC basada principalmente en variables no clínicas | Desalineación de recursos |
| Alto costo | MIPRES y tecnologías extremas con alta volatilidad | Déficit y cola no financiada |
| Solvencia | Indicadores contables sin stress técnico suficiente | Deterioro tardíamente visible |
| Liquidez | Cuentas por pagar y pagos tardíos | Riesgo de red y acceso |
| Talento | Escasez de perfiles actuariales + salud + datos | Baja capacidad de implementación |
| Gobierno | Modelos sin versionamiento o validación independiente | Riesgo de modelo |

La hoja de ruta debe atacar estas brechas en orden de dependencia.

## 4. Mapa de dependencias

La secuencia técnica recomendada es:

| Capacidad | Depende de | Habilita |
|---|---|---|
| Calidad de datos RIPS-FEV | Catálogos, llaves, fechas, pagos | Reservas, morbilidad, alto costo |
| Reconciliación financiera | Contabilidad, tesorería, cuentas médicas | Reporting confiable |
| IBNR estandarizado | Triángulos y corte de datos | Solvencia y liquidez |
| Morbilidad longitudinal | RIPS, farmacia, afiliación | UPC ajustada por riesgo |
| Alto costo separado | CAC, MIPRES, eventos extremos | Pooling y presupuestos |
| Stress testing | Reservas, liquidez, morbilidad | Capital y planes de mitigación |
| Gobierno de modelos | Versionamiento, validación, comités | Uso regulatorio o financiero |
| Reporting sectorial | Estándares y definiciones comunes | Comparabilidad |

Intentar saltar directamente a IA avanzada sin estas capas aumenta riesgo de opacidad y error.

## 5. Escenarios base

Una arquitectura de planeación puede usar cinco escenarios.

| Escenario | Descripción | Señal principal |
|---|---|---|
| Continuidad frágil | Se mantiene arquitectura actual con mejoras parciales | Déficit técnico persistente |
| Datos primero | RIPS-FEV y reconciliación mejoran antes de modelos avanzados | Mayor visibilidad de pasivos |
| Morbilidad prospectiva | UPC incorpora gradualmente ajuste clínico | Redistribución de recursos |
| Choque de alto costo | Nuevas tecnologías y enfermedades severas presionan cola | Volatilidad y necesidad de pooling |
| Transformación integrada | Datos, reservas, morbilidad, alto costo y solvencia se integran | Gestión prospectiva |

Cada escenario debe probarse con indicadores comunes, no con narrativas aisladas.

## 6. Variables de escenario

Las variables mínimas:

| Variable | Bajo | Base | Alto |
|---|---:|---:|---:|
| Crecimiento de exposición | - | Esperado | + |
| Morbilidad crónica | Estable | Tendencia | Acelerada |
| Inflación médica | Moderada | Esperada | Alta |
| Alto costo | P50 | P75 | P95/P99 |
| Rezago de radicación | Mejora | Histórico | Deterioro |
| Glosa levantada | Baja | Esperada | Alta |
| Liquidez | Suficiente | Ajustada | Restringida |
| Calidad de datos | Débil | Mejorando | Robusta |
| Tecnología | Lenta | Normal | Rápida |
| Regulación | Sin cambio | Gradual | Disruptiva |

El modelo de escenarios debe permitir cambiar estas variables y observar impacto en reservas, caja, solvencia y suficiencia UPC.

## 7. Escenario 1: continuidad frágil

Este escenario asume mejoras marginales, pero sin rediseño metodológico profundo.

Características:

- reservas calculadas con métodos heterogéneos;
- datos parcialmente reconciliados;
- UPC con ajuste clínico limitado;
- alto costo tratado con mecanismos fragmentados;
- stress testing no integrado al cierre financiero;
- reporting más descriptivo que prospectivo.

Riesgos:

- subestimación de pasivos;
- deterioro de liquidez;
- acumulación de cuentas por pagar;
- selección adversa;
- déficit técnico no visible oportunamente;
- decisiones reactivas.

Uso del escenario: definir el costo de no modernizar.

## 8. Escenario 2: datos primero

Este escenario prioriza calidad, interoperabilidad y reconciliación antes de cambios financieros mayores.

Acciones:

- fortalecer llaves de afiliado, prestación, factura y pago;
- separar fechas de prestación, radicación, reconocimiento y pago;
- reconciliar cuentas médicas con contabilidad;
- monitorear completitud diagnóstica;
- crear tableros de rezagos, glosas y pagos;
- documentar rupturas de serie.

Resultado esperado:

- mejor IBNR;
- mayor visibilidad de obligaciones;
- detección de backlog;
- bases aptas para morbilidad y alto costo;
- reducción de discusiones sobre calidad de datos.

Riesgo: al mejorar datos, pueden emerger pasivos antes no visibles. Esto no es falla del modelo; es corrección de visibilidad.

## 9. Escenario 3: morbilidad prospectiva

Este escenario incorpora gradualmente ajuste por riesgo clínico en análisis de suficiencia.

Acciones:

- construir matriz afiliado-mes;
- crear agrupadores de condiciones;
- validar diagnósticos con farmacia y procedimientos;
- estimar GLM/GAM de costo esperado;
- comparar contra modelo demográfico;
- operar inicialmente en shadow mode;
- medir redistribución por EPS, región y cohorte;
- auditar riesgo de upcoding.

Resultado esperado:

- mejor explicación de diferencias de costo;
- detección de poblaciones subcompensadas;
- evidencia técnica para ajuste de UPC;
- soporte para gestión clínica y prevención.

Riesgo: incentivos de codificación oportunista si el modelo se vuelve financiero sin controles.

## 10. Escenario 4: choque de alto costo

Este escenario prueba presión por cola extrema.

Supuestos posibles:

- aumento de tratamientos oncológicos;
- nuevas terapias biológicas;
- incremento de enfermedades huérfanas diagnosticadas;
- mayor severidad en ERC;
- judicialización de tecnologías;
- concentración de pocos pacientes con costo extremo;
- rezagos de pago asociados a facturas grandes.

Acciones:

- separar alto costo de gasto ordinario;
- aplicar modelos frecuencia-severidad;
- calcular P95/P99 y TVaR;
- definir umbrales de pooling;
- mapear CAC, MIPRES, UPC y reservas;
- evitar doble conteo;
- crear tablero de casos materiales.

Resultado esperado:

- presupuesto más realista;
- reservas de cola;
- mecanismos de pooling;
- mejor protección de liquidez.

## 11. Escenario 5: transformación integrada

Este escenario representa el estado objetivo.

Características:

- datos RIPS-FEV integrados y reconciliados;
- IBNR estandarizado con backtesting;
- UPC analizada con morbilidad;
- alto costo modelado con riesgo colectivo;
- stress testing recurrente;
- reporting ejecutivo y técnico;
- gobierno de modelos;
- pilotos regulatorios o financieros graduales;
- transparencia de supuestos.

El resultado no es un modelo único. Es una arquitectura de decisión.

## 12. Hoja de ruta por horizontes

Una hoja de ruta pragmática:

| Horizonte | Prioridad | Entregable |
|---|---|---|
| 0–6 meses | Auditoría de datos y reservas | Diagnóstico de brechas |
| 6–12 meses | IBNR estandarizado y reconciliación | Nota técnica base |
| 12–18 meses | Tablero de liquidez, glosas y alto costo | Monitoreo mensual |
| 18–24 meses | Piloto de morbilidad UPC en shadow mode | Modelo GLM/GAM validado |
| 24–36 meses | Riesgo colectivo MIPRES/alto costo | Distribución de pérdida |
| 3–5 años | Stress testing integrado | Capital y solvencia económica |
| 5–10 años | Plataforma predictiva sectorial | Gestión prospectiva continua |

Las fechas son orientativas. La secuencia importa más que el calendario exacto.

## 13. Fase 1: estabilización de datos

Objetivo: crear una base confiable para decisiones.

Entregables:

- inventario de fuentes;
- diccionario de datos;
- validaciones de calidad;
- reconciliación con contabilidad;
- tablero de completitud;
- identificación de duplicados;
- control de fechas críticas;
- linaje de extracción;
- documentación de limitaciones.

Indicadores:

| Indicador | Meta conceptual |
|---|---|
| Servicios con afiliado válido | Alto |
| Diagnósticos válidos | Alto |
| Facturas cruzadas con pago/estado | Alto |
| Duplicados críticos | Bajo |
| Reconciliación contable | Materialmente explicada |
| Campos críticos faltantes | Bajo |

Sin esta fase, las fases posteriores tienen riesgo alto.

## 14. Fase 2: reservas y pasivos

Objetivo: estandarizar IBNR, obligaciones conocidas e IBNER.

Entregables:

- triángulos de pagos, reconocidos, radicados y glosas;
- selección metodológica;
- expected loss ratio;
- segmentación alto costo;
- backtesting;
- puente contable-actuarial;
- análisis de variación;
- sensibilidad;
- comité de aprobación.

Indicadores:

- error de backtesting;
- IBNR / costo mensual;
- cuentas por pagar / costo mensual;
- rezago prestación-pago;
- glosa levantada;
- concentración por prestador;
- pasivo no reconciliado.

## 15. Fase 3: alto costo y pooling

Objetivo: separar cola extrema de gasto ordinario.

Entregables:

- catálogo de condiciones de alto costo;
- modelo frecuencia-severidad;
- umbrales de pooling;
- escenarios P90/P95/P99;
- tablero de casos materiales;
- reglas de doble conteo;
- integración CAC/MIPRES/UPC;
- estimación de IBNR alto costo.

Indicadores:

- top 1% share;
- alto costo / costo total;
- casos sobre umbral;
- TVaR;
- costo por condición;
- presupuesto esperado vs observado;
- rezago de pago alto costo.

## 16. Fase 4: morbilidad y UPC

Objetivo: medir suficiencia según riesgo clínico.

Entregables:

- matriz afiliado-mes;
- agrupadores clínicos;
- modelo demográfico benchmark;
- modelo clínico GLM/GAM;
- comparación O/E;
- análisis por EPS, región y cohorte;
- auditoría de codificación;
- shadow model.

Indicadores:

- mejora de calibración;
- O/E por decil de riesgo;
- estabilidad de score;
- prevalencia crónica;
- concentración de subcompensación;
- sensibilidad a codificación.

## 17. Fase 5: solvencia y liquidez

Objetivo: conectar pasivos, caja y patrimonio económico.

Entregables:

- modelo de flujo de caja;
- escenarios de estrés;
- capital económico;
- reverse stress testing;
- indicadores de alerta;
- plan de mitigación;
- reporting para comité.

Indicadores:

- caja / pagos próximos 30 días;
- stress loss / patrimonio;
- déficit acumulado bajo escenario adverso;
- ratio de suficiencia UPC;
- patrimonio económico / pasivo técnico;
- deterioro de cartera;
- edad de cuentas por pagar.

## 18. Fase 6: institucionalización

Objetivo: convertir modelos en proceso permanente.

Entregables:

- política de gobierno de modelos;
- repositorio versionado;
- periodicidad de recalibración;
- validación independiente;
- comité técnico;
- documentación estándar;
- entrenamiento;
- reportes reproducibles;
- plan de actualización normativa o metodológica.

Indicadores:

- modelos con versión documentada;
- corridas reproducibles;
- cambios aprobados;
- hallazgos cerrados;
- backtesting ejecutado;
- reportes entregados a tiempo.

## 19. Priorización

No todas las iniciativas tienen el mismo valor ni la misma dependencia.

| Iniciativa | Valor | Dependencia | Prioridad |
|---|---|---|---|
| Auditoría de datos | Alta | Baja | Muy alta |
| Reconciliación contable | Alta | Media | Muy alta |
| IBNR estandarizado | Alta | Media | Muy alta |
| Tablero de liquidez | Alta | Media | Alta |
| Alto costo separado | Alta | Media | Alta |
| Morbilidad UPC | Muy alta | Alta | Alta, después de datos |
| ML avanzado | Media/alta | Alta | Media |
| IA generativa | Experimental | Muy alta | Exploratoria |
| Capital económico | Alta | Alta | Media/alta |
| Plataforma sectorial | Muy alta | Muy alta | Largo plazo |

La prioridad inicial debe ser técnica y operacional, no cosmética.

## 20. Pilotos

Los pilotos reducen riesgo de implementación.

Pilotos recomendados:

| Piloto | Objetivo |
|---|---|
| IBNR estandarizado | Comparar métodos y backtesting |
| Morbilidad GLM | Medir mejora sobre demográfico |
| Alto costo Monte Carlo | Estimar cola y presupuesto |
| Glosas predictivas | Estimar reconocimiento futuro |
| Liquidez 13 semanas | Proyectar caja médica |
| RIPS-FEV calidad | Medir completitud y trazabilidad |
| Shadow UPC | Simular transferencias sin efecto financiero |

Cada piloto debe tener hipótesis, datos, responsables, métrica de éxito y decisión posterior.

## 21. Shadow model

El shadow model es un modelo paralelo que no afecta pagos ni reportes oficiales inicialmente.

Usos:

- probar estabilidad;
- depurar datos;
- medir impacto financiero;
- identificar ganadores y perdedores;
- detectar incentivos perversos;
- generar evidencia;
- preparar transición.

El paso de shadow model a uso financiero debe requerir:

- datos suficientemente confiables;
- backtesting;
- validación independiente;
- auditoría de incentivos;
- documentación;
- aprobación de gobierno.

## 22. Gestión del cambio

La reforma técnica afecta múltiples actores.

| Actor | Interés |
|---|---|
| EPS | Suficiencia, liquidez, riesgo de selección |
| IPS | Pago oportuno, glosas, contratos |
| Regulador | Solvencia, transparencia, estabilidad |
| ADRES | Asignación y compensación |
| Pacientes | Acceso y continuidad |
| Actuarios | Métodos y documentación |
| Tecnología | Datos e interoperabilidad |
| Finanzas | Contabilidad, caja, reporting |
| Auditoría médica | Pertinencia y reconocimiento |

La gestión del cambio debe incluir capacitación, comunicación, pilotos y reglas claras.

## 23. Gobierno de escenarios

Los escenarios deben gobernarse como modelos.

| Elemento | Requisito |
|---|---|
| Dueño | Área responsable |
| Propósito | Decisión que soporta |
| Variables | Drivers explícitos |
| Supuestos | Documentados y aprobados |
| Datos | Fuente y corte |
| Frecuencia | Mensual, trimestral o por evento |
| Validación | Backtesting y revisión |
| Salida | Indicadores y decisiones |
| Archivo | Versionamiento |
| Comité | Aprobación y seguimiento |

Un escenario sin dueño ni decisión asociada pierde utilidad.

## 24. KPIs de implementación

La hoja de ruta necesita indicadores de avance.

| KPI | Interpretación |
|---|---|
| % fuentes integradas | Cobertura de datos |
| % reconciliación contable | Control financiero |
| modelos con backtesting | Madurez actuarial |
| tiempo de cierre actuarial | Eficiencia |
| hallazgos de datos cerrados | Mejora operacional |
| capítulos o notas técnicas aprobadas | Documentación |
| escenarios ejecutados | Gobierno de riesgo |
| pilotos en shadow mode | Preparación |
| modelos con validación independiente | Control |
| decisiones tomadas con evidencia | Uso real |

La implementación no se mide por número de modelos construidos, sino por decisiones mejor soportadas.

## 25. Riesgos de implementación

| Riesgo | Mitigación |
|---|---|
| Datos insuficientes | Fase de calidad y reconciliación |
| Resistencia institucional | Pilotos y transparencia |
| Opacidad de modelos | GLM/GAM base + XAI |
| Incentivos perversos | Auditoría de codificación |
| Doble conteo | Mapa de capas financieras |
| Falta de talento | Formación y documentación |
| Cambios regulatorios | Diseño modular |
| Sobrecarga operativa | Priorización por materialidad |
| Dependencia de proveedor | Estándares abiertos |
| Uso prematuro | Shadow mode obligatorio |

El riesgo más grave es usar modelos avanzados antes de tener datos y gobierno.

## 26. Roadmap integrado

Una secuencia integrada:

1. Inventario de datos.
2. Validación y reconciliación.
3. Triángulos y reservas base.
4. Backtesting y documentación.
5. Tableros de liquidez y glosas.
6. Segmentación de alto costo.
7. Modelo frecuencia-severidad.
8. Modelo de morbilidad UPC.
9. Shadow model de transferencias.
10. Stress testing integrado.
11. Capital económico.
12. Gobierno de modelos.
13. Reporting estandarizado.
14. Recalibración periódica.
15. Mejora continua.

Esta secuencia evita depender de un único “gran proyecto” y permite capturar valor incremental.

## 27. Criterios de éxito

La reforma técnica es exitosa si:

- reduce incertidumbre de reservas;
- mejora reconciliación de pasivos;
- detecta problemas de liquidez antes;
- explica diferencias de costo por morbilidad;
- separa alto costo de gasto ordinario;
- permite escenarios accionables;
- documenta supuestos y limitaciones;
- mejora comparabilidad entre periodos;
- reduce decisiones basadas en promedios simples;
- habilita discusión regulatoria basada en evidencia.

No basta con producir dashboards. Deben cambiar decisiones.

## 28. Qué no debe hacerse

Errores a evitar:

- implementar IA antes de reconciliar datos;
- usar pagos como único proxy de costo;
- mezclar UPC, MIPRES, CAC y glosas sin capas;
- aplicar Chain Ladder sin revisar cambios operativos;
- usar un score de riesgo para selección de afiliados;
- pagar por codificación sin auditoría;
- ignorar eventos posteriores;
- no documentar cambios metodológicos;
- tratar el stress testing como formalidad;
- entregar resultados sin rango de incertidumbre.

Estos errores generan una falsa sensación de precisión.

## 29. Conclusión

La modernización actuarial del sistema de salud colombiano debe ser gradual, técnica y gobernada. El punto de partida no es un modelo sofisticado, sino una base confiable de datos, reservas reconciliadas y definiciones claras. Desde allí puede avanzarse hacia morbilidad, alto costo, pooling, solvencia, liquidez, stress testing y modelos predictivos.

La hoja de ruta propuesta convierte los capítulos anteriores en un programa de implementación. Primero se mide mejor. Luego se reserva mejor. Después se financia mejor. Finalmente se gobierna mejor.

El valor práctico de esta arquitectura es que permite pasar de discusiones reactivas sobre déficit y pagos a una gestión prospectiva de riesgo, suficiencia, liquidez y sostenibilidad.

## Fuentes de trabajo del proyecto

- ASOP No. 56, *Modeling*, como referencia para propósito, estructura, datos, supuestos, validación, consistencia y riesgo de modelo.
- ASOP No. 57, *Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities*.
- ASOP No. 28, *Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities*.
- `gemini-deep-research-report.md`, secciones sobre brechas regulatorias, metodológicas, datos, talento y recomendaciones priorizadas para Colombia.
- `chatgpt-deep-research-report.md`, secciones sobre recomendaciones de corto, mediano y largo plazo, ajuste de riesgo, MIPRES, RIPS, reservas y modernización actuarial.

## Próximo capítulo

➡️ **40 · Colombia Implementation Playbook and Templates** *(pendiente de crear)*
