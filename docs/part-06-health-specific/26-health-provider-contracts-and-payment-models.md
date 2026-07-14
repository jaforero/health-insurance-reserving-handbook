---
title: "Health Provider Contracts and Payment Models"
part: "Parte VI · Especificidades de salud"
chapter: 26
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Health Provider Contracts and Payment Models

Este capítulo desarrolla el efecto de los contratos con prestadores y las modalidades de pago sobre el reserving de salud. En seguros de salud, la obligación financiera no depende únicamente de la prestación médica ocurrida. También depende de cómo se pactó el pago: evento, tarifa, capitación, paquete, pago global prospectivo, riesgo compartido, stop-loss, incentivos de calidad, descuentos, glosas y conciliaciones.

Dos reclamaciones clínicamente equivalentes pueden generar pasivos distintos si una se paga por evento y otra está incluida en un contrato capitado. Por tanto, el método actuarial debe reflejar la sustancia económica del contrato y no solo la forma administrativa del registro.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Identificar las principales modalidades de pago a prestadores.
- Entender cómo cada modalidad afecta la ocurrencia, reporte, reconocimiento y pago.
- Separar pasivos por evento, capitación, paquetes, pagos prospectivos y riesgo compartido.
- Reconocer cuándo un triángulo de pagos es apropiado y cuándo puede ser engañoso.
- Diseñar segmentaciones por contrato para reserving.
- Definir controles de reconciliación entre contratos, facturación, cuentas por pagar y reservas.

## 1. Sustancia económica del contrato

La primera pregunta actuarial no es cómo está registrada la cuenta, sino qué obligación económica asumió el pagador.

Una misma prestación puede estar bajo:

- pago por evento;
- tarifa negociada;
- capitación;
- paquete;
- pago por caso;
- presupuesto global;
- pago global prospectivo;
- riesgo compartido;
- reembolso;
- contrato mixto.

Cada modalidad distribuye riesgo de manera distinta entre asegurador, EPS, pagador, IPS, red, profesional o proveedor.

## 2. Pago por evento

El pago por evento, o fee-for-service, remunera cada servicio prestado. La obligación se genera cuando ocurre y se reconoce el servicio cubierto, sujeto a auditoría, tarifas y glosas.

Características:

- alta trazabilidad por servicio;
- fuerte dependencia de volumen;
- sensibilidad a utilización;
- posibilidad de glosas por pertinencia, tarifa o soporte;
- rezago entre prestación, radicación y pago;
- compatibilidad con triángulos pagados o incurridos.

En esta modalidad, el reserving tradicional suele ser aplicable si los datos son estables y el proceso de pago no cambia materialmente.

## 3. Tarifa negociada

Muchos contratos por evento usan tarifas pactadas. La severidad depende de:

- manual tarifario;
- descuentos;
- actualizaciones anuales;
- acuerdos por prestador;
- reglas de auditoría;
- topes;
- exclusiones;
- copagos o cuotas moderadoras;
- impuestos o retenciones.

Un cambio tarifario puede parecer tendencia de severidad. El actuario debe distinguir inflación médica real de renegociación contractual.

## 4. Capitación

La capitación paga un monto fijo por persona cubierta durante un periodo, usualmente por mes, a cambio de asumir parte de la atención.

La obligación contractual puede expresarse como:

$$
P_t = N_t \times \text{tarifa capitada}_t
$$

donde:

- \(N_t\) es la población o exposición reconocida;
- la tarifa capitada puede variar por grupo, riesgo, región o contrato.

La reserva no se calcula igual que en pago por evento. Debe considerar:

- devengo de la cápita;
- población elegible;
- ajustes retroactivos;
- novedades de afiliación;
- exclusiones;
- servicios por fuera de la cápita;
- liquidación contractual;
- riesgo de insuficiencia médica dentro del contrato.

## 5. Capitación parcial

La capitación puede cubrir solo ciertos servicios:

- primer nivel;
- consultas;
- promoción y prevención;
- medicamentos ambulatorios;
- laboratorio;
- imagenología;
- odontología;
- redes específicas;
- cohortes o patologías.

La reserva debe separar lo incluido y lo excluido. Si no se separa, puede haber doble conteo o subestimación.

Ejemplo:

| Servicio | Incluido en cápita | Tratamiento |
|---|---|---|
| Consulta general | Sí | Devengo capitado |
| Urgencias | No | Pago por evento |
| Medicamentos básicos | Sí | Dentro de cápita |
| Alto costo | No | Reserva separada |

## 6. Paquetes

Un paquete paga un monto fijo por un conjunto de servicios asociados a un episodio o procedimiento.

Ejemplos:

- parto;
- cirugía específica;
- procedimiento ambulatorio;
- atención integral de una patología;
- evento quirúrgico con insumos incluidos;
- tratamiento por ciclo.

Riesgos actuariales:

- definición incompleta del paquete;
- servicios adicionales no incluidos;
- complicaciones;
- readmisiones;
- pagos parciales;
- glosas por alcance;
- cambios de mix de casos.

La reserva debe considerar si el paquete cierra completamente el riesgo o si deja componentes por fuera.

## 7. Pago por caso

El pago por caso remunera un episodio según clasificación clínica o administrativa. Puede parecerse a DRG, grupos de complejidad o categorías internas.

La severidad depende de:

- clasificación del caso;
- reglas de agrupación;
- severidad del diagnóstico;
- comorbilidades;
- estancia;
- complicaciones;
- exclusiones;
- outliers.

En reserving, puede ser necesario estimar no solo número de casos, sino distribución de categorías.

## 8. Pago global prospectivo

El pago global prospectivo define un monto esperado para cubrir una población, servicio, red o periodo. Puede estar sujeto a liquidación posterior.

La obligación puede tener componentes:

$$
\text{Pasivo} =
\text{devengo base}
+ \text{ajustes esperados}
+ \text{incentivos}
- \text{recuperaciones}
$$

El reserving debe evaluar:

- periodo de cobertura;
- población cubierta;
- servicios incluidos;
- reglas de liquidación;
- indicadores de cumplimiento;
- corredores de riesgo;
- calidad;
- saldos pendientes.

## 9. Presupuesto global

Un presupuesto global fija una asignación para un prestador, red o población. Puede ser retrospectivo, prospectivo o mixto.

Riesgos:

- insuficiencia del presupuesto;
- pagos adicionales por sobreutilización;
- subejecución;
- ajustes por calidad;
- cambios de población;
- servicios no incluidos;
- controversias de liquidación.

El actuario debe distinguir entre devengo presupuestal y costo médico esperado. El presupuesto no siempre equivale al pasivo último.

## 10. Riesgo compartido

Los contratos de riesgo compartido distribuyen desviaciones entre pagador y prestador.

Mecanismos comunes:

- shared savings;
- shared losses;
- corredores de riesgo;
- stop-loss;
- capitation with carve-outs;
- garantías de resultado;
- pagos condicionados a desempeño;
- ajustes por calidad;
- techos y pisos.

La reserva debe reflejar la fórmula contractual, no solo los pagos realizados.

## 11. Corredores de riesgo

Un corredor de riesgo limita la exposición de una parte cuando el costo observado se desvía de un objetivo.

Ejemplo conceptual:

| Resultado | Tratamiento |
|---|---|
| Costo dentro de ±5% | Sin ajuste |
| Ahorro mayor a 5% | Se comparte ahorro |
| Exceso mayor a 5% | Se comparte pérdida |

La reserva debe estimar la distribución del costo final y la probabilidad de caer en cada tramo.

## 12. Stop-loss contractual

Un stop-loss contractual limita el costo reconocido por evento, persona, periodo o prestador.

Puede aplicar a:

- eventos individuales;
- pacientes de alto costo;
- medicamentos;
- hospitalizaciones;
- patologías específicas;
- costo agregado del contrato.

La reserva debe considerar:

- deducible o attachment point;
- límite máximo;
- base de cálculo;
- exclusiones;
- recuperación esperada;
- tiempo de liquidación;
- riesgo de disputa.

Un stop-loss reduce severidad neta esperada, pero puede introducir rezago de recuperación.

## 13. Incentivos de calidad

Los contratos pueden incluir pagos o descuentos por indicadores:

- oportunidad;
- satisfacción;
- resolutividad;
- readmisiones;
- adherencia a guías;
- resultados clínicos;
- control de crónicos;
- prevención;
- reporte oportuno.

Estos componentes pueden generar pasivos o recuperaciones adicionales. Deben reservarse si son materiales y estimables.

## 14. Pagos basados en valor

Los modelos basados en valor intentan alinear pago con resultado clínico, eficiencia o calidad. Pueden combinar:

- pago base;
- bono por desempeño;
- penalidad;
- ahorro compartido;
- garantía de resultado;
- ajuste por riesgo;
- medición de indicadores.

Desde reserving, el reto es que el pasivo depende de información futura de desempeño. Se requieren supuestos sobre cumplimiento, medición y liquidación.

## 15. Contratos mixtos

Muchos contratos reales combinan modalidades:

| Componente | Modalidad |
|---|---|
| Atención primaria | Capitación |
| Urgencias | Evento |
| Cirugías | Paquete |
| Alto costo | Carve-out |
| Medicamentos especiales | Pago prospectivo o evento |
| Calidad | Bono o penalidad |

La reserva debe modelar cada componente por separado si los patrones de desarrollo son distintos.

## 16. Carve-outs

Un carve-out excluye ciertos servicios de una modalidad principal.

Ejemplos:

- alto costo fuera de cápita;
- medicamentos especiales fuera de paquete;
- UCI fuera de tarifa fija;
- insumos específicos facturados aparte;
- tecnologías no incluidas;
- servicios judicializados.

Los carve-outs son fuente frecuente de errores de reserva. Si se asume que todo está incluido en la cápita, se subestima. Si se reserva todo por evento además de la cápita, se sobreestima.

## 17. Devengo vs pago

En contratos prospectivos, el devengo puede ocurrir aunque no haya factura individual. En contratos por evento, el devengo suele depender de prestación y reconocimiento.

La diferencia es crítica:

| Modalidad | Base de devengo | Base de pago |
|---|---|---|
| Evento | Servicio reconocido | Cuenta auditada |
| Capitación | Población cubierta | Giro periódico |
| Paquete | Episodio cubierto | Factura o liquidación |
| PGP | Periodo o población | Cronograma contractual |
| Riesgo compartido | Resultado final | Liquidación posterior |

El reserving debe medir obligación devengada, no solo flujo de caja.

## 18. Reconciliación contractual

Cada contrato relevante debe reconciliar:

- población o volumen cubierto;
- periodo de vigencia;
- servicios incluidos;
- servicios excluidos;
- tarifa o fórmula;
- pagos realizados;
- cuentas pendientes;
- glosas;
- descuentos;
- incentivos;
- saldos a favor;
- liquidaciones pendientes.

La reconciliación evita duplicidad entre reservas actuariales, cuentas por pagar y provisiones contractuales.

## 19. Segmentación por modalidad de pago

La modalidad de pago debe ser una dimensión de segmentación. Un triángulo que mezcla evento, capitación y paquetes puede producir factores sin significado económico.

Segmentación mínima:

- evento;
- capitación;
- paquete;
- prospectivo;
- riesgo compartido;
- alto costo carve-out;
- reembolso;
- contrato especial.

Si el volumen es insuficiente, se pueden agrupar contratos con comportamiento similar, documentando la decisión.

## 20. Implicaciones para triángulos

### Triángulos pagados

Son útiles para pago por evento y algunos paquetes. Pueden ser inapropiados para capitación pura si los pagos responden a cronograma contractual y no a ocurrencia médica.

### Triángulos incurridos

Pueden ser útiles si el incurrido refleja obligación económica. En contratos prospectivos, el incurrido debe construirse desde devengo contractual y no desde facturación individual únicamente.

### Triángulos de cuentas conocidas

Son útiles cuando hay inventario de facturas, saldos o liquidaciones pendientes.

### Triángulos por componente

Para contratos mixtos, puede requerirse un triángulo por componente contractual.

## 21. Selección metodológica

| Modalidad | Método candidato |
|---|---|
| Evento estable | Chain Ladder, Mack, Bootstrap |
| Evento inmaduro | Bornhuetter-Ferguson, Cape Cod |
| Capitación | Devengo contractual, PMPM, suficiencia médica |
| Paquete | Frecuencia-severidad por episodio |
| Riesgo compartido | Simulación o escenarios |
| Stop-loss | Severidad truncada y recuperación |
| Incentivos | Modelo de probabilidad de cumplimiento |
| Alto costo carve-out | Modelo separado de cola |

La metodología debe seguir el contrato. Usar un método estándar sin entender la modalidad puede producir reservas técnicamente inconsistentes.

## 22. Riesgo de doble conteo

El doble conteo ocurre cuando el mismo costo se reserva en más de un componente.

Ejemplos:

- cápita registrada y servicios incluidos reservados por evento;
- paquete completo y servicios internos facturados aparte;
- pago directo contado como pago EPS;
- glosa reservada como cuenta pendiente y como IBNR;
- recuperación stop-loss no descontada del pasivo bruto;
- incentivo negativo incluido en tarifa y provisionado otra vez.

Controles:

- matriz de inclusión/exclusión;
- identificador contractual;
- trazabilidad de componentes;
- reconciliación con pagos;
- revisión de saldos negativos;
- pruebas de duplicidad.

## 23. Riesgo de subestimación

La subestimación ocurre cuando se asume que un contrato transfiere más riesgo del que realmente transfiere.

Ejemplos:

- servicios excluidos de cápita no reservados;
- complicaciones fuera de paquete ignoradas;
- liquidaciones retrospectivas no provisionadas;
- corredores de riesgo no modelados;
- alto costo por fuera de PGP no identificado;
- población retroactiva no reconocida.

La lectura jurídica y técnica del contrato es parte del proceso actuarial.

## 24. Datos requeridos

Datos mínimos por contrato:

| Campo | Uso |
|---|---|
| ID contrato | Segmentación y trazabilidad |
| Prestador/red | Análisis de comportamiento |
| Modalidad | Selección metodológica |
| Vigencia | Devengo |
| Servicios incluidos | Evitar doble conteo |
| Exclusiones | Reservas adicionales |
| Tarifa/fórmula | Estimación de pasivo |
| Población cubierta | Exposición |
| Pagos | Reconciliación |
| Saldos | Cuentas conocidas |
| Glosas | Incertidumbre |
| Incentivos | Ajustes |
| Stop-loss | Recuperaciones |

Sin estos campos, el modelo puede ser estadísticamente correcto pero contractualmente equivocado.

## 25. Aplicación al contexto colombiano

En Colombia, las modalidades contractuales pueden combinar pago por evento, capitación, paquetes, pagos globales prospectivos, presupuestos, giros directos y acuerdos de conciliación.

Riesgos específicos:

- diferencias entre fecha de prestación, radicación, contabilización y pago;
- glosas y devoluciones;
- servicios PBS y no PBS;
- tecnologías o medicamentos con financiación especial;
- alto costo;
- giro directo;
- contratos por red;
- ajustes retroactivos de población;
- conciliaciones masivas;
- saldos entre EPS e IPS.

Para reserving, la modalidad contractual debe integrarse con la taxonomía de estados de reclamación y con la reconciliación contable.

## 26. Ejemplo conceptual

Supóngase un contrato mixto:

| Componente | Modalidad | Estimación |
|---|---|---:|
| Atención primaria | Capitación | 1,000 |
| Urgencias | Evento | 300 |
| Alto costo | Carve-out | 250 |
| Incentivo calidad | Probable bono | 50 |
| Recuperación stop-loss | Esperada | -40 |

Pasivo estimado:

$$
R = 1{,}000 + 300 + 250 + 50 - 40 = 1{,}560
$$

Si se modela todo como pagos por evento, se pierde la sustancia económica de la cápita y del stop-loss. Si se modela todo como cápita, se omite alto costo y urgencias fuera del acuerdo.

## 27. Backtesting contractual

El backtesting debe comparar:

- reserva estimada vs liquidación final;
- pagos por componente;
- desviación de población;
- desviación de utilización;
- desviación de severidad;
- glosas esperadas vs reales;
- incentivos provisionados vs liquidados;
- recuperaciones stop-loss esperadas vs reales;
- saldos pendientes por antigüedad.

La evaluación debe hacerse por modalidad, no solo en agregado.

## 28. Gobierno y documentación

La nota técnica debe documentar:

- modalidades contractuales incluidas;
- criterio de segmentación;
- interpretación económica;
- fuentes de datos;
- reglas de devengo;
- reglas de inclusión/exclusión;
- metodología por componente;
- supuestos de liquidación;
- reconciliación con contabilidad;
- cambios contractuales relevantes;
- limitaciones.

Cuando el contrato es material o complejo, debe existir revisión legal, financiera y actuarial coordinada.

## 29. Checklist práctico

Antes de cerrar una reserva con contratos de prestadores, confirmar:

- Cada contrato material tiene modalidad identificada.
- Los servicios incluidos y excluidos están documentados.
- La exposición cubierta está reconciliada.
- Los pagos se separan por componente.
- Las glosas no se duplican.
- Los carve-outs están identificados.
- Los incentivos y penalidades se estiman si son materiales.
- Los stop-loss y recuperaciones se modelan.
- Los cambios contractuales se reflejan en supuestos.
- El método elegido corresponde a la sustancia económica.

## 30. Conclusiones

Los contratos con prestadores son determinantes en reserving de salud. La modalidad de pago define cuándo surge la obligación, cómo se observa, qué rezagos aparecen, qué riesgos se transfieren y qué componentes deben estimarse.

Una reserva robusta no debe mezclar modalidades incompatibles ni asumir que todo pago refleja desarrollo médico. Debe segmentar por sustancia económica, reconciliar saldos, evitar doble conteo y documentar supuestos contractuales. Este enfoque mejora la precisión técnica y la comunicación con áreas financieras, operativas y jurídicas.

El siguiente capítulo aborda glosas, devoluciones, auditoría médica y controversias desde una perspectiva general de salud, antes de su aplicación específica al contexto colombiano.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 45, The Use of Health Status Based Risk Adjustment Methodologies.
- ASOP No. 50, Determining Minimum Value and Actuarial Value under the Affordable Care Act.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre provider payment models, value-based care, capitation and health reserving.

## Próximo capítulo

➡️ **[Health Claims Audit, Denials and Disputes](27-health-claims-audit-denials-and-disputes.md)**
