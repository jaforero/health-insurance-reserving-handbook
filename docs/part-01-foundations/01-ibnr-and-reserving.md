---
title: IBNR y reservas
description: Introducción práctica al IBNR, las reservas de siniestros y la lógica actuarial que conecta pagos, incurridos, ultimate y suficiencia técnica.
status: draft
version: "0.1.5"
chapter: "01"
part: "part-01-foundations"
language: "es"
last_updated: "2026-07-14"
---

# IBNR y reservas

El reserving actuarial busca estimar el costo último de eventos ya ocurridos, aun cuando parte de la información todavía no se haya observado en pagos, facturación, auditoría, conciliación o registro contable. En salud, este problema es especialmente relevante porque el ciclo de una reclamación puede incluir prestación del servicio, radicación, validación, autorización, glosa, conciliación, pago y ajustes posteriores.

IBNR significa *incurred but not reported*: siniestros o reclamaciones ocurridas pero aún no reportadas o no suficientemente reconocidas en la información disponible. En la práctica, muchas organizaciones usan IBNR como una etiqueta amplia para el pasivo no observado o no completamente registrado. Conviene separar conceptos, porque no todos los faltantes tienen la misma naturaleza.

## Qué se está estimando

Para un periodo de ocurrencia o año de origen, el objetivo central es estimar:

$$
Ultimate = Pagado\ acumulado + No\ pagado
$$

El componente no pagado puede descomponerse así:

$$
No\ pagado = Reserva\ caso + IBNR + IBNER
$$

donde:

- `Reserva caso` es el monto reconocido para reclamaciones ya reportadas, pero no completamente pagadas.
- `IBNR` representa reclamaciones ocurridas que aún no han sido reportadas o registradas.
- `IBNER` significa *incurred but not enough reported*: reclamaciones reportadas, pero con monto insuficientemente estimado.

En salud, la frontera entre estos componentes puede no ser limpia. Una reclamación puede estar radicada pero no auditada, parcialmente glosada, pendiente de soporte, en conciliación o con pago parcial. Por eso el actuario debe entender la operación y no limitarse a aplicar un método mecánico.

## Pagado, incurrido y ultimate

La base pagada observa desembolsos reales. Tiene una ventaja: suele ser objetiva. Su debilidad es que puede rezagarse frente a la ocurrencia del servicio.

La base incurrida combina pagos más reservas caso. Tiene una ventaja: puede reconocer antes parte del costo esperado. Su debilidad es que depende de prácticas de estimación, reglas operativas, suficiencia de reservas caso y consistencia del proceso.

La relación básica es:

$$
Incurrido = Pagado + Reserva\ caso
$$

El ultimate es el costo final esperado de todas las reclamaciones de un periodo de origen:

$$
Ultimate = Incurrido\ observado + Desarrollo\ futuro\ del\ incurrido
$$

o, desde la base pagada:

$$
Ultimate = Pagado\ observado + Desarrollo\ futuro\ del\ pagado
$$

Ambas bases pueden ser útiles. La pregunta no es cuál es universalmente mejor, sino cuál responde mejor al patrón de desarrollo, calidad de datos y objetivo de la estimación.

## Por qué existe el IBNR

El IBNR existe porque el proceso de observación tiene rezagos. En salud, los rezagos pueden venir de:

- demora entre fecha de servicio y fecha de radicación;
- auditoría médica o administrativa;
- glosas, devoluciones y conciliaciones;
- pagos parciales;
- contratos por capitación, evento, paquete o presupuestos globales;
- cambios regulatorios o de codificación;
- ajustes contables posteriores;
- diferencias entre fecha de prestación, fecha de factura, fecha de registro y fecha de pago.

La reserva no se estima para explicar el pasado ya cerrado. Se estima porque, en la fecha de valuación, la información observada es incompleta.

## Año de origen y fecha de valuación

Un análisis de reservas necesita definir al menos dos ejes:

- `Año de origen`: periodo al que pertenece la reclamación. Puede definirse por fecha de ocurrencia, fecha de servicio, fecha de admisión, fecha de egreso o fecha de radicación, según el objetivo.
- `Fecha de valuación`: fecha hasta la cual se considera observada la información.

La diferencia entre estas dos dimensiones produce la edad de desarrollo:

$$
Edad\ de\ desarrollo = Fecha\ de\ valuación - Periodo\ de\ origen
$$

Los años de origen antiguos tienen más desarrollo observado. Los años recientes tienen menos desarrollo y, por tanto, más incertidumbre.

## Reserving como proceso, no solo como fórmula

Un método actuarial produce una estimación, pero la suficiencia de reservas depende de un proceso más amplio:

1. Definir el objetivo de la estimación.
2. Entender la operación de reclamaciones.
3. Seleccionar la base de datos adecuada.
4. Construir triángulos consistentes.
5. Revisar calidad, completitud y cambios de proceso.
6. Seleccionar métodos apropiados.
7. Evaluar sensibilidad e incertidumbre.
8. Documentar supuestos, limitaciones y juicio profesional.
9. Comunicar resultados de forma trazable.

La estimación final debe ser defendible. No basta con que el modelo corra; debe ser claro qué representa, qué excluye y qué tan confiable es.

## Ejemplo conceptual

Supongamos que para el año de origen 2025, a la fecha de valuación se han pagado 100 y se han registrado reservas caso por 40. El incurrido observado es:

$$
Incurrido = 100 + 40 = 140
$$

Si el análisis actuarial estima que el ultimate esperado es 170, entonces:

$$
No\ pagado = 170 - 100 = 70
$$

Ese no pagado se puede descomponer como:

$$
No\ pagado = Reserva\ caso\ 40 + IBNR/IBNER\ 30
$$

La lectura es importante: el IBNR no es necesariamente todo lo no pagado. Si existe reserva caso, una parte del pasivo ya está reconocida en el incurrido.

## Buenas prácticas iniciales

Antes de aplicar métodos de desarrollo, conviene responder:

- ¿La fecha de origen representa ocurrencia, servicio, radicación o pago?
- ¿Los datos están netos o brutos de recuperaciones?
- ¿Hay cambios de codificación, red, contrato o mezcla de riesgo?
- ¿La reserva caso es consistente en el tiempo?
- ¿Existen pagos negativos, reversos, glosas o ajustes masivos?
- ¿Se están mezclando líneas de negocio con patrones distintos?
- ¿El periodo más reciente tiene suficiente madurez para extrapolar?

Estas preguntas evitan errores comunes: estimar sobre una base inconsistente, mezclar procesos distintos o interpretar como tendencia lo que en realidad es un cambio operativo.

## Relación con los siguientes capítulos

Este capítulo define el problema. Los siguientes capítulos explican cómo estructurar la información para estimarlo:

- construcción de triángulos;
- lags de desarrollo;
- triángulos incrementales y acumulados;
- factores edad-a-edad;
- métodos determinísticos, estocásticos y modelos estadísticos.

El punto de partida es simple: una reserva actuarial es una estimación del costo último pendiente de observar. La calidad de esa estimación depende de la calidad de la estructura de datos, del método seleccionado y del juicio aplicado.

## Siguiente capítulo

Continúa con [Construcción de triángulos](02-triangle-construction.md).

