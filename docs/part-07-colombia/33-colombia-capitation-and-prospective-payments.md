---
title: "Reservas para capitación y modalidades de pago prospectivo en Colombia"
description: "Criterios de reserva para capitación, pagos prospectivos y otras modalidades contractuales del sistema de salud colombiano."
chapter: 33
part: "part-07-colombia"
language: "es"
status: "draft"
version: "0.1.11"
last_updated: "2026-07-14"
jurisdiction: "Colombia"
---

# Reservas para capitación y modalidades de pago prospectivo en Colombia

> En una modalidad prospectiva, el costo contractual puede devengarse antes de que se conozca el detalle completo de las prestaciones. Por tanto, reservar no consiste únicamente en proyectar facturas: exige separar el pasivo contractual, el riesgo médico retenido y los ajustes de liquidación.

---

## Advertencia de alcance

Este capítulo presenta criterios técnicos y actuariales. No constituye asesoría jurídica, contable, tributaria ni una interpretación oficial de las normas colombianas.

Antes de aplicar sus recomendaciones deben verificarse:

* el Decreto 780 de 2016 y sus modificaciones;
* el Decreto 441 de 2022;
* la Resolución 2284 de 2023 y sus modificaciones;
* la Resolución 948 de 2026 y sus anexos técnicos;
* la regulación vigente del SIIFA;
* la Circular Única de la Superintendencia Nacional de Salud;
* el acuerdo de voluntades aplicable;
* las reglas institucionales de reservas y reconocimiento contable;
* las instrucciones particulares de las autoridades competentes.

Las obligaciones dependen del contenido contractual. La denominación comercial de un contrato no sustituye el análisis de la transferencia económica de riesgo.

---

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector podrá:

* diferenciar capitación, paquete, caso, pago global prospectivo y riesgo compartido;
* identificar qué riesgos asume cada parte;
* separar devengo contractual, servicios prestados e IBNR;
* construir reservas para contratos prospectivos;
* tratar altas, retiros y variaciones de población;
* estimar ajustes retrospectivos;
* modelar corredores de riesgo, stop-loss y garantías;
* evitar el uso incorrecto de triángulos de pagos;
* validar la suficiencia financiera de los acuerdos;
* reconciliar contratos, RIPS, facturas y pagos;
* documentar supuestos y limitaciones.

---

## Contenido

1. Motivación
2. Modalidades de pago
3. Sustancia económica del contrato
4. Perspectiva de EPS e IPS
5. Componentes del pasivo
6. Modelo mínimo de datos
7. Periodo de devengo
8. Capitación
9. Pago global prospectivo
10. Paquetes y pago por caso
11. Acuerdos de riesgo compartido
12. Corredores de riesgo
13. Stop-loss contractual
14. Componentes variables
15. Población y exposición
16. Ajuste por riesgo
17. Prestaciones pendientes de reporte
18. Cuentas conocidas
19. Liquidación contractual
20. Modelos actuariales
21. Uso de triángulos
22. Frecuencia-severidad
23. Modelos PMPM
24. Credibilidad y Bayes
25. Escenarios y suficiencia
26. Reconocimiento de ingresos y costos
27. RIPS, FEV y trazabilidad
28. Giro directo
29. Reconciliación
30. Validación y backtesting
31. Implementación SQL
32. Implementación Python
33. Implementación R
34. Caso numérico
35. Gobierno
36. Riesgos y limitaciones
37. Matriz metodológica
38. Checklist
39. Conclusiones

---

## 1. Motivación

En pago por evento, la unidad económica suele ser cada prestación facturada.

En una modalidad prospectiva, el pago puede pactarse anticipadamente con base en:

* afiliados;
* población asignada;
* episodio;
* diagnóstico;
* paquete;
* periodo;
* presupuesto global;
* resultados de calidad;
* riesgo compartido.

Por ello, pueden existir obligaciones aunque:

* no se haya recibido una factura detallada;
* no se haya cerrado la población definitiva;
* falten RIPS;
* no se haya realizado la liquidación contractual;
* existan indicadores pendientes;
* el pago haya sido parcial;
* todavía no se conozca la utilización completa.

El problema actuarial comprende, al menos:

[
Reserva
=======

PasivoContractual
+
RiesgoMedicoRetenido
+
AjustesDeLiquidacion
+
OtrosComponentes
]

---

## 2. Modalidades de pago

El Decreto 441 de 2022 define diferentes modalidades dentro de los acuerdos de voluntades, entre ellas el pago por capitación, el pago individual por caso o paquete y el pago global prospectivo. La clasificación debe basarse en la sustancia del acuerdo y no únicamente en su nombre.

## 2.1 Pago por capitación

Modalidad prospectiva en la que se reconoce un valor fijo por persona durante un periodo definido para financiar un conjunto acordado de servicios o tecnologías.

Representación básica:

[
Pago_t^{Cap}
============

\sum_{m=1}^{M_t}
N_{m,t}
\times
Tarifa_{m,t}
]

donde:

* (N_{m,t}): personas o unidades elegibles;
* (Tarifa_{m,t}): valor per cápita aplicable;
* (m): segmento de riesgo.

## 2.2 Pago global prospectivo

Modalidad mediante la cual se pacta anticipadamente una suma global para una población determinada y un periodo definido, ajustable por nivel de riesgo y variación del volumen de población conforme al acuerdo.

## 2.3 Pago individual por caso, paquete o canasta

Se pacta un valor anticipado por:

* caso atendido;
* condición;
* diagnóstico;
* episodio;
* conjunto integral de atenciones;
* paquete o canasta.

La unidad de pago es el caso o episodio, no cada servicio individual.

## 2.4 Grupo relacionado de diagnóstico

Agrupa casos con características clínicas y consumo esperado semejantes.

Puede incorporar ajustes por:

* complejidad;
* comorbilidad;
* severidad;
* estancia;
* complicaciones;
* traslado;
* condiciones extremas.

## 2.5 Acuerdo de riesgo compartido

La remuneración final depende total o parcialmente de:

* resultados clínicos;
* utilización;
* costo;
* calidad;
* indicadores;
* eventos evitables;
* límites de pérdida o ganancia.

---

## 3. Sustancia económica del contrato

## 3.1 Preguntas críticas

Antes de escoger una metodología, debe determinarse:

1. ¿Cuál es la unidad de pago?
2. ¿Qué población está cubierta?
3. ¿Qué servicios están incluidos?
4. ¿Qué servicios están excluidos?
5. ¿Quién asume el riesgo de frecuencia?
6. ¿Quién asume el riesgo de severidad?
7. ¿Existe ajuste por riesgo?
8. ¿Existe liquidación retrospectiva?
9. ¿Hay corredor, stop-loss o techo?
10. ¿Hay componente de calidad?
11. ¿Qué eventos permiten renegociación?
12. ¿Cómo se tratan altas y retiros?
13. ¿Qué información soporta la factura?
14. ¿Cuándo se considera devengada la obligación?

## 3.2 Clasificación por transferencia de riesgo

| Modalidad         |   Riesgo de frecuencia |     Riesgo de severidad | Riesgo poblacional |
| ----------------- | ---------------------: | ----------------------: | -----------------: |
| Evento            |                Pagador |                 Pagador |            Pagador |
| Caso o paquete    |      Prestador parcial |       Prestador parcial |            Pagador |
| Capitación        |              Prestador | Prestador según alcance |         Compartido |
| PGP               | Prestador o compartido |  Prestador o compartido |         Compartido |
| Riesgo compartido |             Compartido |              Compartido |         Compartido |

Esta matriz debe adaptarse al contrato real.

---

## 4. Perspectiva de EPS e IPS

## 4.1 EPS o entidad pagadora

Debe estimar:

* obligación fija devengada;
* pagos pendientes;
* ajustes por población;
* servicios excluidos;
* componentes no transferidos;
* liquidaciones finales;
* incentivos o penalizaciones probables;
* obligaciones derivadas de stop-loss.

## 4.2 IPS o red prestadora

Debe estimar:

* ingreso contractual devengado;
* costos médicos incurridos;
* servicios prestados no reportados;
* déficit o superávit del contrato;
* pagos pendientes del pagador;
* devoluciones esperadas;
* ajustes por desempeño;
* obligación por prestadores subcontratados.

## 4.3 Asimetría

La reserva de la EPS no es necesariamente igual al ingreso reconocido por la IPS.

Pueden existir diferencias por:

* criterios contables;
* disputas;
* población;
* calidad;
* momento de liquidación;
* glosas;
* compensaciones;
* componentes contingentes.

---

## 5. Componentes del pasivo

## 5.1 Obligación fija devengada

[
R_t^{Fixed}
===========

## Devengado_t

Pagado_t
]

## 5.2 Ajuste de población

[
R_t^{Pop}
=========

E[
PagoFinal_t^{Poblacion}
-----------------------

PagoProvisional_t
]
]

## 5.3 Servicios excluidos

[
R_t^{Excluded}
==============

E[
CostoUltimo_t^{Excluded}
------------------------

Observado_t^{Excluded}
]
]

## 5.4 Riesgo retenido

[
R_t^{Retained}
==============

E[
CostoRetenido_t
---------------

PagadoRetenido_t
]
]

## 5.5 Liquidación

[
R_t^{Settlement}
================

E[
LiquidacionFinal_t
------------------

ReconocimientoActual_t
]
]

## 5.6 Componente de calidad

[
R_t^{Quality}
=============

E[
Incentivos_t-Penalidades_t
]
]

## 5.7 Reserva total

[
R_t^{Total}
===========

R_t^{Fixed}
+
R_t^{Pop}
+
R_t^{Excluded}
+
R_t^{Retained}
+
R_t^{Settlement}
+
R_t^{Quality}
]

La suma debe evitar duplicidades.

---

## 6. Modelo mínimo de datos

## 6.1 Contrato

```text
contrato_id
tipo_modalidad
fecha_inicio
fecha_fin
poblacion_objetivo
servicios_incluidos
servicios_excluidos
tarifa_base
metodo_ajuste_riesgo
corredor_inferior
corredor_superior
stop_loss
componente_calidad
frecuencia_liquidacion
```

## 6.2 Población

```text
contrato_id
periodo
afiliado_id_hash
fecha_ingreso
fecha_retiro
dias_elegibles
segmento_riesgo
factor_ajuste
estado_afiliacion
```

## 6.3 Prestaciones

```text
contrato_id
prestacion_id
afiliado_id_hash
fecha_prestacion
tipo_servicio
diagnostico
procedimiento
valor
incluido_en_contrato
```

## 6.4 Liquidaciones

```text
contrato_id
periodo
fecha_liquidacion
poblacion_provisional
poblacion_final
valor_provisional
valor_final
ajuste
estado
```

## 6.5 Indicadores

```text
contrato_id
periodo
indicador
meta
resultado
valor_incentivo
valor_penalidad
estado_validacion
```

---

## 7. Periodo de devengo

## 7.1 Capitación mensual

La obligación puede devengarse diariamente:

[
Devengo_{a,t}
=============

Tarifa_{a,t}
\times
\frac{DiasElegibles_{a,t}}{DiasPeriodo_t}
]

## 7.2 PGP

El devengo puede distribuirse:

* uniformemente;
* por exposición;
* por estacionalidad;
* por utilización esperada;
* por hitos contractuales.

## 7.3 Paquete

El devengo depende de:

* inicio del episodio;
* terminación;
* cumplimiento de condiciones;
* alta;
* cierre clínico;
* periodo de garantía.

## 7.4 Error frecuente

Registrar el costo únicamente cuando llega la factura.

En una modalidad prospectiva, la obligación puede haberse devengado antes.

---

## 8. Capitación

## 8.1 Reserva básica

[
R_t^{Cap}
=========

\sum_a
Tarifa_{a,t}
Exposicion_{a,t}
----------------

Pagos_t
+
Ajustes_t
]

## 8.2 Exposición

[
Exposicion_{a,t}
================

\frac{DiasElegibles_{a,t}}{DiasPeriodo_t}
]

## 8.3 Tarifa ajustada

[
Tarifa_{a,t}
============

TarifaBase_t
\times
FactorRiesgo_{a,t}
\times
FactorRegion_{a,t}
\times
FactorContractual_{a,t}
]

## 8.4 Liquidación de novedades

Deben considerarse:

* ingresos retroactivos;
* retiros retroactivos;
* fallecimientos;
* traslados;
* duplicidades;
* suspensión;
* movilidad;
* cambios de grupo de riesgo.

## 8.5 Riesgo no transferido

Incluso en capitación pueden quedar a cargo de la EPS:

* alto costo;
* medicamentos específicos;
* urgencias fuera de red;
* traslados;
* tecnologías excluidas;
* atenciones ordenadas judicialmente;
* desviaciones por población.

Estos componentes requieren reservas separadas.

---

## 9. Pago global prospectivo

## 9.1 Fórmula general

[
PGP_t
=====

Base_t
\times
AjustePoblacion_t
\times
AjusteRiesgo_t
+
AjustesContractuales_t
]

## 9.2 Reserva

[
R_t^{PGP}
=========

## E[PGP_t^{Final}\mid\mathcal F_t]

Pagado_t
]

## 9.3 Componentes

* valor fijo;
* actualización de población;
* riesgo;
* cumplimiento;
* exclusiones;
* liquidación;
* acuerdos de calidad;
* techo o piso.

## 9.4 PGP no equivale a capitación

Aunque ambos son prospectivos:

* capitación usa típicamente una unidad per cápita;
* PGP usa una suma global para una población;
* el mecanismo de ajuste puede ser diferente;
* el reparto de riesgo puede ser distinto.

---

## 10. Paquetes y pago por caso

## 10.1 Reserva por episodios abiertos

[
R_t^{Package}
=============

\sum_{e\in Open(t)}
E[
PagoFinal_e
-----------

Pagado_e(t)
\mid X_e
]
]

## 10.2 Componentes

* tarifa base;
* complejidad;
* severidad;
* complicación;
* estancia;
* implantes;
* reingreso;
* garantía;
* exclusiones.

## 10.3 Episodios iniciados no informados

[
IBNR_t^{Episode}
================

E[
\text{episodios ocurridos no reportados}
]
\times
E[
CostoPorEpisodio
]
]

## 10.4 Tail contractual

Puede existir desarrollo posterior por:

* reingresos;
* complicaciones;
* servicios de garantía;
* liquidación tardía;
* ajuste de clasificación.

---

## 11. Acuerdos de riesgo compartido

## 11.1 Resultado financiero

[
Resultado_t
===========

## IngresoContractual_t

CostoElegible_t
]

## 11.2 Compartición

[
Ajuste_t
========

g(Resultado_t)
]

donde (g) representa la regla contractual.

## 11.3 Reserva

[
R_t^{RiskShare}
===============

## E[g(Resultado_t)\mid\mathcal F_t]

AjusteReconocido_t
]

## 11.4 No linealidad

Si el acuerdo tiene umbrales, no es correcto aplicar la regla al costo esperado:

[
g(E[Costo])
\neq
E[g(Costo)]
]

Se requiere simular la distribución del costo.

---

## 12. Corredores de riesgo

Sea:

* (B): presupuesto objetivo;
* (C): costo final;
* (L): límite inferior;
* (U): límite superior.

Ejemplo:

[
Ajuste(C)
=========

\begin{cases}
\alpha(C-L), & C<L\
0, & L\leq C\leq U\
\beta(C-U), & C>U
\end{cases}
]

La reserva es:

[
R^{Corridor}
============

E[Ajuste(C)\mid\mathcal F_t]
]

Debe estimarse mediante simulación cuando (C) sea incierto.

---

## 13. Stop-loss contractual

## 13.1 Por persona

[
Recoverable_a
=============

\max(0,C_a-D)
]

donde (D) es el deducible.

## 13.2 Por contrato

[
Recoverable
===========

\max(0,C-Attachment)
]

## 13.3 Reserva bruta y recuperación

[
R^{Gross}
=========

E[CostoFuturo]
]

[
Asset^{Recovery}
================

E[Recoverable]
]

Se recomienda mantenerlos separados y reconocer la recuperación según el marco aplicable.

---

## 14. Componentes variables

## 14.1 Calidad

[
QualityPayment
==============

Base
\times
Score
\times
Rate
]

## 14.2 Indicadores pendientes

Si el resultado no está cerrado:

[
R^{Quality}
===========

\sum_k
P(Meta_k)
Valor_k
-------

PenalidadEsperada_k
]

## 14.3 Riesgo de medición

La reserva debe considerar:

* retraso en datos;
* disputa del indicador;
* auditoría;
* cambio de definición;
* población incompleta.

---

## 15. Población y exposición

## 15.1 Afiliados-mes

[
MM_t
====

\sum_a
\frac{DiasElegibles_{a,t}}{DiasPeriodo_t}
]

## 15.2 Población provisional

[
Adjustment_t
============

Tarifa_t
(
MM_t^{Final}
------------

MM_t^{Provisional}
)
]

## 15.3 Exposición no homogénea

Una persona afiliada durante diez días no equivale necesariamente a un tercio de una persona-mes cuando:

* existe alta utilización inicial;
* hay selección temporal;
* se presentan hospitalizaciones;
* existen periodos de protección.

Deben analizarse patrones por duración de afiliación.

---

## 16. Ajuste por riesgo

## 16.1 Modelo multiplicativo

[
ExpectedCost_a
==============

BaseCost
\times
RiskScore_a
]

## 16.2 Calibración contractual

El score debe corresponder a:

* población;
* servicios incluidos;
* periodo;
* definición contractual;
* información disponible.

## 16.3 Riesgo de codificación

Los scores pueden afectarse por:

* completitud diagnóstica;
* diferencias de IPS;
* intensificación de codificación;
* cambios tecnológicos;
* retraso de información.

## 16.4 Reserva

[
R_t^{RiskAdjustment}
====================

E[
PagoFinal(RiskScore^{Final})
----------------------------

PagoActual
]
]

---

## 17. Prestaciones pendientes de reporte

Un contrato prospectivo no elimina el IBNR médico.

El detalle de prestaciones puede ser necesario para:

* seguimiento de suficiencia;
* exclusiones;
* liquidación;
* alto costo;
* calidad;
* gestión clínica;
* pagos a subcontratistas.

## 17.1 Completitud

[
UltimateCost_t
==============

\frac{ObservedCost_t}{Completion_t}
]

## 17.2 Uso

Esta estimación mide el costo médico, no necesariamente la cuenta por pagar contractual.

Es fundamental no confundir:

[
CostoMedicoIncurrido
]

con:

[
PasivoContractual
]

---

## 18. Cuentas conocidas

La existencia de un pago prospectivo no excluye:

* facturas pendientes;
* ajustes;
* cuentas por servicios fuera del alcance;
* subcontratos;
* reembolsos;
* incentivos;
* conciliaciones.

Clasificación:

[
KnownOutstanding
================

FixedDue
+
ExcludedServices
+
SettlementDue
+
OtherKnown
]

---

## 19. Liquidación contractual

## 19.1 Provisional vs. final

[
SettlementAdjustment
====================

## FinalContractValue

ProvisionalRecognition
]

## 19.2 Factores

* población final;
* riesgo final;
* indicadores;
* exclusiones;
* notas crédito;
* incumplimientos;
* eventos extremos;
* cambios normativos.

## 19.3 Reserva

[
R_t^{Settlement}
================

E[SettlementAdjustment\mid\mathcal F_t]
]

Puede ser positiva o negativa.

---

## 20. Modelos actuariales

## 20.1 Medición directa

Para componentes fijos.

## 20.2 Bornhuetter-Ferguson

Para costos retenidos recientes:

[
IBNR^{BF}
=========

ExpectedUltimate
\times
PercentUnreported
]

## 20.3 PMPM

[
ExpectedUltimate
================

MembersMonths
\times
ExpectedPMPM
]

## 20.4 Frecuencia-severidad

[
ExpectedCost
============

ExpectedFrequency
\times
ExpectedSeverity
]

## 20.5 GLM

[
\log(\mu)
=========

\beta_0
+
\beta^\top X
+
\log(Exposicion)
]

## 20.6 Simulación

Para corredores, topes y riesgo compartido.

---

## 21. Uso de triángulos

## 21.1 Cuándo son útiles

* servicios excluidos;
* paquetes reportados con retraso;
* costo médico interno;
* pagos a subcontratistas;
* episodios abiertos;
* benchmark.

## 21.2 Cuándo no son apropiados

No se recomienda usar un paid Chain Ladder sobre los pagos fijos de capitación para estimar el costo último contractual.

El pago fijo depende del contrato, no del desarrollo de siniestros.

## 21.3 Triángulos alternativos

* prestaciones informadas;
* episodios;
* población;
* liquidaciones;
* costos excluidos;
* pagos variables.

---

## 22. Frecuencia-severidad

## 22.1 Frecuencia

[
N_t
\sim
NegBin(\lambda_t,k)
]

[
\log(\lambda_t)
===============

X_t^\top\beta
+
\log(MM_t)
]

## 22.2 Severidad

[
S_t
\sim
Gamma(\mu_t,\phi)
]

## 22.3 Costo

[
C_t
===

N_tS_t
]

Este enfoque facilita evaluar la suficiencia del contrato.

---

## 23. Modelos PMPM

## 23.1 PMPM observado

[
PMPM_t^{Obs}
============

\frac{Costo_t^{Obs}}{MM_t}
]

## 23.2 PMPM último

[
PMPM_t^{Ult}
============

\frac{PMPM_t^{Obs}}{Completion_t}
]

## 23.3 Resultado

[
Margin_t
========

## ContractPMPM_t

UltimateMedicalPMPM_t
]

Debe aclararse que margen contractual y reserva contable son medidas diferentes.

---

## 24. Credibilidad y modelos bayesianos

Para contratos pequeños:

[
\theta_c
\sim
N(\mu,\tau^2)
]

[
Y_{ct}
\mid\theta_c
\sim
Distribution(\theta_c)
]

Esto permite compartir información entre:

* contratos;
* regiones;
* prestadores;
* poblaciones.

Es preferible a utilizar promedios inestables por contrato.

---

## 25. Escenarios y suficiencia

## 25.1 Escenario base

Experiencia esperada.

## 25.2 Adverso

* mayor utilización;
* mayor severidad;
* deterioro de población;
* menor ajuste de riesgo;
* penalidades;
* retraso de información.

## 25.3 Extremo

* epidemia;
* evento de alto costo;
* pérdida de red;
* cambio regulatorio;
* concentración de pacientes.

## 25.4 Ratio de suficiencia

[
SufficiencyRatio
================

\frac{IngresoContractualEsperado}
{CostoMedicoUltimoEsperado}
]

No debe interpretarse aisladamente de gastos, capital y riesgo.

---

## 26. Reconocimiento de ingresos y costos

La metodología debe separar:

* ingreso facturado;
* ingreso devengado;
* ingreso cobrado;
* costo observado;
* costo incurrido;
* obligación contractual;
* ajustes contingentes.

No debe utilizarse la factura como único criterio de devengo.

---

## 27. RIPS, FEV y trazabilidad

La Resolución 948 de 2026 regula nuevamente los RIPS como soporte de la factura electrónica de venta en salud. Para acuerdos de capitación, contempla que la primera factura pueda expedirse sin RIPS; ello confirma que la facturación inicial y el detalle de prestaciones pueden tener momentos diferentes.

## 27.1 Implicación actuarial

Deben conservarse por separado:

* factura contractual;
* población;
* RIPS;
* servicios;
* liquidación;
* pagos.

## 27.2 Validaciones

* contrato vigente;
* población elegible;
* periodo correcto;
* modalidad;
* CUV cuando corresponda;
* correspondencia entre población y pago;
* completitud posterior de RIPS.

---

## 28. Giro directo

El giro directo modifica el flujo financiero, pero no necesariamente la sustancia de la obligación.

Debe identificarse:

* pagador económico;
* pagador operativo;
* beneficiario;
* imputación contractual;
* fecha de reconocimiento;
* fecha de giro;
* saldo posterior.

Las reglas de giro directo para UPC y presupuestos máximos han sido desarrolladas dentro del Decreto 780 de 2016 y sus modificaciones.

## 28.1 Riesgo de doble conteo

Un giro directo puede aparecer:

* en ADRES;
* en EPS;
* en IPS;
* en conciliación contractual.

La reconciliación debe garantizar que el mismo pago no reduzca dos veces el pasivo.

---

## 29. Reconciliación

## 29.1 Ecuación contractual

[
ValorFinal
==========

Base
+
AjustePoblacion
+
AjusteRiesgo
+
Calidad
+
ServiciosAdicionales
--------------------

Penalidades
]

## 29.2 Saldo

[
Saldo
=====

## ValorFinal

## PagosDirectos

## PagosEPS

NotasCredito
]

## 29.3 Fuentes

Reconciliar:

* contrato;
* SIIFA;
* facturación;
* población;
* ADRES;
* pagos;
* RIPS;
* contabilidad;
* liquidaciones.

---

## 30. Validación y backtesting

## 30.1 Reserva contractual

Comparar:

[
\widehat R_t
]

con:

[
LiquidacionFinal_t-Pagos_t
]

## 30.2 Costo médico

Comparar:

[
\widehat C_t^{Ultimate}
]

con el costo posteriormente observado.

## 30.3 Métricas

* sesgo;
* MAE;
* RMSE;
* error porcentual;
* estabilidad;
* cobertura;
* suficiencia.

## 30.4 Validación por componente

* población;
* riesgo;
* calidad;
* exclusiones;
* ajustes;
* alto costo;
* pago fijo.

---

## 31. Implementación SQL

## 31.1 Exposición

```sql
SELECT
    contract_id,
    period,
    SUM(
        eligible_days * 1.0
        / period_days
    ) AS member_months
FROM contract_enrollment
GROUP BY
    contract_id,
    period;
```

## 31.2 Devengo de capitación

```sql
SELECT
    contract_id,
    period,
    SUM(
        eligible_days * 1.0
        / period_days
        * base_rate
        * risk_factor
        * regional_factor
    ) AS accrued_capitation
FROM contract_enrollment
GROUP BY
    contract_id,
    period;
```

## 31.3 Saldo

```sql
SELECT
    c.contract_id,
    c.period,
    c.accrued_value
        + COALESCE(c.population_adjustment, 0)
        + COALESCE(c.risk_adjustment, 0)
        + COALESCE(c.quality_adjustment, 0)
        - COALESCE(p.total_paid, 0)
        AS outstanding_balance
FROM contract_accrual c
LEFT JOIN contract_payments p
    ON c.contract_id = p.contract_id
   AND c.period = p.period;
```

---

## 32. Implementación Python

```python
from __future__ import annotations

import pandas as pd


def calculate_capitation_accrual(
    enrollment: pd.DataFrame,
) -> pd.DataFrame:
    required = {
        "contract_id",
        "period",
        "eligible_days",
        "period_days",
        "base_rate",
        "risk_factor",
        "regional_factor",
    }

    missing = required.difference(enrollment.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    data = enrollment.copy()

    data["exposure"] = (
        data["eligible_days"] / data["period_days"]
    )

    data["accrued_amount"] = (
        data["exposure"]
        * data["base_rate"]
        * data["risk_factor"]
        * data["regional_factor"]
    )

    return (
        data.groupby(
            ["contract_id", "period"],
            as_index=False,
        )
        .agg(
            member_months=("exposure", "sum"),
            accrued_amount=("accrued_amount", "sum"),
        )
    )
```

## 32.1 Reserva contractual

```python
def calculate_contract_reserve(
    contracts: pd.DataFrame,
) -> pd.Series:
    required = {
        "accrued_amount",
        "population_adjustment",
        "risk_adjustment",
        "quality_adjustment",
        "excluded_services",
        "paid_to_date",
    }

    missing = required.difference(contracts.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    expected_final = (
        contracts["accrued_amount"]
        + contracts["population_adjustment"]
        + contracts["risk_adjustment"]
        + contracts["quality_adjustment"]
        + contracts["excluded_services"]
    )

    return expected_final - contracts["paid_to_date"]
```

---

## 33. Implementación R

```r
library(dplyr)

capitation_accrual <- enrollment |>
  mutate(
    exposure = eligible_days / period_days,
    accrued_amount =
      exposure *
      base_rate *
      risk_factor *
      regional_factor
  ) |>
  group_by(contract_id, period) |>
  summarise(
    member_months = sum(exposure),
    accrued_amount = sum(accrued_amount),
    .groups = "drop"
  )
```

## 33.1 PMPM

```r
contract_results <- contract_data |>
  mutate(
    observed_pmpm =
      observed_cost / member_months,
    ultimate_pmpm =
      observed_pmpm / completion_factor,
    expected_ultimate =
      ultimate_pmpm * member_months,
    expected_margin =
      contractual_revenue - expected_ultimate
  )
```

---

## 34. Caso numérico

Supóngase un contrato capitado mensual.

| Componente                     |           Valor |
| ------------------------------ | --------------: |
| Afiliados-mes                  |         100.000 |
| Tarifa base                    |         120.000 |
| Factor de riesgo               |            1,04 |
| Factor regional                |            1,02 |
| Pagado                         | 12.000 millones |
| Ajuste población esperado      |    200 millones |
| Penalidad esperada             |     80 millones |
| Servicios excluidos pendientes |    350 millones |

## 34.1 Devengo

[
Devengo
=======

100{,}000
\times
120{,}000
\times
1.04
\times
1.02
]

[
Devengo
=======

12{,}729.6\text{ millones}
]

## 34.2 Valor final esperado

[
ValorFinal
==========

12{,}729.6
+
200
---

80
+
350
]

[
ValorFinal
==========

13{,}199.6
]

## 34.3 Reserva

[
Reserva
=======

## 13{,}199.6

12{,}000
]

[
Reserva
=======

1{,}199.6
]

## 34.4 Costo médico

Supóngase:

* costo observado: 10.500 millones;
* completitud: 85%.

[
CostoUltimo
===========

$$
\frac{10{,}500}{0.85}
$$

12{,}352.9
]

Este costo no es igual a la reserva contractual. Permite evaluar suficiencia:

[
MargenMedicoEsperado
====================

$$
12{,}729.6-12{,}352.9
$$

376.7
]

El análisis debe incorporar gastos y componentes excluidos antes de concluir que el contrato es suficiente.

---

## 35. Gobierno y documentación

La nota técnica debe incluir:

1. modalidad;
2. sustancia económica;
3. servicios incluidos y excluidos;
4. unidad de pago;
5. población;
6. riesgo transferido;
7. riesgo retenido;
8. reglas de devengo;
9. ajustes;
10. corredores;
11. stop-loss;
12. calidad;
13. fuentes de datos;
14. reconciliación;
15. modelos;
16. validación;
17. escenarios;
18. limitaciones;
19. ajustes manuales;
20. responsables.

## 35.1 Inventario contractual

Debe existir una ficha estandarizada por contrato.

## 35.2 Versionado

Conservar:

* contrato original;
* otrosíes;
* fecha de vigencia;
* parámetros;
* liquidaciones;
* modificaciones.

---

## 36. Riesgos y limitaciones

## 36.1 Riesgo contractual

Interpretación incorrecta del alcance.

## 36.2 Riesgo poblacional

Afiliados incompletos o retroactivos.

## 36.3 Riesgo clínico

Utilización y severidad mayores.

## 36.4 Riesgo de reporte

RIPS incompletos.

## 36.5 Riesgo de contraparte

Incumplimiento de EPS, IPS o proveedor.

## 36.6 Riesgo regulatorio

Cambios en reglas, cobertura o financiación.

## 36.7 Riesgo de modelo

Confundir costo médico con obligación contractual.

---

## 37. Matriz metodológica

| Componente          | Método recomendado        |
| ------------------- | ------------------------- |
| Pago fijo capitado  | Devengo contractual       |
| Ajuste de población | Modelo de exposición      |
| Ajuste por riesgo   | Modelo contractual        |
| Servicios excluidos | BF o Chain Ladder         |
| Episodios abiertos  | Modelo por caso           |
| Corredor de riesgo  | Simulación                |
| Stop-loss           | Frecuencia-severidad      |
| Calidad             | Probabilidad × monto      |
| Liquidación         | Valor esperado            |
| Costo médico        | PMPM/frecuencia-severidad |
| IBNR clínico        | Completion factors        |
| Contrato pequeño    | Credibilidad/Bayes        |

---

## 38. Checklist

## Contrato

* [ ] Modalidad identificada.
* [ ] Alcance documentado.
* [ ] Riesgo transferido definido.
* [ ] Servicios excluidos identificados.
* [ ] Reglas de liquidación disponibles.
* [ ] Otrosíes versionados.

## Población

* [ ] Afiliados conciliados.
* [ ] Días elegibles calculados.
* [ ] Novedades retroactivas consideradas.
* [ ] Factores de riesgo validados.
* [ ] Población provisional y final diferenciadas.

## Reserva

* [ ] Devengo contractual calculado.
* [ ] Pagos conciliados.
* [ ] Ajustes poblacionales estimados.
* [ ] Riesgo retenido reservado.
* [ ] Servicios excluidos reservados.
* [ ] Calidad estimada.
* [ ] Stop-loss separado.
* [ ] Se descartó doble conteo.

## Validación

* [ ] Liquidaciones históricas revisadas.
* [ ] Backtesting ejecutado.
* [ ] Costo médico validado.
* [ ] Escenarios realizados.
* [ ] Suficiencia analizada.
* [ ] Resultados reconciliados.

## Gobierno

* [ ] Nota técnica actualizada.
* [ ] Revisión contractual realizada.
* [ ] Código versionado.
* [ ] Datos congelados.
* [ ] Ajustes manuales documentados.
* [ ] Revisión independiente completada.

---

## 39. Conclusiones

Las modalidades prospectivas requieren una lógica distinta a la del reserving tradicional por evento.

En capitación y PGP deben separarse:

[
PasivoContractual
]

[
CostoMedicoIncurrido
]

[
RiesgoRetenido
]

[
AjusteDeLiquidacion
]

Un paid Chain Ladder aplicado sobre pagos fijos no estima apropiadamente la obligación contractual, porque el flujo depende de la tarifa y la exposición.

La metodología más robusta combina:

* devengo contractual para componentes fijos;
* modelos de exposición para población;
* PMPM o frecuencia-severidad para costo médico;
* BF para servicios excluidos recientes;
* simulación para corredores;
* modelos de probabilidad para calidad;
* reconciliación con RIPS, FEV, SIIFA y pagos.

El análisis debe basarse en la sustancia económica del contrato. Dos acuerdos llamados “capitación” pueden transferir riesgos diferentes y, por tanto, requerir reservas distintas.

---

## Referencias normativas

* Decreto 780 de 2016 y sus modificaciones.
* Decreto 441 de 2022.
* Decreto 489 de 2024.
* Resolución 2284 de 2023.
* Resolución 1962 de 2025.
* Resolución 948 de 2026.
* Circular Única de la Superintendencia Nacional de Salud.
* Normas vigentes del SIIFA.
* Instrucciones vigentes sobre reservas técnicas y cuentas por pagar.

## Referencias técnicas

* Born, R. y Ferguson, R. *The Actuary and IBNR*.
* Friedland, J. *Estimating Unpaid Claims Using Basic Techniques*.
* Wüthrich, M. y Merz, M. *Stochastic Claims Reserving Methods in Insurance*.
* McCullagh, P. y Nelder, J. *Generalized Linear Models*.
* Bühlmann, H. y Gisler, A. *A Course in Credibility Theory*.
* Gelman, A. et al. *Bayesian Data Analysis*.

---

## Próximo capítulo

➡️ **26-colombian-health-reserving-high-cost-and-complex-cases.md**

Tema propuesto:

> Modelación individual y agregada de enfermedades de alto costo, casos complejos y colas clínicas.
