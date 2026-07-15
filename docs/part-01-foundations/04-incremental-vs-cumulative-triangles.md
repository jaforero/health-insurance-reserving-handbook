---
title: Triángulos incrementales vs. acumulados
description: Comparación práctica entre triángulos incrementales y acumulados, sus usos, riesgos y transformaciones en reserving actuarial de salud.
status: draft
version: "0.1.5"
chapter: "04"
part: "part-01-foundations"
language: "es"
last_updated: "2026-07-14"
---

# Triángulos incrementales vs. acumulados

Los triángulos pueden presentarse en forma incremental o acumulada. Ambos describen la misma experiencia, pero responden preguntas distintas. La forma incremental muestra cuánto ocurre en cada edad de desarrollo. La forma acumulada muestra cuánto se ha observado hasta esa edad.

En reserving, confundir estas dos estructuras produce errores materiales. Muchos métodos clásicos se aplican sobre acumulados, pero gran parte del diagnóstico se entiende mejor con incrementales.

## Definición incremental

Un triángulo incremental contiene el monto observado en una edad específica de desarrollo:

$$
X_{i,j}
$$

donde:

- \(i\) es el periodo de origen;
- \(j\) es la edad de desarrollo;
- \(X_{i,j}\) es el pago, incurrido o conteo observado únicamente en esa edad.

Ejemplo:

| Año origen | dev_0 | dev_1 | dev_2 |
| --- | ---: | ---: | ---: |
| 2023 | 100 | 50 | 20 |
| 2024 | 120 | 55 |  |
| 2025 | 130 |  |  |

Aquí, el valor `50` para 2023 en `dev_1` representa lo ocurrido durante la segunda edad de desarrollo, no el total acumulado.

## Definición acumulada

Un triángulo acumulado contiene el monto observado hasta una edad de desarrollo:

$$
C_{i,j} = \sum_{k=0}^{j} X_{i,k}
$$

Ejemplo acumulado equivalente:

| Año origen | dev_0 | dev_1 | dev_2 |
| --- | ---: | ---: | ---: |
| 2023 | 100 | 150 | 170 |
| 2024 | 120 | 175 |  |
| 2025 | 130 |  |  |

El valor `150` para 2023 en `dev_1` representa el total observado hasta esa edad.

## Transformación entre formas

De incremental a acumulado:

$$
C_{i,j} = C_{i,j-1} + X_{i,j}
$$

con:

$$
C_{i,0} = X_{i,0}
$$

De acumulado a incremental:

$$
X_{i,j} = C_{i,j} - C_{i,j-1}
$$

con:

$$
X_{i,0} = C_{i,0}
$$

Estas fórmulas parecen simples, pero requieren que las celdas estén ordenadas correctamente y que los valores faltantes sean tratados como no observados, no como cero.

## Cuándo usar acumulados

Los acumulados son útiles para:

- estimar factores edad-a-edad;
- aplicar Chain Ladder;
- estimar ultimate;
- medir madurez;
- comparar desarrollo acumulado entre años de origen;
- revisar si una cohorte se acerca a su valor final.

La mayoría de métodos de desarrollo se formula sobre acumulados porque el patrón acumulado tiende a ser más estable que el incremental.

## Cuándo usar incrementales

Los incrementales son útiles para:

- detectar efectos calendario;
- identificar pagos negativos o reversos;
- analizar estacionalidad;
- revisar cambios operativos;
- separar pagos tardíos;
- detectar celdas atípicas;
- modelar distribuciones de pagos por edad.

En salud, los incrementales ayudan a identificar acumulación de cuentas, cambios de auditoría, pagos extraordinarios o correcciones masivas.

## Riesgos en acumulados

Un acumulado puede ocultar problemas. Si hay un pago negativo en una edad, el acumulado puede seguir creciendo o apenas disminuir, y el problema puede pasar desapercibido.

También puede ocultar efectos calendario. Una celda incremental extraordinaria puede elevar el acumulado, pero no siempre es evidente qué periodo calendario causó el salto.

Por eso el análisis debe revisar ambas vistas.

## Riesgos en incrementales

Los incrementales son más volátiles. Si se usan directamente para proyectar sin estabilización, pueden producir resultados erráticos.

En portafolios pequeños, una reclamación de alto costo puede dominar una celda incremental. En salud, esto es frecuente con enfermedades de alto costo, hospitalizaciones extensas o medicamentos especializados.

El incremental permite diagnosticar, pero no siempre es la mejor base directa para un método determinístico simple.

## Valores faltantes y ceros

Una celda vacía en el triángulo significa no observada. No debe reemplazarse automáticamente por cero.

Ejemplo:

| Año origen | dev_0 | dev_1 | dev_2 |
| --- | ---: | ---: | ---: |
| 2025 | 130 |  |  |

El vacío en `dev_1` no significa que no habrá pagos en esa edad. Significa que, a la fecha de valuación, todavía no se ha observado.

Un cero observado es distinto:

| Año origen | dev_0 | dev_1 |
| --- | ---: | ---: |
| 2024 | 130 | 0 |

Este cero puede significar que sí hubo observación y no se registró monto incremental. La distinción es crítica.

## Pagos negativos y reversos

Los pagos negativos pueden aparecer por:

- reversos contables;
- recuperaciones;
- glosas aceptadas;
- correcciones de facturación;
- anulaciones;
- reclasificaciones.

En acumulados, un pago negativo puede generar factores menores que 1. Esto no siempre es error, pero debe explicarse.

Si los factores de desarrollo son menores que 1 sin justificación, el actuario debe revisar si la base de datos mezcla pagos brutos, netos, recuperaciones o ajustes.

## Ejemplo de lectura

Si el triángulo incremental muestra un aumento fuerte en el año calendario 2024 para varios años de origen, puede existir un efecto operacional. El acumulado mostrará valores más altos, pero el incremental permite ubicar el origen temporal del cambio.

Si el acumulado muestra que los años recientes tienen baja madurez, el incremental ayuda a revisar si la falta de madurez se debe a rezago normal o a una interrupción de pagos.

## Buenas prácticas

Para cada análisis de reserving conviene mantener:

- triángulo incremental;
- triángulo acumulado;
- reconciliación entre ambos;
- identificación explícita de vacíos vs. ceros;
- revisión de pagos negativos;
- validación de totales contra fuentes contables u operativas.

La recomendación práctica es construir ambos triángulos siempre, aunque el método principal use solo uno.

## Capítulos relacionados

Anterior: [Lags de desarrollo y transformaciones de triángulos](03-development-lags-and-triangle-transformations.md).  
Siguiente: [Factores edad-a-edad](05-age-to-age-development-factors.md).

