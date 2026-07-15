---
title: Método Chain Ladder
description: Explicación práctica del método Chain Ladder para estimar ultimate e IBNR a partir de triángulos acumulados de pagos o incurridos.
status: draft
version: "0.1.6"
chapter: "06"
part: "part-02-classical-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Método Chain Ladder

Chain Ladder es uno de los métodos clásicos más usados en reserving actuarial. Su lógica es directa: si los años de origen históricos muestran un patrón de desarrollo relativamente estable, ese patrón puede usarse para proyectar los años de origen inmaduros hacia ultimate.

El método se aplica normalmente sobre triángulos acumulados. Puede usarse sobre pagos acumulados, incurridos acumulados, número de reclamaciones o cualquier medida que tenga un patrón de desarrollo razonablemente interpretable.

## Idea central

Sea $C_{i,j}$ el valor acumulado para el año de origen $i$ a edad de desarrollo $j$. Chain Ladder estima factores de desarrollo entre edades:

$$
f_j =
\frac{\sum_i C_{i,j+1}}{\sum_i C_{i,j}}
$$

Luego proyecta cada año de origen desde su última edad observada $k$ hasta ultimate:

$$
Ultimate_i = C_{i,k} \times \prod_{j=k}^{J-1} f_j
$$

El IBNR se calcula como:

$$
IBNR_i = Ultimate_i - C_{i,k}
$$

La simplicidad del método es su principal fortaleza y también su principal riesgo. Si el patrón histórico no es representativo, la proyección puede ser engañosa.

## Datos requeridos

Para aplicar Chain Ladder se necesita:

- un triángulo acumulado;
- una definición consistente de periodo de origen;
- una definición consistente de edad de desarrollo;
- datos observados hasta una fecha de valuación;
- suficiente historia para estimar factores;
- revisión de cambios operativos o de mezcla.

En salud, estos requisitos deben revisarse con cuidado porque los lags de radicación, auditoría, glosas y pago pueden cambiar por política interna, regulación, red de prestadores o tipo de contrato.

## Cálculo paso a paso

El proceso básico es:

1. Construir el triángulo acumulado.
2. Calcular factores observados entre edades.
3. Seleccionar factores edad-a-edad.
4. Calcular factores acumulados hacia ultimate.
5. Proyectar ultimate por año de origen.
6. Calcular IBNR por año de origen.
7. Revisar resultados y sensibilidad.

## Ejemplo conceptual

Supongamos un triángulo acumulado:

| Año origen | dev_0 | dev_1 | dev_2 |
| --- | ---: | ---: | ---: |
| 2022 | 100 | 150 | 180 |
| 2023 | 120 | 168 |  |
| 2024 | 130 |  |  |

El factor seleccionado de `dev_0` a `dev_1` es:

$$
f_0 =
\frac{150 + 168}{100 + 120}
= 1.445
$$

El factor de `dev_1` a `dev_2` es:

$$
f_1 =
\frac{180}{150}
= 1.200
$$

Para 2024, observado solo en `dev_0`, el factor acumulado hacia ultimate es:

$$
CDF_0 = 1.445 \times 1.200 = 1.734
$$

Entonces:

$$
Ultimate_{2024} = 130 \times 1.734 = 225.4
$$

$$
IBNR_{2024} = 225.4 - 130 = 95.4
$$

## Aplicación sobre base pagada

En base pagada, Chain Ladder proyecta pagos futuros. La interpretación es:

$$
IBNR^{pagado} = Ultimate - Pagado\ acumulado
$$

Esta estimación incluye todo lo no pagado. Si no se separa reserva caso, el resultado puede interpretarse como pasivo pendiente total sobre base pagada, no exclusivamente IBNR puro.

La base pagada suele ser objetiva, pero puede tener mayor rezago. En salud, esto puede producir factores altos en edades tempranas y mayor sensibilidad en años recientes.

## Aplicación sobre base incurrida

En base incurrida:

$$
Incurrido = Pagado + Reserva\ caso
$$

Chain Ladder proyecta el incurrido observado hacia ultimate:

$$
IBNR^{incurrido} = Ultimate - Incurrido\ observado
$$

El pasivo no pagado total se puede leer como:

$$
No\ pagado = Reserva\ caso + IBNR^{incurrido}
$$

La base incurrida puede ser más madura, pero depende de la calidad y consistencia de las reservas caso.

## Supuestos implícitos

Chain Ladder supone que:

- los patrones históricos de desarrollo son aplicables al futuro;
- la mezcla de riesgo no cambia de forma material;
- la operación de reporte, auditoría y pago es estable;
- no hay efectos calendario dominantes sin ajuste;
- los datos son comparables entre años de origen;
- los factores seleccionados representan el desarrollo esperado.

Estos supuestos rara vez se cumplen perfectamente. La tarea actuarial es evaluar si son suficientemente razonables para el uso previsto.

## Riesgos comunes

Errores frecuentes:

- aplicar Chain Ladder a triángulos incrementales por accidente;
- reemplazar celdas no observadas por cero;
- mezclar bases pagadas e incurridas;
- ignorar pagos negativos o reversos;
- usar factores contaminados por cambios operativos;
- no segmentar portafolios con patrones distintos;
- interpretar resultados como exactos en vez de estimaciones.

En salud, otro riesgo importante es no separar cambios de utilización real de cambios en rezagos administrativos.

## Implementación mínima en Python

Una estructura básica es:

```python
factors = {}

for age in development_ages[:-1]:
    current = triangle[age]
    next_age = triangle[age + 1]
    valid = current.notna() & next_age.notna() & (current > 0)
    factors[age] = next_age[valid].sum() / current[valid].sum()

ultimate = {}

for origin_year, row in triangle.iterrows():
    latest_age = row.last_valid_index()
    latest_value = row[latest_age]
    cdf = 1.0

    for age in range(latest_age, max(development_ages)):
        cdf *= factors[age]

    ultimate[origin_year] = latest_value * cdf
```

El código debe complementarse con controles de datos, diagnósticos y trazabilidad de supuestos.

## Buenas prácticas

Para usar Chain Ladder de forma defendible:

- mostrar triángulo acumulado;
- mostrar factores observados;
- justificar factores seleccionados;
- revisar sensibilidad;
- comparar bases pagada e incurrida;
- documentar exclusiones;
- explicar cambios operativos relevantes;
- reconciliar resultados con datos fuente.

Chain Ladder no reemplaza el juicio actuarial. Es una forma estructurada de trasladar patrones históricos hacia años inmaduros.

## Capítulos relacionados

Anterior: [Factores edad-a-edad](../part-01-foundations/05-age-to-age-development-factors.md).  
Siguiente: [Diagnósticos de Chain Ladder](07-chain-ladder-diagnostics.md).

