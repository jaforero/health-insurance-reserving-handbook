---
title: "Método Bornhuetter-Ferguson"
description: "Especificación actuarial, datos, fórmulas, sensibilidad y gobierno del método Bornhuetter-Ferguson para reservas de salud."
chapter: "11"
part: "02-classical-reserving"
language: "es"
status: "review"
version: "0.6.0"
last_updated: "2026-07-17"
tags:
  - bornhuetter-ferguson
  - prior
  - chain-ladder
  - ibnr
  - salud
---

# Método Bornhuetter-Ferguson

## 1. Propósito

Bornhuetter-Ferguson (BF) combina dos fuentes distintas:

- el desarrollo observado, usado para estimar qué proporción ya emergió;
- una expectativa previa de costo último, usada únicamente sobre la proporción pendiente.

Por esta razón suele ser útil para periodos recientes, donde Chain Ladder puede reaccionar de forma extrema a un observado todavía pequeño. BF no elimina la necesidad de validar el patrón ni convierte un prior débil en evidencia confiable.

## 2. Notación

Para el periodo de origen $i$:

- $C_i$: acumulado observado a la edad actual;
- $CDF_i$: factor desde la edad actual hasta ultimate;
- $p_i$: proporción desarrollada;
- $q_i$: proporción no desarrollada;
- $U_i^{prior}$: ultimate esperado antes de aplicar la experiencia emergente;
- $U_i^{BF}$: ultimate BF;
- $R_i^{BF}$: IBNR BF.

La madurez se obtiene del patrón de desarrollo:

$$
p_i = \frac{1}{CDF_i}
$$

$$
q_i = 1 - p_i
$$

Cuando el CDF es menor que uno, $q_i$ es negativo. El motor debe mostrarlo y exigir interpretación; no debe corregirlo silenciosamente.

## 3. Construcción del prior

### 3.1 Ultimate directo

El usuario puede suministrar una expectativa última por origen:

$$
U_i^{prior}
$$

La fuente puede ser presupuesto, pricing, forecast, estudio de frecuencia y severidad u otra estimación independiente. Debe documentarse unidad, fecha, alcance, ajustes y responsable.

### 3.2 Exposición por tasa

Si existe una exposición $E_i$ y una tasa esperada $r_i$:

$$
U_i^{prior} = E_i r_i
$$

En salud, ejemplos de exposición incluyen miembros-mes o contratos-mes; la tasa debe estar expresada en una unidad compatible. Si la tasa proviene del mismo triángulo sin una separación metodológica clara, la independencia del prior puede ser aparente.

### 3.3 Ajustes de comparabilidad

Antes de usar el prior se revisan:

- tendencia y fecha de nivel;
- cambios de beneficio, red, deducibles y copagos;
- mezcla de producto, región, prestador y población;
- grandes reclamaciones, reaseguro, recuperaciones y glosas;
- moneda, inflación y unidades;
- consistencia entre periodos de exposición y ocurrencia.

## 4. Fórmulas

BF aplica el prior solo a la porción pendiente:

$$
R_i^{BF} = q_i U_i^{prior}
$$

$$
U_i^{BF} = C_i + R_i^{BF}
$$

En contraste, Chain Ladder estima:

$$
U_i^{CL} = \frac{C_i}{p_i}
$$

$$
R_i^{CL} = U_i^{CL} - C_i
$$

Una representación equivalente muestra los pesos:

$$
U_i^{BF} = p_i U_i^{CL} + q_i U_i^{prior}
$$

Esta igualdad no significa que se promedien dos reservas independientes: ambos términos comparten el patrón que determina $p_i$.

## 5. Ejemplo numérico

Supóngase:

- acumulado observado: $C_i = 72$;
- CDF: $1.25$;
- madurez: $p_i = 0.80$;
- prior de ultimate: $U_i^{prior} = 100$.

Entonces:

$$
q_i = 1 - 0.80 = 0.20
$$

$$
R_i^{BF} = 0.20 \times 100 = 20
$$

$$
U_i^{BF} = 72 + 20 = 92
$$

Para Chain Ladder:

$$
U_i^{CL} = \frac{72}{0.80} = 90
$$

$$
R_i^{CL} = 90 - 72 = 18
$$

BF supera a Chain Ladder en 2 porque el prior de 100 es mayor que el ultimate implícito de 90. Para un origen maduro, $q_i$ sería menor y la diferencia se reduciría.

## 6. Sensibilidad del prior

Para un shock multiplicativo $s$:

$$
U_{i,s}^{prior} = s U_i^{prior}
$$

$$
R_{i,s}^{BF} = q_i s U_i^{prior}
$$

La sensibilidad absoluta frente al escenario base es:

$$
Impacto_{i,s} = q_i U_i^{prior}(s-1)
$$

La sensibilidad es mayor para orígenes inmaduros. Los shocks deben reflejar riesgos plausibles y no elegirse únicamente para producir un rango deseado.

## 7. Diagnósticos

### 7.1 Patrón de desarrollo

BF depende de $p_i$. Deben aplicarse los diagnósticos de suficiencia, estabilidad, calendario y backtesting descritos en [Diagnósticos de Chain Ladder](07-chain-ladder-diagnostics.md).

### 7.2 Prior

Por origen se revisa:

- conciliación exacta de periodos;
- valores faltantes, duplicados o negativos;
- fecha y unidad de la tasa;
- trazabilidad de ajustes;
- comparación de prior contra experiencia histórica en base comparable;
- independencia frente al observado;
- concentración del IBNR en periodos recientes.

### 7.3 Comparación con Chain Ladder

La diferencia firmada es:

$$
Delta_i = U_i^{BF} - U_i^{CL}
$$

Como ambos parten del mismo $C_i$:

$$
Delta_i = R_i^{BF} - R_i^{CL}
$$

La explicación debe separar diferencias por prior, madurez, cola, segmentación y selección de factores.

## 8. Datos y contrato de implementación

El cálculo reproducible requiere una fila por periodo de origen con:

| Campo | Requisito |
|---|---|
| periodo de origen | único y conciliado con el triángulo |
| acumulado observado | misma medida y moneda del patrón |
| CDF o madurez | derivado de factores seleccionados documentados |
| ultimate directo | requerido en modo directo |
| exposición y tasa | requeridos en modo exposición por tasa |
| metadatos | fuente, fecha, unidad, versión y ajustes |

El resultado conserva insumos normalizados, configuración, diagnósticos, sensibilidad y hashes. Los archivos fuente del usuario no deben incorporarse al repositorio ni al ZIP de resultados.

## 9. Limitaciones

BF puede ser poco confiable cuando:

- el prior no es comparable o no tiene trazabilidad;
- la exposición no corresponde al periodo de riesgo;
- el patrón cambia materialmente;
- el portafolio es heterogéneo y no está segmentado;
- el CDF o la cola carecen de soporte;
- grandes reclamaciones dominan el resultado;
- el prior se ajusta retrospectivamente para coincidir con la respuesta deseada.

BF determinístico no cuantifica por sí solo incertidumbre de parámetros, proceso ni modelo.

## 10. Relación con Demo 6

Demo 6 implementa el contrato descrito: prior directo o exposición por tasa, conciliación por origen, cálculo BF posterior a Chain Ladder, shocks, comparación firmada y exportación auditable. La documentación del método debe permanecer sincronizada con:

- `src/health_reserving/bornhuetter_ferguson.py`;
- `tests/test_bornhuetter_ferguson.py`;
- [Demo 6](../examples/06-demo-chain-ladder-datos-propios.md).

## 11. Referencias y alcance profesional

- [Método Chain Ladder](06-chain-ladder-method.md)
- [Método Benktander](12-benktander-method.md)
- [Método Cape Cod](13-cape-cod-method.md)
- [Comparación de métodos clásicos](14-classical-reserving-methods-comparison.md)
- [Bibliografía y evidencia](../bibliography.md)

Las referencias principales son `BORN-FERGUSON-1972` y `FRIEDLAND-2010`. Los principios de propósito, calidad de datos, supuestos, pruebas, documentación, sensibilidad y seguimiento se apoyan en `ASB-ASOP01-2013`, `ASB-ASOP28-2024` y `ASB-ASOP56-2019`. Estas fuentes no sustituyen la normativa colombiana ni la política actuarial de la entidad.
