---
title: "Bootstrap Chain Ladder"
part: "Parte III · Reserving estocástico"
chapter: 9
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

09-bootstrap-chain-ladder.md
---

title: Bootstrap Chain Ladder
subtitle: Simulación estocástica de reservas, distribución predictiva e incertidumbre
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 09
status: Draft
last_updated: 2026-07-14
language: es
tags:

* IBNR
* reserving
* bootstrap
* chain ladder
* stochastic reserving
* prediction error
* health insurance

---

# Bootstrap Chain Ladder

> Chain Ladder produce una estimación puntual. Bootstrap Chain Ladder transforma esa estimación en una distribución predictiva de reservas posibles.

---

## Objetivos de aprendizaje

Al finalizar este capítulo, el lector podrá:

* explicar la motivación del Bootstrap Chain Ladder;
* diferenciar incertidumbre de parámetros y riesgo de proceso;
* formular Chain Ladder como un modelo de Poisson sobredispersado;
* calcular valores ajustados y residuos;
* corregir residuos por grados de libertad;
* generar pseudo-triángulos;
* reestimar factores de desarrollo en cada simulación;
* simular pagos futuros;
* construir distribuciones de ultimate e IBNR;
* calcular percentiles, VaR, TVaR y coeficientes de variación;
* validar la estabilidad del procedimiento;
* reconocer cuándo Bootstrap no es apropiado;
* implementar el método en Python y R.

---

## Contenido

1. Introducción
2. Motivación
3. Qué problema resuelve
4. Relación con Chain Ladder
5. Fuentes de incertidumbre
6. Formulación ODP
7. Triángulo incremental y valores ajustados
8. Residuos de Pearson
9. Ajuste de residuos
10. Algoritmo Bootstrap
11. Simulación del riesgo de proceso
12. Distribución predictiva de reservas
13. Métricas de riesgo
14. Ejemplo conceptual
15. Diagnósticos
16. Selección del número de simulaciones
17. Tratamiento de valores negativos
18. Tail factor
19. Dependencia y efectos calendario
20. Aplicación en salud
21. Comparación con Mack
22. Implementación en Python
23. Implementación en R
24. Pseudocódigo de producción
25. Validación y backtesting
26. Gobierno del modelo
27. Errores comunes
28. Ventajas y limitaciones
29. Checklist
30. Conclusiones
31. Referencias

---

## 1. Introducción

El Chain Ladder determinístico estima el costo último mediante patrones históricos de desarrollo.

Para el periodo de origen (i):

[
\widehat U_i
============

C_{i,k_i}
\prod_{j=k_i}^{J-1}
\widehat f_j
]

y la reserva es:

[
\widehat R_i
============

\widehat U_i-C_{i,k_i}
]

Este resultado no informa directamente:

* cuán variable puede ser la reserva;
* si la distribución es simétrica;
* cuál es el percentil 75, 95 o 99;
* cuál es la probabilidad de superar una reserva determinada;
* cuánto capital adicional podría requerirse.

Bootstrap Chain Ladder aborda estas preguntas mediante simulación.

---

## 2. Motivación

Supóngase que dos portafolios tienen la misma reserva esperada:

[
\widehat R_A
============

$$
\widehat R_B
$$

100
]

Sin embargo:

* el portafolio A presenta miles de reclamaciones pequeñas y estables;
* el portafolio B presenta pocas reclamaciones grandes y volátiles.

Un Chain Ladder determinístico puede producir el mismo resultado puntual para ambos, aunque el riesgo sea muy diferente.

Bootstrap permite estimar distribuciones como:

[
R_A
\sim
F_A
]

[
R_B
\sim
F_B
]

donde (F_B) puede ser más dispersa y asimétrica.

---

## 3. Qué problema resuelve

Bootstrap Chain Ladder permite estimar:

* distribución del ultimate;
* distribución del IBNR;
* error estándar predictivo;
* coeficiente de variación;
* percentiles;
* Value at Risk;
* Tail Value at Risk;
* probabilidad de insuficiencia;
* sensibilidad a variación histórica.

No corrige automáticamente:

* datos deficientes;
* cambios regulatorios;
* efectos calendario;
* heterogeneidad del portafolio;
* colas no observadas;
* cambios en prácticas de pago;
* sesgos en los factores seleccionados.

Bootstrap cuantifica incertidumbre bajo un modelo. No convierte un modelo incorrecto en uno correcto.

---

## 4. Relación con Chain Ladder

Bootstrap Chain Ladder utiliza Chain Ladder como modelo central.

El procedimiento básico es:

```text
Triángulo observado
        ↓
Ajuste Chain Ladder
        ↓
Valores esperados
        ↓
Residuos
        ↓
Remuestreo
        ↓
Pseudo-triángulo
        ↓
Reestimación de factores
        ↓
Proyección futura
        ↓
Simulación del proceso
        ↓
Reserva simulada
```

La estimación media debería permanecer cercana al Chain Ladder original, aunque pueden existir diferencias por:

* ajuste de residuos;
* distribución utilizada para riesgo de proceso;
* tratamiento de ceros;
* tail factor;
* truncamiento;
* implementación numérica.

---

## 5. Fuentes de incertidumbre

## 5.1 Riesgo de parámetros

Los factores de desarrollo se estiman a partir de una muestra histórica finita.

Si se observara otra historia, los factores serían diferentes.

Bootstrap representa este riesgo al:

1. remuestrear residuos;
2. generar pseudo-triángulos;
3. reestimar factores en cada simulación.

## 5.2 Riesgo de proceso

Incluso si los parámetros fueran conocidos, los pagos futuros serían aleatorios.

Bootstrap representa este riesgo simulando pagos futuros alrededor de sus valores esperados.

## 5.3 Riesgo de modelo

Corresponde a que la estructura elegida sea incorrecta.

Ejemplos:

* desarrollo no estable;
* efectos calendario;
* segmentación insuficiente;
* distribución inadecuada;
* tail mal seleccionado.

El Bootstrap estándar no captura de manera completa el riesgo de modelo.

## 5.4 Riesgo estructural

Cambios en:

* legislación;
* contratación;
* inflación;
* operación;
* codificación;
* población;
* beneficios.

Deben modelarse mediante escenarios o modelos alternativos.

---

## 6. Formulación ODP

Una formulación frecuente del Bootstrap Chain Ladder utiliza el modelo de Poisson sobredispersado, ODP por sus siglas en inglés.

Sea:

[
X_{i,j}
]

el valor incremental del periodo de origen (i) y desarrollo (j).

Se supone:

[
E[X_{i,j}]
==========

\mu_{i,j}
]

y:

[
Var(X_{i,j})
============

\phi\mu_{i,j}
]

donde:

* (\mu_{i,j}): media esperada;
* (\phi): parámetro de dispersión.

Una especificación multiplicativa es:

[
\mu_{i,j}
=========

\alpha_i\beta_j
]

o, en forma GLM:

[
\log(\mu_{i,j})
===============

a_i+b_j
]

El modelo ODP reproduce la estructura central de Chain Ladder bajo determinadas condiciones.

---

## 7. Triángulo incremental y valores ajustados

Bootstrap suele trabajar sobre el triángulo incremental.

Sea:

[
C_{i,j}
=======

\sum_{h=0}^{j}
X_{i,h}
]

El Chain Ladder produce valores acumulados ajustados:

[
\widehat C_{i,j}
]

Los incrementales ajustados son:

[
\widehat X_{i,0}
================

\widehat C_{i,0}
]

[
\widehat X_{i,j}
================

## \widehat C_{i,j}

\widehat C_{i,j-1}
]

para (j>0).

Los valores ajustados representan la media estimada bajo el modelo.

---

## 8. Residuos de Pearson

Los residuos de Pearson se definen como:

[
r_{i,j}
=======

\frac{
X_{i,j}-\widehat X_{i,j}
}{
\sqrt{\widehat X_{i,j}}
}
]

Bajo ODP:

[
Var(r_{i,j})
\approx
\phi
]

La dispersión puede estimarse mediante:

[
\widehat\phi
============

\frac{
\sum_{i,j}r_{i,j}^2
}{
N-p
}
]

donde:

* (N): número de celdas observadas;
* (p): número efectivo de parámetros.

En una parametrización típica de origen y desarrollo:

[
p
=

I+J-1
]

debido a una restricción de identificabilidad.

---

## 9. Ajuste de residuos

Los residuos brutos suelen subestimar la variabilidad porque el modelo fue estimado con los mismos datos.

Una corrección frecuente es:

[
r_{i,j}^{adj}
=============

r_{i,j}
\sqrt{
\frac{N}{N-p}
}
]

Otra formulación utiliza:

[
r_{i,j}^{adj}
=============

\frac{
r_{i,j}
}{
\sqrt{1-h_{i,j}}
}
]

donde (h_{i,j}) es el leverage de la observación.

La implementación seleccionada debe documentarse porque diferentes ajustes producen resultados distintos.

## 9.1 Centrado

Antes del remuestreo puede centrarse el conjunto de residuos:

[
\widetilde r_{i,j}
==================

## r_{i,j}^{adj}

\overline r^{adj}
]

Esto ayuda a evitar introducir sesgo sistemático.

## 9.2 Residuo en celdas extremas

Los residuos de celdas con:

* valores ajustados muy pequeños;
* ceros;
* incrementales negativos;
* alta influencia;

pueden ser inestables.

Deben investigarse antes de incorporarlos al conjunto de remuestreo.

---

## 10. Algoritmo Bootstrap

Sea (B) el número de simulaciones.

Para cada simulación (b=1,\dots,B):

## Paso 1. Remuestrear residuos

Seleccionar con reemplazo:

[
r_{i,j}^{*(b)}
]

del conjunto de residuos ajustados.

## Paso 2. Generar incrementales pseudo-observados

[
X_{i,j}^{*(b)}
==============

\widehat X_{i,j}
+
r_{i,j}^{*(b)}
\sqrt{\widehat X_{i,j}}
]

## Paso 3. Tratar valores inválidos

Según la metodología:

* truncar en cero;
* utilizar una transformación;
* usar remuestreo paramétrico;
* conservar negativos cuando sean económicamente válidos.

## Paso 4. Acumular

[
C_{i,j}^{*(b)}
==============

\sum_{h=0}^{j}
X_{i,h}^{*(b)}
]

## Paso 5. Reestimar factores

[
\widehat f_j^{*(b)}
===================

\frac{
\sum_i C_{i,j+1}^{*(b)}
}{
\sum_i C_{i,j}^{*(b)}
}
]

## Paso 6. Proyectar el triángulo inferior

Para cada celda futura:

[
\widehat C_{i,j+1}^{*(b)}
=========================

\widehat C_{i,j}^{*(b)}
\widehat f_j^{*(b)}
]

## Paso 7. Obtener incrementales futuros esperados

[
\widehat X_{i,j+1}^{*(b)}
=========================

## \widehat C_{i,j+1}^{*(b)}

\widehat C_{i,j}^{*(b)}
]

## Paso 8. Simular riesgo de proceso

Generar:

[
X_{i,j}^{proc,(b)}
]

alrededor de:

[
\widehat X_{i,j}^{*(b)}
]

## Paso 9. Calcular reserva simulada

[
R^{(b)}
=======

\sum_{i,j\in futuro}
X_{i,j}^{proc,(b)}
]

El conjunto:

[
{R^{(1)},R^{(2)},\ldots,R^{(B)}}
]

aproxima la distribución predictiva.

---

## 11. Simulación del riesgo de proceso

## 11.1 Gamma

Una elección común es:

[
X_{i,j}^{proc}
\sim
Gamma
\left(
shape=
\frac{\widehat\mu_{i,j}}{\widehat\phi},
;
scale=
\widehat\phi
\right)
]

porque:

[
E[X]
====

\widehat\mu_{i,j}
]

y:

[
Var(X)
======

\widehat\phi\widehat\mu_{i,j}
]

## 11.2 Poisson sobredispersado

Puede representarse mediante una distribución con media:

[
\widehat\mu_{i,j}
]

y varianza:

[
\widehat\phi\widehat\mu_{i,j}
]

## 11.3 Lognormal

En algunas aplicaciones monetarias:

[
X_{i,j}^{proc}
\sim
Lognormal(m_{i,j},s_{i,j}^2)
]

con parámetros calibrados para reproducir media y varianza.

## 11.4 Selección

La distribución debe reflejar:

* soporte;
* asimetría;
* presencia de ceros;
* cola;
* naturaleza de la variable.

No debe seleccionarse únicamente por conveniencia computacional.

---

## 12. Distribución predictiva de reservas

La media bootstrap es:

[
\overline R
===========

\frac{1}{B}
\sum_{b=1}^{B}
R^{(b)}
]

La desviación estándar es:

[
SD(R)
=====

\sqrt{
\frac{1}{B-1}
\sum_{b=1}^{B}
(R^{(b)}-\overline R)^2
}
]

El coeficiente de variación es:

[
CV
==

\frac{SD(R)}{\overline R}
]

El percentil (q) es:

[
VaR_q
=====

F_R^{-1}(q)
]

donde (F_R) es la distribución empírica simulada.

---

## 13. Métricas de riesgo

## 13.1 Percentiles

* (P50): mediana;
* (P75): nivel prudencial moderado;
* (P90): nivel adverso;
* (P95): cola alta;
* (P99): escenario extremo bajo el modelo.

## 13.2 Value at Risk

[
VaR_q(R)
========

F_R^{-1}(q)
]

## 13.3 Tail Value at Risk

[
TVaR_q(R)
=========

E[
R\mid R>VaR_q(R)
]
]

En una simulación:

[
TVaR_q
======

\frac{
\sum_{b:R^{(b)}>VaR_q}R^{(b)}
}{
#{b:R^{(b)}>VaR_q}
}
]

## 13.4 Probabilidad de insuficiencia

Para una reserva contabilizada (R^{book}):

[
P(R>R^{book})
]

se estima como:

[
\widehat P
==========

\frac{1}{B}
\sum_{b=1}^{B}
I(R^{(b)}>R^{book})
]

---

## 14. Ejemplo conceptual

Supóngase que el Chain Ladder determinístico produce:

[
R^{CL}
======

100
]

Después de 10.000 simulaciones:

| Medida              | Resultado |
| ------------------- | --------: |
| Media               |       101 |
| Mediana             |        98 |
| Desviación estándar |        15 |
| CV                  |     14,9% |
| P75                 |       110 |
| P90                 |       121 |
| P95                 |       130 |
| P99                 |       155 |
| TVaR 95             |       145 |

La diferencia entre media y mediana indica asimetría.

La reserva contabilizada de 115 tendría una probabilidad de insuficiencia aproximada de:

[
P(R>115)
========

18%
]

por ejemplo, según la distribución simulada.

---

## 15. Diagnósticos

Bootstrap no debe ejecutarse antes de revisar el modelo base.

## 15.1 Residuos

Evaluar:

* media;
* varianza;
* asimetría;
* outliers;
* relación con valores ajustados;
* patrón por desarrollo;
* patrón por origen;
* patrón por calendario.

## 15.2 Independencia

Los residuos no deberían mostrar estructura sistemática.

Si muestran diagonales:

* inflación;
* cambio operativo;
* efecto calendario.

Si muestran tendencias por origen:

* cambio de mezcla;
* crecimiento;
* cambio de exposición.

Si muestran tendencias por desarrollo:

* forma incorrecta del patrón.

## 15.3 Heterocedasticidad

ODP supone:

[
Var(X_{i,j})
============

\phi\mu_{i,j}
]

Si la varianza crece de manera distinta, puede requerirse:

* Gamma;
* Tweedie;
* segmentación;
* GLM alternativo.

---

## 16. Número de simulaciones

## 16.1 Media y desviación estándar

Para estimaciones centrales, varios miles de simulaciones pueden ser suficientes.

## 16.2 Percentiles altos

Para estimar (P99), 1.000 simulaciones producen solo unas diez observaciones por encima del percentil.

Se recomienda usar más simulaciones cuando se requieren colas:

* 10.000;
* 25.000;
* 50.000;
* 100.000.

## 16.3 Estabilidad Monte Carlo

Ejecutar el modelo con diferentes semillas y comparar:

* media;
* SD;
* P95;
* P99;
* TVaR.

La variación por simulación debe ser pequeña respecto de la materialidad.

---

## 17. Tratamiento de valores negativos

En salud y otros portafolios, los incrementales pueden ser negativos por:

* reversos;
* recuperaciones;
* notas crédito;
* ajustes;
* glosas;
* recobros;
* reclasificaciones.

## 17.1 Truncar en cero

Ventaja:

* simplifica la simulación.

Desventaja:

* introduce sesgo positivo;
* elimina información económica.

## 17.2 Separar componentes

Modelar por separado:

[
X^{gross}
]

y:

[
X^{recovery}
]

Después:

[
X^{net}
=======

X^{gross}-X^{recovery}
]

## 17.3 Distribución con soporte real

Puede utilizarse un modelo que permita negativos, siempre que sea coherente.

## 17.4 Recomendación

No aplicar truncamiento automático sin medir el sesgo resultante.

---

## 18. Tail factor

Si el triángulo no llega al ultimate, debe incorporarse un tail.

Sea:

[
T
]

el factor de cola.

Entonces:

[
U_i
===

C_{i,J}T
]

## 18.1 Tail fijo

No incorpora incertidumbre adicional.

## 18.2 Tail estocástico

Puede simularse:

[
\log(T)
\sim
N(\mu_T,\sigma_T^2)
]

o mediante otra distribución.

## 18.3 Dependencia

El tail puede estar relacionado con los factores tardíos. Simularlo independientemente puede subestimar o sobreestimar la variabilidad.

## 18.4 Health insurance

En muchos portafolios médicos la cola es corta, pero puede ser material por:

* alto costo;
* litigios;
* recobros;
* glosas;
* coordinación de beneficios;
* ajustes retrospectivos.

---

## 19. Dependencia y efectos calendario

Bootstrap residual estándar presupone que los residuos pueden remuestrearse como observaciones intercambiables.

Este supuesto puede fallar por:

* inflación común;
* pandemia;
* cambios regulatorios;
* cambios de plataforma;
* pagos masivos;
* concentración por proveedor;
* dependencia entre periodos de origen.

## 19.1 Bootstrap por bloques

Remuestrear bloques completos, por ejemplo:

* diagonales calendario;
* prestadores;
* periodos;
* regiones.

## 19.2 Bootstrap estratificado

Remuestrear dentro de grupos homogéneos:

* desarrollo;
* producto;
* tipo de servicio;
* régimen.

## 19.3 Modelo explícito de calendario

Utilizar un GLM:

[
\log(\mu_{i,j})
===============

\alpha_i+\beta_j+\gamma_{i+j}
]

antes de hacer bootstrap.

---

## 20. Aplicación en salud

Bootstrap puede ser útil para:

* pagos médicos;
* cuentas incurridas;
* farmacia;
* hospitalización;
* incapacidad;
* reembolsos;
* reservas por proveedores;
* carteras maduras;
* análisis de suficiencia;
* stress testing.

## 20.1 Ventajas en salud

* alto volumen;
* patrones de desarrollo cortos;
* posibilidad de segmentación;
* gran cantidad de observaciones;
* necesidad de percentiles.

## 20.2 Riesgos específicos

* estacionalidad;
* cambios de red;
* inflación médica;
* cambios de tarifa;
* retroactividad;
* codificación;
* ajustes de elegibilidad;
* glosas;
* pagos directos;
* contratos prospectivos.

## 20.3 No usar sobre pagos fijos prospectivos

No es apropiado aplicar Bootstrap Chain Ladder sobre pagos contractuales de capitación si el flujo depende del devengo contractual y no del desarrollo de siniestros.

---

## 21. Comparación con Mack

| Característica               |     Mack | Bootstrap |
| ---------------------------- | -------: | --------: |
| Base Chain Ladder            |       Sí |        Sí |
| Cálculo analítico            |       Sí |        No |
| Simulación                   |       No |        Sí |
| Distribución completa        |       No |        Sí |
| Error estándar               |       Sí |        Sí |
| Percentiles empíricos        |       No |        Sí |
| Asimetría                    | Limitada |        Sí |
| VaR y TVaR                   | Limitado |        Sí |
| Velocidad                    |     Alta |     Menor |
| Decisiones de implementación |    Menos |       Más |
| Transparencia                |     Alta |  Moderada |
| Riesgo de proceso            |       Sí |        Sí |
| Riesgo de parámetros         |       Sí |        Sí |
| Riesgo de modelo             |       No |        No |

Mack y Bootstrap deben verse como herramientas complementarias.

Diferencias materiales entre ambos pueden indicar:

* asimetría;
* muestras pequeñas;
* residuos extremos;
* implementación distinta;
* supuestos inadecuados.

---

## 22. Implementación en Python

El siguiente ejemplo utiliza `chainladder`.

```python
from __future__ import annotations

import chainladder as cl
import pandas as pd


def fit_bootstrap_chainladder(
    triangle: cl.Triangle,
    n_sims: int = 10_000,
    random_state: int = 12345,
):
    if n_sims < 1_000:
        raise ValueError(
            "Use at least 1,000 simulations; "
            "more are recommended for tail percentiles."
        )

    bootstrap = cl.BootstrapODPSample(
        n_sims=n_sims,
        random_state=random_state,
    )

    simulated_triangles = bootstrap.fit_transform(triangle)

    model = cl.Chainladder().fit(simulated_triangles)

    return bootstrap, model
```

## 22.1 Extracción de resultados

```python
bootstrap, model = fit_bootstrap_chainladder(
    triangle=paid_triangle,
    n_sims=25_000,
    random_state=20260714,
)

ibnr_simulated = model.ibnr_

summary = {
    "mean": ibnr_simulated.mean(),
    "std": ibnr_simulated.std(),
    "p50": ibnr_simulated.quantile(0.50),
    "p75": ibnr_simulated.quantile(0.75),
    "p90": ibnr_simulated.quantile(0.90),
    "p95": ibnr_simulated.quantile(0.95),
    "p99": ibnr_simulated.quantile(0.99),
}
```

## 22.2 TVaR

```python
import numpy as np


def empirical_tvar(
    values: pd.Series | np.ndarray,
    q: float = 0.95,
) -> float:
    array = np.asarray(values, dtype=float)

    if not 0 < q < 1:
        raise ValueError("q must be between 0 and 1.")

    var = np.quantile(array, q)
    tail = array[array >= var]

    if tail.size == 0:
        return float(var)

    return float(tail.mean())
```

## 22.3 Probabilidad de insuficiencia

```python
def probability_of_deficiency(
    simulations: pd.Series | np.ndarray,
    booked_reserve: float,
) -> float:
    array = np.asarray(simulations, dtype=float)

    return float(
        np.mean(array > booked_reserve)
    )
```

> La API exacta puede variar entre versiones del paquete. El entorno de producción debe fijar versiones y probar resultados antes de su uso.

---

## 23. Implementación en R

El paquete `ChainLadder` permite ejecutar bootstrap mediante `BootChainLadder`.

```r
library(ChainLadder)

set.seed(20260714)

bootstrap_fit <- BootChainLadder(
  Triangle = paid_triangle,
  R = 25000,
  process.distr = "gamma"
)
```

## 23.1 Resumen

```r
summary(bootstrap_fit)

reserve_simulations <- bootstrap_fit$IBNR.Totals

quantile(
  reserve_simulations,
  probs = c(0.50, 0.75, 0.90, 0.95, 0.99)
)

mean(reserve_simulations)
sd(reserve_simulations)
```

## 23.2 TVaR

```r
empirical_tvar <- function(x, q = 0.95) {
  stopifnot(q > 0, q < 1)

  var_q <- as.numeric(
    quantile(x, probs = q, names = FALSE)
  )

  mean(x[x >= var_q])
}

tvar_95 <- empirical_tvar(
  reserve_simulations,
  q = 0.95
)
```

## 23.3 Probabilidad de insuficiencia

```r
booked_reserve <- 120

probability_of_deficiency <- mean(
  reserve_simulations > booked_reserve
)
```

---

## 24. Pseudocódigo de producción

```text
INPUT:
    Incremental triangle
    Segmentation
    Valuation date
    Number of simulations
    Process distribution
    Tail assumptions
    Random seed

VALIDATE:
    Reconcile totals
    Check missing cells
    Check negative values
    Check structural breaks
    Check calendar effects
    Review outliers

FIT:
    Convert incremental to cumulative
    Estimate Chain Ladder factors
    Calculate fitted values
    Calculate residuals
    Adjust residuals
    Estimate dispersion

FOR simulation = 1 to B:
    Resample adjusted residuals
    Generate pseudo-observed incremental triangle
    Recalculate cumulative triangle
    Refit development factors
    Project lower triangle
    Simulate process variance
    Apply stochastic tail
    Calculate ultimate
    Calculate reserve

OUTPUT:
    Mean reserve
    Median
    Standard deviation
    CV
    Percentiles
    VaR
    TVaR
    Probability of deficiency
    Results by origin period
    Results by segment
```

---

## 25. Validación y backtesting

## 25.1 Holdout diagonal

Eliminar una diagonal conocida, ajustar el modelo y predecirla.

Comparar:

[
\widehat X_{i,j}
]

con:

[
X_{i,j}^{observed}
]

## 25.2 Cobertura

Para intervalos predictivos:

[
Coverage_q
==========

\frac{
#{X^{obs}\in[L_q,U_q]}
}{
N
}
]

Un intervalo de 95% debería cubrir aproximadamente 95% de observaciones bajo repetición y si el modelo está bien especificado.

## 25.3 Backtesting por cierre

Para cada fecha histórica:

1. reconstruir el triángulo disponible;
2. ejecutar bootstrap;
3. observar el desarrollo posterior;
4. medir posición del resultado real en la distribución.

## 25.4 PIT

El Probability Integral Transform puede evaluar calibración:

[
PIT_t
=====

F_t(R_t^{observed})
]

Bajo buena calibración, los PIT deberían aproximarse a una distribución uniforme.

---

## 26. Gobierno del modelo

Documentar:

1. triángulo utilizado;
2. definición de origen;
3. definición de desarrollo;
4. incremental o acumulado;
5. segmentación;
6. modelo base;
7. residuos;
8. corrección de residuos;
9. parámetro de dispersión;
10. distribución de proceso;
11. número de simulaciones;
12. semilla;
13. tail;
14. tratamiento de negativos;
15. outliers;
16. efectos calendario;
17. validación;
18. limitaciones;
19. resultados;
20. selección final.

## 26.1 Reproducibilidad

El mismo:

* dataset;
* código;
* semilla;
* versión de paquetes;

debe producir resultados equivalentes.

## 26.2 Monitoreo

Comparar en cada cierre:

* media;
* SD;
* P95;
* P99;
* CV;
* posición de la reserva registrada;
* variación respecto del cierre anterior.

---

## 27. Errores comunes

* ejecutar bootstrap sobre un triángulo no validado;
* asumir que más simulaciones corrigen un mal modelo;
* omitir riesgo de proceso;
* simular solo parámetros;
* no ajustar residuos;
* truncar negativos sin análisis;
* usar una distribución inadecuada;
* ignorar tail;
* interpretar (P95) como peor caso;
* tratar VaR como capital suficiente universal;
* usar bootstrap con efectos calendario no modelados;
* mezclar segmentos heterogéneos;
* utilizar residuos no intercambiables;
* ignorar cambios operativos;
* no fijar la semilla;
* reportar percentiles sin error Monte Carlo.

---

## 28. Ventajas y limitaciones

## 28.1 Ventajas

* produce distribución completa;
* captura asimetría;
* permite percentiles;
* permite VaR y TVaR;
* integra riesgo de parámetros y proceso;
* es conceptualmente accesible;
* puede extenderse;
* es útil para capital y escenarios;
* sirve como benchmark de Mack.

## 28.2 Limitaciones

* depende de Chain Ladder;
* supone estabilidad histórica;
* requiere decisiones metodológicas;
* puede ser sensible a outliers;
* puede ser computacionalmente costoso;
* no captura automáticamente dependencia;
* no captura riesgo estructural;
* puede producir resultados inestables en triángulos pequeños;
* requiere tratamiento cuidadoso de negativos y ceros.

---

## 29. Checklist

## Datos

* [ ] El triángulo reconcilia con la fuente.
* [ ] Los incrementales están correctamente definidos.
* [ ] Los negativos fueron investigados.
* [ ] Los periodos incompletos fueron tratados.
* [ ] Los segmentos son homogéneos.
* [ ] Los cambios operativos están documentados.

## Modelo base

* [ ] Chain Ladder es razonable.
* [ ] Los factores son estables.
* [ ] No existen efectos calendario no tratados.
* [ ] Los residuos fueron revisados.
* [ ] La dispersión fue estimada.
* [ ] Los outliers fueron analizados.

## Bootstrap

* [ ] Se documentó el ajuste de residuos.
* [ ] Se documentó la distribución de proceso.
* [ ] Se fijó la semilla.
* [ ] El número de simulaciones es suficiente.
* [ ] Se incluyó tail cuando corresponde.
* [ ] Se evaluó el error Monte Carlo.
* [ ] Se midió la probabilidad de insuficiencia.

## Validación

* [ ] Se realizó holdout.
* [ ] Se realizó backtesting.
* [ ] Se comparó con Mack.
* [ ] Se comparó con Chain Ladder.
* [ ] Se revisó cobertura.
* [ ] Se analizaron diferencias por segmento.

## Gobierno

* [ ] El código está versionado.
* [ ] Las versiones de paquetes están fijadas.
* [ ] El resultado es reproducible.
* [ ] Las limitaciones están comunicadas.
* [ ] Existe revisión independiente.

---

## 30. Conclusiones

Bootstrap Chain Ladder extiende Chain Ladder mediante simulación.

Su objetivo no es reemplazar la estimación central, sino estimar la distribución predictiva de reservas posibles.

El método combina:

[
RiesgoDeParametros
]

y:

[
RiesgoDeProceso
]

a través de:

1. remuestreo de residuos;
2. generación de pseudo-triángulos;
3. reestimación de factores;
4. simulación de pagos futuros.

La principal ventaja frente a Mack es que permite obtener distribuciones asimétricas, percentiles, VaR y TVaR.

Su principal limitación es que depende de los mismos supuestos estructurales de Chain Ladder.

Por tanto, el flujo correcto es:

```text
Validación de datos
        ↓
Diagnóstico de Chain Ladder
        ↓
Bootstrap
        ↓
Validación predictiva
        ↓
Comparación con Mack
        ↓
Juicio actuarial
```

Bootstrap no debe utilizarse como una caja negra ni como sustituto de la evaluación actuarial.

---

## 31. Referencias

* England, P. D. y Verrall, R. J. *Analytic and Bootstrap Estimates of Prediction Errors in Claims Reserving*.
* England, P. D. y Verrall, R. J. *Stochastic Claims Reserving in General Insurance*.
* Mack, T. *Distribution-Free Calculation of the Standard Error of Chain Ladder Reserve Estimates*.
* Wüthrich, M. V. y Merz, M. *Stochastic Claims Reserving Methods in Insurance*.
* Taylor, G. *Loss Reserving: An Actuarial Perspective*.
* Friedland, J. *Estimating Unpaid Claims Using Basic Techniques*.
* Pinheiro, P., Andrade e Silva, J. y Centeno, M. *Bootstrap Methodology in Claim Reserving*.
* Actuarial Standard of Practice No. 5 — Incurred Health and Disability Claims.
* Actuarial Standard of Practice No. 23 — Data Quality.
* Actuarial Standard of Practice No. 41 — Actuarial Communications.
* Actuarial Standard of Practice No. 56 — Modeling.

---

## Próximo capítulo

➡️ **10-comparing-mack-vs-bootstrap.md**

Tema:

> Comparación entre estimación analítica y simulación de la incertidumbre de reservas.
