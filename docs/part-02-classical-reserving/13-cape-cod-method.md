---
title: Método Cape Cod
description: Explicación del método Cape Cod para estimar pérdidas esperadas a partir de exposición y experiencia desarrollada, combinando exposición y desarrollo.
status: draft
version: "0.1.6"
chapter: "13"
part: "part-02-classical-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Método Cape Cod

El método Cape Cod es un método clásico que estima una pérdida esperada usando la propia experiencia histórica desarrollada y una medida de exposición. Puede verse como una forma de construir una expectativa previa para métodos como Bornhuetter-Ferguson, pero derivada de la experiencia del portafolio.

En salud, Cape Cod es útil cuando se dispone de exposición razonable, como meses-miembro, vidas aseguradas, primas devengadas, unidades de contrato o población cubierta.

## Idea central

Cape Cod estima una tasa esperada de pérdida o costo por exposición. Luego usa esa tasa para calcular la pérdida esperada de cada año de origen.

La lógica es:

$$
Pérdida\ esperada_i =
Exposición_i \times Tasa\ esperada
$$

La tasa esperada se estima a partir de experiencia histórica ajustada por desarrollo:

$$
Tasa\ esperada =
\frac{\sum_i Observado_i}
{\sum_i Exposición_i \times p_i}
$$

donde \(p_i\) es el porcentaje desarrollado del año de origen \(i\).

## Relación con Bornhuetter-Ferguson

BF requiere una pérdida esperada previa. Cape Cod puede proveer esa expectativa:

$$
E_i = Exposición_i \times Tasa\ Cape\ Cod
$$

Luego BF calcula:

$$
Ultimate^{BF}_i =
Observado_i + E_i \times (1 - p_i)
$$

Por eso Cape Cod no siempre se presenta como método aislado; muchas veces se usa para calibrar la expectativa previa.

## Componentes del método

Cape Cod necesita:

- observados acumulados;
- factores de desarrollo o porcentajes desarrollados;
- exposición por año de origen;
- selección de años incluidos;
- ajustes de tendencia o nivel de costo, si aplica.

En salud, la exposición debe elegirse con cuidado. Meses-miembro suele ser más informativo que número de pólizas si la permanencia varía.

## Porcentaje desarrollado

Igual que en BF:

$$
p_i = \frac{1}{CDF_i}
$$

Si un año está 60% desarrollado, su observado representa aproximadamente 60% del ultimate esperado.

Cape Cod ajusta la exposición por ese porcentaje:

$$
Exposición\ desarrollada_i =
Exposición_i \times p_i
$$

Esto evita comparar un año maduro con uno inmaduro como si tuvieran la misma cantidad de información.

## Ejemplo conceptual

Supongamos:

| Año | Observado | Exposición | % desarrollado |
| --- | ---: | ---: | ---: |
| 2022 | 900 | 1,000 | 100% |
| 2023 | 800 | 1,100 | 80% |
| 2024 | 500 | 1,200 | 50% |

La exposición desarrollada es:

$$
1,000 \times 1.00 + 1,100 \times 0.80 + 1,200 \times 0.50
= 2,480
$$

El observado total es:

$$
900 + 800 + 500 = 2,200
$$

La tasa Cape Cod es:

$$
\frac{2,200}{2,480} = 0.887
$$

La pérdida esperada para 2024 sería:

$$
1,200 \times 0.887 = 1,064
$$

## Ajuste por tendencia

Si los costos médicos crecen con el tiempo, la experiencia histórica debe ajustarse antes de estimar la tasa.

Una forma simple:

$$
Observado\ ajustado_i =
Observado_i \times (1 + t)^{n_i}
$$

También puede ajustarse la exposición o la tasa esperada. La clave es que todos los años queden en una base comparable.

Sin ajuste de tendencia, Cape Cod puede subestimar años recientes si los costos médicos aumentan.

## Cuándo usar Cape Cod

Cape Cod es útil cuando:

- hay exposición confiable;
- los años tienen distinta madurez;
- se quiere una pérdida esperada basada en experiencia propia;
- los años recientes son inmaduros;
- se necesita calibrar BF;
- se quiere estabilizar estimaciones en segmentos pequeños.

En salud, puede ser útil para comparar costo por miembro, costo por afiliado expuesto o costo por unidad contractual.

## Riesgos

Riesgos principales:

- exposición mal definida;
- mezcla de riesgo cambiante;
- tendencia médica no ajustada;
- inclusión de años atípicos;
- cambios de beneficio o cobertura;
- uso de experiencia inmadura sin ajuste correcto;
- segmentación insuficiente.

La tasa Cape Cod puede parecer objetiva, pero depende de decisiones de selección y ajuste.

## Comparación con Chain Ladder

Chain Ladder usa principalmente el patrón de desarrollo del observado. Cape Cod introduce exposición.

Si la exposición crece rápido, Chain Ladder puede interpretar crecimiento de volumen como crecimiento de siniestralidad. Cape Cod ayuda a separar volumen y costo esperado por unidad.

Sin embargo, si la exposición no captura la complejidad del riesgo, el método puede ser insuficiente. En salud, dos portafolios con los mismos meses-miembro pueden tener morbilidad muy distinta.

## Implementación mínima

```python
percent_developed = 1 / cdf
developed_exposure = exposure * percent_developed

cape_cod_rate = observed.sum() / developed_exposure.sum()

expected_loss = exposure * cape_cod_rate
bf_ibnr = expected_loss * (1 - percent_developed)
bf_ultimate = observed + bf_ibnr
```

La implementación debe permitir exclusiones, ajustes de tendencia y segmentación.

## Buenas prácticas

Para usar Cape Cod:

- definir exposición con precisión;
- revisar cambios de mix;
- ajustar tendencia si es material;
- excluir años atípicos con justificación;
- comparar contra Chain Ladder y BF externo;
- documentar sensibilidad de la tasa esperada;
- reconciliar con indicadores de costo por miembro.

Cape Cod es más útil cuando conecta reserving con exposición y pricing técnico.

## Capítulos relacionados

Anterior: [Método Benktander](12-benktander-method.md).  
Siguiente: [Comparación de métodos clásicos de reserving](14-classical-reserving-methods-comparison.md).

