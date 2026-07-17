---
title: "Método Benktander"
description: "Derivación, forma cerrada, criterios de iteración y especificación reproducible del método Benktander."
chapter: "12"
part: "02-classical-reserving"
language: "es"
status: "review"
version: "0.6.0"
last_updated: "2026-07-17"
tags:
  - benktander
  - bornhuetter-ferguson
  - chain-ladder
  - ibnr
---

# Método Benktander

## 1. Propósito

Benktander actualiza iterativamente la expectativa previa de Bornhuetter-Ferguson. Cada iteración usa como nuevo prior el ultimate estimado en la iteración anterior. El resultado se desplaza de forma controlada desde el prior inicial hacia Chain Ladder.

El método es útil para estudiar cuánto depende la reserva de una expectativa externa y cuánto de la experiencia emergente. El número de iteraciones es un supuesto visible; no debe elegirse para alcanzar una cifra predeterminada.

## 2. Notación

Para un periodo de origen $i$:

- $C_i$: acumulado observado;
- $p_i$: proporción desarrollada;
- $q_i = 1-p_i$: proporción no desarrollada;
- $U_i^{(0)}$: prior inicial;
- $U_i^{(n)}$: ultimate después de $n$ iteraciones;
- $U_i^{CL} = C_i/p_i$: ultimate Chain Ladder.

Se requiere $p_i > 0$. Cuando $p_i = 1$, el periodo está completamente desarrollado y todos los métodos producen $U_i = C_i$.

## 3. Recurrencia

La primera iteración corresponde a Bornhuetter-Ferguson:

$$
U_i^{(1)} = C_i + q_i U_i^{(0)}
$$

Las iteraciones siguientes aplican la misma estructura:

$$
U_i^{(n)} = C_i + q_i U_i^{(n-1)}
$$

La reserva en cada iteración es:

$$
R_i^{(n)} = U_i^{(n)} - C_i
$$

## 4. Forma cerrada

Como $C_i = p_i U_i^{CL}$, la recurrencia tiene solución:

$$
U_i^{(n)} = (1-q_i^n)U_i^{CL} + q_i^n U_i^{(0)}
$$

Los pesos suman uno. El peso del prior inicial es $q_i^n$ y el peso de Chain Ladder es $1-q_i^n$.

Si $0 \le q_i < 1$:

$$
\lim_{n \to \infty} U_i^{(n)} = U_i^{CL}
$$

La convergencia es más rápida en periodos maduros porque $q_i$ es pequeño. En periodos recientes, el prior conserva peso durante más iteraciones.

## 5. Ejemplo numérico

Use el mismo caso del capítulo BF:

- $C_i = 72$;
- $p_i = 0.80$;
- $q_i = 0.20$;
- $U_i^{(0)} = 100$;
- $U_i^{CL} = 90$.

| Iteración | Cálculo | Ultimate | IBNR |
|---:|---|---:|---:|
| 0 | prior inicial | 100.00 | 28.00 |
| 1 | $72 + 0.20(100)$ | 92.00 | 20.00 |
| 2 | $72 + 0.20(92)$ | 90.40 | 18.40 |
| 3 | $72 + 0.20(90.40)$ | 90.08 | 18.08 |
| límite | Chain Ladder | 90.00 | 18.00 |

La forma cerrada para dos iteraciones confirma:

$$
U_i^{(2)} = (1-0.20^2)(90) + 0.20^2(100) = 90.40
$$

## 6. Selección del número de iteraciones

El número $n$ debe definirse y revelarse. La decisión puede considerar:

- madurez del origen;
- independencia y credibilidad del prior;
- estabilidad y backtesting del patrón;
- materialidad de la diferencia entre prior y Chain Ladder;
- consistencia con la política metodológica;
- facilidad de explicación y reproducción.

Una política uniforme de una o dos iteraciones puede ser operativamente sencilla, pero no es universalmente superior. Usar diferentes $n$ por segmento u origen exige una regla previa y trazable.

## 7. Sensibilidad

La comparación mínima incluye $n=0$, $n=1$, $n=2$, $n=3$ y Chain Ladder. El cambio entre iteraciones es:

$$
U_i^{(n)} - U_i^{(n-1)} = p_i q_i^{n-1}(U_i^{CL} - U_i^{(0)})
$$

La dirección del cambio depende de si Chain Ladder está por encima o por debajo del prior. También deben evaluarse shocks al prior y al patrón; variar únicamente $n$ subestima la incertidumbre del modelo.

## 8. Diagnósticos

Antes de aplicar Benktander se requiere:

1. validar el triángulo y el patrón;
2. conciliar y documentar el prior;
3. revisar $p_i$ y $q_i$ por origen;
4. explicar CDF menores que uno o madurez fuera de $[0,1]$;
5. comparar resultados por origen y total;
6. comprobar la forma iterativa contra la forma cerrada;
7. ejecutar sensibilidad y backtesting.

Una prueba de implementación esencial es que ambas fórmulas produzcan el mismo resultado dentro de la tolerancia numérica definida.

## 9. Contrato de implementación para v0.6.0

El incremento propuesto para Demo 6 debe:

- reutilizar sin modificar el resultado Chain Ladder y el prior BF ya conciliado;
- aceptar un entero no negativo de iteraciones;
- calcular resultado iterativo y forma cerrada;
- mostrar pesos de Chain Ladder y del prior;
- producir ultimate e IBNR por origen y total;
- exportar configuración, resultados, sensibilidad y diagnósticos;
- probar casos maduros, inmaduros, múltiples iteraciones y entradas inválidas.

Hasta que ese código y sus pruebas se integren, este capítulo funciona como especificación técnica y no como afirmación de funcionalidad disponible.

## 10. Limitaciones

Benktander comparte las limitaciones de Chain Ladder y BF. Además:

- la iteración no crea información nueva;
- un prior sesgado puede seguir influyendo materialmente;
- un patrón inestable atrae el resultado hacia un benchmark débil;
- la convergencia a Chain Ladder no demuestra que Chain Ladder sea correcto;
- el método determinístico no cuantifica incertidumbre de proceso o parámetros.

## 11. Referencias y alcance profesional

- [Diagnósticos de Chain Ladder](07-chain-ladder-diagnostics.md)
- [Bornhuetter-Ferguson](11-bornhuetter-ferguson.md)
- [Cape Cod](13-cape-cod-method.md)
- [Comparación de métodos clásicos](14-classical-reserving-methods-comparison.md)
- [Demo 6](../examples/06-demo-chain-ladder-datos-propios.md)
- [Bibliografía y evidencia](../bibliography.md)

La aplicación se apoya en `FRIEDLAND-2010` y en los principios generales de `ASB-ASOP01-2013`, `ASB-ASOP28-2024` y `ASB-ASOP56-2019`. La selección de iteraciones y la aptitud del método son decisiones profesionales dependientes del propósito, los datos y la jurisdicción.
