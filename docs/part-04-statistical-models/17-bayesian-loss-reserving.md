---
title: Reserving bayesiano
description: Introducción práctica al reserving bayesiano para combinar información previa y experiencia observada, obtener distribuciones posteriores y proyectar el IBNR.
status: draft
version: "0.1.8"
chapter: "17"
part: "part-04-statistical-models"
language: "es"
last_updated: "2026-07-14"
---

# Reserving bayesiano

El reserving bayesiano combina información previa con datos observados para obtener una distribución posterior de parámetros, ultimates e IBNR. En lugar de limitarse a una estimación puntual, representa explícitamente la incertidumbre que el modelo reconoce.

Su valor es especialmente claro cuando existe información externa relevante, segmentos con poca experiencia o estructuras jerárquicas. Su principal riesgo es producir resultados aparentemente precisos a partir de priors, likelihoods o dependencias mal especificadas.

## Objetivos

Al finalizar este capítulo, el lector podrá:

- interpretar prior, likelihood y posterior;
- diferenciar distribución posterior y posterior predictiva;
- construir una formulación bayesiana de reserving;
- utilizar modelos jerárquicos para credibilidad parcial;
- interpretar intervalos creíbles y predictivos;
- revisar diagnósticos de MCMC;
- realizar verificaciones predictivas;
- documentar sensibilidad, gobierno y limitaciones.

## Teorema de Bayes

Sea \(\theta\) el conjunto de parámetros y (y) los datos observados:

$$
p(\theta\mid y)=
\frac{p(y\mid \theta)p(\theta)}{p(y)}
$$

En forma proporcional:

$$
p(\theta\mid y)
\propto
p(y\mid \theta)p(\theta)
$$

donde:

- \(p(\theta)\): distribución previa o *prior*;
- \(p(y\mid \theta)\): verosimilitud o *likelihood*;
- \(p(\theta\mid y)\): distribución posterior.

## Distribución posterior predictiva

La predicción de una celda futura \(\widetilde y\) integra la incertidumbre de parámetros:

$$
p(\widetilde y\mid y)=
\int
p(\widetilde y\mid \theta)
p(\theta\mid y)
\,d\theta
$$

Cada muestra posterior de parámetros genera una posible trayectoria futura. Al agregar celdas futuras se obtiene una distribución posterior predictiva del IBNR.

## Prior o información previa

El prior puede incorporar:

- experiencia de cierres anteriores;
- estudios de pricing;
- benchmarks externos;
- experiencia de productos similares;
- restricciones físicas o actuariales;
- juicio experto estructurado.

Tipos habituales:

- débilmente informativo;
- informativo;
- jerárquico;
- robusto;
- de regularización.

Un prior no informativo en una parametrización puede ser informativo después de una transformación. Por eso debe evaluarse en la escala de resultados actuariales, no solo en la escala de coeficientes.

## Verificación predictiva previa

Antes de usar los datos, se simula desde:

$$
p(\widetilde y)=
\int p(\widetilde y\mid \theta)p(\theta)\,d\theta
$$

Las simulaciones deben producir valores plausibles de:

- incrementales;
- factores implícitos;
- ultimate;
- IBNR;
- severidad y dispersión;
- cola.

Si el prior permite con alta probabilidad reservas absurdas, debe revisarse antes del ajuste.

## Likelihood

La likelihood representa el mecanismo generador de los datos observados. Posibles elecciones:

- Poisson u ODP;
- Gamma;
- Tweedie;
- lognormal;
- binomial negativa para conteos;
- frecuencia y severidad;
- modelos de estados para pagado, incurrido y reserva caso.

El soporte debe ser compatible con ceros, negativos y reversos. La elección también determina la relación entre media y varianza.

## Modelo bayesiano sobre el triángulo

Para un incremental positivo (Y_{i,j}):

$$
Y_{i,j}\sim
\operatorname{Gamma}(\mu_{i,j},\phi)
$$

con:

$$
\log(\mu_{i,j})=
\log(e_i)+\alpha_i+\beta_j
$$

Los efectos pueden tener priors:

$$
\alpha_i\sim N(0,\sigma_{\alpha}^2)
$$

$$
\beta_j\sim N(m_j,\sigma_{\beta}^2)
$$

La identificación requiere una categoría de referencia, una restricción de suma cero u otra parametrización equivalente.

## Chain Ladder bayesiano

Los factores de desarrollo pueden tratarse como variables aleatorias:

$$
\log(f_j)\sim N(m_j,s_j^2)
$$

y la proyección puede formularse como:

$$
C_{i,j+1}\mid C_{i,j},f_j,\sigma_j
\sim
p(C_{i,j+1}\mid C_{i,j},f_j,\sigma_j)
$$

La posterior de cada (f_j) combina la experiencia del triángulo con la información previa. La cola puede incluirse como otro parámetro aleatorio.

## Modelos jerárquicos

Los portafolios de salud tienen niveles naturales:

```text
Portafolio
├── Producto
├── Región
├── Prestador
├── Cohorte
└── Periodo de origen
```

Un efecto por segmento puede expresarse como:

$$
\gamma_s\sim N(\mu_{\gamma},\tau_{\gamma}^2)
$$

Los segmentos con poca información se acercan al promedio del grupo, mientras que los segmentos con más datos conservan mayor independencia. Este mecanismo es una forma de credibilidad parcial.

La agrupación solo es válida si los segmentos son comparables. Compartir información entre poblaciones estructuralmente diferentes puede introducir sesgo.

## Priors de regularización

Los coeficientes de regresión pueden usar priors normales o Student-(t) centrados en cero. Las escalas deben seleccionarse en función del enlace.

Con enlace logarítmico, un coeficiente de 1 implica multiplicar la media por:

$$
e^1\approx2.72
$$

Por tanto, un prior (N(0,10^2)) puede ser extremadamente amplio en la escala de costos. La escala debe comprobarse mediante simulación previa.

Para parámetros positivos pueden usarse distribuciones half-normal, exponencial o lognormal, según el significado actuarial.

## Inferencia computacional

Las posteriores rara vez tienen solución cerrada. Métodos frecuentes:

- Gibbs;
- Metropolis-Hastings;
- Hamiltonian Monte Carlo;
- NUTS;
- inferencia variacional, con validación adicional.

HMC y NUTS utilizan gradientes para explorar posteriores de alta dimensión. Su eficiencia no elimina problemas de geometría, identificación o priors inadecuados.

## Diagnósticos de MCMC

### Cadenas y trazas

Las cadenas deben explorar la misma región posterior sin tendencias persistentes ni bloqueos.

### \(\widehat R\)

\(\widehat R\) compara variación entre y dentro de cadenas. Valores alejados de uno indican falta de convergencia.

### Tamaño efectivo de muestra

El ESS traduce autocorrelación en una cantidad aproximada de muestras independientes.

### Error estándar Monte Carlo

El MCSE cuantifica el error numérico de estimar una cantidad posterior con una muestra finita.

### Divergencias

Las transiciones divergentes pueden indicar regiones posteriores difíciles o parametrización inadecuada. No deben ignorarse aumentando ciegamente el número de iteraciones.

### Energía y autocorrelación

Revisar diagnósticos específicos del algoritmo y la persistencia entre muestras.

Los umbrales de aceptación deben definirse en el estándar del proyecto y evaluarse junto con gráficos y sensibilidad.

## Verificación predictiva posterior

Se simulan réplicas:

$$
y^{rep}\sim p(y^{rep}\mid y)
$$

y se comparan con los datos observados mediante:

- totales por diagonal;
- distribución de incrementales;
- ceros y extremos;
- factores implícitos;
- residuos por origen, desarrollo y calendario;
- estadísticos de cola;
- patrones por segmento.

Un modelo puede converger numéricamente y aun representar mal los datos.

## Intervalo creíble e intervalo predictivo

Un intervalo creíble para un parámetro describe su probabilidad posterior condicional al modelo y los datos.

Un intervalo predictivo para la reserva futura incluye además riesgo de proceso. Por eso suele ser más amplio.

No deben confundirse:

- posterior de la media esperada;
- posterior de parámetros;
- posterior predictiva del IBNR;
- distribución de suficiencia frente a una reserva registrada.

## Cálculo del IBNR

Para cada muestra posterior (m):

1. simular o predecir cada celda futura;
2. agregar por periodo de origen;
3. sumar el triángulo inferior;
4. almacenar \(IBNR^{(m)}\).

Entonces pueden calcularse:

$$
E[IBNR\mid y]
$$

$$
Q_q(IBNR\mid y)
$$

$$
P(IBNR>R_{booked}\mid y)
$$

Estos resultados siguen condicionados al modelo y a los priors.

## Ejemplo en Python con PyMC

El siguiente modelo Gamma usa la parametrización por media y desviación estándar disponible en PyMC:

```python
import numpy as np
import pymc as pm

origin_idx = observed["origin_idx"].to_numpy()
development_idx = observed["development_idx"].to_numpy()
exposure = observed["exposure"].to_numpy()
y_observed = observed["incremental_paid"].to_numpy()

with pm.Model() as model:
    intercept = pm.Normal("intercept", mu=0.0, sigma=2.0)
    sigma_origin = pm.HalfNormal("sigma_origin", sigma=0.5)

    origin_raw = pm.Normal(
        "origin_raw",
        mu=0.0,
        sigma=1.0,
        shape=observed["origin_idx"].nunique(),
    )
    origin_effect = origin_raw * sigma_origin

    development_effect = pm.Normal(
        "development_effect",
        mu=0.0,
        sigma=1.0,
        shape=observed["development_idx"].nunique(),
    )

    log_mu = (
        intercept
        + origin_effect[origin_idx]
        + development_effect[development_idx]
        + np.log(exposure)
    )
    mu = pm.math.exp(log_mu)

    coefficient_of_variation = pm.HalfNormal(
        "coefficient_of_variation",
        sigma=0.5,
    )

    paid = pm.Gamma(
        "paid",
        mu=mu,
        sigma=coefficient_of_variation * mu,
        observed=y_observed,
    )

    idata = pm.sample(
        draws=2000,
        tune=2000,
        chains=4,
        random_seed=20260714,
        target_accept=0.9,
    )

    pm.sample_posterior_predictive(
        idata,
        extend_inferencedata=True,
        random_seed=20260714,
    )
```

El modelo es ilustrativo. Una implementación de producción debe imponer identificación, construir predicciones de celdas futuras y validar priors, geometría y posterior predictiva.

## Ejemplo en R con `brms`

```r
library(brms)

fit <- brm(
  incremental_paid ~
    factor(development_age) +
    (1 | origin_period) +
    offset(log(exposure)),
  family = Gamma(link = "log"),
  prior = c(
    prior(normal(0, 1), class = "b"),
    prior(normal(0, 2), class = "Intercept"),
    prior(exponential(2), class = "sd")
  ),
  data = observed,
  chains = 4,
  iter = 4000,
  seed = 20260714
)

summary(fit)
pp_check(fit)
```

## Aplicación en seguros de salud

El enfoque bayesiano es útil para:

- productos nuevos;
- regiones o prestadores con poca experiencia;
- enfermedades de alto costo;
- integración de pricing y reserving;
- actualización secuencial por cierre;
- modelos de frecuencia y severidad;
- combinación de información pagada e incurrida;
- incorporación explícita de incertidumbre de cola.

Debe tenerse especial cuidado con:

- cambios de población;
- reformas regulatorias;
- sesgo de selección;
- información previa no comparable;
- grandes reclamaciones;
- dependencia entre prestadores y periodos;
- datos censurados o incompletos.

## Comparación con otros métodos

| Método | Resultado principal | Información previa | Distribución predictiva |
| --- | --- | --- | --- |
| Chain Ladder | Estimación puntual | Implícita en factores | No |
| Mack | MSEP y error estándar | No explícita | Requiere aproximación |
| Bootstrap | Muestra predictiva | Historia observada | Sí, bajo el esquema de simulación |
| GLM | Coeficientes y media | No explícita | Mediante extensión o simulación |
| Bayesiano | Posterior y posterior predictiva | Explícita | Sí |

## Sensibilidad

Repetir el análisis con:

- priors alternativos plausibles;
- distintas familias;
- otra segmentación;
- cola alternativa;
- inclusión y exclusión de periodos atípicos;
- parametrización centrada y no centrada;
- modelos con y sin efecto calendario.

Las decisiones materiales deben reflejarse en escenarios, no ocultarse dentro de un único prior.

## Controles de producción

Documentar:

1. modelo generador y likelihood;
2. parametrización e identificación;
3. priors y su justificación;
4. verificaciones predictivas previas;
5. algoritmo e hiperparámetros;
6. semilla y versiones;
7. diagnósticos de convergencia;
8. verificaciones predictivas posteriores;
9. construcción del triángulo futuro;
10. agregación y dependencia;
11. sensibilidad;
12. comparación con benchmarks;
13. limitaciones y revisión independiente.

## Buenas prácticas

- comenzar con un GLM o modelo jerárquico simple;
- justificar priors en la escala actuarial;
- realizar simulación predictiva previa;
- usar parametrizaciones identificables;
- revisar divergencias y ESS;
- validar la posterior predictiva;
- comparar con Chain Ladder, Mack y Bootstrap;
- separar incertidumbre cuantificada y riesgo estructural;
- mantener el modelo reproducible y revisable.

## Referencias

- Gelman, A. et al. *Bayesian Data Analysis*.
- McElreath, R. *Statistical Rethinking*.
- Wüthrich, M. V. y Merz, M. *Stochastic Claims Reserving Methods in Insurance*.
- [Documentación oficial de la distribución Gamma en PyMC](https://www.pymc.io/projects/docs/en/stable/api/distributions/generated/pymc.Gamma.html).

## Capítulos relacionados

Anterior: [Modelos aditivos generalizados](16-gam-for-loss-reserving.md).  
Siguiente: [Machine learning para reserving](../part-05-machine-learning/18-machine-learning-for-loss-reserving.md).
