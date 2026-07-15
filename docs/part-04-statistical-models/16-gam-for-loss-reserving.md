---
title: Modelos aditivos generalizados para reserving
description: Introducción práctica a los modelos aditivos generalizados para representar patrones no lineales de desarrollo, calendario, exposición y tendencia médica.
status: draft
version: "0.1.8"
chapter: "16"
part: "part-04-statistical-models"
language: "es"
last_updated: "2026-07-14"
---

# Modelos aditivos generalizados para reserving

Los modelos aditivos generalizados, o GAM, extienden los GLM reemplazando algunos efectos lineales o categóricos por funciones suaves estimadas a partir de los datos.

Esta flexibilidad es útil cuando el desarrollo, la tendencia médica, la estacionalidad o la utilización cambian de manera no lineal. La suavización puede reducir la volatilidad de estimar un coeficiente independiente para cada edad, pero también introduce decisiones de regularización que deben validarse.

## Objetivos

Al finalizar este capítulo, el lector podrá:

- explicar la relación entre GLM y GAM;
- interpretar bases, splines y penalización;
- leer grados efectivos de libertad;
- seleccionar y validar parámetros de suavización;
- modelar desarrollo, calendario y estacionalidad;
- detectar sobreajuste y concurvidad;
- proyectar celdas futuras;
- aplicar GAM a reserving de salud con gobierno apropiado.

## Del GLM al GAM

Un GLM tiene la forma:

$$
g(\mu_i)=\beta_0+x_i^{\top}\beta
$$

Un GAM permite:

$$
g(\mu_i)=\beta_0+
f_1(x_{i1})+
f_2(x_{i2})+
\cdots+
f_q(x_{iq})
$$

Las funciones \(f_k\) se estiman como curvas suaves. El modelo sigue siendo aditivo en la escala del enlace, aunque la relación con cada predictor puede ser no lineal.

## Por qué suavizar

En un GLM categórico, cada edad de desarrollo puede tener su propio coeficiente. Con pocos datos, esos coeficientes pueden ser inestables.

Un suavizador comparte información entre edades cercanas y puede representar:

- descenso rápido seguido de una cola lenta;
- tendencia médica que cambia gradualmente;
- estacionalidad anual;
- relación no lineal entre utilización y costo;
- comportamiento de prestadores según volumen;
- efectos de edad del afiliado.

La suavización no debe ocultar cambios reales. Un quiebre regulatorio o de sistema puede requerir un indicador explícito o un modelo por regímenes.

## Representación mediante bases

Una función suave puede escribirse como:

$$
f(x)=\sum_{k=1}^{K}b_k(x)\theta_k
$$

donde:

- \(b_k(x)\) son funciones base;
- \(\theta_k\) son coeficientes;
- (K) determina el tamaño máximo de la base.

Bases frecuentes:

- splines de regresión de placa delgada;
- splines cúbicos;
- B-splines;
- splines cíclicos;
- productos tensoriales para interacciones.

Un (K) grande no obliga a una curva compleja si existe penalización suficiente, pero aumenta costo y puede complicar el ajuste.

## Penalización

Para evitar curvas excesivamente onduladas se añade una penalización, por ejemplo:

$$
\lambda
\int [f''(x)]^2\,dx
$$

El parámetro \(\lambda\) controla el compromiso entre ajuste y suavidad:

- \(\lambda\) grande: curva más suave;
- \(\lambda\) pequeño: curva más flexible.

En forma matricial, el criterio penalizado puede expresarse como:

$$
-2\ell(\theta)+
\sum_m \lambda_m\theta^{\top}S_m\theta
$$

donde \(S_m\) es una matriz de penalización.

## Grados efectivos de libertad

Los grados efectivos de libertad, EDF, resumen la complejidad estimada de un efecto suave.

Interpretación aproximada:

- EDF cercano a 1: efecto casi lineal;
- EDF moderado: curvatura relevante;
- EDF alto: patrón complejo que requiere revisión.

Un EDF alto no prueba sobreajuste, pero debe evaluarse junto con validación, tamaño de muestra, residuos y estabilidad temporal.

## Selección de suavización

Métodos frecuentes:

- REML;
- máxima verosimilitud;
- GCV;
- UBRE o AIC, según la familia y escala;
- validación cruzada temporal.

En `mgcv`, `method="REML"` permite estimar parámetros de suavización mediante máxima verosimilitud restringida. La selección automática debe complementarse con validación actuarial.

## Formulación para reserving

Sea (Y_{i,j}) el incremental de origen (i) y desarrollo (j). Un modelo posible es:

$$
\log(\mu_{i,j})=
\log(e_i)+
f_{dev}(j)+
f_{origin}(i)+
x_{i,j}^{\top}\gamma
$$

Una extensión con calendario es:

$$
\log(\mu_{i,j})=
\log(e_i)+
f_{dev}(j)+
f_{calendar}(i+j)+
x_{i,j}^{\top}\gamma
$$

Origen, desarrollo y calendario mantienen una relación exacta. Usar tres suavizadores flexibles sin restricciones puede producir confusión de efectos e inestabilidad. La estructura debe ser identificable y responder a una hipótesis actuarial.

## Estacionalidad

Para datos mensuales, la estacionalidad puede modelarse con un spline cíclico:

$$
f_{season}(mes),
\qquad f_{season}(1)=f_{season}(13)
$$

La continuidad entre diciembre y enero evita un salto artificial en el borde.

La estacionalidad observada debe distinguirse de:

- días hábiles;
- calendario de pagos;
- cierres contables;
- vacaciones;
- campañas de radicación;
- cambios de utilización.

## Interacciones

Un efecto conjunto puede representarse con productos tensoriales:

$$
f(desarrollo, calendario)
$$

o:

$$
f(utilización, severidad)
$$

Las interacciones aumentan rápidamente la complejidad y requieren suficiente cobertura de datos. No deben usarse para llenar regiones futuras muy alejadas de la experiencia observada.

## Concurvidad

La concurvidad es el análogo no lineal de la multicolinealidad. Ocurre cuando una función suave puede explicarse mediante otras funciones del modelo.

Consecuencias:

- efectos individuales inestables;
- bandas amplias;
- interpretación ambigua;
- sensibilidad a pequeñas variaciones de datos;
- extrapolación poco confiable.

En triángulos, la relación origen-desarrollo-calendario es una fuente natural de concurvidad.

## Distribución y enlace

Los GAM usan las mismas familias conceptuales que los GLM:

- Poisson o cuasi-Poisson;
- Gamma;
- Tweedie;
- binomial negativa;
- otras familias compatibles con la respuesta.

La suavización no resuelve incompatibilidades de soporte. Un GAM Gamma sigue sin admitir ceros o negativos.

## Proyección futura

Para proyectar el triángulo inferior:

1. construir las covariables futuras;
2. verificar que estén dentro de un rango razonable;
3. predecir en la escala del enlace;
4. transformar a montos incrementales;
5. agregar por origen y total;
6. incorporar incertidumbre de parámetros y proceso.

Los splines pueden extrapolar linealmente o según reglas de borde que no representan una cola actuarial. La extrapolación debe revisarse visualmente y compararse con un tail factor o escenario explícito.

## Diagnósticos

Revisar:

- residuos de deviance y Pearson;
- residuos por origen, desarrollo y calendario;
- EDF por término;
- suficiencia de dimensión de base;
- concurvidad;
- influencia;
- dispersión;
- bandas de incertidumbre;
- ajuste en bordes;
- desempeño fuera de muestra.

### Señales de sobreajuste

- curvas con oscilaciones sin interpretación;
- gran variación entre cierres;
- excelente ajuste interno y mal *backtesting*;
- predicciones negativas o extremas en otra familia o enlace;
- alta sensibilidad a (K), penalización o pocas observaciones.

### Señales de subajuste

- patrones claros en residuos;
- EDF pegado al límite de la base;
- sesgo sistemático por edad;
- estacionalidad remanente;
- errores concentrados en cambios de pendiente.

## Validación

La validación aleatoria puede filtrar información futura en un problema triangular. Es preferible usar:

- retención de diagonales;
- validación por fecha de corte;
- ventanas temporales móviles;
- comparación de cierres históricos;
- validación por segmento.

Comparar siempre con:

- Chain Ladder;
- GLM más simple;
- método a priori cuando exista poca madurez;
- escenarios estructurales.

## Ejemplo en R

El paquete `mgcv` permite especificar suavizadores mediante `s()` y seleccionar suavización por REML:

```r
library(mgcv)

fit <- gam(
  incremental_paid ~
    s(development_age, k = 8) +
    s(calendar_index, k = 8) +
    factor(product) +
    offset(log(exposure)),
  family = Gamma(link = "log"),
  data = observed,
  method = "REML"
)

summary(fit)
gam.check(fit)
concurvity(fit, full = TRUE)
```

Para un efecto mensual cíclico:

```r
seasonal_fit <- gam(
  incremental_paid ~
    s(development_age, k = 8) +
    s(month_of_year, bs = "cc", k = 12) +
    offset(log(exposure)),
  family = Gamma(link = "log"),
  data = observed,
  method = "REML",
  knots = list(month_of_year = c(0.5, 12.5))
)
```

## Ejemplo conceptual en Python

Una implementación con `pyGAM` puede estructurarse así:

```python
from pygam import GammaGAM, f, s

model = GammaGAM(
    s(0, n_splines=8) +
    s(1, n_splines=8) +
    f(2)
)

model.gridsearch(X_train, y_train)
prediction = model.predict(X_future)
```

Las columnas del ejemplo representan desarrollo, calendario y producto. El tratamiento de exposición, restricciones y versiones de la API debe validarse antes de producción.

## Aplicación en seguros de salud

Los GAM pueden representar:

- curva de desarrollo de pagos;
- utilización por edad;
- estacionalidad de servicios;
- tendencia médica no lineal;
- comportamiento por volumen de prestador;
- efectos de duración de afiliación;
- relaciones entre exposición y severidad;
- cambios graduales de codificación.

No deben suavizarse indiscriminadamente:

- reformas con fecha definida;
- cambios de sistema;
- modificaciones contractuales discretas;
- epidemias;
- depuración extraordinaria de cuentas.

Estos eventos suelen requerir variables indicadoras, segmentación o escenarios.

## Comparación de modelos

| Aspecto | Chain Ladder | GLM | GAM |
| --- | --- | --- | --- |
| Desarrollo | Factores | Efectos lineales o categóricos | Curva suave |
| Variables adicionales | Limitadas | Sí | Sí |
| No linealidad | Implícita | Mediante diseño | Directa mediante suavizadores |
| Regularización | No usual | Opcional | Central |
| Interpretación | Alta | Alta o media | Media, apoyada en gráficos |
| Riesgo de sobreajuste | Bajo o medio | Medio | Medio o alto sin control |
| Extrapolación | Mediante factores | Según predictor | Sensible a bordes y bases |

## Incertidumbre

Las bandas de un efecto suave no son intervalos predictivos de reserva.

Para la distribución de reserva se requiere considerar:

- covarianza de coeficientes y suavizadores;
- incertidumbre del parámetro de suavización;
- riesgo de proceso;
- cola;
- dependencia entre celdas y segmentos;
- riesgo de modelo.

Puede utilizarse simulación a partir de la distribución aproximada de coeficientes, Bootstrap o una formulación bayesiana.

## Controles de producción

Documentar:

1. familia y enlace;
2. variables lineales y suaves;
3. tipo y tamaño de bases;
4. método de suavización;
5. restricciones de identificación;
6. exposición y *offset*;
7. tratamiento de bordes;
8. concurvidad;
9. diagnóstico de dimensión de base;
10. validación temporal;
11. incertidumbre predictiva;
12. comparación con GLM y Chain Ladder;
13. versiones de software.

## Buenas prácticas

- ajustar primero un GLM interpretable;
- añadir suavizadores solo donde exista una hipótesis;
- visualizar cada efecto con bandas;
- revisar bordes y extrapolación;
- validar por cierre, no solo aleatoriamente;
- controlar concurvidad;
- probar sensibilidad a bases y penalización;
- traducir el resultado a una narrativa actuarial clara.

## Referencias

- Hastie, T. y Tibshirani, R. *Generalized Additive Models*.
- Wood, S. N. *Generalized Additive Models: An Introduction with R*.
- [Documentación oficial de `gam` en `mgcv`](https://stat.ethz.ch/R-manual/R-devel/library/mgcv/html/gam.html).

## Capítulos relacionados

Anterior: [Modelos lineales generalizados](15-glm-for-loss-reserving.md).  
Siguiente: [Reserving bayesiano](17-bayesian-loss-reserving.md).
