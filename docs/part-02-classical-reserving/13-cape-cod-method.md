---
title: "Método Cape Cod"
description: "Estimación Cape Cod basada en exposición, madurez, tendencia y reconciliación para reservas de seguros de salud."
chapter: "13"
part: "02-classical-reserving"
language: "es"
status: "review"
version: "0.6.0"
last_updated: "2026-07-17"
tags:
  - cape-cod
  - exposicion
  - chain-ladder
  - ibnr
  - salud
---

# Método Cape Cod

## 1. Propósito

Cape Cod combina un patrón de desarrollo con exposición. A diferencia de Bornhuetter-Ferguson, la tasa esperada se estima a partir de la experiencia agregada disponible, ajustada por la proporción desarrollada.

El método puede estabilizar periodos recientes cuando la exposición es relevante, comparable y correctamente nivelada. También puede ocultar heterogeneidad si se agrupan cohortes con tasas de costo estructuralmente diferentes.

## 2. Notación

Para cada origen $i$:

- $C_i$: acumulado observado;
- $E_i$: exposición;
- $a_i$: factor de ajuste a una base común;
- $E_i^* = E_i a_i$: exposición ajustada;
- $p_i$: proporción desarrollada;
- $q_i = 1-p_i$: proporción no desarrollada;
- $r$: tasa última esperada estimada por Cape Cod;
- $U_i^{CC}$: ultimate Cape Cod;
- $R_i^{CC}$: IBNR Cape Cod.

La exposición y la tasa deben compartir unidad. Por ejemplo, miembros-mes por costo esperado por miembro-mes produce un importe.

## 3. Preparación de exposición

El factor $a_i$ lleva cada origen a una base comparable y puede incluir, cuando corresponda:

- tendencia médica;
- nivel tarifario o contractual;
- cambios de beneficio;
- mezcla de población, producto, región o red;
- moneda e inflación;
- reaseguro, recuperaciones o grandes reclamaciones.

Los componentes deben documentarse por separado. No se recomienda usar un único factor opaco cuyo efecto no pueda reconciliarse.

## 4. Estimación de la tasa

La exposición desarrollada equivalente es $E_i^* p_i$. La tasa Cape Cod básica es:

$$
r = \frac{\sum_i C_i}{\sum_i E_i^* p_i}
$$

El denominador debe ser positivo y material. La fórmula supone que una tasa común, después de ajustes, representa los orígenes incluidos.

El ultimate por origen es:

$$
U_i^{CC} = C_i + q_i E_i^* r
$$

La reserva es:

$$
R_i^{CC} = q_i E_i^* r
$$

La forma de credibilidad equivalente es:

$$
U_i^{CC} = p_i U_i^{CL} + q_i E_i^* r
$$

## 5. Ejemplo numérico

Considere tres orígenes ya expresados en una base común:

| Origen | Exposición $E_i^*$ | Madurez $p_i$ | Observado $C_i$ | Exposición desarrollada $E_i^*p_i$ |
|---|---:|---:|---:|---:|
| A | 1,000 | 0.90 | 90 | 900 |
| B | 1,200 | 0.70 | 84 | 840 |
| C | 1,400 | 0.40 | 56 | 560 |
| **Total** | **3,600** |  | **230** | **2,300** |

La tasa estimada es:

$$
r = \frac{230}{2300} = 0.10
$$

| Origen | IBNR $q_iE_i^*r$ | Ultimate |
|---|---:|---:|
| A | 10 | 100 |
| B | 36 | 120 |
| C | 84 | 140 |
| **Total** | **130** | **360** |

El ejemplo es sintético y fue construido para facilitar la reconciliación; no es una selección de tasa para uso profesional.

## 6. Ventana de experiencia y ponderación

La selección de orígenes influye en $r$. Deben compararse:

- toda la historia comparable;
- ventanas recientes;
- exclusiones justificadas;
- segmentos homogéneos;
- escenarios con y sin grandes reclamaciones.

Puede incorporarse un peso $w_i$ definido antes del cálculo:

$$
r_w = \frac{\sum_i w_i C_i}{\sum_i w_i E_i^* p_i}
$$

El peso no debe duplicar ajustes ya incluidos en exposición ni emplearse para forzar una cifra.

## 7. Diferencia frente a Bornhuetter-Ferguson

| Elemento | Bornhuetter-Ferguson | Cape Cod |
|---|---|---|
| tasa o ultimate esperado | externo o definido previamente | estimado con experiencia del grupo |
| dependencia del observado | usa el observado para madurez y suma el IBNR | usa el observado también para estimar $r$ |
| fortaleza | incorpora una expectativa independiente | obtiene una tasa coherente con experiencia agregada |
| riesgo | prior no comparable o sesgado | circularidad, heterogeneidad y ventana inadecuada |

Cape Cod no reemplaza automáticamente a BF. La elección depende de la calidad de la exposición, la independencia deseada y la homogeneidad del portafolio.

## 8. Diagnósticos

### 8.1 Exposición

Se valida:

- completitud por origen;
- unidad y periodo de cobertura;
- conciliación con sistemas de afiliación o pólizas;
- consistencia de ajustes y tendencia;
- valores cero, negativos, faltantes o duplicados;
- cambios de mezcla no capturados.

### 8.2 Patrón

La madurez procede de Chain Ladder y requiere los diagnósticos del capítulo 7. Un patrón inestable sesga tanto el denominador de $r$ como la porción pendiente.

### 8.3 Tasa

Se compara $r$ por ventana, segmento y escenario. También se evalúan tasas implícitas maduras:

$$
r_i^{implícita} = \frac{C_i}{E_i^*p_i}
$$

La dispersión o tendencia sistemática de estas tasas puede indicar que una tasa común no es apropiada.

### 8.4 Backtesting

En cada corte retrospectivo se recalculan patrón, exposición ajustada y tasa usando solo información disponible. El resultado se compara con pagos o ultimate emergente sin fuga de información.

## 9. Contrato de implementación para v0.6.0

El incremento propuesto para Demo 6 debe:

- reutilizar el patrón validado de Chain Ladder;
- aceptar exposición por origen y factores de ajuste trazables;
- estimar la tasa con una ventana configurable;
- bloquear denominadores no positivos o periodos no conciliados;
- producir tasa, exposición desarrollada, ultimate e IBNR por origen;
- comparar Cape Cod con Chain Ladder, BF y Benktander;
- exportar entradas normalizadas, configuración, resultados, sensibilidad y diagnósticos;
- incluir pruebas numéricas y de reconciliación.

Hasta integrar el código y sus pruebas, este capítulo es una especificación técnica, no una funcionalidad declarada del demo.

## 10. Limitaciones

Cape Cod puede fallar cuando:

- la exposición no mide el riesgo subyacente;
- la tasa cambia estructuralmente entre orígenes;
- los ajustes de tendencia o beneficio son incompletos;
- grandes reclamaciones dominan la experiencia;
- la misma experiencia se usa para seleccionar múltiples supuestos sin control;
- el patrón de desarrollo no es estable;
- la ventana se selecciona después de observar el resultado.

El método determinístico no produce por sí solo una distribución predictiva.

## 11. Referencias y alcance profesional

- [Diagnósticos de Chain Ladder](07-chain-ladder-diagnostics.md)
- [Bornhuetter-Ferguson](11-bornhuetter-ferguson.md)
- [Benktander](12-benktander-method.md)
- [Comparación de métodos clásicos](14-classical-reserving-methods-comparison.md)
- [Exposición, utilización y severidad en salud](../part-06-health-specific/23-health-exposure-utilization-and-severity.md)
- [Bibliografía y evidencia](../bibliography.md)

La especificación se apoya principalmente en `FRIEDLAND-2010` y en los principios de propósito, datos, supuestos, validación y documentación de `ASB-ASOP01-2013`, `ASB-ASOP28-2024` y `ASB-ASOP56-2019`. Debe complementarse con la regulación colombiana y la política interna vigentes a la fecha de valuación.
