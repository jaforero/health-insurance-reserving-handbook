---
title: Chain Ladder de Mack
description: Introducción práctica al modelo de Mack para cuantificar el error de predicción de reservas Chain Ladder sin especificar una distribución completa.
status: draft
version: "0.1.7"
chapter: "08"
part: "part-03-stochastic-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Chain Ladder de Mack

El método Chain Ladder produce una estimación puntual del costo último y del IBNR. El modelo de Mack conserva esa estimación central y añade una medida analítica de su incertidumbre.

Su aporte principal es estimar el error cuadrático medio de predicción sin imponer una distribución completa a los siniestros. Por eso se describe como un método *distribution-free*: trabaja con supuestos sobre medias, varianzas e independencia, pero no exige que los datos sigan una distribución específica.

## Objetivos

Al finalizar este capítulo, el lector podrá:

- explicar la relación entre Chain Ladder determinístico y Mack;
- identificar los supuestos del modelo;
- interpretar riesgo de proceso y riesgo de parámetros;
- estimar varianzas de desarrollo;
- leer el MSEP, el error estándar y el coeficiente de variación;
- construir intervalos de predicción con las cautelas apropiadas;
- reconocer limitaciones relevantes en seguros de salud.

## De la estimación puntual a la incertidumbre

Sea (C_{i,j}) el valor acumulado del periodo de origen (i) a edad de desarrollo (j). Chain Ladder estima los factores:

$$
\widehat f_j =
\frac{\sum_i C_{i,j+1}}
{\sum_i C_{i,j}}
$$

y proyecta el último valor observado de cada periodo de origen hasta ultimate.

Mack utiliza los mismos factores y los mismos ultimates esperados. La diferencia es que también estima cuánto puede desviarse el resultado futuro de esa proyección.

En forma conceptual:

```text
Triángulo acumulado
        ↓
Chain Ladder
        ↓
Ultimate e IBNR esperados
        ↓
Modelo de Mack
        ↓
Error estándar y MSEP
```

## Supuestos del modelo

### Media condicional

El primer supuesto establece que:

$$
E[C_{i,j+1}\mid C_{i,j}] = f_j C_{i,j}
$$

En promedio, el acumulado siguiente es proporcional al acumulado actual. Este es el supuesto central de Chain Ladder.

### Varianza condicional

En la formulación clásica de Mack:

$$
\mathrm{Var}(C_{i,j+1}\mid C_{i,j})
= \sigma_j^2 C_{i,j}
$$

El parámetro $\sigma_j^2$ representa la variabilidad del paso de desarrollo (j) a (j+1). La varianza aumenta con el volumen acumulado, aunque la variabilidad relativa tiende a disminuir.

Una generalización frecuente utiliza:

$$
\mathrm{Var}(C_{i,j+1}\mid C_{i,j})
= \sigma_j^2 C_{i,j}^{\alpha}
$$

con un parámetro $\alpha$ seleccionado según la estructura de varianza. La versión clásica corresponde a $\alpha=1$.

### Independencia entre periodos de origen

Los periodos de origen se consideran independientes. Este supuesto puede fallar cuando varias filas comparten efectos de calendario, inflación médica, cambios regulatorios, alteraciones de red o choques operativos.

## Estimación de factores

El estimador de Mack coincide con el factor Chain Ladder ponderado por volumen:

$$
\widehat f_j =
\frac{\sum_{i=1}^{n_j} C_{i,j+1}}
{\sum_{i=1}^{n_j} C_{i,j}}
$$

donde (n_j) es el número de pares observados para la transición (j\rightarrow j+1).

La proyección esperada se obtiene mediante:

$$
\widehat C_{i,j+1}=\widehat f_j C_{i,j}
$$

## Estimación de la varianza de desarrollo

Para una transición con al menos dos pares observados:

$$
\widehat\sigma_j^2 =
\frac{1}{n_j-1}
\sum_{i=1}^{n_j}
C_{i,j}
\left(
\frac{C_{i,j+1}}{C_{i,j}}-\widehat f_j
\right)^2
$$

Esta expresión mide la dispersión de los factores individuales alrededor del factor seleccionado, ponderada por el volumen.

Las últimas edades suelen tener pocas observaciones. Cuando no es posible estimar directamente una varianza, debe aplicarse una regla documentada, por ejemplo:

- extrapolación a partir de edades anteriores;
- suavizamiento;
- selección conservadora;
- exclusión de una edad inmaterial;
- análisis mediante escenarios.

## Dos fuentes de incertidumbre

### Riesgo de proceso

Representa la variación aleatoria del desarrollo futuro incluso si los factores verdaderos fueran conocidos.

En salud puede originarse en:

- oportunidad de radicación;
- auditoría y autorización;
- glosas y conciliaciones;
- fecha efectiva de pago;
- severidad de reclamaciones tardías;
- reaperturas y ajustes.

### Riesgo de parámetros

Surge porque los factores y las varianzas se estiman con una muestra histórica limitada. Es mayor cuando:

- el triángulo tiene pocas filas;
- las últimas edades tienen pocas observaciones;
- existen valores atípicos;
- la mezcla de negocio cambia;
- la historia disponible no representa el periodo actual.

## Error cuadrático medio de predicción

Para una reserva estimada $\widehat R$, el error cuadrático medio de predicción se interpreta como:

$$
\mathrm{MSEP}(\widehat R) = \text{varianza de proceso}
+
\text{varianza de parámetros}
$$

El error estándar de predicción es:

$$
SE(\widehat R)=
\sqrt{\mathrm{MSEP}(\widehat R)}
$$

El MSEP puede calcularse por periodo de origen y para la reserva total. El total no debe obtenerse sumando errores estándar; se agregan varianzas y covarianzas según las fórmulas del modelo y luego se toma la raíz cuadrada.

## Coeficiente de variación

Una medida relativa es:

$$
CV =
\frac{SE(\widehat R)}{\widehat R}
$$

El CV permite comparar incertidumbre entre segmentos de diferente tamaño. No tiene umbrales universales: su interpretación depende del portafolio, materialidad, uso del resultado y madurez del triángulo.

Un CV alto puede indicar:

- poca credibilidad;
- desarrollo inestable;
- reserva pequeña respecto del error estándar;
- segmentación inadecuada;
- cambios estructurales no modelados.

## Intervalos de predicción

Una aproximación normal produce:

$$
\widehat R \pm z_{1-\alpha/2}SE(\widehat R)
$$

Para un intervalo bilateral aproximado del 95 %, (z_{0.975}\approx1.96).

Esta aproximación puede generar límites inferiores negativos o no reflejar asimetría. Alternativas frecuentes incluyen:

- aproximación lognormal ajustada a la media y varianza;
- simulación Bootstrap;
- modelos paramétricos;
- escenarios actuariales.

El modelo de Mack estima los dos primeros momentos; la construcción de percentiles requiere una hipótesis adicional sobre la forma de la distribución.

## Ejemplo conceptual

Supóngase una reserva Chain Ladder de 100 y un error estándar de 15:

$$
CV=\frac{15}{100}=15\%
$$

Con aproximación normal, el intervalo bilateral del 95 % es:

$$
100 \pm 1.96(15)
$$

es decir, aproximadamente entre 70.6 y 129.4.

La lectura correcta no es que la reserva deba ubicarse necesariamente dentro de ese rango. El intervalo depende de los supuestos del modelo, de la calidad del triángulo y de la aproximación distributiva seleccionada.

## Diagnósticos antes de usar Mack

Mack hereda la estructura de Chain Ladder. Antes de interpretar su error estándar deben revisarse:

- estabilidad de factores edad-a-edad;
- residuos por periodo de origen y desarrollo;
- efectos de calendario;
- heterocedasticidad no representada;
- periodos de origen influyentes;
- cambios en operación, beneficios o contratación;
- suficiencia de observaciones en la cola;
- consistencia de la fecha de valuación.

Un error estándar pequeño no prueba que el modelo sea adecuado. Puede ser artificialmente bajo si existe un sesgo estructural que el modelo no reconoce.

## Consideraciones para seguros de salud

Los triángulos de salud suelen presentar cola corta, gran volumen y alta sensibilidad a procesos administrativos. Esto favorece el uso de Mack como indicador rápido y transparente, pero también genera riesgos específicos:

- cambios en radicación electrónica pueden modificar el patrón;
- glosas masivas pueden producir dependencia entre filas;
- contratos capitados y por evento no deben mezclarse sin análisis;
- epidemias o reformas pueden introducir efectos calendario;
- datos pagados e incurridos pueden tener estructuras de varianza distintas;
- meses incompletos pueden distorsionar las primeras edades.

Conviene estimar y comparar Mack sobre bases pagadas e incurridas cuando ambas tienen calidad suficiente.

## Implementación en Python

Con `chainladder`, una estructura típica es:

```python
import chainladder as cl

triangle = cl.Triangle(
    data,
    origin="origin_period",
    development="development_age",
    columns="cumulative_paid",
    cumulative=True,
)

model = cl.MackChainladder().fit(triangle)

ultimate = model.ultimate_
ibnr = model.ibnr_
standard_error = model.full_std_err_
```

La API exacta puede cambiar entre versiones. El entorno del proyecto debe fijar dependencias y validar los resultados contra un ejemplo conocido.

## Implementación en R

Con el paquete `ChainLadder`:

```r
library(ChainLadder)

fit <- MackChainLadder(
  Triangle = triangle,
  est.sigma = "Mack"
)

summary(fit)
plot(fit)
```

## Controles de producción

Una ejecución reproducible debe conservar:

1. triángulo de entrada y fecha de corte;
2. base pagada o incurrida;
3. segmentación;
4. factores observados y seleccionados;
5. varianzas por edad;
6. tratamiento de la última varianza;
7. tail factor y su incertidumbre;
8. ultimate e IBNR por origen;
9. MSEP, error estándar y CV;
10. método usado para intervalos;
11. diagnósticos y excepciones;
12. comparación con cierre anterior.

## Ventajas y limitaciones

### Ventajas

- conserva la estimación central de Chain Ladder;
- es rápido y transparente;
- separa conceptualmente proceso y parámetros;
- no requiere especificar una distribución completa;
- es un benchmark útil para modelos de simulación.

### Limitaciones

- depende de que Chain Ladder sea razonable;
- supone independencia entre periodos de origen;
- no modela directamente efectos de calendario;
- requiere decisiones para edades con poca información;
- no produce por sí solo una distribución predictiva completa;
- no captura automáticamente riesgo de modelo o cambio estructural.

## Buenas prácticas

- reportar la estimación puntual junto con su incertidumbre;
- evitar presentar el error estándar como garantía de suficiencia;
- explicar el método usado para convertir MSEP en percentiles;
- comparar resultados con Bootstrap;
- probar sensibilidad a factores y tail;
- documentar desviaciones de los supuestos;
- complementar el resultado con escenarios cuando existan cambios estructurales.

## Capítulos relacionados

Anterior: [Comparación de métodos clásicos](../part-02-classical-reserving/14-classical-reserving-methods-comparison.md).  
Siguiente: [Bootstrap Chain Ladder](09-bootstrap-chain-ladder.md).
