---
title: "Demo 3 · Triángulos mensuales de reclamaciones pagadas de salud"
description: "Demo r2 con base 72×36, vista tradicional 36×36, runoff simulado, cola explícita y terminología actuarial precisa."
chapter: "demo-03"
part: "examples"
language: "es"
status: "review"
version: "0.6.0-r2"
last_updated: "2026-07-18"
---

# Demo 3 · Triángulos mensuales de reclamaciones pagadas de salud

Este demo genera datos sintéticos pagados, estima factores mensuales y completa el triángulo con Chain Ladder. La revisión r2 separa tres conceptos que no deben confundirse:

- **base de estimación:** 72 meses de origen × 36 edades de desarrollo (`dev_0` a `dev_35`);
- **vista tradicional:** últimos 36 meses de origen × las mismas 36 edades;
- **runoff simulado:** pagos completos hasta `dev_48`, usados para sustentar y validar una cola sintética 35→48.

!!! warning "Nombre correcto del resultado"
    Con un triángulo agregado exclusivamente pagado, la diferencia entre el costo estimado y el pagado observado se denomina en este demo **pasivo no pagado estimado**. No puede identificarse por separado el IBNR puro, la reserva de siniestros reportados pendientes (RBNS) ni el IBNER sin información adicional.

## 1. Por qué la base es 72×36 y la vista 36×36

Una matriz 36×36 es una presentación mensual tradicional: 36 periodos de origen y 36 edades. Sin embargo, al corte de valuación solo una fila aporta el enlace más tardío 34→35. Esto es insuficiente como argumento para seleccionar un factor estable.

Por eso r2 utiliza seis años de orígenes para estimar:

| Elemento | Dimensión | Uso |
|---|---:|---|
| Base completa | 72×36 | estimación de factores y diagnósticos |
| Vista tradicional | 36×36 | lectura y comunicación del triángulo |
| Runoff sintético | 72×49 | verdad conocida del generador, no entrada observable |

En la base 72×36, el enlace 34→35 conserva 37 observaciones. Esto mejora el ejercicio, pero no constituye un mínimo actuarial universal: todavía deben revisarse homogeneidad, cambios operativos, volumen, dispersión, estacionalidad y estabilidad temporal.

![Vista actuarial tradicional 36×36](../assets/demo_triangulos_mensuales/triangulo_pagado_mensual_acumulado.svg)

## 2. Edad terminal y cola

La proyección observada termina en edad 35. El generador, por ser sintético, conoce pagos hasta edad 48. Su factor de cola es:

$$
f_{35\rightarrow48}^{cola}=\frac{C_{48}^{simulado}}{C_{35}^{simulado}}
$$

Con la parametrización predeterminada es aproximadamente `1.00524958`. El resultado anterior a la cola se llama **acumulado proyectado a edad 35**. Solo después de aplicar la cola explícita se presenta como **costo final técnico estimado**.

![Maduración pagada y cola](../assets/demo_triangulos_mensuales/curva_maduracion_mensual.svg)

En datos reales, una cola no se obtiene por declarar que la última edad es suficiente. Debe sustentarse con runoff posterior, segmentos comparables, estudios externos pertinentes o una metodología documentada.

## 3. Qué se puede estimar

Para cada origen $i$, con último acumulado observado $P_{i,k}$:

$$
\widehat{C}_{i,35}=P_{i,k}\times CDF_{k\rightarrow35}
$$

$$
\widehat{C}_{i,final}=\widehat{C}_{i,35}\times f_{35\rightarrow48}^{cola}
$$

$$
\widehat{L}_{i,no\ pagado}=\widehat{C}_{i,final}-P_{i,k}
$$

El código **no aplica un piso de cero** al residual. Un valor negativo permanece visible y requiere investigar recuperaciones, ajustes, cambios de definición o factores menores que uno.

## 4. Qué falta para una estimación más realista

Un archivo real debería incorporar o reconciliar, cuando corresponda:

- fecha de ocurrencia, fecha de reporte/aviso y fecha de pago;
- reserva caso o incurrido reportado;
- estado, cierre y reapertura de la reclamación;
- exposición y costo esperado independiente para BF/Benktander;
- cobertura, prestador, contrato, región y población homogénea;
- bruto/neto, recuperaciones y marcas de reclamaciones grandes;
- runoff posterior para la cola;
- cambios de tarifas, beneficios, adjudicación y procesos operativos.

Sin fecha de reporte y reserva caso no se separan IBNR puro, RBNS e IBNER. Sin cola sustentada, no corresponde denominar costo final al acumulado de edad 35.

## 5. Suficiencia por factor

![Observaciones por factor](../assets/demo_triangulos_mensuales/observaciones_por_factor.svg)

La línea de 24 observaciones es una heurística didáctica, no un estándar profesional. El conteo es solo una señal: la calidad y representatividad de esas observaciones importan tanto como su cantidad.

## 6. Archivos r2

| Archivo | Interpretación |
|---|---|
| `triangulo_pagado_mensual_acumulado.csv` | base completa 72×36 |
| `vista_tradicional_36x36.csv` | últimos 36 orígenes para presentación |
| `triangulo_pagado_mensual_incremental.csv` | pagos incrementales observados |
| `factores_mensuales_edad_a_edad.csv` | factores a edad 35 y conteos |
| `resultados_proyeccion_pasivo_no_pagado.csv` | costo a edad 35, cola, costo final y pasivo no pagado |
| `prior_bornhuetter_ferguson_mensual.csv` | prior sintético compatible con Demo 6 |
| `diagnostico_suficiencia.csv` | dimensiones y evidencia por enlace |

Los nombres antiguos `ibnr_estimado` y `ultimate_estimado` se retiraron de estas salidas para evitar expectativas que los datos no soportan.

## 7. Reproducción

```bash
python scripts/generate_demo_monthly_triangles.py --language es
```

El diseño documentado fija edades 0–35 y runoff 0–48. Cambiarlos exige revisar patrón, cola, pruebas y documentación.

## 8. Uso profesional

El demo es educativo y sintético. No constituye una reserva contable, una opinión actuarial ni una recomendación universal de 72×36. Antes de usar datos propios se requiere reconciliación, selección de segmentos, justificación de factores y cola, backtesting, sensibilidad y revisión independiente.
