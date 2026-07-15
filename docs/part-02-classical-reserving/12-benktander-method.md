---
title: Método Benktander
description: Explicación del método Benktander como combinación iterativa entre Bornhuetter-Ferguson y Chain Ladder para estimar ultimate e IBNR.
status: draft
version: "0.1.6"
chapter: "12"
part: "part-02-classical-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Método Benktander

El método Benktander puede entenderse como un puente entre Bornhuetter-Ferguson y Chain Ladder. Usa una expectativa previa, como BF, pero permite que la experiencia observada gane más peso de forma gradual.

En términos prácticos, Benktander es útil cuando se quiere evitar la sensibilidad completa de Chain Ladder en años inmaduros, pero también se quiere que la experiencia observada influya más que en un BF puro.

## Intuición

Bornhuetter-Ferguson estima la parte no desarrollada usando una pérdida esperada previa:

$$
Ultimate^{BF} =
Observado + Esperado \times (1 - p)
$$

Chain Ladder estima ultimate proyectando lo observado:

$$
Ultimate^{CL} =
\frac{Observado}{p}
$$

Benktander combina ambas ideas. Parte de una expectativa previa y la actualiza con el desarrollo observado.

## Fórmula de primer orden

Una forma común de expresar Benktander es:

$$
Ultimate^{B}_i =
Observado_i + Ultimate^{BF}_i \times (1 - p_i)
$$

donde:

- \(Observado_i\) es el monto acumulado observado;
- \(Ultimate^{BF}_i\) es el ultimate estimado por BF;
- \(p_i\) es el porcentaje desarrollado.

Esta expresión genera una estimación entre BF y Chain Ladder, dependiendo de la madurez.

## Interpretación como credibilidad

Benktander puede verse como una forma de dar credibilidad parcial a la experiencia observada. Cuando el año de origen es inmaduro, la expectativa previa conserva peso. Cuando gana madurez, el observado tiene mayor influencia.

En términos conceptuales:

$$
Ultimate^{B} =
w \times Ultimate^{CL} + (1 - w) \times Ultimate^{BF}
$$

donde el peso \(w\) aumenta con la madurez. La fórmula exacta puede variar según la implementación, pero la intuición es la misma: combinar desarrollo observado y expectativa previa.

## Relación con BF

BF usa la expectativa previa para la parte no observada. Benktander toma el resultado BF y lo vuelve a desarrollar parcialmente. Por eso suele quedar más cerca de Chain Ladder que BF, pero no tan sensible como Chain Ladder puro.

Para años muy inmaduros:

- Chain Ladder puede ser inestable;
- BF puede ser demasiado dependiente de la expectativa previa;
- Benktander puede ofrecer una transición intermedia.

## Ejemplo conceptual

Supongamos:

- observado: 100;
- CDF: 2.0;
- porcentaje desarrollado: 50%;
- pérdida esperada: 180.

BF:

$$
Ultimate^{BF} =
100 + 180 \times 0.50 = 190
$$

Benktander:

$$
Ultimate^{B} =
100 + 190 \times 0.50 = 195
$$

Chain Ladder:

$$
Ultimate^{CL} =
100 \times 2.0 = 200
$$

En este ejemplo, Benktander queda entre BF y Chain Ladder.

## Cuándo usar Benktander

Benktander puede ser útil cuando:

- existe expectativa previa razonable;
- los años recientes tienen baja madurez;
- Chain Ladder parece demasiado sensible;
- BF parece demasiado conservador o demasiado rígido;
- se busca una transición gradual hacia experiencia observada;
- se quiere comparar varios métodos clásicos.

En salud, puede ser útil para segmentos donde existe presupuesto técnico o costo esperado, pero también se quiere reconocer la experiencia emergente del año.

## Riesgos

El método comparte riesgos con BF y Chain Ladder:

- si la expectativa previa es débil, el resultado también lo será;
- si los factores de desarrollo están contaminados, la transición hacia Chain Ladder hereda ese sesgo;
- si se aplica mecánicamente, puede parecer más sofisticado sin agregar mejor juicio;
- puede ser difícil de comunicar si no se explica la intuición.

Benktander no elimina incertidumbre. Solo cambia el balance entre expectativa previa y experiencia observada.

## Comparación de métodos

Una práctica útil es mostrar una tabla por año de origen:

| Año origen | Chain Ladder | BF | Benktander |
| --- | ---: | ---: | ---: |
| 2023 | 210 | 200 | 205 |
| 2024 | 230 | 215 | 222 |
| 2025 | 250 | 220 | 235 |

Si Benktander está sistemáticamente cerca de Chain Ladder, la experiencia observada domina. Si está cerca de BF, la expectativa previa domina.

## Implementación mínima

```python
percent_reported = 1 / cdf

expected_loss = exposure * expected_cost_per_unit
bf_ultimate = observed + expected_loss * (1 - percent_reported)

benktander_ultimate = observed + bf_ultimate * (1 - percent_reported)
benktander_ibnr = benktander_ultimate - observed
```

Esta implementación debe acompañarse de sensibilidad en `expected_cost_per_unit` y en factores de desarrollo.

## Uso en reportes

Benktander suele ser útil en reportes comparativos, no necesariamente como único método final. Puede mostrar cómo cambia la estimación al dar más peso a experiencia observada.

Un reporte puede presentar:

- Chain Ladder como método basado en experiencia;
- BF como método basado en expectativa previa;
- Benktander como método intermedio;
- selección final como juicio documentado.

## Buenas prácticas

Para usar Benktander:

- documentar expectativa previa;
- mostrar porcentaje desarrollado;
- comparar contra BF y Chain Ladder;
- explicar por qué se requiere método intermedio;
- evaluar sensibilidad;
- evitar selección automática sin criterio.

El valor del método está en su interpretación, no en su complejidad.

## Capítulos relacionados

Anterior: [Bornhuetter-Ferguson](11-bornhuetter-ferguson.md).  
Siguiente: [Método Cape Cod](13-cape-cod-method.md).

