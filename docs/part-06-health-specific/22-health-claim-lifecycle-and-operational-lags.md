---
title: "Health Claim Lifecycle and Operational Lags"
part: "Parte VI · Especificidades de salud"
chapter: 22
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Health Claim Lifecycle and Operational Lags

Este capítulo desarrolla el ciclo operativo de una reclamación de salud y su relación con los rezagos actuariales. En seguros de salud, el desarrollo de pérdidas no depende únicamente del tiempo transcurrido desde la ocurrencia médica. También depende de procesos administrativos: autorización, prestación, facturación, radicación, auditoría, glosa, conciliación, contabilización y pago.

La consecuencia actuarial es directa: antes de seleccionar una metodología de IBNR o de reservas, debe definirse qué evento se está midiendo, qué fecha ordena el triángulo y qué estado operativo representa cada observación. Dos triángulos construidos con la misma base económica pueden producir conclusiones distintas si usan fechas diferentes.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Describir el ciclo de vida de una reclamación de salud desde la prestación hasta el pago final.
- Diferenciar fecha de servicio, fecha de autorización, fecha de radicación, fecha contable y fecha de pago.
- Identificar rezagos operativos y su efecto sobre triángulos pagados, incurridos y reportados.
- Separar IBNR puro, IBNER, cuentas conocidas pendientes, glosas y reaperturas.
- Definir reglas de corte consistentes para valoración actuarial.
- Construir controles de reconciliación entre reserving, contabilidad y operación.

## 1. Por qué el ciclo de vida importa

En ramos de cola corta, como muchas coberturas de salud, puede parecer que los pagos se desarrollan rápidamente. Sin embargo, la velocidad observada de pago no siempre representa la velocidad real de ocurrencia del costo médico. Una reclamación puede haber sido prestada, facturada, auditada, objetada, corregida y pagada en diferentes momentos.

El actuario debe distinguir entre:

- la ocurrencia clínica del evento;
- el conocimiento operativo de la reclamación;
- el reconocimiento contable;
- el pago financiero;
- la resolución final de controversias.

La reserva depende de cuál de estos hitos se usa como base.

## 2. Línea de tiempo básica

Una reclamación típica puede atravesar los siguientes eventos:

| Hito | Descripción | Relevancia actuarial |
|---|---|---|
| Elegibilidad | Verificación de cobertura del afiliado | Define exposición |
| Autorización | Aprobación previa o concurrente | Señal temprana de utilización |
| Prestación | Servicio médico efectivamente prestado | Fecha económica primaria |
| Facturación | Emisión de cuenta o factura | Inicio del flujo administrativo |
| Radicación | Recepción formal por el pagador | Fecha de reporte operativo |
| Auditoría | Revisión médica, contractual o tarifaria | Afecta monto reconocido |
| Glosa/devolución | Objeción total o parcial | Genera incertidumbre de monto y tiempo |
| Respuesta | Contestación del prestador | Actualiza probabilidad de reconocimiento |
| Conciliación | Acuerdo o decisión sobre controversia | Reduce incertidumbre |
| Contabilización | Registro en cuentas por pagar o provisión | Conecta con estados financieros |
| Pago | Giro al prestador o beneficiario | Base de triángulos pagados |
| Cierre | No se esperan movimientos adicionales | Define madurez |
| Reapertura | Ajuste posterior al cierre | Riesgo de desarrollo tardío |

No todos los portafolios observan todos los hitos. La ausencia de una fecha no elimina el fenómeno económico; solo reduce la trazabilidad.

## 3. Fechas críticas

### Fecha de servicio

La fecha de servicio representa el momento económico de la prestación. Es usualmente la mejor aproximación al periodo de ocurrencia para reserving de salud.

Ventajas:

- se alinea con el consumo real de servicios;
- permite medir estacionalidad médica;
- facilita análisis por cohorte de prestación;
- es adecuada para estimar IBNR puro.

Limitaciones:

- puede corregirse después;
- puede venir incompleta o inconsistente;
- en hospitalizaciones puede existir rango de fechas;
- puede diferir de la fecha de egreso o de facturación.

### Fecha de autorización

La autorización puede anticipar una prestación, pero no siempre implica que el servicio ocurrió.

Es útil para:

- vigilancia temprana;
- servicios de alto costo;
- cirugía programada;
- gestión de redes;
- estimaciones preliminares de severidad.

No debe tratarse automáticamente como ocurrencia. Una autorización puede cancelarse, modificarse o usarse parcialmente.

### Fecha de radicación

La fecha de radicación representa el momento en que el pagador recibe formalmente la cuenta.

Es central para:

- triángulos reportados;
- medición de rezago de reporte;
- control de cuentas conocidas;
- auditoría de facturación.

Pero no representa la ocurrencia clínica. Si se usa como origen del triángulo, se modela el proceso administrativo, no el periodo de prestación.

### Fecha contable

La fecha contable refleja cuándo la obligación se reconoce en libros. Puede depender de políticas internas, sistemas, corte de cierre o criterios de auditoría.

Debe reconciliarse con la reserva actuarial, pero no siempre es la mejor fecha para modelar desarrollo.

### Fecha de pago

La fecha de pago indica salida de caja. Es observable y verificable, por eso los triángulos pagados suelen ser robustos.

Sin embargo, los pagos pueden estar afectados por:

- ciclos de tesorería;
- giros directos;
- conciliaciones masivas;
- retrasos administrativos;
- priorización de pagos;
- acuerdos contractuales.

El actuario debe separar desarrollo económico de desarrollo financiero.

## 4. Tipos de rezago

En salud conviene separar al menos cinco rezagos:

| Rezago | Fórmula conceptual | Interpretación |
|---|---|---|
| Prestación a radicación | fecha de radicación - fecha de servicio | Retraso de facturación/reporte |
| Radicación a auditoría | fecha de auditoría - fecha de radicación | Velocidad de revisión |
| Auditoría a reconocimiento | fecha de reconocimiento - fecha de auditoría | Resolución administrativa |
| Reconocimiento a pago | fecha de pago - fecha de reconocimiento | Ciclo financiero |
| Servicio a pago | fecha de pago - fecha de servicio | Desarrollo total observado |

Estos rezagos no son intercambiables. Un portafolio puede tener reporte rápido y pago lento, o reporte lento y pago rápido. Las implicaciones de reserva son distintas.

## 5. Estados operativos

Una reclamación puede clasificarse por estado. Una taxonomía mínima incluye:

| Estado | Definición | Tratamiento actuarial |
|---|---|---|
| No reportada | Servicio ocurrido pero no radicado | IBNR puro |
| Reportada sin auditar | Cuenta recibida pendiente de revisión | Cuenta conocida con incertidumbre |
| Auditada reconocida | Monto aceptado total o parcialmente | Pasivo más observable |
| Glosada | Monto objetado | Probabilidad de reconocimiento |
| Devuelta | Cuenta rechazada por forma o soporte | Posible reradicación |
| En conciliación | Disputa activa | Modelo de resolución |
| Pagada parcial | Existe saldo pendiente | Reserva por remanente |
| Pagada total | Sin saldo esperado | Cierre provisional |
| Cerrada | No se esperan movimientos | Sin reserva salvo reapertura |
| Reabierta | Nuevo movimiento posterior | Desarrollo tardío |

Una reserva robusta no solo estima montos; también estima transiciones entre estados.

## 6. IBNR, IBNER y cuentas conocidas

En salud es útil separar:

| Componente | Descripción |
|---|---|
| IBNR puro | Servicios ocurridos pero no reportados |
| IBNER | Desarrollo adicional sobre cuentas ya reportadas |
| Cuentas conocidas pendientes | Reclamaciones radicadas no pagadas |
| Glosas esperadas a reconocer | Parte probable de cuentas objetadas |
| Ajustes y reaperturas | Movimientos posteriores al cierre inicial |

La reserva total puede expresarse como:

$$
R = R_{\text{IBNR}} + R_{\text{IBNER}} + R_{\text{known}} + R_{\text{dispute}} + R_{\text{reopen}}
$$

La separación no siempre es contable, pero es útil para diagnóstico, validación y comunicación.

## 7. Triángulos afectados por el ciclo operativo

### Triángulos pagados

Los triángulos pagados usan pagos como medida de desarrollo. Son estables cuando el flujo de pagos es regular, pero pueden distorsionarse por cambios de tesorería o conciliaciones.

Preguntas de control:

- ¿La política de pagos cambió durante el periodo?
- ¿Hay giros directos que no pasan por el flujo habitual?
- ¿Se realizaron pagos masivos atrasados?
- ¿Existen acuerdos de pago que rompen el patrón histórico?

### Triángulos incurridos

Los triángulos incurridos buscan capturar una medida más cercana al costo esperado final. En salud, “incurrido” puede significar:

- facturado;
- permitido;
- auditado;
- reconocido;
- contabilizado;
- pagado más reserva caso a caso.

La definición debe documentarse. No existe un único incurrido operativo universal.

### Triángulos reportados

Los triángulos reportados miden cuentas radicadas o conocidas. Son útiles para separar rezago de reporte de rezago de pago.

Pueden construirse con:

- conteo de reclamaciones;
- monto facturado;
- monto permitido preliminar;
- monto reconocido;
- monto en controversia.

## 8. Riesgo de mezcla de procesos

Un error frecuente es mezclar procesos en un mismo triángulo. Por ejemplo:

- usar fecha de servicio como origen y fecha contable como desarrollo;
- mezclar pagos ordinarios con conciliaciones extraordinarias;
- incluir devoluciones como si fueran glosas sustantivas;
- tratar pagos parciales como cierre total;
- no separar prestadores con ciclos de facturación muy distintos.

La mezcla reduce interpretabilidad y puede producir factores de desarrollo inestables.

## 9. Segmentación por ciclo operativo

Además de la segmentación actuarial tradicional, puede requerirse segmentación por operación:

| Segmento operativo | Motivo |
|---|---|
| Hospitalario vs ambulatorio | Diferente severidad y rezago |
| Alto costo vs corriente | Diferente gestión y revisión |
| Red contratada vs no contratada | Diferente facturación y auditoría |
| Pago directo vs reembolso | Diferente ciclo financiero |
| Prestadores grandes vs pequeños | Diferente comportamiento administrativo |
| Capitación vs evento | Diferente naturaleza del pasivo |
| Cuentas con glosa vs sin glosa | Diferente incertidumbre |

La segmentación debe balancear homogeneidad y credibilidad. Demasiados segmentos generan volatilidad.

## 10. Reglas de corte

La fecha de corte determina qué información puede usarse en la valoración.

Una regla de corte debe especificar:

- fecha exacta de valoración;
- bases de datos incluidas;
- movimientos posteriores excluidos;
- tratamiento de pagos en tránsito;
- tratamiento de cuentas radicadas después del corte;
- versión de catálogos y contratos;
- ajustes manuales permitidos;
- reconciliación contable.

Sin una regla de corte explícita, el backtesting puede estar contaminado por información futura.

## 11. Reconciliación con contabilidad

La reserva actuarial debe reconciliarse con los registros financieros. La reconciliación mínima debería incluir:

| Fuente | Control |
|---|---|
| Pagos | Cruce con tesorería |
| Cuentas por pagar | Cruce con contabilidad |
| Facturas radicadas | Cruce con operación |
| Glosas | Cruce con auditoría médica |
| Contratos | Cruce con condiciones vigentes |
| Reservas caso a caso | Cruce con inventario de saldos |

Diferencias entre modelos actuariales y saldos contables no son necesariamente errores, pero deben explicarse.

## 12. Diagnósticos recomendados

Antes de seleccionar método, conviene producir diagnósticos operativos:

- distribución de días entre servicio y radicación;
- distribución de días entre radicación y pago;
- proporción de pagos parciales;
- proporción de cuentas glosadas;
- porcentaje de cuentas reabiertas;
- monto promedio por estado;
- aging de cuentas conocidas;
- evolución mensual de cuentas pendientes;
- velocidad de cierre por prestador;
- estabilidad de patrones por cohorte.

Estos diagnósticos muestran si el problema principal es ocurrencia no reportada, pago lento, controversia o contabilización.

## 13. Ejemplo conceptual

Supóngase una cohorte de servicios de enero:

| Estado al corte | Monto observado | Tratamiento |
|---|---:|---|
| Pagado | 800 | No requiere reserva adicional salvo reapertura |
| Radicado pendiente | 120 | Cuenta conocida pendiente |
| Glosado | 50 | Reserva según probabilidad de reconocimiento |
| No reportado esperado | 90 | IBNR puro |
| Ajustes esperados | 20 | IBNER o ajuste posterior |

La reserva no debe calcularse únicamente como diferencia contra el pago. Debe reconocer la naturaleza de cada componente:

$$
R = 120 + p_{\text{glosa}} \cdot 50 + 90 + 20
$$

Si la probabilidad de reconocimiento de glosas es 40%, entonces:

$$
R = 120 + 0.40 \cdot 50 + 90 + 20 = 250
$$

Este ejemplo ilustra por qué la clasificación operativa mejora la explicación de la reserva.

## 14. Relación con modelos multiestado

Cuando se dispone de historia de estados, el ciclo operativo puede modelarse como proceso multiestado:

$$
\text{Radicada} \rightarrow \text{Auditada} \rightarrow \text{Pagada}
$$

o:

$$
\text{Radicada} \rightarrow \text{Glosada} \rightarrow \text{Conciliada} \rightarrow \text{Pagada}
$$

La reserva esperada puede estimarse combinando:

- probabilidad de transición;
- tiempo esperado en cada estado;
- monto esperado reconocido;
- probabilidad de reapertura.

Este enfoque es especialmente útil para glosas, devoluciones, pagos parciales y reclamaciones de alto costo.

## 15. Implicaciones para selección metodológica

El ciclo operativo orienta la elección del método:

| Situación | Método candidato |
|---|---|
| Patrón estable de pagos | Chain Ladder pagado |
| Pagos lentos pero reporte estable | Triángulo reportado o incurrido |
| Cambios fuertes de mix | Bornhuetter-Ferguson o Cape Cod |
| Cuentas conocidas relevantes | Inventario caso a caso más IBNR |
| Glosas materiales | Modelo de reconocimiento y resolución |
| Datos claim-level robustos | GLM, GAM, ML o multiestado |
| Cambios operativos recientes | Escenarios y juicio actuarial |

La metodología debe responder al proceso dominante. Si el principal rezago es administrativo, un modelo puramente pagado puede confundir operación con riesgo médico.

## 16. Controles de gobierno

La documentación del ciclo de vida debe incluir:

- diccionario de fechas;
- definición de estados;
- mapa de sistemas fuente;
- reglas de corte;
- reglas de exclusión;
- reconciliación con contabilidad;
- cambios operativos relevantes;
- responsables de datos;
- limitaciones conocidas;
- impacto en selección metodológica.

Esta documentación se alinea con principios de calidad de datos, uso de modelos y comunicación actuarial.

## 17. Checklist práctico

Antes de construir una reserva de salud, confirmar:

- La fecha de servicio está definida y validada.
- La fecha de radicación está disponible o tiene proxy documentado.
- La fecha de pago se reconcilia con tesorería.
- Las cuentas conocidas están separadas del IBNR puro.
- Las glosas tienen estado y monto identificable.
- Los pagos parciales no se tratan como cierres definitivos sin validación.
- Las reaperturas se monitorean.
- Los cambios de sistemas o políticas están documentados.
- La segmentación captura diferencias operativas relevantes.
- El backtesting usa información disponible al corte.

## 18. Conclusiones

En seguros de salud, el ciclo operativo de la reclamación es parte del modelo actuarial. La misma prestación puede observarse en diferentes momentos y estados, y cada observación responde a un proceso distinto.

Una estimación robusta de reservas requiere separar ocurrencia, reporte, auditoría, controversia, contabilización y pago. Esta separación mejora la selección metodológica, la validación, la explicación de variaciones y la reconciliación financiera.

El siguiente paso es conectar estos rezagos con exposición, utilización, severidad y morbilidad, que son los motores técnicos del costo médico.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre health claims, completion factors y reserving.

## Próximo capítulo

➡️ **[Health Exposure, Utilization and Severity](23-health-exposure-utilization-and-severity.md)**
