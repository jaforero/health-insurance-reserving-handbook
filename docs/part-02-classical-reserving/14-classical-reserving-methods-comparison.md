---
title: "Comparación de métodos clásicos de reservas"
description: "Marco reconciliado para comparar Chain Ladder, Bornhuetter-Ferguson, Benktander y Cape Cod por origen, total, sensibilidad y backtesting."
chapter: "14"
part: "02-classical-reserving"
language: "es"
status: "review"
version: "0.6.0"
last_updated: "2026-07-17"
tags:
  - chain-ladder
  - bornhuetter-ferguson
  - benktander
  - cape-cod
  - comparacion
---

# Comparación de métodos clásicos de reservas

## 1. Propósito

Comparar métodos no consiste en presentar cuatro totales sin reconciliación. Todos deben partir del mismo corte, alcance, moneda, medida, segmentación y observado. Las diferencias se explican por patrón, prior, exposición, tasa, madurez y reglas de selección.

Este capítulo define un contrato común para Chain Ladder (CL), Bornhuetter-Ferguson (BF), Benktander (BK) y Cape Cod (CC).

## 2. Base común

Para cada origen $i$ se conserva:

- $C_i$: acumulado observado;
- $p_i$: proporción desarrollada;
- $q_i=1-p_i$: proporción pendiente;
- $U_i^{prior}$: prior BF y Benktander;
- $E_i^*$: exposición ajustada Cape Cod;
- $r$: tasa Cape Cod;
- $n$: número de iteraciones Benktander.

Los ultimates son:

$$
U_i^{CL} = \frac{C_i}{p_i}
$$

$$
U_i^{BF} = C_i + q_i U_i^{prior}
$$

$$
U_i^{BK(n)} = (1-q_i^n)U_i^{CL} + q_i^n U_i^{prior}
$$

$$
U_i^{CC} = C_i + q_i E_i^* r
$$

Para cualquier método $m$:

$$
R_i^m = U_i^m - C_i
$$

## 3. Interpretación de los pesos

| Método | Fuente principal para la parte pendiente | Comportamiento |
|---|---|---|
| Chain Ladder | experiencia emergente proyectada por el patrón | sensible a orígenes inmaduros y factores |
| BF | prior externo | reduce dependencia del observado reciente |
| Benktander | mezcla iterativa de prior y CL | converge a CL al aumentar iteraciones |
| Cape Cod | tasa estimada con exposición y experiencia agregada | estabiliza usando una tasa común |

El método más complejo no es necesariamente el más adecuado. La selección depende de la calidad relativa de cada fuente.

## 4. Ejemplo reconciliado por origen

Supóngase:

- $C_i=72$;
- $p_i=0.80$ y $q_i=0.20$;
- $U_i^{prior}=100$;
- Benktander con $n=2$;
- exposición ajustada $E_i^*=1000$;
- tasa Cape Cod $r=0.095$.

| Método | Ultimate | IBNR | Explicación |
|---|---:|---:|---|
| Chain Ladder | 90.00 | 18.00 | $72/0.80$ |
| BF | 92.00 | 20.00 | $72+0.20(100)$ |
| Benktander 2 | 90.40 | 18.40 | $0.96(90)+0.04(100)$ |
| Cape Cod | 91.00 | 19.00 | $72+0.20(1000)(0.095)$ |

Como el observado es común, las diferencias de ultimate son exactamente iguales a las diferencias de IBNR.

## 5. Reconciliación por origen y total

La salida debe incluir una fila por origen y método con:

| Campo | Descripción |
|---|---|
| origen | periodo reconciliado |
| edad actual | última edad observada |
| observado | $C_i$ |
| CDF y madurez | patrón común |
| prior | ultimate BF/BK, si aplica |
| exposición y tasa | Cape Cod, si aplica |
| iteraciones | Benktander, si aplica |
| ultimate | estimación del método |
| IBNR | ultimate menos observado |
| diferencia contra CL | firmada, no absoluta |

El total debe reconciliarse:

$$
U_{total}^m = \sum_i U_i^m
$$

$$
R_{total}^m = \sum_i R_i^m = U_{total}^m - \sum_i C_i
$$

Una diferencia firmada respecto de CL es:

$$
Delta_i^m = R_i^m - R_i^{CL}
$$

Los métodos son estimaciones alternativas y no deben presentarse en gráficos apilados.

## 6. Matriz de selección

| Condición | CL | BF | Benktander | Cape Cod |
|---|---|---|---|---|
| patrón estable y origen maduro | fuerte candidato | útil como contraste | cercano a CL | útil si exposición es confiable |
| origen muy reciente | puede ser volátil | útil con prior robusto | controla transición | útil con exposición homogénea |
| prior independiente fuerte | no lo usa | fuerte candidato | permite credibilidad gradual | puede servir de contraste |
| exposición confiable, prior externo débil | no la usa | limitado | limitado | fuerte candidato |
| cambios estructurales no ajustados | débil | débil | débil | débil |
| patrón inestable | débil | también afecta madurez | también afecta pesos | afecta tasa y madurez |

La tabla orienta preguntas; no determina automáticamente el método seleccionado.

## 7. Comparación diagnóstica

### 7.1 Patrón común

Todos los métodos dependen directa o indirectamente de $p_i$. Se revisan suficiencia, estabilidad, calendario, cola y backtesting antes de comparar resultados.

### 7.2 Priors y exposición

BF y Benktander requieren un prior trazable. Cape Cod requiere exposición comparable y una tasa estable. Las fuentes deben conciliarse por origen y conservar metadatos.

### 7.3 Madurez

Las diferencias deben analizarse por banda de madurez. Un total puede ocultar compensaciones entre orígenes recientes y antiguos.

### 7.4 Segmentación

La comparación debe repetirse en segmentos actuarialmente relevantes cuando el volumen lo permita. Agregar poblaciones con patrones o tasas distintas puede crear una aparente estabilidad.

## 8. Backtesting común

En cada corte retrospectivo se recalculan todos los insumos usando solo información disponible en ese corte:

1. patrón y cola;
2. prior o su versión histórica;
3. exposición y factores de nivel;
4. tasa Cape Cod;
5. número o política de iteraciones.

Se reportan error firmado, error absoluto, WAPE y runoff bajo la misma convención. Un método no debe recibir información retrospectiva más reciente que otro.

## 9. Sensibilidad común

La matriz mínima de escenarios incluye:

- patrón: reglas alternativas y exclusiones;
- cola: base, inferior y superior;
- BF/BK: shocks al prior;
- BK: iteraciones;
- CC: ventana, tendencia, exposición y tasa;
- segmentación: agregado frente a segmentos;
- medida: pagado frente a incurrido, cuando ambos son confiables.

Cada escenario conserva configuración, versión y resultado por origen. El rango no es un intervalo de confianza.

## 10. Selección y conclusión

Una conclusión profesional debe indicar:

- propósito y uso;
- método central y métodos de contraste;
- razones de selección;
- datos y supuestos materiales;
- resultados por origen y total;
- sensibilidades y backtests;
- limitaciones e incertidumbre;
- reconciliación y aprobación.

No se recomienda promediar métodos mecánicamente sin una justificación de pesos. Si se selecciona un punto dentro de un rango, la regla debe ser reproducible y no depender solo del resultado deseado.

## 11. Estado de implementación

| Componente | Estado en Demo 6 al inicio del sprint |
|---|---|
| Chain Ladder | implementado y probado |
| Bornhuetter-Ferguson | implementado y probado |
| Benktander | especificado en este paquete; implementación pendiente |
| Cape Cod | especificado en este paquete; implementación pendiente |
| backtesting ampliado | especificado; implementación pendiente |
| comparación de cuatro métodos | contrato definido; implementación pendiente |

Esta separación evita confundir documentación objetivo con funcionalidad ya disponible.

## 12. Criterios de aceptación para v0.6.0

La comparación clásica estará completa cuando:

1. los cuatro métodos usen una base reconciliada;
2. las fórmulas tengan pruebas numéricas;
3. existan resultados por origen y total;
4. las diferencias se expliquen mediante insumos visibles;
5. sensibilidad y backtesting sean reproducibles;
6. los ZIP no contengan archivos fuente privados;
7. documentación, pruebas, auditorías y build estricto estén limpios.

## 13. Referencias y alcance profesional

- [Diagnósticos de Chain Ladder](07-chain-ladder-diagnostics.md)
- [Bornhuetter-Ferguson](11-bornhuetter-ferguson.md)
- [Benktander](12-benktander-method.md)
- [Cape Cod](13-cape-cod-method.md)
- [Demo 6](../examples/06-demo-chain-ladder-datos-propios.md)
- [Bibliografía y evidencia](../bibliography.md)

Las referencias metodológicas principales son `BORN-FERGUSON-1972` y `FRIEDLAND-2010`. El marco de propósito, materialidad, razonabilidad, pruebas, sensibilidad, documentación y seguimiento se apoya en `ASB-ASOP01-2013`, `ASB-ASOP28-2024`, `ASB-ASOP43-2007` y `ASB-ASOP56-2019`. ASOP 43 se usa únicamente como referencia análoga; ninguna de estas fuentes reemplaza la normativa colombiana aplicable.
