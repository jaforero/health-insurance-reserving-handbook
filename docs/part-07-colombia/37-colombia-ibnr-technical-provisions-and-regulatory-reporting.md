---
title: "IBNR, provisiones técnicas y reporte regulatorio en Colombia"
description: "Articulación entre IBNR, provisiones técnicas, cierre financiero y reporte regulatorio en el sistema de salud colombiano."
chapter: 37
part: "part-07-colombia"
language: "es"
status: "draft"
version: "0.1.11"
last_updated: "2026-07-14"
jurisdiction: "Colombia"
---

# IBNR, provisiones técnicas y reporte regulatorio en Colombia

Este capítulo define un marco técnico para estimar, documentar, controlar y reportar provisiones de siniestros en salud en Colombia, con énfasis en IBNR, obligaciones conocidas, obligaciones no liquidadas, desarrollo de pagos, glosas, alto costo, suficiencia patrimonial y reporting regulatorio.

El propósito no es reemplazar la normativa vigente ni emitir una interpretación legal. El propósito es construir una guía actuarial que permita que una EPS, asegurador, consultor, auditor o regulador estructure una nota técnica robusta, reconciliable y defendible. En la práctica colombiana, la estimación de pasivos en salud debe integrar datos asistenciales, cuentas médicas, pagos, glosas, contabilidad, contratos, liquidez, alto costo, UPC, MIPRES, presupuestos máximos y juicio actuarial.

Una provisión técnicamente razonable no es solo un número. Es un sistema de estimación, control, explicación y gobierno.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Diferenciar IBNR, IBNER, obligaciones conocidas liquidadas, obligaciones conocidas no liquidadas y pasivos pendientes de pago.
- Diseñar una arquitectura de provisiones técnicas para salud en Colombia.
- Construir triángulos de pagos, incurridos, radicados, reconocidos y glosados.
- Aplicar Chain Ladder, Bornhuetter-Ferguson, Cape Cod, GLM y métodos caso a caso según segmento.
- Reconciliar resultados actuariales con contabilidad, tesorería y operación.
- Documentar supuestos, limitaciones, sensibilidad y cambios metodológicos.
- Preparar reporting ejecutivo, técnico y regulatorio.

## 1. Concepto de provisión técnica en salud

Una provisión técnica representa la mejor estimación disponible de obligaciones asociadas a servicios ya ocurridos o esperados bajo la cobertura vigente, según el alcance financiero definido. En salud, el pasivo puede emerger por servicios prestados, cuentas radicadas, cuentas en auditoría, glosas parcialmente reconocibles, pagos pendientes, servicios autorizados no facturados y siniestros ocurridos pero aún no reportados.

Una forma general de descomposición es:

$$
\text{Pasivo total} = \text{Pendiente conocido} + \text{IBNER} + \text{IBNR} + \text{Margen o ajuste prudencial}
$$

donde:

- pendiente conocido corresponde a obligaciones identificadas y pendientes de pago o reconocimiento;
- IBNER captura desarrollo adicional sobre siniestros ya reportados;
- IBNR captura siniestros ocurridos pero no reportados o no registrados en la base usada;
- margen o ajuste prudencial cubre incertidumbre, si el marco contable o regulatorio lo requiere.

El uso de cada componente debe estar definido en la nota técnica. No debe haber doble conteo entre componentes.

## 2. Taxonomía de pasivos

Una taxonomía práctica para salud en Colombia puede estructurarse así:

| Componente | Descripción | Fuente típica |
|---|---|---|
| Obligaciones liquidadas pendientes de pago | Cuentas reconocidas o liquidadas, aún no pagadas | Pagos, contabilidad, tesorería |
| Obligaciones conocidas no liquidadas | Cuentas radicadas o en auditoría sin valor final | Radicación, auditoría médica |
| Glosas con probabilidad de reconocimiento | Valor objetado que puede levantarse | Glosas, conciliaciones |
| IBNER | Desarrollo adicional de cuentas ya reportadas | Triángulos de incurridos/reconocidos |
| IBNR puro | Servicios prestados no reportados ni radicados | Triángulos, autorizaciones, patrones históricos |
| Alto costo caso a caso | Eventos materiales con seguimiento individual | CAC, MIPRES, UCI, oncología, ERC |
| Servicios autorizados no facturados | Autorizaciones con alta probabilidad de uso | Autorizaciones, red prestadora |
| Ajustes por corte | Cuentas en tránsito o rezagos de carga | Operación, tecnología |

Esta taxonomía debe conectarse con el plan contable y con el reporte regulatorio aplicable. Si la taxonomía actuarial y la contable no coinciden, debe existir un puente de reconciliación.

## 3. Fechas críticas

El cálculo de provisiones depende de fechas. Las más importantes son:

| Fecha | Uso |
|---|---|
| Prestación | Periodo de incurrencia clínica |
| Radicación | Desarrollo operativo de cuentas |
| Facturación | Control de FEV y cuentas emitidas |
| Auditoría | Ciclo de glosa y reconocimiento |
| Reconocimiento | Incurrido técnico o contable |
| Pago | Flujo de caja y triángulo de pagos |
| Cierre contable | Corte oficial de reporte |

Un error frecuente es construir triángulos con fecha de factura como si fuera fecha de prestación. Esto puede producir reservas artificialmente bajas o altas, según el patrón de radicación.

La nota técnica debe declarar explícitamente:

- fecha origen;
- fecha desarrollo;
- fecha de corte;
- tratamiento de cuentas posteriores al cierre;
- tratamiento de reversos, anulaciones y notas crédito.

## 4. Bases de estimación

Las provisiones pueden estimarse sobre distintas bases:

| Base | Pregunta | Uso |
|---|---|---|
| Facturado | ¿Qué se cobró? | Auditoría, glosas, presión operativa |
| Radicado | ¿Qué llegó al pagador? | Rezagos y cuentas en proceso |
| Reconocido | ¿Qué se acepta como obligación? | Incurrido técnico |
| Pagado | ¿Qué salió de caja? | Liquidez y cash flow |
| Técnico depurado | ¿Cuál es el costo esperado económico? | Reserving y suficiencia |

El resultado principal debe usar la base que mejor representa la obligación que se quiere medir. En salud, el valor pagado puede estar afectado por liquidez; el facturado puede estar afectado por glosas; el reconocido puede depender de criterios de auditoría. Por eso, a menudo se requieren varias vistas.

## 5. Triángulos relevantes

Una EPS o asegurador de salud debería mantener más de un triángulo.

| Triángulo | Periodo origen | Periodo desarrollo | Uso |
|---|---|---|---|
| Pagos | Prestación | Pago | Flujo de caja e IBNR pagado |
| Reconocidos | Prestación | Reconocimiento | Incurrido técnico |
| Radicados | Prestación | Radicación | Rezago operativo |
| Facturados | Prestación | Facturación | Presión de cuentas |
| Glosas | Radicación | Resolución | IBNER por glosa |
| Alto costo | Prestación / diagnóstico | Pago / reconocimiento | Eventos extremos |

El triángulo de pagos no sustituye el triángulo de reconocidos. Ambos responden preguntas distintas.

## 6. Métodos aplicables

La elección metodológica debe depender de madurez del segmento, calidad de datos y estabilidad del proceso.

| Método | Uso recomendado | Riesgo |
|---|---|---|
| Chain Ladder | Segmentos estables con desarrollo creíble | Sensible a cambios operativos |
| Bornhuetter-Ferguson | Periodos inmaduros o cambios recientes | Depende de expected loss |
| Cape Cod | Cuando se necesita expected loss desde experiencia | Mezcla exposición y experiencia |
| GLM reserving | Datos granulares o celdas con covariables | Mayor complejidad |
| Caso a caso | Alto costo material | Subjetividad y seguimiento manual |
| Simulación | Colas, alto costo, stress testing | Requiere supuestos fuertes |
| Método híbrido | Salud con operación cambiante | Riesgo de doble conteo |

Una metodología robusta normalmente combina varios métodos y usa selección actuarial explícita.

## 7. Chain Ladder en salud

Chain Ladder proyecta desarrollo futuro a partir de factores históricos:

$$
F_{a,d} = \frac{C_{a,d+1}}{C_{a,d}}
$$

y:

$$
\widehat{C}_{a,\infty} = C_{a,d} \times \prod_{k=d}^{D} F_k
$$

En salud, Chain Ladder puede funcionar para bloques masivos y estables, pero se debilita si:

- cambia la política de pagos;
- hay represamiento de cuentas;
- cambian reglas de glosa;
- cambia la red de prestadores;
- se implementa una nueva plataforma;
- hay intervención administrativa;
- se modifica la facturación electrónica;
- hay cambios de cobertura o tecnologías.

Por eso, cada factor seleccionado debe ir acompañado de diagnóstico operacional.

## 8. Bornhuetter-Ferguson

Bornhuetter-Ferguson combina experiencia emergida con expectativa previa:

$$
\widehat{Ultimate}_{a} = \text{Emergido}_{a} + \text{Expected}_{a} \times (1 - \% \text{emergido}_{a})
$$

En salud, el expected puede construirse con:

- UPC o ingreso esperado;
- siniestralidad esperada;
- morbilidad ajustada;
- alto costo esperado;
- tendencia médica;
- mezcla de contratos;
- juicio actuarial documentado.

El BF es útil para periodos inmaduros porque evita que pocos pagos tempranos determinen todo el ultimate.

## 9. Expected loss ratio ajustado

El expected loss ratio para Colombia no debería ser plano si existen diferencias materiales de morbilidad y alto costo.

Una estructura posible:

$$
\text{ELR}_{g,t} = \text{ELR base}_{t} \times \text{factor morbilidad}_{g,t} \times \text{factor alto costo}_{g,t} \times \text{factor operación}_{g,t} \times \text{factor tendencia}_{t}
$$

donde $g$ puede ser EPS, régimen, región, cohorte, contrato o segmento.

El factor operación no debe usarse para esconder ineficiencias. Debe capturar cambios reales de desarrollo, radicación, reconocimiento o pago.

## 10. Glosas e IBNER

Las glosas generan un problema específico: el valor reportado inicialmente no es necesariamente el valor final reconocido.

Una cuenta glosada puede:

- mantenerse glosada;
- levantarse parcialmente;
- levantarse totalmente;
- conciliarse;
- litigarse;
- pagarse tardíamente;
- anularse.

El IBNER de glosas puede modelarse como:

$$
E[\text{Reconocimiento futuro}] = \sum_i \text{Valor glosado}_i \times P(\text{levantamiento}_i) \times \text{porcentaje esperado reconocido}_i
$$

Variables útiles:

- causal de glosa;
- prestador;
- servicio;
- valor;
- antigüedad;
- historial de conciliación;
- diagnóstico;
- contrato;
- región;
- auditor responsable.

Las glosas de alto valor deben revisarse caso a caso.

## 11. Alto costo en provisiones

El alto costo no debe mezclarse sin control con gasto ordinario.

Segmentos recomendados:

- Cuenta de Alto Costo;
- MIPRES / No UPC;
- oncología;
- enfermedad renal crónica;
- VIH;
- UCI prolongada;
- trasplantes;
- enfermedades huérfanas;
- medicamentos biológicos;
- neonatos de alta complejidad.

Métodos:

| Segmento | Método |
|---|---|
| Alto costo recurrente | BF con expected clínico |
| Evento material conocido | Caso a caso |
| Tecnología nueva | Escenario + sensibilidad |
| Enfermedad huérfana | Riesgo colectivo |
| Cohorte crónica | Modelo multiestado |

El capítulo 35 desarrolla la lógica de pooling. En provisiones, el punto central es evitar que la cola extrema distorsione factores del gasto ordinario.

## 12. IBNR puro

El IBNR puro corresponde a servicios ocurridos antes del corte que aún no aparecen en la base. En salud puede surgir por:

- prestación no facturada;
- factura no radicada;
- archivo no cargado;
- cuenta devuelta pendiente de corrección;
- servicio autorizado pero no facturado;
- rezago del prestador;
- falla tecnológica;
- acumulación operativa;
- prestación por fuera de red.

La estimación puede usar:

- factores de desarrollo de radicación;
- triángulos de pagos o reconocidos;
- autorizaciones pendientes;
- comportamiento de prestadores;
- modelos de rezago;
- experiencia de cierres previos.

## 13. IBNER

IBNER corresponde a desarrollo posterior sobre siniestros ya conocidos. En salud incluye:

- ajustes de valor;
- pagos adicionales;
- levantamiento de glosas;
- recobros o reversos;
- cuentas complementarias;
- liquidación final de paquetes;
- conciliaciones.

El IBNER puede ser positivo o negativo. Una nota técnica robusta no asume que todo desarrollo sobre reportado es positivo.

## 14. Margen de incertidumbre

Según el marco aplicable, puede requerirse o no un margen explícito. Técnicamente, el margen puede responder a:

- volatilidad de proceso;
- incertidumbre de parámetros;
- riesgo de modelo;
- datos incompletos;
- cambios operativos recientes;
- cola de alto costo;
- litigios o glosas;
- concentración de prestadores;
- cambios regulatorios.

Una estructura posible:

$$
\text{Provisión seleccionada} = \text{Estimación central} + \text{margen técnico}
$$

El margen no debe reemplazar una mala estimación central. Debe cuantificar incertidumbre residual.

## 15. Reconciliación con contabilidad

La provisión actuarial debe reconciliar con libros.

Puente conceptual:

| Elemento | Signo |
|---|---|
| Cuentas por pagar reconocidas | + |
| Cuentas radicadas no reconocidas esperadas | + |
| IBNR puro | + |
| IBNER esperado | + / - |
| Glosas no recuperables | - |
| Pagos posteriores al corte ya considerados | - |
| Reversos o notas crédito | - |
| Margen técnico | + |

La reconciliación debe explicar diferencias entre:

- pasivo contable;
- provisión actuarial;
- reporte regulatorio;
- estimación de tesorería;
- cuentas médicas operativas.

## 16. Reporting regulatorio

Un paquete de reporting debería incluir al menos:

- resumen ejecutivo;
- alcance y fecha de corte;
- definición de pasivo;
- fuentes de datos;
- reconciliación de datos;
- métodos aplicados;
- supuestos seleccionados;
- resultados por segmento;
- comparación con periodo anterior;
- análisis de variación;
- sensibilidad;
- limitaciones;
- controles realizados;
- cambios metodológicos;
- certificaciones internas, si aplican.

Para uso regulatorio, la terminología debe alinearse con las categorías oficiales vigentes. Si el modelo interno usa categorías más detalladas, debe existir mapeo.

## 17. Análisis de variación

Cada cierre debe explicar cambios contra el cierre anterior.

| Driver | Pregunta |
|---|---|
| Exposición | ¿Cambió la población afiliada? |
| Morbilidad | ¿Cambió el perfil clínico? |
| Frecuencia | ¿Aumentaron servicios? |
| Severidad | ¿Cambió costo unitario? |
| Desarrollo | ¿Cambió el patrón de pago o radicación? |
| Glosas | ¿Cambió reconocimiento esperado? |
| Alto costo | ¿Entraron casos extremos? |
| Tendencia | ¿Inflación médica o tecnología? |
| Operación | ¿Backlog, conciliación, intervención? |
| Método | ¿Cambió selección actuarial? |

Sin análisis de variación, el resultado es difícil de gobernar.

## 18. Sensibilidades

Las sensibilidades mínimas:

- factores de desarrollo altos/bajos;
- expected loss ratio alternativo;
- reconocimiento de glosas;
- rezago de radicación;
- cola de alto costo;
- inflación médica;
- exclusión/inclusión de outliers;
- cambio de base pagado vs reconocido;
- margen técnico;
- selección de método.

El objetivo no es multiplicar escenarios, sino identificar qué supuestos cambian materialmente la conclusión.

## 19. Backtesting

El backtesting debe comparar estimaciones anteriores contra desarrollo observado.

Métricas:

| Métrica | Uso |
|---|---|
| Error ultimate | Precisión agregada |
| Error por origen | Detección de sesgo temporal |
| Error por segmento | Problemas en alto costo o glosas |
| Desarrollo posterior | Adecuación de IBNR |
| O/E | Calibración de expected loss |
| Error de cola | Alto costo subestimado |

El backtesting debe documentarse y afectar selecciones futuras. Si el modelo se equivoca sistemáticamente, el método debe ajustarse.

## 20. Gobierno y aprobación

Un proceso de provisiones debe tener gobierno formal.

| Etapa | Responsable típico |
|---|---|
| Extracción de datos | Tecnología / datos |
| Validación de datos | Actuarial + operación |
| Reconciliación contable | Finanzas |
| Selección metodológica | Actuarial |
| Revisión clínica | Auditoría médica |
| Revisión de alto costo | Gestión de riesgo / clínica |
| Revisión independiente | Riesgos / auditoría interna |
| Aprobación | Dirección financiera / técnica |
| Reporte | Finanzas / actuarial / cumplimiento |

El comité debe registrar decisiones, supuestos, cambios y disensos materiales.

## 21. Modelo de nota técnica

Una nota técnica mínima puede tener esta estructura:

1. Objetivo.
2. Alcance.
3. Marco normativo aplicable.
4. Definiciones.
5. Fecha de corte.
6. Fuentes de datos.
7. Validación y reconciliación.
8. Segmentación.
9. Métodos.
10. Supuestos.
11. Resultados.
12. Análisis de variación.
13. Sensibilidades.
14. Backtesting.
15. Limitaciones.
16. Gobierno y aprobaciones.
17. Anexos.

La nota debe permitir reconstruir el resultado.

## 22. Señales de alerta

Indicadores que requieren revisión:

- caída abrupta de IBNR sin cambio operativo documentado;
- reducción de factores de desarrollo sin evidencia;
- aumento de glosas no reconocido en provisión;
- alto crecimiento de cuentas radicadas no liquidadas;
- aumento del rezago prestación-pago;
- divergencia entre pagos y reconocidos;
- concentración de pasivo en pocos prestadores;
- cambio material de mix de servicios;
- aumento de alto costo no reflejado en expected loss;
- diferencias entre contabilidad y base actuarial;
- crecimiento de autorizaciones no facturadas.

Estas señales no implican error automáticamente, pero requieren explicación.

## 23. Relación con liquidez

La provisión mide obligación esperada. La liquidez mide capacidad de pago. Ambas se conectan pero no son equivalentes.

Una entidad puede tener provisión adecuada y déficit de caja. También puede mostrar pagos bajos por restricción de liquidez y, por tanto, un triángulo de pagos artificialmente inmaduro. En esos casos, el uso exclusivo de pagos puede subestimar el pasivo económico.

Por eso, el reporting debe incluir:

- pasivo reconocido;
- IBNR;
- pagos esperados próximos meses;
- backlog de cuentas;
- edad de cuentas por pagar;
- concentración por prestador;
- cuentas de alto valor.

## 24. Relación con solvencia

La provisión técnica alimenta la evaluación de solvencia. Si el pasivo está subestimado, el patrimonio y los indicadores de solvencia se ven artificialmente mejores.

El análisis de solvencia debe considerar:

- estimación central;
- margen técnico;
- stress de alto costo;
- deterioro de glosas;
- aumento de rezagos;
- insuficiencia UPC;
- concentración de riesgo;
- dependencia de pagos extraordinarios o mecanismos de compensación.

El capítulo 38 puede desarrollar este tema con mayor profundidad.

## 25. Checklist operativo

Antes de cerrar provisiones, verificar:

- ¿Está definida la fecha de corte?
- ¿La población está reconciliada?
- ¿Las fuentes de datos están documentadas?
- ¿Prestación, radicación, reconocimiento y pago están separadas?
- ¿Hay puente con contabilidad?
- ¿Se separan obligaciones conocidas, IBNER e IBNR?
- ¿Se analizan glosas?
- ¿Se separa alto costo?
- ¿Se identifican outliers?
- ¿Se documentan cambios operativos?
- ¿Se comparan varios métodos?
- ¿Se justifica la selección actuarial?
- ¿Se hacen sensibilidades?
- ¿Se ejecuta backtesting?
- ¿Se documentan limitaciones?
- ¿Hay aprobación formal?

## 26. Conclusión

La estimación de IBNR y provisiones técnicas en salud en Colombia requiere más que aplicar factores de desarrollo. Requiere integrar operación, auditoría médica, glosas, pagos, alto costo, morbilidad, contabilidad y liquidez.

El estándar técnico esperado debe ser una provisión trazable, reconciliable, segmentada, sensible a la cola y documentada. La metodología puede iniciar con Chain Ladder y Bornhuetter-Ferguson, pero debe evolucionar hacia modelos que reflejen morbilidad, alto costo, rezagos operativos y calidad de datos.

Un buen proceso de provisiones no elimina la incertidumbre. La hace visible, medible y gobernable.

## Fuentes de trabajo del proyecto

- ASOP No. 28, *Statements of Actuarial Opinion Regarding Health Insurance Assets and Liabilities*.
- ASOP No. 43, *Property/Casualty Unpaid Claim Estimates*, usado como referencia conceptual sobre estimaciones de obligaciones por siniestros ocurridos.
- ASOP No. 56, *Modeling*, como referencia para uso previsto, estructura, datos, supuestos, validación y riesgo de modelo.
- `gemini-deep-research-report.md`, secciones sobre reservas IBNR, Cuenta de Alto Costo, MIPRES, presupuestos máximos y brechas regulatorias/metodológicas.
- `chatgpt-deep-research-report.md`, secciones sobre SGSSS, reservas, solvencia, IBNR, modelos actuariales y recomendaciones para Colombia.

## Próximo capítulo

➡️ **38 · Colombia Solvency, Liquidity and Stress Testing** *(pendiente de crear)*
