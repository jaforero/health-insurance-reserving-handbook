---
title: "Health Exposure, Utilization and Severity"
part: "Parte VI · Especificidades de salud"
chapter: 23
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

# Health Exposure, Utilization and Severity

Este capítulo desarrolla tres motores fundamentales del costo médico en seguros de salud: exposición, utilización y severidad. En reserving, estos conceptos son necesarios para interpretar la experiencia histórica, construir metodologías de completitud, diseñar modelos frecuencia-severidad y evaluar si los patrones observados de pagos o incurridos reflejan desarrollo normal, cambio de mix, cambio de exposición o deterioro real del costo.

Un modelo de reservas de salud que solo observa pagos acumulados puede ser suficiente en portafolios estables y homogéneos. Sin embargo, cuando cambian la población cubierta, la red de prestadores, el perfil epidemiológico, la modalidad contractual o la codificación, la reserva debe descomponer el costo en componentes explicables. La relación básica es:

$$
\text{Costo médico} = \text{Exposición} \times \text{Utilización} \times \text{Severidad}
$$

Esta descomposición no reemplaza los triángulos. Los complementa.

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector debería poder:

- Definir exposición en seguros de salud y seleccionar unidades apropiadas.
- Diferenciar utilización, frecuencia, intensidad y mix de servicios.
- Medir severidad y distinguirla de cambios tarifarios, clínicos o contractuales.
- Construir métricas PMPM, PEPM, frecuencia por mil y costo unitario.
- Separar cambios de volumen, precio y mix en la experiencia.
- Integrar exposición, utilización y severidad en reserving, backtesting y análisis de suficiencia.

## 1. Descomposición del costo médico

El costo médico agregado puede expresarse como:

$$
C = E \times U \times S
$$

donde:

- \(E\) es la exposición;
- \(U\) es la utilización por unidad de exposición;
- \(S\) es la severidad o costo promedio por servicio, reclamación o evento.

Dependiendo de la granularidad, esta relación puede formularse de varias formas:

$$
C = \text{miembros-mes} \times \frac{\text{servicios}}{\text{miembros-mes}} \times \frac{\text{costo}}{\text{servicios}}
$$

o:

$$
C = \text{vidas expuestas} \times \frac{\text{reclamaciones}}{\text{vida}} \times \frac{\text{costo}}{\text{reclamación}}
$$

La selección de unidad depende del producto, la cobertura, la disponibilidad de datos y la pregunta actuarial.

## 2. Exposición

La exposición mide la cantidad de riesgo cubierta durante un periodo. En salud, la exposición rara vez se limita a contar pólizas. Lo usual es medir personas cubiertas y tiempo cubierto.

Unidades frecuentes:

| Unidad | Uso |
|---|---|
| Afiliados | Conteo simple al corte |
| Vidas-mes | Exposición temporal en salud |
| Miembros-mes | Equivalente frecuente en modelos PMPM |
| Contratos-mes | Productos colectivos o empresariales |
| Familias-mes | Coberturas familiares |
| Cápitas-mes | Contratos capitados |
| Días de cobertura | Exposición granular |

La exposición debe reflejar el tiempo durante el cual el asegurador o pagador asumió riesgo. Una persona cubierta medio mes no debe equivaler automáticamente a una persona cubierta todo el mes.

## 3. Miembros-mes

La unidad más común en salud es miembros-mes:

$$
\text{Miembros-mes} = \sum_i \frac{\text{días cubiertos}_{i}}{\text{días del mes}}
$$

Ejemplo:

| Afiliado | Días cubiertos en el mes | Miembros-mes |
|---|---:|---:|
| A | 30 | 1.00 |
| B | 15 | 0.50 |
| C | 0 | 0.00 |
| D | 30 | 1.00 |

Exposición total:

$$
1.00 + 0.50 + 0.00 + 1.00 = 2.50
$$

Esta medida permite comparar meses con diferente número de afiliados, altas, bajas o traslados.

## 4. Exposición promedio vs exposición devengada

Es común ver exposición calculada como promedio de afiliados al inicio y final del mes:

$$
E_t = \frac{N_{t, inicio} + N_{t, fin}}{2}
$$

Este método puede ser aceptable si los movimientos son pequeños y uniformes. Sin embargo, puede fallar cuando hay:

- afiliación masiva;
- retiros concentrados;
- movilidad entre planes;
- cambios contractuales;
- entrada o salida de grupos empresariales;
- cambios regulatorios de población.

Para reserving, la exposición devengada basada en días cubiertos es preferible cuando existe información granular.

## 5. Utilización

La utilización mide la cantidad de servicios consumidos por unidad de exposición. Puede expresarse como:

$$
U = \frac{\text{número de servicios}}{\text{exposición}}
$$

o, en escala práctica:

$$
U_{1000} = \frac{\text{servicios}}{\text{miembros-mes}} \times 1000
$$

La utilización no es una única variable. Puede medirse por:

- consultas;
- urgencias;
- hospitalizaciones;
- días cama;
- procedimientos;
- medicamentos;
- laboratorios;
- imágenes diagnósticas;
- terapias;
- eventos de alto costo.

Cada tipo de servicio tiene patrón de desarrollo, severidad y sensibilidad clínica diferente.

## 6. Frecuencia, intensidad y mix

La utilización puede descomponerse en frecuencia e intensidad.

| Concepto | Pregunta |
|---|---|
| Frecuencia | ¿Cuántos eventos ocurren? |
| Intensidad | ¿Cuántos servicios por evento? |
| Mix | ¿Qué tipos de servicios componen el costo? |
| Severidad | ¿Cuánto cuesta cada servicio o evento? |

Ejemplo hospitalario:

$$
\text{Costo hospitalario} =
\text{admisiones} \times
\text{días por admisión} \times
\text{costo por día}
$$

Un aumento de costo puede venir de más admisiones, mayor estancia, mayor costo unitario o cambio hacia casos más complejos. La reserva debe distinguir estos motores cuando el cambio es material.

## 7. Severidad

La severidad mide el costo promedio por unidad de utilización:

$$
S = \frac{\text{costo}}{\text{número de servicios}}
$$

También puede medirse como:

- costo por reclamación;
- costo por evento;
- costo por admisión;
- costo por día cama;
- costo por procedimiento;
- costo por tratamiento;
- costo por episodio clínico.

La severidad observada puede cambiar por:

- inflación médica;
- cambio tarifario;
- cambio en mezcla de servicios;
- mayor complejidad clínica;
- cambio de red;
- cambio contractual;
- codificación distinta;
- reconocimiento contable diferente;
- glosas o ajustes.

Por tanto, una severidad mayor no siempre significa deterioro médico real.

## 8. PMPM y PEPM

Dos métricas frecuentes son PMPM y PEPM.

PMPM significa per member per month:

$$
\text{PMPM} = \frac{\text{costo médico}}{\text{miembros-mes}}
$$

PEPM significa per employee per month y se usa en contextos empresariales:

$$
\text{PEPM} = \frac{\text{costo médico}}{\text{empleados-mes}}
$$

PMPM es más apropiado cuando el riesgo depende de todos los miembros cubiertos. PEPM puede ser útil cuando la contratación y facturación se basan en empleados titulares.

## 9. Relación con reserving

La descomposición exposición-utilización-severidad ayuda en reserving de varias formas:

| Uso | Aplicación |
|---|---|
| Normalización | Comparar periodos con exposición distinta |
| Diagnóstico | Separar volumen, precio y mix |
| Selección de método | Definir si usar triángulos, PMPM o frecuencia-severidad |
| Backtesting | Explicar desviaciones reserva vs real |
| Escenarios | Proyectar cambios de morbilidad o tarifa |
| Segmentación | Identificar subpoblaciones con desarrollo distinto |

Cuando la exposición cambia rápidamente, un triángulo de montos puede mostrar crecimiento que no corresponde a deterioro. Normalizar por exposición evita conclusiones equivocadas.

## 10. Métodos basados en completitud PMPM

En salud, una alternativa común a los triángulos tradicionales es estimar el costo último por PMPM usando factores de completitud.

Si \(C_{t,d}\) es el costo observado para el periodo de servicio \(t\) al desarrollo \(d\), y \(E_t\) es la exposición, entonces:

$$
\text{PMPM observado}_{t,d} = \frac{C_{t,d}}{E_t}
$$

Si \(q_d\) es el porcentaje esperado de completitud al desarrollo \(d\), entonces:

$$
\widehat{\text{PMPM último}}_{t} =
\frac{\text{PMPM observado}_{t,d}}{q_d}
$$

La reserva estimada es:

$$
\widehat{R}_{t} =
E_t \times \widehat{\text{PMPM último}}_{t} - C_{t,d}
$$

Este enfoque es útil cuando la exposición está bien medida y el desarrollo es relativamente corto.

## 11. Método frecuencia-severidad

El enfoque frecuencia-severidad estima por separado número de eventos y costo por evento.

$$
\widehat{C} =
E \times \widehat{F} \times \widehat{S}
$$

donde:

- \(E\) es exposición;
- \(\widehat{F}\) es frecuencia esperada por unidad de exposición;
- \(\widehat{S}\) es severidad esperada por evento.

La reserva se obtiene como:

$$
\widehat{R} = \widehat{C}_{\text{último}} - C_{\text{observado}}
$$

Este enfoque es especialmente útil cuando frecuencia y severidad tienen drivers distintos.

## 12. Ajuste por mix

El mix puede distorsionar la interpretación de severidad. Supóngase que el costo promedio sube de 100 a 120. Esto puede deberse a:

- incremento tarifario;
- más servicios de alta complejidad;
- cambio de red;
- reducción de servicios baratos;
- aumento real de intensidad.

Una forma simple de separar mix y severidad es fijar ponderaciones base:

$$
S^{\text{estandarizada}}_t =
\sum_k w_{k,0} \times S_{k,t}
$$

donde \(w_{k,0}\) es la participación del servicio \(k\) en el periodo base.

Si la severidad estandarizada crece menos que la observada, parte del aumento proviene de cambio de mix.

## 13. Ajuste por riesgo y morbilidad

La exposición simple no siempre captura el riesgo. Dos poblaciones con el mismo número de miembros-mes pueden tener costos esperados distintos por edad, sexo, diagnóstico, región o condición clínica.

Una exposición ajustada por riesgo puede expresarse como:

$$
E^{*} = \sum_i E_i \times r_i
$$

donde \(r_i\) es un factor de riesgo relativo.

Esto permite calcular PMPM ajustado:

$$
\text{PMPM ajustado} = \frac{C}{E^{*}}
$$

El ajuste por riesgo es útil cuando cambia la composición de la población. Sin ajuste, el modelo puede confundir mayor morbilidad con tendencia médica o deterioro operativo.

## 14. Tendencia médica

La tendencia médica combina cambios en utilización, severidad, tecnología, inflación, comportamiento del prestador y morbilidad.

Una descomposición práctica:

$$
1 + T =
(1 + T_U)(1 + T_S)(1 + T_M) - 1
$$

donde:

- \(T_U\) es tendencia de utilización;
- \(T_S\) es tendencia de severidad o precio;
- \(T_M\) es efecto de mix o morbilidad.

En reserving, la tendencia puede afectar periodos recientes con desarrollo incompleto. No debe aplicarse mecánicamente sin validar si el cambio ya está reflejado en los datos observados.

## 15. Estacionalidad

La utilización médica puede tener patrones estacionales:

- enfermedades respiratorias;
- periodos escolares;
- vacaciones;
- ciclos de autorización;
- cierres contables;
- campañas de promoción y prevención;
- epidemias o brotes.

La estacionalidad puede afectar tanto ocurrencia como reporte. Un método mensual debe separar:

- estacionalidad clínica;
- estacionalidad administrativa;
- estacionalidad de pago;
- efectos calendario por días hábiles.

## 16. Shocks de utilización

Algunos eventos rompen patrones históricos:

- epidemias;
- pandemias;
- cambios regulatorios;
- ampliación de cobertura;
- entrada o salida de prestadores;
- acumulación de demanda represada;
- cambios de autorizaciones;
- litigios o fallos judiciales;
- cambios en canales de atención.

En estos casos, los factores históricos de desarrollo pueden ser insuficientes. Puede requerirse juicio actuarial, escenarios, Bornhuetter-Ferguson, modelos con covariables o ajustes explícitos.

## 17. Calidad de datos

La medición de exposición, utilización y severidad requiere controles específicos:

| Control | Riesgo mitigado |
|---|---|
| Días cubiertos válidos | Exposición sobre/subestimada |
| Afiliados duplicados | PMPM artificialmente bajo |
| Servicios duplicados | Utilización artificialmente alta |
| Códigos homologados | Rupturas de serie |
| Montos negativos identificados | Ajustes mal clasificados |
| Pagos parciales trazables | Severidad incompleta |
| Contratos vigentes | Precios mal interpretados |
| Fechas consistentes | Leakage o rezagos erróneos |

Los controles deben ejecutarse antes de modelar. Modelos sofisticados no compensan definiciones inconsistentes.

## 18. Aplicación al contexto colombiano

En Colombia, la medición debe considerar:

- afiliados y exposición por régimen, plan, región y grupo de riesgo;
- trazabilidad de RIPS, factura electrónica y pagos;
- UPC, presupuestos máximos, exclusiones y mecanismos especiales;
- cambios normativos que afecten reporte o reconocimiento;
- glosas, devoluciones y conciliaciones;
- contratación por evento, capitación, paquete o pago global prospectivo;
- alto costo y concentración por patología;
- diferencias entre prestación, radicación, contabilización y pago.

La exposición ajustada por riesgo es relevante porque el costo esperado no depende únicamente del número de afiliados. La morbilidad, la edad, la región, el acceso y el tipo de red pueden cambiar materialmente el costo último.

## 19. Ejemplo numérico

Supóngase:

| Periodo | Miembros-mes | Servicios | Costo observado |
|---|---:|---:|---:|
| Enero | 10,000 | 2,000 | 500,000 |
| Febrero | 12,000 | 2,640 | 712,800 |

Para enero:

$$
U = \frac{2{,}000}{10{,}000} = 0.20
$$

$$
S = \frac{500{,}000}{2{,}000} = 250
$$

Para febrero:

$$
U = \frac{2{,}640}{12{,}000} = 0.22
$$

$$
S = \frac{712{,}800}{2{,}640} = 270
$$

El costo total creció 42.6%, pero ese crecimiento se descompone en:

- exposición: 20.0%;
- utilización por miembro: 10.0%;
- severidad: 8.0%;
- efecto combinado: el resto.

Sin esta descomposición, se podría atribuir erróneamente todo el aumento a tendencia médica.

## 20. Implicaciones para backtesting

Cuando una reserva difiere del desarrollo real, el análisis debe preguntar:

- ¿La exposición real fue distinta de la esperada?
- ¿La utilización cambió por frecuencia o intensidad?
- ¿La severidad cambió por tarifa, mix o complejidad?
- ¿Hubo cambios de reporte o pago?
- ¿El desarrollo incompleto fue normal o anómalo?
- ¿El error está concentrado en segmentos específicos?

El backtesting de salud debe explicar variaciones, no solo medir error agregado.

## 21. Checklist práctico

Antes de usar métricas de exposición, utilización y severidad en reserving, validar:

- La exposición está medida en unidades consistentes.
- Los afiliados parciales se tratan correctamente.
- La utilización se define por tipo de servicio.
- La severidad excluye duplicados y ajustes mal clasificados.
- Los cambios de mix están identificados.
- La tendencia médica separa precio, utilización y morbilidad.
- Los shocks recientes están documentados.
- El modelo no usa información posterior al corte.
- Los resultados se reconcilian con pagos, incurridos y saldos conocidos.

## 22. Conclusiones

Exposición, utilización y severidad son el puente entre experiencia médica y reserving actuarial. Permiten explicar por qué cambia el costo y reducen el riesgo de interpretar crecimiento de montos como desarrollo puro.

En seguros de salud, esta descomposición es especialmente importante porque el costo puede cambiar por población, morbilidad, acceso, red, tarifas, glosas, contratos y comportamiento operativo. Integrar estas métricas mejora la selección metodológica, el backtesting, la comunicación y el gobierno de reservas.

El siguiente paso es estudiar tendencia médica, estacionalidad y shocks, que explican cómo estos motores evolucionan en el tiempo.

## Referencias

- ASOP No. 1, Introductory Actuarial Standard of Practice.
- ASOP No. 23, Data Quality.
- ASOP No. 38, Using Models Outside the Actuary's Area of Expertise.
- ASOP No. 43, Property/Casualty Unpaid Claim Estimates.
- ASOP No. 56, Modeling.
- Society of Actuaries, materiales técnicos sobre health reserving, PMPM, trend y completion factors.

## Próximo capítulo

➡️ **[Health Medical Trend, Seasonality and Shocks](24-health-medical-trend-seasonality-and-shocks.md)**
