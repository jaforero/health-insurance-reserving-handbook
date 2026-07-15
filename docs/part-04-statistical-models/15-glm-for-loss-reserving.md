---
title: Modelos lineales generalizados para reserving
description: Guía práctica para modelar reclamaciones incrementales y estimar reservas mediante modelos lineales generalizados con distribuciones y enlaces actuarialmente apropiados.
status: draft
version: "0.1.8"
chapter: "15"
part: "part-04-statistical-models"
language: "es"
last_updated: "2026-07-14"
---

# Modelos lineales generalizados para reserving

Los modelos lineales generalizados, o GLM por sus siglas en inglés, permiten representar el desarrollo de reclamaciones dentro de un marco estadístico explícito. A diferencia de un método determinístico, un GLM especifica una distribución, una relación entre media y varianza, un predictor y una función de enlace.

En reserving, los GLM suelen aplicarse a celdas incrementales. Pueden reproducir la estructura de Chain Ladder y extenderla con exposición, inflación, producto, región, prestador u otras variables explicativas.

## Objetivos

Al finalizar este capítulo, el lector podrá:

- identificar los componentes de un GLM;
- seleccionar una distribución y una función de enlace;
- formular un modelo sobre un triángulo incremental;
- incorporar exposición mediante un *offset*;
- interpretar coeficientes y predicciones;
- diagnosticar sobre-dispersión y mala especificación;
- proyectar el triángulo inferior;
- cuantificar incertidumbre de proceso y parámetros;
- reconocer riesgos de aplicación en seguros de salud.

## Por qué usar un GLM

Chain Ladder resume el desarrollo mediante factores. Un GLM permite expresar el mismo problema como una relación estadística entre celdas.

Esta formulación aporta:

- estimación por máxima verosimilitud o cuasi-verosimilitud;
- errores estándar de parámetros;
- residuos y medidas de ajuste;
- comparación de especificaciones;
- incorporación de variables adicionales;
- validación fuera de muestra;
- simulación predictiva.

El GLM no elimina la necesidad de construir y validar correctamente el triángulo. Una estructura estadística sofisticada no compensa errores en periodos de origen, edades de desarrollo o fecha de valuación.

## Componentes del modelo

Un GLM tiene tres elementos.

### Componente aleatorio

La variable respuesta (Y_i) pertenece a una familia de dispersión exponencial. Su media y varianza se expresan como:

$$
E[Y_i]=\mu_i
$$

$$
\mathrm{Var}(Y_i)=\phi V(\mu_i)
$$

donde:

- \(\mu_i\) es la media condicional;
- \(\phi\) es el parámetro de dispersión;
- \(V(\mu_i)\) es la función de varianza.

### Componente sistemático

El predictor lineal es:

$$
\eta_i = \beta_0 + \beta_1x_{i1}+\cdots+\beta_px_{ip}
$$

### Función de enlace

La función de enlace conecta la media con el predictor:

$$
g(\mu_i)=\eta_i
$$

El enlace logarítmico es frecuente en reserving porque garantiza medias positivas:

$$
\log(\mu_i)=\eta_i
$$

## Formulación sobre el triángulo

Sea (Y_{i,j}) el monto incremental del periodo de origen (i) a edad de desarrollo (j). Una especificación básica es:

$$
\log(\mu_{i,j})=\alpha_i+\beta_j
$$

donde:

- \(\alpha_i\) representa diferencias entre periodos de origen;
- \(\beta_j\) representa el patrón de desarrollo.

Una extensión con exposición (e_i) utiliza:

$$
\log(\mu_{i,j})=
\log(e_i)+\alpha_i+\beta_j
$$

El término \(\log(e_i)\) es un *offset*: su coeficiente se fija en uno.

También pueden incluirse variables como producto, región, tipo de servicio o indicador de cambio operativo:

$$
\log(\mu_{i,j})=
\log(e_i)+\alpha_i+\beta_j+x_{i,j}^{\top}\gamma
$$

## Origen, desarrollo y calendario

El periodo calendario está determinado por origen y desarrollo:

$$
calendario=origen+desarrollo
$$

Por esta relación, un modelo con conjuntos completos de efectos categóricos de origen, desarrollo y calendario no es identificable sin restricciones adicionales.

Opciones habituales:

- modelar origen y desarrollo;
- sustituir parte de los efectos por tendencias;
- imponer restricciones de identificación;
- usar penalización;
- incluir variables calendario específicas y justificadas;
- aplicar un modelo jerárquico o suavizado.

La parametrización debe permitir separar razonablemente desarrollo, tendencia y choque calendario.

## Selección de distribución

| Familia | Función de varianza | Uso posible | Advertencia |
| --- | --- | --- | --- |
| Poisson | \(V(\mu)=\mu\) | Conteos o estructura Chain Ladder | Puede subestimar dispersión |
| Poisson sobredispersado | \(V(\mu)=\mu\), \(\phi\) libre | Incrementales no negativos | Es una formulación de cuasi-verosimilitud |
| Gamma | \(V(\mu)=\mu^2\) | Montos positivos continuos | No admite ceros ni negativos |
| Tweedie | \(V(\mu)=\mu^p\) | Mezcla de ceros y montos positivos | Requiere seleccionar o estimar \(p\) |
| Binomial negativa | \(V(\mu)=\mu+\kappa\mu^2\) | Conteos sobredispersos | No es una distribución de montos agregados |

La familia debe elegirse según la naturaleza de la respuesta, no únicamente por el menor AIC.

### Incrementales negativos

Reversos, recuperaciones, glosas y ajustes pueden producir valores negativos. Poisson, Gamma y Tweedie estándar no los admiten.

Antes de modelar se debe decidir si corresponde:

- corregir un error de datos;
- separar pagos y recuperaciones;
- agregar periodos;
- usar otra distribución;
- modelar componentes positivos y negativos;
- aplicar escenarios fuera del GLM principal.

## Exposición y pesos

La exposición puede representar afiliados-mes, pólizas, vidas o unidades de riesgo. Debe distinguirse entre:

- *offset*, que ajusta la media esperada por exposición;
- peso de frecuencia, que representa observaciones repetidas;
- peso de varianza, que modifica la precisión relativa.

Usar exposición como peso cuando corresponde un *offset* cambia la interpretación del modelo.

## Estimación

Los parámetros se estiman maximizando la log-verosimilitud:

$$
\ell(\beta)=
\sum_i \log f(y_i\mid \beta,\phi)
$$

En muchos GLM, el cálculo se realiza mediante mínimos cuadrados reponderados iterativamente, o IRLS.

La estimación produce:

- coeficientes;
- matriz de covarianza;
- valores ajustados;
- residuos;
- deviance;
- log-verosimilitud;
- criterios de información, cuando son comparables.

## Interpretación con enlace logarítmico

Si un coeficiente es \(\beta_k\), el cambio multiplicativo esperado es:

$$
\exp(\beta_k)
$$

Por ejemplo, \(\beta_k=0.10\) implica, manteniendo lo demás constante:

$$
\exp(0.10)-1\approx10.5\%
$$

Para variables categóricas, la interpretación siempre es respecto de la categoría de referencia.

## Proyección del triángulo inferior

Después de ajustar el modelo a las celdas observadas:

1. construir las covariables de cada celda futura;
2. calcular \(\widehat\eta_{i,j}\);
3. transformar a la escala de respuesta;
4. sumar incrementales futuros por periodo de origen;
5. obtener ultimate e IBNR.

Con enlace logarítmico:

$$
\widehat\mu_{i,j}=\exp(\widehat\eta_{i,j})
$$

$$
\widehat{IBNR}=
\sum_{i,j\in\text{futuro}}\widehat\mu_{i,j}
$$

La matriz futura debe conservar la misma codificación de variables, niveles categóricos y tratamiento de exposición usados en el ajuste.

## Incertidumbre predictiva

El error estándar de la media ajustada no equivale a la incertidumbre de la reserva futura.

Una distribución predictiva debe incluir:

- incertidumbre de parámetros;
- riesgo de proceso;
- dependencia relevante;
- incertidumbre de cola;
- riesgo de modelo mediante escenarios o modelos alternativos.

Opciones de cálculo:

- simulación paramétrica de coeficientes y proceso;
- Bootstrap;
- aproximación delta;
- modelo bayesiano;
- combinación con escenarios actuariales.

## Diagnósticos

### Residuos

Revisar residuos de Pearson y deviance por:

- periodo de origen;
- edad de desarrollo;
- periodo calendario;
- producto o segmento;
- tamaño del valor ajustado.

Patrones sistemáticos indican mala especificación.

### Dispersión

Una estimación conceptual es:

$$
\widehat\phi=
\frac{\sum_i r_{P,i}^2}{n-p}
$$

Valores muy superiores a uno bajo Poisson sugieren sobre-dispersión. La causa puede ser heterogeneidad, dependencia, variables omitidas o una familia inadecuada.

### Influencia

Investigar:

- leverage;
- distancia de Cook;
- celdas con gran deviance;
- sensibilidad al retirar diagonales o filas.

### Ajuste y selección

Usar con cautela:

- deviance;
- AIC y BIC;
- log-verosimilitud;
- validación temporal;
- error predictivo en diagonales retenidas.

AIC solo es comparable entre modelos ajustados a la misma respuesta y datos bajo verosimilitudes compatibles.

## Validación temporal

Un esquema útil es el *backtesting* por fecha de corte:

1. reconstruir un triángulo histórico;
2. ajustar el GLM;
3. predecir la siguiente diagonal;
4. comparar predicción y observación;
5. repetir para varios cierres.

Métricas posibles:

- sesgo total;
- MAE;
- RMSE;
- deviance predictiva;
- cobertura de intervalos;
- error por edad y segmento.

MAPE puede ser inestable cuando existen valores cercanos a cero.

## Ejemplo en Python

El siguiente ejemplo usa nombres de clase vigentes en `statsmodels` y un enlace logarítmico explícito:

```python
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

observed = df.loc[df["is_observed"]].copy()

model = smf.glm(
    formula=(
        "incremental_paid ~ "
        "C(origin_period) + C(development_age)"
    ),
    data=observed,
    family=sm.families.Gamma(
        link=sm.families.links.Log()
    ),
    offset=np.log(observed["exposure"]),
)

result = model.fit()
print(result.summary())
```

Este ejemplo requiere incrementales positivos. Para predecir, el *offset* futuro debe suministrarse nuevamente con la exposición correspondiente.

## Ejemplo en R

```r
fit <- glm(
  incremental_paid ~
    factor(origin_period) +
    factor(development_age) +
    offset(log(exposure)),
  family = Gamma(link = "log"),
  data = observed
)

summary(fit)
```

## Aplicación en seguros de salud

Los GLM pueden incorporar explícitamente:

- afiliados-mes;
- grupo etario y sexo;
- región;
- producto y plan de beneficios;
- tipo de prestador;
- ámbito hospitalario o ambulatorio;
- inflación médica;
- utilización;
- canal de radicación;
- cambio de contrato;
- indicador de gran reclamación.

Debe evitarse introducir variables conocidas solo después de la fecha de valuación. Eso produciría fuga de información y una validación artificialmente favorable.

## Comparación con Chain Ladder

| Aspecto | Chain Ladder | GLM |
| --- | --- | --- |
| Patrón de desarrollo | Factores explícitos | Efectos estimados |
| Variables adicionales | Limitadas | Sí |
| Distribución | No explícita | Explícita o cuasi-likelihood |
| Residuos | Diagnósticos auxiliares | Parte central del modelo |
| Inferencia | Limitada | Sí |
| Validación predictiva | Posible | Natural dentro del flujo |
| Complejidad | Baja | Media |

Un GLM de origen y desarrollo puede reproducir una estructura equivalente a Chain Ladder bajo determinadas especificaciones. Por eso Chain Ladder es un benchmark natural.

## Controles de producción

Documentar:

1. definición de la respuesta;
2. celdas observadas y futuras;
3. exposición y *offset*;
4. familia y enlace;
5. variables y codificación;
6. restricciones de identificación;
7. tratamiento de ceros y negativos;
8. dispersión;
9. diagnósticos;
10. validación temporal;
11. incertidumbre predictiva;
12. versión de datos, código y dependencias;
13. comparación con métodos actuariales de referencia.

## Buenas prácticas

- comenzar con una especificación simple;
- utilizar Chain Ladder como benchmark;
- justificar familia y enlace;
- revisar origen, desarrollo y calendario;
- separar predicción de la media y distribución predictiva;
- validar con cierres históricos;
- probar sensibilidad a segmentación y cola;
- comunicar limitaciones y riesgo de modelo.

## Referencias

- McCullagh, P. y Nelder, J. A. *Generalized Linear Models*.
- England, P. D. y Verrall, R. J. *Stochastic Claims Reserving in General Insurance*.
- Wüthrich, M. V. y Merz, M. *Stochastic Claims Reserving Methods in Insurance*.
- [Documentación oficial de GLM en statsmodels](https://www.statsmodels.org/stable/glm.html).

## Capítulos relacionados

Anterior: [Comparación entre Mack y Bootstrap](../part-03-stochastic-reserving/10-comparing-mack-vs-bootstrap.md).  
Siguiente: [Modelos aditivos generalizados](16-gam-for-loss-reserving.md).
