---
title: Factores edad-a-edad
description: Introducción a los factores de desarrollo edad-a-edad, su cálculo, selección, diagnóstico y uso en métodos Chain Ladder para reservas de salud.
status: draft
version: "0.1.5"
chapter: "05"
part: "part-01-foundations"
language: "es"
last_updated: "2026-07-14"
---

# Factores edad-a-edad

Los factores edad-a-edad miden cómo crece una medida acumulada entre una edad de desarrollo y la siguiente. Son la base de muchos métodos determinísticos de reserving, especialmente Chain Ladder.

Un factor edad-a-edad responde una pregunta concreta: dado lo observado a cierta edad, ¿cuánto esperamos observar en la edad siguiente?

## Definición

Sea $C_{i,j}$ el valor acumulado para el periodo de origen $i$ a edad de desarrollo $j$. El factor observado entre $j$ y $j+1$ es:

$$
f_{i,j} = \frac{C_{i,j+1}}{C_{i,j}}
$$

Si $C_{i,j}$ es cero o no está observado, el factor no debe calcularse sin análisis adicional.

Ejemplo:

| Año origen | dev_0 | dev_1 | Factor 0-1 |
| --- | ---: | ---: | ---: |
| 2022 | 100 | 150 | 1.500 |
| 2023 | 120 | 168 | 1.400 |
| 2024 | 130 |  |  |

El año 2024 no tiene factor 0-1 porque falta la observación en `dev_1`.

## Factor ponderado por volumen

Una forma común de seleccionar el factor para una edad es usar el promedio ponderado por volumen:

$$
f_j =
\frac{\sum_i C_{i,j+1}}{\sum_i C_{i,j}}
$$

Este enfoque da más peso a años de origen con mayor volumen. Es frecuente en Chain Ladder porque evita que años pequeños dominen la selección.

## Promedio simple

Otra opción es el promedio simple de factores individuales:

$$
f_j =
\frac{1}{n}\sum_i f_{i,j}
$$

Este enfoque da el mismo peso a cada año de origen. Puede ser útil cuando los años tienen volúmenes comparables, pero puede ser inestable si hay años pequeños con factores extremos.

## Mediana y selecciones robustas

La mediana reduce sensibilidad a valores atípicos:

$$
f_j = Mediana(f_{i,j})
$$

También pueden usarse promedios recortados, exclusión de años atípicos o selecciones por juicio actuarial. La selección debe documentarse, especialmente si se excluyen observaciones.

## Factor acumulado hacia ultimate

Los factores edad-a-edad se combinan para proyectar desde una edad observada hasta ultimate.

Si un año de origen tiene última edad observada $k$, el factor acumulado hacia ultimate es:

$$
CDF_k = \prod_{j=k}^{J-1} f_j
$$

La estimación de ultimate es:

$$
Ultimate_i = C_{i,k} \times CDF_k
$$

Y el IBNR sobre esa base es:

$$
IBNR_i = Ultimate_i - C_{i,k}
$$

## Ejemplo numérico

Supongamos estos factores seleccionados:

| Edad | Factor |
| --- | ---: |
| 0-1 | 1.50 |
| 1-2 | 1.20 |
| 2-3 | 1.05 |

Si un año de origen tiene observado 100 en edad 1, su CDF hacia ultimate es:

$$
CDF_1 = 1.20 \times 1.05 = 1.26
$$

Entonces:

$$
Ultimate = 100 \times 1.26 = 126
$$

$$
IBNR = 126 - 100 = 26
$$

## Diagnóstico de factores

Antes de seleccionar factores, conviene revisar:

- tendencia por año de origen;
- volatilidad por edad;
- factores menores que 1;
- años de origen con volumen pequeño;
- celdas afectadas por cambios calendario;
- diferencias entre pagado e incurrido;
- cambios de mezcla de riesgo;
- impactos de alto costo.

Un factor no es solo un número. Es una síntesis de comportamiento histórico bajo supuestos de estabilidad.

## Factores menores que 1

Un factor menor que 1 indica que el acumulado disminuyó entre edades. Esto puede ocurrir por:

- recuperaciones;
- reversos;
- glosas;
- reclasificaciones;
- ajustes contables;
- datos netos de recuperaciones.

No debe descartarse automáticamente, pero debe entenderse. En muchos contextos de pagos brutos, un acumulado decreciente puede indicar problema de datos o definición.

## Selección por base pagada e incurrida

Los factores sobre base pagada e incurrida suelen ser diferentes.

La base pagada puede tener factores más altos en edades tempranas porque los pagos emergen lentamente. La base incurrida puede tener factores más cercanos a 1 porque la reserva caso anticipa parte del costo.

Esto no significa que la base incurrida siempre sea superior. Si la reserva caso es inconsistente, sus factores pueden ser engañosos.

## Sensibilidad

Pequeños cambios en factores tempranos pueden producir impactos grandes en años inmaduros. Por eso la selección debe evaluarse con sensibilidad.

Una práctica útil es comparar:

- promedio ponderado por volumen;
- promedio simple;
- últimos tres años;
- exclusión de años atípicos;
- selección manual documentada.

La diferencia entre escenarios muestra cuánto juicio hay en la estimación.

## Relación con Chain Ladder

Chain Ladder asume que el patrón histórico de desarrollo es razonablemente aplicable a los años de origen inmaduros. Los factores edad-a-edad son la forma práctica de trasladar ese patrón.

El método es potente por su simplicidad, pero sus supuestos deben revisarse:

- estabilidad de mezcla;
- estabilidad operativa;
- datos completos;
- exposición comparable;
- ausencia de efectos calendario dominantes;
- desarrollo suficientemente maduro en años históricos.

Si estos supuestos no se sostienen, puede ser necesario ajustar los datos, segmentar o usar métodos alternativos.

## Ejemplo mínimo en Python

Una forma directa de calcular factores ponderados por volumen es:

```python
factors = {}

for age in development_ages[:-1]:
    current = cumulative_triangle[age]
    next_age = cumulative_triangle[age + 1]

    valid = current.notna() & next_age.notna() & (current > 0)

    factors[age] = next_age[valid].sum() / current[valid].sum()
```

El cálculo debe ir acompañado de validaciones. No basta con producir el diccionario de factores.

## Buenas prácticas

Para documentar una selección de factores:

- indicar base usada: pagada, incurrida u otra;
- describir periodo histórico;
- mostrar factores observados;
- explicar exclusiones;
- justificar selección final;
- cuantificar sensibilidad;
- reconciliar impacto en ultimate e IBNR;
- registrar limitaciones.

Una selección de factores defendible debe poder ser revisada por otra persona y reproducida con los mismos datos.

## Cierre de la Parte 1

Con estos conceptos, la base de reserving queda definida:

- qué es IBNR;
- cómo se construye un triángulo;
- qué representan los lags;
- cómo se relacionan incrementales y acumulados;
- cómo se calculan factores de desarrollo.

Los siguientes capítulos usan esta base para introducir métodos clásicos, estocásticos, estadísticos y modelos aplicados a salud.

## Capítulo relacionado

Anterior: [Triángulos incrementales vs. acumulados](04-incremental-vs-cumulative-triangles.md).

