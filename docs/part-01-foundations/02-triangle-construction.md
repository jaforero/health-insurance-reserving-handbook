---
title: Construcción de triángulos
description: Guía práctica para construir triángulos actuariales de desarrollo a partir de datos de reclamaciones, definiendo origen, desarrollo, valuación y medidas acumuladas.
status: draft
version: "0.1.5"
chapter: "02"
part: "part-01-foundations"
language: "es"
last_updated: "2026-07-14"
---

# Construcción de triángulos

Un triángulo de desarrollo organiza la experiencia histórica por periodo de origen y edad de desarrollo. Es una de las estructuras más usadas en reserving porque muestra, en una sola tabla, cuánto se ha observado para cada cohorte y qué parte sigue pendiente de madurar.

En salud, los triángulos permiten estudiar pagos, incurridos, reclamaciones reportadas, número de servicios, severidad, glosas, autorizaciones o cualquier medida que se desarrolle con el tiempo. La estructura es la misma; lo que cambia es la variable de análisis.

## Estructura básica

Un triángulo tiene:

- filas: años o periodos de origen;
- columnas: edades de desarrollo;
- celdas: valor observado para una combinación de origen y desarrollo.

Por ejemplo, en un triángulo anual:

| Año de origen | dev_0 | dev_1 | dev_2 | dev_3 |
| --- | ---: | ---: | ---: | ---: |
| 2022 | 100 | 150 | 175 | 185 |
| 2023 | 110 | 165 | 190 |  |
| 2024 | 130 | 180 |  |  |
| 2025 | 140 |  |  |  |

La diagonal observada está formada por las últimas celdas disponibles para cada año de origen. Las celdas vacías corresponden a desarrollo futuro no observado.

## Definir el periodo de origen

La primera decisión es definir qué significa “origen”. En salud, puede ser:

- fecha de servicio;
- fecha de admisión;
- fecha de egreso;
- fecha de radicación;
- fecha de autorización;
- fecha de factura;
- fecha contable.

La elección depende del objetivo. Para estimar costo de servicios ya prestados, la fecha de servicio o egreso suele ser más cercana al concepto de ocurrencia. Para análisis operativo de facturación, la fecha de radicación puede ser útil, pero no mide exactamente el mismo riesgo.

Un error frecuente es mezclar definiciones. Por ejemplo, usar fecha de servicio para algunos registros y fecha de pago para otros produce patrones de desarrollo artificiales.

## Definir la edad de desarrollo

La edad de desarrollo mide cuánto tiempo ha pasado desde el periodo de origen hasta el periodo de observación. Si el origen es anual y la valuación también es anual:

$$
Edad\ de\ desarrollo = Año\ de\ valuación - Año\ de\ origen
$$

Si el origen es mensual, la edad se mide en meses:

$$
Edad\ de\ desarrollo = Mes\ de\ valuación - Mes\ de\ origen
$$

La granularidad debe balancear estabilidad y sensibilidad:

- mensual: más detalle, más volatilidad;
- trimestral: balance útil en muchos portafolios;
- anual: más estable, pero menos sensible a cambios recientes.

## Formato largo antes del triángulo

Antes de construir el triángulo, conviene tener una tabla en formato largo:

| origen | desarrollo | medida |
| --- | ---: | ---: |
| 2022 | 0 | 100 |
| 2022 | 1 | 150 |
| 2022 | 2 | 175 |
| 2023 | 0 | 110 |
| 2023 | 1 | 165 |

Este formato es más fácil de auditar, filtrar y agregar. El triángulo es una tabla pivote de esa base.

La transformación conceptual es:

$$
Triángulo_{i,j} = \sum Medida\ para\ origen\ i\ y\ desarrollo\ j
$$

## Medidas frecuentes

Los triángulos pueden construirse sobre diferentes medidas:

- pagos incrementales;
- pagos acumulados;
- incurrido acumulado;
- reserva caso;
- número de reclamaciones reportadas;
- número de servicios;
- monto glosado;
- monto autorizado;
- costo por miembro;
- costo por servicio.

No todas las medidas sirven para el mismo método. Chain Ladder, por ejemplo, suele aplicarse sobre acumulados no decrecientes o razonablemente estables. Si una medida puede disminuir por reversos o ajustes, debe analizarse con cuidado.

## Agregación y segmentación

La segmentación correcta es crítica. Un triángulo demasiado agregado puede ocultar patrones distintos; uno demasiado granular puede ser inestable.

Segmentaciones útiles en salud incluyen:

- régimen, línea o producto;
- tipo de servicio;
- red o contrato;
- zona geográfica;
- tipo de prestador;
- canal de autorización;
- población de alto costo;
- grupos de morbilidad.

La regla práctica es separar segmentos cuando tengan patrones de desarrollo materialmente diferentes y suficiente volumen para estimar.

## Diagonal y madurez

El triángulo observado siempre está limitado por una diagonal. Para un año de valuación fijo, los años de origen recientes tienen menor desarrollo.

La madurez puede expresarse como:

$$
Madurez_i = \frac{Pago\ acumulado\ observado_i}{Ultimate\ estimado_i}
$$

Un año con baja madurez tendrá mayor dependencia de supuestos de desarrollo. Por eso los años recientes suelen concentrar la mayor incertidumbre de reservas.

## Control de calidad del triángulo

Antes de modelar, deben revisarse controles básicos:

- celdas faltantes inesperadas;
- pagos negativos o reversos;
- saltos abruptos por cambios operativos;
- duplicados;
- cambios de codificación;
- diferencias entre bruto y neto;
- mezcla de monedas o unidades;
- inconsistencias entre pagado, incurrido y reserva caso;
- diagonales que no coinciden con la fecha de corte.

Un triángulo puede estar técnicamente construido y aun así ser inapropiado para estimar. La calidad actuarial depende de entender qué representa cada celda.

## Ejemplo reproducible mínimo

La lógica básica en Python es una agregación y pivote:

```python
triangle = (
    claims
    .groupby(["origin_year", "development_age"])["paid_amount"]
    .sum()
    .reset_index()
    .pivot(
        index="origin_year",
        columns="development_age",
        values="paid_amount",
    )
)
```

El código es simple; las decisiones importantes están antes del código: fecha de origen, medida, segmentación, filtros y consistencia de datos.

## Buenas prácticas

Un triángulo de reserving debe ser:

- reproducible desde datos fuente;
- consistente con la fecha de valuación;
- documentado en su definición de origen y desarrollo;
- separado por segmentos cuando sea necesario;
- revisado contra reportes contables u operativos;
- estable en su metodología de construcción a través del tiempo.

La construcción del triángulo es una etapa actuarial, no solo una tarea de ingeniería de datos.

## Capítulos relacionados

Anterior: [IBNR y reservas](01-ibnr-and-reserving.md).  
Siguiente: [Lags de desarrollo y transformaciones de triángulos](03-development-lags-and-triangle-transformations.md).

