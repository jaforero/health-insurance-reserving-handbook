---
title: Método Bornhuetter-Ferguson
description: Explicación del método Bornhuetter-Ferguson, que combina experiencia observada con una expectativa previa de pérdidas para estimar reservas.
status: draft
version: "0.1.6"
chapter: "11"
part: "part-02-classical-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Método Bornhuetter-Ferguson

Bornhuetter-Ferguson, usualmente abreviado BF, es un método clásico que combina dos fuentes de información: la experiencia observada y una expectativa previa de pérdidas. Es especialmente útil cuando los años de origen recientes tienen poca madurez y Chain Ladder puede ser demasiado sensible al desarrollo observado.

La idea central es no permitir que una observación temprana, posiblemente inestable, determine todo el ultimate. En cambio, BF reconoce lo observado y estima la parte no observada usando una expectativa previa.

## Intuición

Chain Ladder proyecta el observado:

$$
Ultimate^{CL} = Observado \times CDF
$$

Bornhuetter-Ferguson proyecta solo la parte no observada de una expectativa previa:

$$
Ultimate^{BF} =
Observado + ELR \times Exposición \times (1 - \%Desarrollado)
$$

donde:

- `ELR` es la razón esperada de pérdidas o costo esperado;
- `Exposición` puede ser prima, miembros, meses-miembro u otra base;
- `%Desarrollado` es la proporción del ultimate que se espera ya observada.

## Fórmula general

Si \(A_i\) es el monto observado para el año de origen \(i\), \(E_i\) es la pérdida esperada a priori y \(p_i\) es el porcentaje desarrollado, entonces:

$$
Ultimate^{BF}_i = A_i + E_i \times (1 - p_i)
$$

El IBNR es:

$$
IBNR^{BF}_i = E_i \times (1 - p_i)
$$

En base pagada, \(A_i\) puede ser pagado acumulado. En base incurrida, puede ser incurrido acumulado.

## Porcentaje desarrollado

El porcentaje desarrollado se deriva del factor acumulado hacia ultimate:

$$
p_i = \frac{1}{CDF_i}
$$

Si un año tiene un CDF de 2.0, se interpreta que está aproximadamente 50% desarrollado:

$$
p_i = \frac{1}{2.0} = 50\%
$$

Por tanto, BF asigna la pérdida esperada al porcentaje no desarrollado:

$$
1 - p_i
$$

## Pérdida esperada

La pérdida esperada puede estimarse con:

- prima devengada multiplicada por razón esperada de pérdida;
- exposición multiplicada por costo esperado por unidad;
- presupuesto técnico;
- tarifa esperada;
- experiencia ajustada por tendencia;
- benchmark externo;
- juicio actuarial documentado.

En salud, una base común puede ser:

$$
E_i = Meses\ miembro_i \times Costo\ esperado\ por\ miembro
$$

El costo esperado debe considerar tendencia médica, mezcla de riesgo, contrato, red y cambios regulatorios relevantes.

## Ejemplo conceptual

Supongamos:

- pagado observado: 100;
- CDF: 2.0;
- pérdida esperada: 180.

El porcentaje desarrollado es:

$$
p = \frac{1}{2.0} = 0.50
$$

La parte no desarrollada es:

$$
1 - p = 0.50
$$

Entonces:

$$
IBNR^{BF} = 180 \times 0.50 = 90
$$

$$
Ultimate^{BF} = 100 + 90 = 190
$$

Chain Ladder habría estimado:

$$
Ultimate^{CL} = 100 \times 2.0 = 200
$$

BF modera el resultado porque usa la expectativa previa para la parte no observada.

## Cuándo usar BF

BF es útil cuando:

- los años recientes tienen baja madurez;
- los datos observados son volátiles;
- existe una expectativa previa confiable;
- Chain Ladder produce resultados excesivamente sensibles;
- hay cambios de mix o exposición;
- el análisis necesita incorporar pricing, presupuesto o visión técnica previa.

En salud, BF puede ser apropiado para años recientes con pocos meses de desarrollo o para segmentos con baja credibilidad.

## Riesgos del método

BF depende de la calidad de la pérdida esperada. Si la expectativa previa está mal calibrada, el método puede dar una falsa sensación de estabilidad.

Riesgos frecuentes:

- usar una ELR desactualizada;
- no ajustar por tendencia médica;
- ignorar cambios de morbilidad;
- aplicar la misma expectativa a segmentos heterogéneos;
- no reconciliar contra experiencia observada;
- tratar BF como menos incierto solo porque es más estable.

La estabilidad no equivale a precisión.

## Comparación con Chain Ladder

Chain Ladder da más peso a la experiencia observada. BF da más peso a la expectativa previa, especialmente en años inmaduros.

Para años maduros, ambos métodos tienden a acercarse porque el porcentaje no desarrollado es pequeño. Para años recientes, la diferencia puede ser material.

Esto puede resumirse así:

| Situación | Chain Ladder | Bornhuetter-Ferguson |
| --- | --- | --- |
| Alta madurez | Muy útil | Similar a Chain Ladder |
| Baja madurez | Muy sensible | Más estable |
| Buena expectativa previa | No la usa directamente | La incorpora |
| Expectativa previa débil | No depende de ella | Riesgo alto |

## Implementación mínima

```python
percent_reported = 1 / cdf
expected_loss = exposure * expected_cost_per_unit
bf_ibnr = expected_loss * (1 - percent_reported)
bf_ultimate = observed + bf_ibnr
```

El reto no está en la fórmula. Está en definir una expectativa previa defendible y segmentada adecuadamente.

## Buenas prácticas

Para documentar BF:

- explicar fuente de pérdida esperada;
- mostrar exposición usada;
- justificar tendencia y ajustes;
- mostrar CDF y porcentaje desarrollado;
- comparar contra Chain Ladder;
- evaluar sensibilidad de ELR o costo esperado;
- documentar juicio profesional.

Un BF bien usado hace explícita la expectativa previa. Un BF mal usado solo oculta una selección subjetiva.

## Capítulos relacionados

Anterior: [Diagnósticos de Chain Ladder](07-chain-ladder-diagnostics.md).  
Siguiente: [Método Benktander](12-benktander-method.md).

