---
title: Diagnósticos de Chain Ladder
description: Controles y diagnósticos para evaluar si Chain Ladder es apropiado, detectar factores atípicos, efectos calendario y problemas de datos.
status: draft
version: "0.1.6"
chapter: "07"
part: "part-02-classical-reserving"
language: "es"
last_updated: "2026-07-14"
---

# Diagnósticos de Chain Ladder

Un resultado de Chain Ladder solo es útil si el triángulo y los factores son razonables. Los diagnósticos permiten evaluar si el método está usando información representativa o si está extrapolando ruido, cambios operativos o problemas de datos.

El objetivo de diagnosticar no es encontrar una excusa para ajustar todo. El objetivo es saber cuándo el método es defendible, cuándo requiere ajuste y cuándo debe complementarse con otro enfoque.

## Qué debe revisar un diagnóstico

Un diagnóstico mínimo debe cubrir:

- calidad del triángulo;
- consistencia de la diagonal;
- factores observados;
- factores seleccionados;
- efectos calendario;
- estabilidad de mezcla;
- sensibilidad de ultimate e IBNR;
- comparación contra otras bases o métodos.

En salud, también debe considerar glosas, auditoría, radicación, cambios de red y cambios en contratos con prestadores.

## Revisión del triángulo acumulado

El primer control es visual y aritmético:

- ¿Los acumulados crecen de forma razonable?
- ¿Hay acumulados que disminuyen?
- ¿Existen celdas vacías inesperadas?
- ¿Hay saltos abruptos?
- ¿La última diagonal corresponde a la fecha de valuación?
- ¿Los totales coinciden con reportes fuente?

Un acumulado decreciente puede ser válido si los datos están netos de recuperaciones o reversos, pero debe explicarse.

## Revisión de incrementales

Aunque Chain Ladder use acumulados, los incrementales ayudan a identificar problemas:

- pagos negativos;
- pagos extraordinarios;
- limpieza de backlog;
- efectos calendario;
- cambios en velocidad de pago;
- interrupciones operativas.

Un incremento anormal en un año calendario puede contaminar varios factores acumulados.

## Factores observados

Los factores individuales son:

$$
f_{i,j} =
\frac{C_{i,j+1}}{C_{i,j}}
$$

La revisión debe comparar factores por edad y por año de origen.

Preguntas clave:

- ¿Los factores disminuyen con la edad de desarrollo?
- ¿Hay factores extremos?
- ¿Los años recientes se comportan distinto?
- ¿Los factores en base pagada e incurrida cuentan la misma historia?
- ¿Los factores altos corresponden a bajo volumen?

Un factor extremo no siempre debe excluirse. Primero debe entenderse la causa.

## Factores seleccionados

Una selección de factores debe ser trazable. Conviene mostrar:

- promedio ponderado por volumen;
- promedio simple;
- mediana;
- últimos años;
- exclusiones;
- selección final.

La selección final puede diferir de una fórmula automática, pero debe tener justificación técnica.

## Efectos calendario

Los efectos calendario se manifiestan en diagonales. En salud, pueden aparecer por:

- cambio regulatorio;
- acumulación de facturas;
- cambio de sistema;
- política de auditoría;
- variación en glosas;
- reforma de contratos;
- interrupciones de red;
- eventos sanitarios extraordinarios.

Si un efecto calendario es material, los factores históricos pueden no representar desarrollo futuro.

## Diagnóstico de madurez

La madurez de un año de origen puede aproximarse como:

$$
Madurez_i =
\frac{Observado_i}{Ultimate_i}
$$

Los años con baja madurez concentran la incertidumbre. En un análisis de reservas, es útil mostrar qué porcentaje del IBNR total proviene de los años más recientes.

Si la mayoría de la reserva depende de uno o dos años inmaduros, la sensibilidad de factores tempranos debe ser explícita.

## Sensibilidad de factores

Una práctica básica es recalcular ultimate e IBNR bajo varios conjuntos de factores:

- selección base;
- factores ponderados por volumen;
- últimos tres años;
- exclusión de años atípicos;
- escenario prudente;
- escenario optimista.

La sensibilidad ayuda a separar precisión aparente de incertidumbre real.

## Comparación pagado vs. incurrido

Si existen ambas bases, deben compararse:

- ultimate sobre base pagada;
- ultimate sobre base incurrida;
- reserva caso observada;
- IBNR sobre base incurrida;
- no pagado total.

Una diferencia grande entre bases puede indicar:

- reserva caso insuficiente o excesiva;
- rezago de pagos;
- cambios de reporte;
- variación de mix;
- problemas de datos.

No hay una regla universal: la diferencia debe interpretarse con contexto operativo.

## Validación contra experiencia externa o expectativa

Los resultados pueden contrastarse con:

- tendencias de costo médico;
- exposición o afiliados;
- frecuencia y severidad;
- presupuesto;
- reportes contables;
- experiencia de meses recientes;
- conocimiento de cambios operativos.

Si Chain Ladder produce una reserva incompatible con estos elementos, se debe investigar la razón.

## Señales de alerta

Algunas señales requieren revisión:

- factores muy volátiles en edades tempranas;
- factores menores que 1 sin explicación;
- ultimate que disminuye frente a estimaciones anteriores sin causa clara;
- años recientes con IBNR desproporcionado;
- gran diferencia entre pagado e incurrido;
- celdas históricas corregidas sin documentación;
- cambios de método no documentados.

Estas señales no invalidan automáticamente el método, pero impiden tratar el resultado como mecánico.

## Documentación del diagnóstico

Un diagnóstico debe dejar evidencia de:

- datos usados;
- fecha de valuación;
- controles realizados;
- anomalías encontradas;
- decisiones tomadas;
- factores seleccionados;
- sensibilidad;
- limitaciones.

La documentación es parte del resultado actuarial. Permite que el análisis sea revisado, auditado y reproducido.

## Ejemplo de control automático

Un control simple de factores extremos:

```python
observed_factors = next_age / current

flags = observed_factors[
    (observed_factors < 1.0) |
    (observed_factors > observed_factors.quantile(0.95))
]
```

Este control no decide por el actuario. Solo identifica celdas que requieren revisión.

## Buenas prácticas

Un buen diagnóstico debe ser:

- sistemático;
- reproducible;
- visual cuando aporte claridad;
- conectado con la operación;
- documentado;
- proporcional a la materialidad.

Si el diagnóstico es débil, la estimación también lo es, aunque las fórmulas estén correctas.

## Capítulos relacionados

Anterior: [Método Chain Ladder](06-chain-ladder-method.md).  
Siguiente: [Bornhuetter-Ferguson](11-bornhuetter-ferguson.md).

