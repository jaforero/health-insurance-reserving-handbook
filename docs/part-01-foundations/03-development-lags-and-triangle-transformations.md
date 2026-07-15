---
title: Lags de desarrollo y transformaciones de triángulos
description: Explicación de rezagos de desarrollo, calendarios de observación y transformaciones necesarias para preparar triángulos actuariales consistentes.
status: draft
version: "0.1.5"
chapter: "03"
part: "part-01-foundations"
language: "es"
last_updated: "2026-07-14"
---

# Lags de desarrollo y transformaciones de triángulos

El desarrollo de reclamaciones no ocurre instantáneamente. Entre la fecha de origen y la observación final pueden existir múltiples rezagos: prestación del servicio, radicación, auditoría, registro, pago, ajuste y cierre. Estos rezagos determinan la forma del triángulo y condicionan la selección del método actuarial.

Un lag de desarrollo es la distancia temporal entre el periodo de origen y el periodo en que se observa una medida. En reserving, entender los lags es tan importante como calcular factores.

## Tipos de lag

En salud, los principales lags incluyen:

- `lag de reporte`: tiempo entre servicio y radicación o registro;
- `lag de adjudicación`: tiempo entre radicación y aceptación o liquidación;
- `lag de pago`: tiempo entre liquidación y desembolso;
- `lag de auditoría`: tiempo asociado a revisión médica o administrativa;
- `lag de glosa`: tiempo hasta objeción, conciliación o reverso;
- `lag contable`: tiempo hasta reconocimiento en estados financieros.

Cada lag afecta una medida distinta. Un triángulo pagado está dominado por el lag de pago; un triángulo incurrido depende también de la oportunidad y suficiencia de reservas caso.

## Calendario de origen, valuación y desarrollo

Un registro de reclamación puede tener varias fechas:

| Fecha | Uso posible |
| --- | --- |
| Fecha de servicio | Aproxima ocurrencia del costo médico |
| Fecha de admisión | Útil para hospitalizaciones |
| Fecha de egreso | Útil cuando el costo se cierra al alta |
| Fecha de radicación | Mide proceso de facturación |
| Fecha de auditoría | Mide proceso operativo |
| Fecha de pago | Mide flujo de caja |
| Fecha contable | Mide reconocimiento financiero |

La edad de desarrollo se calcula comparando una fecha de observación contra una fecha de origen. Si esas fechas no están definidas de forma estable, el triángulo pierde interpretación.

## Triángulo por año calendario

La celda de un triángulo puede verse como una combinación de tres dimensiones:

$$
Año\ calendario = Año\ de\ origen + Edad\ de\ desarrollo
$$

Por ejemplo, el pago para origen 2023 y desarrollo 1 ocurre en año calendario 2024 si la medición es anual.

Esta identidad permite revisar efectos calendario. Un cambio regulatorio, una pandemia, un ajuste contable o un cambio de sistema puede afectar muchas celdas alineadas por año calendario, no por año de origen.

## Transformaciones comunes

Antes de aplicar métodos, es frecuente transformar triángulos.

### De incremental a acumulado

Si $X_{i,j}$ es el valor incremental del origen $i$ en desarrollo $j$, el acumulado es:

$$
C_{i,j} = \sum_{k=0}^{j} X_{i,k}
$$

Esta transformación se usa porque muchos métodos de desarrollo trabajan sobre acumulados.

### De acumulado a incremental

Si $C_{i,j}$ es acumulado, el incremental es:

$$
X_{i,j} = C_{i,j} - C_{i,j-1}
$$

con:

$$
X_{i,0} = C_{i,0}
$$

El incremental ayuda a revisar calendarios, estacionalidad, pagos negativos y cambios operativos.

### Normalización por exposición

En salud, el volumen cambia por crecimiento de afiliados, mezcla de riesgo o cambios de cobertura. Por eso puede ser útil analizar tasas:

$$
Costo\ por\ exposición_{i,j} =
\frac{Monto_{i,j}}{Meses\ miembro_i}
$$

La normalización no reemplaza el triángulo monetario, pero ayuda a distinguir crecimiento real de crecimiento por volumen.

### Ajuste por tendencia

Si hay inflación médica o tendencia de severidad, los periodos antiguos pueden no ser comparables con los recientes. Un ajuste simple puede llevar montos a nivel de costo actual:

$$
Monto\ ajustado_{i,j} = Monto_{i,j} \times (1 + t)^{n}
$$

donde $t$ es una tasa de tendencia y $n$ es el número de periodos de actualización.

Este ajuste debe usarse con cuidado: si se aplica tendencia y luego se seleccionan factores sin considerar el ajuste, se puede duplicar o distorsionar el efecto.

## Diagonales y cortes de información

La diagonal observada depende de la fecha de corte. Si la fecha de valuación cambia, cambia la diagonal. Un error común es comparar triángulos de distintas valuaciones sin controlar el corte.

Para una valuación anual a 2025:

| Año origen | Última edad observada |
| --- | ---: |
| 2021 | 4 |
| 2022 | 3 |
| 2023 | 2 |
| 2024 | 1 |
| 2025 | 0 |

Los periodos recientes tienen menor madurez. Por eso su estimación depende más del patrón de desarrollo seleccionado.

## Efectos calendario

Un efecto calendario ocurre cuando varios años de origen se ven afectados en el mismo año de observación. Ejemplos:

- cambio de sistema de pagos;
- nueva política de auditoría;
- reforma regulatoria;
- choque de utilización;
- acumulación o limpieza de cuentas pendientes;
- migración de red;
- cambios en codificación o facturación.

En el triángulo, estos efectos aparecen en diagonales o bandas calendario. Si se ignoran, pueden contaminar los factores de desarrollo.

## Diagnóstico visual

Antes de modelar, conviene revisar:

- incrementales por año calendario;
- acumulados por año de origen;
- factores implícitos por edad;
- heatmaps de celdas atípicas;
- comparación pagado vs incurrido;
- desarrollo por segmento.

El objetivo no es producir gráficos decorativos. El objetivo es detectar si el triángulo cumple los supuestos básicos del método.

## Ejemplo conceptual

Si un cambio operativo acelera pagos en 2024, las celdas observadas durante 2024 pueden verse más altas. Si esas celdas se usan sin ajuste, los factores pueden sugerir falsamente que el desarrollo futuro será más rápido para todos los años.

El actuario debe decidir si:

- excluye celdas atípicas;
- ajusta los montos;
- segmenta el periodo;
- selecciona factores manualmente;
- usa un método alternativo.

La transformación correcta depende de la causa del patrón observado.

## Buenas prácticas

Una transformación debe documentarse con:

- motivo;
- fórmula;
- datos afectados;
- impacto esperado;
- sensibilidad del resultado;
- versión reproducible del código o cálculo.

No debe transformarse un triángulo solo para que “se vea mejor”. La transformación debe mejorar la comparabilidad o la interpretación actuarial.

## Capítulos relacionados

Anterior: [Construcción de triángulos](02-triangle-construction.md).  
Siguiente: [Triángulos incrementales vs. acumulados](04-incremental-vs-cumulative-triangles.md).

