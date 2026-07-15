---
title: "Calidad y validación de datos RIPS–FEV en Colombia"
description: "Controles de calidad, consistencia y trazabilidad para datos RIPS y FEV usados en reservas de salud."
chapter: 36
part: "part-07-colombia"
language: "es"
status: "draft"
version: "0.1.11"
last_updated: "2026-07-14"
jurisdiction: "Colombia"
---

# Calidad y validación de datos RIPS–FEV en Colombia

Este capítulo define un marco actuarial y operativo para validar datos de salud en Colombia cuando se usan para reserving, suficiencia UPC, ajuste de riesgo, alto costo, presupuestos prospectivos y monitoreo financiero. El énfasis está en RIPS, facturación electrónica de venta en salud, pagos, glosas, MIPRES, afiliación, prestadores y trazabilidad entre prestación, factura, reconocimiento y pago.

La calidad de datos no es un asunto secundario. En reserving de salud, un error de fecha, identificación, diagnóstico, valor, estado de cuenta o duplicidad puede afectar triángulos, factores de desarrollo, estimaciones IBNR, expected loss ratios, modelos de morbilidad, presupuestos máximos y alertas de liquidez.

El principio rector es simple: ningún modelo actuarial corrige de forma confiable una base de datos que no está reconciliada. La primera línea de defensa no es el modelo, sino la validación.

## Objetivos de aprendizaje

Al terminar este capítulo, el lector debería poder:

- Identificar las fuentes de datos críticas para reserving en salud en Colombia.
- Definir controles de calidad para RIPS, FEV, pagos, glosas, afiliación y autorizaciones.
- Separar fecha de prestación, fecha de radicación, fecha de factura, fecha de reconocimiento y fecha de pago.
- Construir una base analítica apta para triángulos, IBNR y modelos predictivos.
- Detectar duplicados, rezagos, inconsistencias, valores extremos y rupturas operativas.
- Diseñar reconciliaciones entre datos operativos, contables y actuariales.
- Documentar limitaciones y supuestos de datos en una nota técnica.

## 1. Por qué RIPS-FEV importa para reserving

En salud, el siniestro no se observa como un evento único y limpio. Una prestación puede pasar por múltiples etapas:

1. ocurrencia clínica;
2. autorización;
3. prestación;
4. registro clínico;
5. codificación;
6. facturación;
7. radicación;
8. auditoría;
9. glosa o devolución;
10. reconocimiento;
11. pago parcial o total;
12. conciliación;
13. posible reapertura o ajuste.

Cada etapa puede tener una fecha distinta y un valor distinto. Para reserving, confundir estas fechas genera triángulos incorrectos. Para ajuste de riesgo, confundir diagnóstico de evento con diagnóstico histórico puede generar leakage. Para alto costo, confundir facturado con reconocido puede distorsionar severidad.

Por eso, la arquitectura de datos debe preservar el ciclo completo.

## 2. Fuentes críticas

Una base actuarial robusta debe integrar, como mínimo, las siguientes fuentes:

| Fuente | Uso principal | Riesgo de calidad |
|---|---|---|
| Afiliación / BDUA interna | Exposición, población, régimen, permanencia | Duplicidad, traslados, rezagos |
| RIPS | Diagnósticos, procedimientos, fecha de atención | Codificación inconsistente, incompletitud |
| FEV / facturación | Valor facturado, identificación de factura, prestador | Anulaciones, notas crédito, duplicados |
| Radicación | Fecha de recepción de cuenta | Rezago operativo |
| Auditoría médica | Glosas, devoluciones, pertinencia | Criterios cambiantes |
| Pagos | Fecha y valor pagado | Pagos parciales, cruces contables |
| Autorizaciones | Servicios esperados aún no facturados | Autorizaciones no utilizadas |
| MIPRES | Tecnologías No UPC y alto costo | Rezagos, cambios de indicación |
| Cuenta de Alto Costo | Cohortes clínicas específicas | Cobertura parcial |
| Contratos IPS | Modalidad, tarifa, capitación, paquete | Mezcla de precio y riesgo |
| Contabilidad | Obligaciones, cuentas por pagar, provisiones | Diferencias de corte y clasificación |

La integración debe hacerse por llaves estables: afiliado, prestación, factura, prestador, fecha, diagnóstico, servicio, valor y estado financiero.

## 3. Fechas que no deben mezclarse

La fecha correcta depende del objetivo.

| Fecha | Uso actuarial |
|---|---|
| Fecha de ocurrencia clínica | Cohorte de incurrencia |
| Fecha de prestación | Triángulos por servicio |
| Fecha de autorización | Anticipación de gasto futuro |
| Fecha de factura | Control de radicación y FEV |
| Fecha de radicación | Desarrollo operativo |
| Fecha de auditoría | Ciclo de glosa |
| Fecha de reconocimiento | Costo incurrido técnico |
| Fecha de pago | Triángulo de pagos |
| Fecha contable | Cierre financiero |

Un triángulo de pagos normalmente usa fecha de prestación o incurrencia como periodo origen y fecha de pago como desarrollo. Un triángulo de incurridos puede usar fecha de prestación y fecha de reconocimiento. Un análisis de operación puede usar fecha de radicación.

Error común: usar fecha de factura como si fuera fecha de prestación. Esto puede desplazar siniestros entre periodos y falsear patrones de desarrollo.

## 4. Estados de cuenta

Cada cuenta médica debe tener un estado trazable.

| Estado | Interpretación |
|---|---|
| Prestada | Servicio ocurrió |
| Facturada | Cuenta emitida |
| Radicada | Cuenta recibida por pagador |
| Devuelta | No entra a auditoría o pago por causal formal |
| Glosada | Valor objetado |
| Reconocida | Valor aceptado como obligación |
| Pagada parcial | Pago incompleto |
| Pagada total | Obligación extinguida |
| Conciliada | Diferencia resuelta |
| Reabierta | Ajuste posterior |

Para reserving, los estados no son etiquetas administrativas. Son variables predictivas del flujo futuro de pagos y reconocimientos.

## 5. Dimensiones de calidad de datos

Un marco mínimo debe evaluar:

| Dimensión | Pregunta |
|---|---|
| Completitud | ¿Faltan campos críticos? |
| Validez | ¿Los valores cumplen reglas de dominio? |
| Unicidad | ¿Hay duplicados? |
| Consistencia | ¿Campos relacionados se contradicen? |
| Oportunidad | ¿Los datos llegan a tiempo? |
| Exactitud | ¿Reflejan la prestación real? |
| Integridad referencial | ¿Las llaves cruzan entre tablas? |
| Trazabilidad | ¿Se puede reconstruir el ciclo? |
| Estabilidad | ¿Las reglas cambian sin documentarse? |
| Reconciliación | ¿Cuadra con contabilidad y tesorería? |

La validación debe producir indicadores cuantitativos, no solo observaciones cualitativas.

## 6. Validaciones mínimas de estructura

Antes de modelar, la base debe pasar controles básicos.

| Control | Ejemplo |
|---|---|
| Campos obligatorios | Afiliado, fecha, prestador, diagnóstico, valor |
| Tipos de dato | Fechas válidas, valores numéricos positivos |
| Rangos | Edad razonable, valor no negativo |
| Catálogos | CIE-10, CUPS, medicamentos, municipios |
| Llaves | ID factura, ID prestación, ID afiliado |
| Duplicados | Misma factura, prestación, afiliado y valor |
| Fechas imposibles | Pago antes de prestación sin explicación |
| Valores extremos | Facturas por encima de umbral |
| Estados incompatibles | Pagado sin reconocimiento |
| Exposición | Servicio fuera de vigencia de afiliación |

Estas validaciones deben ejecutarse de forma recurrente y dejar evidencia.

## 7. Reconciliación financiera

El reserving debe reconciliar al menos tres vistas:

1. vista operativa;
2. vista contable;
3. vista actuarial.

| Vista | Pregunta |
|---|---|
| Operativa | ¿Qué cuentas existen y en qué estado están? |
| Contable | ¿Qué obligaciones están registradas? |
| Actuarial | ¿Qué pagos o reconocimientos faltan por emerger? |

Una reconciliación mínima:

$$
\text{Facturado} - \text{Devuelto} - \text{Glosado no reconocido} = \text{Reconocido}
$$

Y:

$$
\text{Reconocido} - \text{Pagado} = \text{Pendiente reconocido}
$$

Además:

$$
\text{Pasivo total estimado} = \text{Pendiente reconocido} + \text{IBNR} + \text{IBNER}
$$

donde IBNER representa desarrollo adicional sobre casos ya reportados.

## 8. Separación entre costo facturado, reconocido y pagado

Los tres valores responden preguntas distintas:

| Valor | Pregunta |
|---|---|
| Facturado | ¿Qué cobró el prestador? |
| Reconocido | ¿Qué se acepta como obligación técnica o financiera? |
| Pagado | ¿Qué salió efectivamente de caja? |

Para modelos de costo médico, el valor reconocido suele ser más estable que el facturado si hay glosas relevantes. Para liquidez, el valor pagado es indispensable. Para gestión de auditoría, el facturado y glosado son críticos.

Un reserving robusto puede requerir tres triángulos:

- facturado o radicado;
- reconocido o incurrido;
- pagado.

## 9. Rezagos

Los rezagos son el corazón operativo del IBNR.

| Rezago | Definición |
|---|---|
| Prestación a factura | Tiempo entre atención y emisión |
| Factura a radicación | Tiempo hasta recepción |
| Radicación a auditoría | Tiempo de revisión |
| Auditoría a reconocimiento | Tiempo de aceptación |
| Reconocimiento a pago | Tiempo de tesorería |
| Prestación a pago | Desarrollo total |

Cada rezago puede cambiar por:

- nueva regla de facturación;
- congestión operativa;
- cambios contractuales;
- intervención administrativa;
- ajustes tecnológicos;
- nuevas validaciones;
- disputas con prestadores;
- presión de liquidez.

El análisis de triángulos debe complementarse con indicadores de rezago por etapa.

## 10. Duplicados y notas crédito

Los duplicados pueden inflar severidad, conteos y reservas. Las notas crédito pueden reducir costos retrospectivamente y alterar desarrollo.

Controles:

- detectar factura duplicada exacta;
- detectar duplicado probable por afiliado, prestador, fecha, CUPS y valor;
- vincular notas crédito a factura original;
- mantener historial de anulaciones;
- separar factura corregida de factura nueva;
- documentar reglas de reemplazo.

No se debe simplemente eliminar duplicados sin bitácora. La trazabilidad de eliminación es parte del control.

## 11. Diagnósticos y morbilidad

Para ajuste de riesgo y alto costo, los diagnósticos deben validarse.

Controles recomendados:

| Control | Propósito |
|---|---|
| Diagnóstico principal válido | Evitar códigos no informativos |
| Diagnóstico compatible con edad/sexo | Detectar errores obvios |
| Persistencia clínica | Confirmar condiciones crónicas |
| Diagnóstico + procedimiento | Coherencia clínica |
| Diagnóstico + medicamento | Validación cruzada |
| Cambio abrupto de codificación | Detectar upcoding o cambio operativo |
| Jerarquía de condiciones | Evitar doble conteo de severidad |

Una sola aparición de un diagnóstico puede ser insuficiente para clasificar una condición crónica. La regla puede requerir repetición, confirmación por medicamento o evento hospitalario.

## 12. Prestadores y contratos

La variación de costo puede deberse a riesgo clínico o a precio. El modelo debe distinguirlos.

Variables contractuales relevantes:

- modalidad: evento, paquete, capitación, pago global prospectivo;
- tarifa;
- red;
- nivel de complejidad;
- municipio;
- prestador dominante;
- cambios contractuales;
- acuerdos de conciliación;
- cuentas por fuera de contrato.

Para reserving, un cambio de contrato puede alterar patrones de pago sin que cambie la morbilidad.

## 13. Validación para triángulos

Antes de construir triángulos, validar:

- periodo origen correctamente definido;
- periodo desarrollo correctamente definido;
- exposición por periodo;
- valores negativos tratados;
- pagos parciales agregados;
- anulaciones y reversos;
- cierre de periodos;
- consistencia de moneda;
- cambios de corte;
- cuentas tardías;
- celdas anómalas.

Un triángulo debe poder reconciliarse contra una extracción base.

## 14. Validación para modelos predictivos

Para GLM, GAM, boosting o deep learning, validar:

- separación temporal entre features y target;
- ausencia de leakage;
- variables disponibles al momento de predicción;
- estabilidad de codificación;
- datos faltantes;
- outliers;
- balance de clases;
- representatividad de entrenamiento;
- hold-out temporal;
- población comparable;
- drift de variables.

Un modelo entrenado con datos posteriores al target no es válido para predicción prospectiva.

## 15. Indicadores de calidad

Un tablero mínimo debe incluir:

| Indicador | Fórmula conceptual |
|---|---|
| Completitud diagnóstico | Registros con diagnóstico válido / total |
| Completitud afiliado | Registros con afiliado identificable / total |
| Duplicidad factura | Facturas duplicadas / facturas |
| Rezago prestación-radicación | Promedio y P95 en días |
| Rezago radicación-pago | Promedio y P95 en días |
| Glosa rate | Valor glosado / valor facturado |
| Reconocimiento rate | Valor reconocido / valor facturado |
| Pago rate | Valor pagado / valor reconocido |
| Outliers severidad | Registros sobre umbral / total |
| Linkage afiliación | Servicios cruzados con afiliación / total |
| Linkage pago | Facturas con pago identificado / reconocidas |
| Cambio de mix | Distribución actual vs histórica |

Estos indicadores deben calcularse por EPS, IPS, región, régimen, servicio y cohorte clínica.

## 16. Rupturas de serie

Los modelos actuariales dependen de comparabilidad histórica. Una ruptura de serie ocurre cuando los datos cambian por razones no clínicas.

Ejemplos:

- nueva plataforma de facturación;
- cambio de proveedor tecnológico;
- cambio de reglas de glosa;
- nueva validación de RIPS;
- migración de catálogo;
- intervención administrativa;
- cambio de red prestadora;
- acumulación y depuración de backlog;
- conciliación masiva;
- cambio de política de pago.

Cada ruptura debe documentarse. En algunos casos, el periodo afectado debe excluirse, ajustarse o modelarse por separado.

## 17. Backtesting de datos

El backtesting no es solo para modelos. También aplica a datos.

Preguntas:

- ¿Cuánto de lo reportado inicialmente cambió después de 1, 3, 6 o 12 meses?
- ¿Qué porcentaje de facturas se reabre?
- ¿Qué valor de glosa se recupera?
- ¿Qué tan estable es el diagnóstico?
- ¿Cuánto tarda en emerger el alto costo?
- ¿Qué proporción de pagos llega después del cierre?

El resultado permite estimar IBNR y definir factores de desarrollo operativos.

## 18. Linaje y versionamiento

Cada corrida actuarial debe registrar:

- fecha de extracción;
- fuentes incluidas;
- filtros aplicados;
- reglas de limpieza;
- transformaciones;
- catálogos usados;
- versión de modelo;
- supuestos;
- responsable;
- hash o identificador de dataset;
- diferencias contra corrida anterior.

Sin linaje, no hay reproducibilidad. Sin reproducibilidad, el resultado no es defendible.

## 19. Reglas de aceptación de datos

No toda base debe pasar automáticamente a modelación.

Ejemplo de semáforo:

| Estado | Criterio | Acción |
|---|---|---|
| Verde | Errores no materiales | Usar con documentación |
| Amarillo | Errores materiales pero acotados | Usar con ajustes y sensibilidad |
| Rojo | Errores que cambian conclusión | No usar para estimación principal |

Los umbrales deben definirse por materialidad financiera y por uso. Una tasa de error tolerable para análisis exploratorio puede ser inaceptable para reservas financieras.

## 20. Controles específicos para Colombia

En el contexto colombiano, los controles deben cubrir:

- afiliados activos vs servicios prestados;
- régimen contributivo/subsidiado;
- movilidad entre EPS;
- servicios PBS y No UPC;
- MIPRES;
- Cuenta de Alto Costo;
- glosas y devoluciones;
- pagos parciales;
- facturas conciliadas;
- prestadores intervenidos o con cambios contractuales;
- eventos de alto costo;
- medicamentos regulados o con cambios de precio;
- tecnologías nuevas.

El objetivo es separar riesgo clínico, riesgo operativo y riesgo financiero.

## 21. Relación con auditoría médica

La auditoría médica no debe operar desconectada del reserving. Sus decisiones cambian el valor reconocido, el patrón de pago, la glosa esperada y la probabilidad de litigio.

Variables útiles:

- causal de glosa;
- valor glosado inicial;
- valor levantado;
- tiempo de conciliación;
- prestador;
- servicio;
- diagnóstico;
- recurrencia de causal;
- resultado de auditoría;
- pago posterior.

Estas variables pueden alimentar modelos de reconocimiento y pago futuro.

## 22. Relación con tesorería

El pago observado depende también de liquidez. Un aumento del rezago pago no implica necesariamente menor obligación, pero sí mayor pasivo pendiente.

Por eso, el análisis debe separar:

- incurrido técnico;
- reconocido contable;
- pagado;
- pendiente;
- IBNR;
- IBNER;
- flujo esperado.

Una entidad puede tener un IBNR estable y una presión de caja creciente si el reconocimiento se acumula sin pago oportuno.

## 23. Relación con modelos de alto costo

Para alto costo, la calidad de datos debe ser más estricta:

- identificación única de paciente;
- condición clínica confirmada;
- estadio o severidad;
- medicamento o tecnología;
- continuidad del tratamiento;
- valor unitario;
- periodicidad;
- autorización;
- factura;
- reconocimiento;
- pago;
- mecanismo de financiación.

Un solo paciente mal duplicado puede distorsionar severidad y percentiles.

## 24. Nota técnica de datos

Cada estudio actuarial debe incluir una sección de datos con:

- fuentes;
- periodo;
- población;
- definición de exposición;
- definición de costo;
- campos críticos;
- reglas de exclusión;
- controles realizados;
- errores encontrados;
- ajustes aplicados;
- limitaciones;
- impacto esperado sobre resultados;
- reconciliación financiera;
- responsable y fecha.

Esta sección debe ser suficientemente específica para que un tercero pueda entender qué se usó y qué no.

## 25. Checklist operativo

Antes de cerrar una corrida de reserving o modelo de riesgo, verificar:

- ¿La extracción tiene fecha y versión?
- ¿La población cruza con afiliación?
- ¿Las fechas críticas son válidas?
- ¿Se separa prestación, radicación, reconocimiento y pago?
- ¿Hay duplicados controlados?
- ¿Notas crédito y reversos están tratados?
- ¿Valores negativos están explicados?
- ¿Diagnósticos y procedimientos cumplen catálogos?
- ¿La base cruza con pagos?
- ¿La base reconcilia con contabilidad?
- ¿Se identifican glosas y devoluciones?
- ¿Hay controles por prestador y contrato?
- ¿Se detectaron rupturas de serie?
- ¿Se documentaron exclusiones?
- ¿La calidad es suficiente para el uso previsto?

## 26. Conclusión

La calidad de datos es una condición previa para reserving, ajuste de riesgo y modelación actuarial en salud. En Colombia, la integración entre RIPS, FEV, pagos, glosas, MIPRES, afiliación y contabilidad debe convertirse en una disciplina técnica permanente.

La validación no debe verse como una tarea de soporte. Es parte del modelo actuarial. Define qué se puede estimar, con qué confianza, bajo qué limitaciones y con qué controles.

Un sistema de datos robusto permite pasar de reservas reactivas a gestión prospectiva: mejor IBNR, mejor medición de morbilidad, mejor análisis de alto costo, mejor suficiencia UPC y mejor monitoreo de liquidez.

## Fuentes de trabajo del proyecto

- ASOP No. 23, *Data Quality*, como referencia para selección, revisión, uso y comunicación de datos.
- ASOP No. 56, *Modeling*, como referencia para gobierno, validación, intended use y riesgo de modelo.
- ASOP No. 45, *The Use of Health Status Based Risk Adjustment Methodologies*, como referencia para datos clínicos, farmacia, morbilidad y ajuste de riesgo.
- `gemini-deep-research-report.md`, secciones sobre RIPS-FEV, Cuenta de Alto Costo, MIPRES, presupuestos máximos y brechas de datos.
- `chatgpt-deep-research-report.md`, secciones sobre SGSSS, RIPS, MIPRES, datos clínicos, ajuste de riesgo y recomendaciones de infraestructura.

## Próximo capítulo

➡️ **37 · Colombia IBNR Technical Provisions and Regulatory Reporting** *(pendiente de crear)*
