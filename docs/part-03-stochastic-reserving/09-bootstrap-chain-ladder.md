---
title: Bootstrap Chain Ladder
description: Guía práctica para obtener una distribución predictiva de reservas mediante remuestreo de residuos y simulación del riesgo de proceso.
status: draft
version: "0.1.7"
chapter: "09"
part: "part-03-stochastic-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Bootstrap Chain Ladder

Bootstrap Chain Ladder extiende Chain Ladder mediante simulación. En lugar de producir únicamente un ultimate y un IBNR, genera una distribución de resultados posibles que permite estimar percentiles, asimetría y probabilidad de insuficiencia.

El método no corrige un triángulo inadecuado. Su distribución predictiva es útil solo si la estructura central de Chain Ladder y las decisiones de simulación son razonables.

## Objetivos

Al finalizar este capítulo, el lector podrá:

- diferenciar riesgo de parámetros, proceso y modelo;
- explicar la formulación de Poisson sobredispersado;
- calcular e interpretar residuos;
- describir el algoritmo Bootstrap paso a paso;
- construir percentiles, VaR y TVaR empíricos;
- evaluar convergencia y error Monte Carlo;
- identificar decisiones metodológicas que afectan el resultado;
- reconocer riesgos particulares en seguros de salud.

## Relación con Chain Ladder

Bootstrap utiliza Chain Ladder como modelo central:

```text
Triángulo observado
        ↓
Ajuste Chain Ladder
        ↓
Valores ajustados y residuos
        ↓
Remuestreo de residuos
        ↓
Pseudo-triángulos
        ↓
Reestimación de factores
        ↓
Simulación de pagos futuros
        ↓
Distribución de ultimate e IBNR
```

La media de las simulaciones debe ser razonablemente cercana al Chain Ladder base. Diferencias materiales pueden revelar sesgos de implementación, tratamiento de negativos, selección de cola o una distribución de proceso mal calibrada.

## Fuentes de incertidumbre

### Riesgo de parámetros

Los factores se estiman con una historia finita. Bootstrap representa esta fuente al generar pseudo-triángulos y volver a estimar los factores en cada simulación.

### Riesgo de proceso

Incluso con parámetros conocidos, los pagos futuros son aleatorios. Se representa simulando cada celda futura alrededor de su media proyectada.

### Riesgo de modelo

Es la posibilidad de que la estructura seleccionada sea incorrecta. El Bootstrap estándar no lo captura completamente.

Ejemplos:

- efectos de calendario omitidos;
- segmentación insuficiente;
- cola no observada;
- dependencia entre periodos de origen;
- cambios en prácticas de pago;
- inflación o reforma estructural.

El riesgo de modelo debe tratarse con validación, modelos alternativos y escenarios.

## Formulación ODP

Una formulación frecuente utiliza un modelo de Poisson sobredispersado, conocido como ODP.

Sea (X_{i,j}) el valor incremental del periodo de origen (i) y desarrollo (j):

$$
E[X_{i,j}] = \mu_{i,j}
$$

$$
\mathrm{Var}(X_{i,j}) = \phi\mu_{i,j}
$$

donde $\phi$ es el parámetro de dispersión.

Una estructura multiplicativa es:

$$
\mu_{i,j}=\alpha_i\beta_j
$$

o, con enlace logarítmico:

$$
\log(\mu_{i,j})=a_i+b_j
$$

Bajo ciertas condiciones, esta formulación reproduce las estimaciones centrales de Chain Ladder.

## Valores ajustados

El Bootstrap suele trabajar sobre incrementales. Si $\widehat C_{i,j}$ es el acumulado ajustado:

$$
\widehat X_{i,0}=\widehat C_{i,0}
$$

$$
\widehat X_{i,j} = \widehat C_{i,j}-\widehat C_{i,j-1},
\qquad j>0
$$

Los incrementales ajustados representan la media estimada para las celdas observadas.

## Residuos de Pearson

Una definición habitual es:

$$
r_{i,j}=
\frac{X_{i,j}-\widehat X_{i,j}}
{\sqrt{\widehat X_{i,j}}}
$$

La dispersión puede estimarse como:

$$
\widehat\phi=
\frac{\sum_{i,j}r_{i,j}^2}{N-p}
$$

donde (N) es el número de celdas observadas y (p) el número efectivo de parámetros.

### Ajuste por grados de libertad

Como el modelo se estima con los mismos datos, los residuos brutos pueden subestimar la variabilidad. Una corrección común es:

$$
r_{i,j}^{adj} = r_{i,j}\sqrt{\frac{N}{N-p}}
$$

Otra opción utiliza el leverage de cada observación. La corrección seleccionada debe documentarse y aplicarse de manera consistente.

### Centrado

Antes del remuestreo puede centrarse el conjunto:

$$
\widetilde r_{i,j} = r_{i,j}^{adj}-\overline r^{adj}
$$

El centrado reduce el riesgo de introducir un sesgo sistemático en los pseudo-datos.

## Algoritmo Bootstrap

Para cada simulación (b=1,\ldots,B):

1. Remuestrear con reemplazo residuos ajustados.
2. Generar incrementales pseudo-observados.
3. Tratar celdas inválidas según una política definida.
4. Acumular el pseudo-triángulo.
5. Reestimar factores de desarrollo.
6. Proyectar el triángulo inferior.
7. Obtener las medias incrementales futuras.
8. Simular el riesgo de proceso.
9. Calcular ultimate e IBNR simulados.

Una construcción frecuente de pseudo-observaciones es:

$$
X_{i,j}^{*(b)} = \widehat X_{i,j}
+
r_{i,j}^{*(b)}\sqrt{\widehat X_{i,j}}
$$

El factor reestimado en la simulación (b) es:

$$
\widehat f_j^{*(b)} = \frac{\sum_i C_{i,j+1}^{*(b)}}
{\sum_i C_{i,j}^{*(b)}}
$$

La reserva total simulada es:

$$
R^{(b)}=
\sum_{i,j\in\text{futuro}}X_{i,j}^{proc,(b)}
$$

El conjunto $\{R^{(1)},\ldots,R^{(B)}\}$ aproxima la distribución predictiva bajo el modelo.

## Simulación del riesgo de proceso

### Gamma

Una elección frecuente para incrementales positivos es:

$$
X_{i,j}^{proc}
\sim
\mathrm{Gamma}
\left(
\text{forma}=\frac{\widehat\mu_{i,j}}{\widehat\phi},
\text{escala}=\widehat\phi
\right)
$$

Con esta parametrización:

$$
E[X_{i,j}^{proc}]=\widehat\mu_{i,j}
$$

$$
\mathrm{Var}(X_{i,j}^{proc}) = \widehat\phi\widehat\mu_{i,j}
$$

### Otras opciones

Según los datos pueden considerarse:

- Poisson sobredispersado;
- Tweedie;
- lognormal;
- modelos con frecuencia y severidad;
- simulación empírica segmentada.

La distribución de proceso no es una decisión puramente técnica. Debe ser coherente con el signo, dispersión y comportamiento de las celdas futuras.

## Resultados de la distribución

### Media, mediana y desviación estándar

La media simulada estima el valor esperado bajo el procedimiento. La mediana puede diferir cuando la distribución es asimétrica.

$$
\widehat{SE}_{boot}=\mathrm{sd}(R^{(1)},\ldots,R^{(B)})
$$

### Percentil o VaR

El percentil (q) se estima como:

$$
\mathrm{VaR}_q(R)=Q_q(R)
$$

### TVaR

El promedio de los resultados que exceden el percentil es:

$$
\mathrm{TVaR}_q(R) = E[R\mid R\ge Q_q(R)]
$$

### Probabilidad de insuficiencia

Para una reserva registrada (R_{booked}):

$$
P(R>R_{booked})
$$

Esta probabilidad debe interpretarse dentro del modelo; no incorpora automáticamente eventos estructurales omitidos.

## Número de simulaciones

El número requerido depende del uso. La media converge más rápido que los percentiles extremos.

Buenas prácticas:

- fijar una semilla reproducible;
- ejecutar al menos varios miles de simulaciones para exploración;
- usar más simulaciones para P95, P99 o TVaR;
- repetir el cálculo con semillas distintas;
- medir el error Monte Carlo;
- verificar estabilidad por segmento y total.

Una prueba sencilla compara estimaciones con (B), (2B) y (4B). Si el percentil objetivo cambia materialmente, la simulación aún no es estable.

## Valores negativos, ceros y ajustes

Los incrementales pueden ser negativos por reversos, recuperaciones, glosas o reclasificaciones. Truncarlos automáticamente en cero modifica la media y la varianza.

Antes de decidir debe distinguirse entre:

- error de datos;
- ajuste contable válido;
- recuperación;
- cambio de estimación;
- inestabilidad del modelo.

Posibles tratamientos:

- modelar positivos y negativos por separado;
- usar una distribución compatible con ambos signos;
- agrupar edades o segmentos;
- aplicar una transformación documentada;
- excluir un dato erróneo con trazabilidad;
- utilizar escenarios.

Los valores ajustados muy pequeños también generan residuos inestables y requieren revisión.

## Tail factor

Si el triángulo no alcanza ultimate, la cola debe incorporarse a la simulación. Una cola determinística subestima su contribución a la incertidumbre.

Debe documentarse:

- método de selección;
- fuente de información;
- distribución o escenarios de cola;
- dependencia con factores observados;
- sensibilidad del IBNR y percentiles.

## Dependencia y efectos de calendario

El remuestreo simple supone residuos aproximadamente intercambiables. Esto puede fallar cuando existe:

- inflación médica común;
- cambio regulatorio;
- migración de plataforma;
- choque epidémico;
- campaña de conciliación;
- concentración por prestador.

Alternativas incluyen remuestreo por bloques, modelos con efecto calendario, segmentación, GLM ampliados o escenarios correlacionados.

## Aplicación en seguros de salud

Bootstrap es útil cuando la distribución de reservas es asimétrica o cuando se necesitan percentiles para capital, solvencia y apetito de riesgo.

La implementación debe considerar:

- radicación y pago en periodos cortos;
- estacionalidad de utilización;
- grandes reclamaciones;
- glosas y recobros;
- cambios en red de prestadores;
- diferencias entre pagado e incurrido;
- contratos capitados, prospectivos y por evento;
- exposición y mezcla de población.

Una práctica defendible es ejecutar modelos separados por segmentos homogéneos y agregar resultados incorporando la dependencia relevante.

## Implementación en Python

Un flujo ilustrativo con `chainladder` es:

```python
import chainladder as cl

bootstrap = cl.BootstrapODPSample(
    n_sims=25_000,
    random_state=20260714,
)

simulated_triangles = bootstrap.fit_transform(triangle)
models = cl.Chainladder().fit(simulated_triangles)

ibnr_simulations = models.ibnr_
```

Para resultados almacenados como un arreglo unidimensional:

```python
import numpy as np

values = np.asarray(ibnr_simulations, dtype=float).ravel()

summary = {
    "mean": float(values.mean()),
    "std": float(values.std(ddof=1)),
    "p50": float(np.quantile(values, 0.50)),
    "p75": float(np.quantile(values, 0.75)),
    "p95": float(np.quantile(values, 0.95)),
    "p99": float(np.quantile(values, 0.99)),
}

var_95 = summary["p95"]
tvar_95 = float(values[values >= var_95].mean())
```

La forma exacta del objeto y la API dependen de la versión instalada. Deben fijarse dependencias y probar el resultado contra un caso controlado.

## Implementación en R

Con el paquete `ChainLadder`:

```r
library(ChainLadder)

set.seed(20260714)

fit <- BootChainLadder(
  Triangle = triangle,
  R = 25000,
  process.distr = "gamma"
)

simulations <- fit$IBNR.Totals

quantile(
  simulations,
  probs = c(0.50, 0.75, 0.95, 0.99)
)
```

## Validación y backtesting

### Holdout de diagonal

Se retira una diagonal conocida, se ajusta el modelo con la información anterior y se compara la predicción con lo observado.

### Backtesting por fecha de corte

Para cada cierre histórico:

1. reconstruir la información disponible;
2. ejecutar el modelo;
3. observar el desarrollo posterior;
4. ubicar el resultado real dentro de la distribución predicha;
5. medir sesgo y cobertura.

### Prueba de calibración

Si se producen intervalos del 90 % o 95 %, su cobertura histórica debe revisarse. Una cobertura baja puede indicar subestimación de incertidumbre o sesgo del modelo.

## Controles de producción

Conservar como mínimo:

1. triángulo de entrada;
2. factores y valores ajustados;
3. definición y corrección de residuos;
4. parámetro de dispersión;
5. distribución de proceso;
6. número de simulaciones y semilla;
7. tratamiento de negativos y ceros;
8. método de cola;
9. resultados por origen y total;
10. media, desviación, CV y percentiles;
11. error Monte Carlo;
12. validación y comparación con Mack;
13. versiones de código y dependencias.

## Ventajas y limitaciones

### Ventajas

- produce una distribución predictiva empírica;
- permite intervalos asimétricos;
- entrega percentiles, VaR y TVaR;
- integra riesgo de parámetros y proceso;
- facilita escenarios de suficiencia;
- sirve como contraste del resultado de Mack.

### Limitaciones

- hereda supuestos de Chain Ladder;
- es sensible a outliers y residuos no intercambiables;
- requiere varias decisiones de implementación;
- puede ser computacionalmente intensivo;
- no incorpora automáticamente riesgo estructural;
- puede ser inestable con triángulos pequeños;
- necesita tratamiento cuidadoso de cola, ceros y negativos.

## Buenas prácticas

- validar Chain Ladder antes de simular;
- separar riesgo de parámetros y de proceso;
- fijar semilla y versiones;
- revisar convergencia de percentiles;
- comparar media Bootstrap con Chain Ladder;
- contrastar error estándar con Mack;
- documentar todas las transformaciones;
- complementar con escenarios cuando cambie el entorno.

## Capítulos relacionados

Anterior: [Chain Ladder de Mack](08-mack-chain-ladder.md).  
Siguiente: [Comparación entre Mack y Bootstrap](10-comparing-mack-vs-bootstrap.md).
